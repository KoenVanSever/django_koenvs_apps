from pathlib import Path
from django.db import models
from . import fields
# from django.core.validators import MinValueValidator, MaxValueValidator

# * Help functions


def split_2b(twobyte):
    """ split a 16 bit integer number (<=65535) into two 8 bit integers (<=255) """
    lsb = twobyte % 256
    msb = twobyte // 256
    return [str(lsb), str(msb)]


def merge_2b(lsb, msb):
    """ merge two 8 bit integer numbers (<=255) into one 16 bit integer number (<=65535) """
    twobyte = int(lsb) + 256 * int(msb)
    return twobyte


# * Create your models here.


class Parameter(models.Model):
    """
        Non integer information:
        - short_name: short name for the parameter file (max_length = 50)
        - csv_name: file name of the csv file (max_length = 60)
        - category: OMNI/SafeLED/SafeSign/...

        Integer information:
        Holds bytes that are described in documentation with short names:
        - Bytes 0-127: all 0xFF
        - Bytes 128-215: describted in this model
        - Bytes 216-255: all 0xFF
        * SIDENOTE/TODO on last block -> 220-221 found to be populated: WHAT IS THIS?
    """

    @ classmethod
    def upload_file(cls, path, category=None):
        """ create a DB entry based on a file path """
        with open(path) as file:
            lines = file.readlines()
        data = []
        for line in lines:
            if ";" in line:
                if len(line.split(";")) == 257:
                    data = line.split(";")
        if isinstance(data, list) and len(data) == 257:
            temp = cls()
            temp.csv_name = path.name
            temp.short_name = data[0]
            temp.category = category
            del data[0]
            data = list(map(int, data))
            temp.load_params_from_256_list(data)
            return temp
        else:
            raise AttributeError("data parsed is not right format")

    @ classmethod
    def upload_string(cls, string, csv_name, category=None):
        """ create a DB entry based on a stream/string """
        delim = ";" if ";" in string else ","
        temp = string.rstrip().split(delim)
        ret = cls()
        ret.csv_name = csv_name
        ret.short_name = temp[0]
        del temp[0]
        ret.category = category
        temp = list(map(int, temp))
        ret.load_params_from_256_list(temp)
        return ret

    # * NON INTEGER FIELDS
    short_name = models.CharField(max_length=50, default="default")
    csv_name = models.CharField(
        max_length=60, default="default.csv", unique=True)
    cat_choices = [
        ("OMNI", "Omnidirectional range application"),
        ("SL", "SafeLED application"),
        ("Sign", "SafeSign application"),
    ]
    category = models.CharField(
        max_length=50, choices=cat_choices, blank=True, null=True, default=None)

    # * INTEGER FIELDS
    # /i led settings parameters
    nominal_voltage_1b = fields.OneByteField()  # - byte 139
    # ! nominal_voltage_1b * 100 mV
    nominal_current_2b = fields.TwoByteField()  # - byte 137 (LSB), byte 138 (MSB)
    number_of_leds_1b = fields.OneByteField()  # - byte 145
    led_revision_1b = fields.OneByteField(default=0)  # - byte 146
    # ! LED revision 0: shortLED not mounted, LED revision 1: shortLED mounted
    min_lin_dim_2b = fields.TwoByteField(
        default=300)  # - byte 202 (LSB), byte 203 (MSB)
    digital_dim_freq_2b = fields.TwoByteField(
        default=610)  # - byte 204 (LSB), byte 205 (MSB)
    min_on_time_2b = fields.TwoByteField()  # - byte 208 (LSB), byte 209 (MSB)
    # ! used in real life? meant for HPC according to docs?
    nominal_voltage_2b = fields.TwoByteField()  # - byte 210 (LSB), byte 211 (MSB)
    # ! nominal_voltage_2b * 10 mV, also used for voltage control in HPC!
    load_type_1b = fields.OneByteField()  # - byte 212
    # ! 255 - constant current application, 254 - sign application (constant voltage)
    dual_mon_1b = fields.OneByteField()  # - byte 215
    # ! for HPC, if 255 channels act independent of each other on fautlts, if 1 they act together as one

    # /i dimming curve paramters
    dimming_curve_14_2b = fields.TwoByteField()  # - byte 147 (LSB), byte 148 (MSB)
    dimming_curve_28_2b = fields.TwoByteField()  # - byte 149 (LSB), byte 150 (MSB)
    dimming_curve_34_2b = fields.TwoByteField()  # - byte 151 (LSB), byte 152 (MSB)
    dimming_curve_41_2b = fields.TwoByteField()  # - byte 153 (LSB), byte 154 (MSB)
    dimming_curve_48_2b = fields.TwoByteField()  # - byte 155 (LSB), byte 156 (MSB)
    dimming_curve_52_2b = fields.TwoByteField()  # - byte 157 (LSB), byte 158 (MSB)
    dimming_curve_55_2b = fields.TwoByteField()  # - byte 159 (LSB), byte 160 (MSB)
    dimming_curve_66_2b = fields.TwoByteField()  # - byte 161 (LSB), byte 162 (MSB)

    # /i flux compensation curve parameters
    flux_comp_m25_1b = fields.OneByteField()  # - byte 163
    flux_comp_0_1b = fields.OneByteField()  # - byte 164
    flux_comp_25_1b = fields.OneByteField()  # - byte 165
    flux_comp_50_1b = fields.OneByteField()  # - byte 166
    flux_comp_75_1b = fields.OneByteField()  # - byte 167
    flux_comp_max_1b = fields.OneByteField()  # - byte 168

    # /i artic kit parameters
    ak_power_1window_1b = fields.OneByteField()  # - byte 213
    ak_power_2window_1b = fields.OneByteField()  # - byte 214

    # /i release info parameters
    rel_year_1b = fields.OneByteField(default=20)  # - byte 128
    rel_week_1b = fields.OneByteField(default=43)  # - byte 129
    rel_ver_1b = fields.OneByteField(default=1)  # - byte 130
    rel_not_used_1b = fields.OneByteField(default=0)  # - byte 131
    inv_rel_year_1b = fields.OneByteField(default=235)  # - byte 132
    inv_rel_week_1b = fields.OneByteField(default=212)  # - byte 133
    inv_rel_ver_1b = fields.OneByteField(default=254)  # - byte 134
    inv_rel_not_used_1b = fields.OneByteField(default=255)  # - byte 135
    # ! default to moment of making this file, just for fucking fun

    # /i programming data parameters
    year_1b = fields.OneByteField(default=20)  # - byte 171
    month_1b = fields.OneByteField(default=10)  # - byte 172
    day_1b = fields.OneByteField(default=23)  # - byte 173
    hour_1b = fields.OneByteField(default=23)  # - byte 174
    # ! default to moment of making this file, just for fucking fun

    # /i general/useless parameters
    type_1b = fields.OneByteField(default=1)  # - byte 136
    # ! default to value 1
    thermal_resistance_1b = fields.OneByteField(default=10)  # - byte 140
    # ! used as thermal resistance between LED measurement and LED junction
    max_junction_temp_1b = fields.OneByteField(default=130)  # - byte 141
    flux_bin_info_1b = fields.OneByteField(default=180)  # - byte 142
    color_1b = fields.OneByteField(default=156)  # - byte 143
    # ! 4nm per increment, useless (not used)
    fitting_type_1b = fields.OneByteField(default=1)  # - byte 144

    # /i depreciated/not-implemented parameters
    led_pwm_l1_b2 = fields.TwoByteField()  # - byte 175 (LSB), byte 176 (MSB)
    led_pwm_l2_b2 = fields.TwoByteField()  # - byte 177 (LSB), byte 178 (MSB)
    led_pwm_l3_b2 = fields.TwoByteField()  # - byte 179 (LSB), byte 180 (MSB)
    led_pwm_l4_b2 = fields.TwoByteField()  # - byte 181 (LSB), byte 182 (MSB)
    led_pwm_l5_b2 = fields.TwoByteField()  # - byte 183 (LSB), byte 184 (MSB)
    led_pwm_l6_b2 = fields.TwoByteField()  # - byte 185 (LSB), byte 186 (MSB)
    u_led_vl1_b2 = fields.TwoByteField()  # - byte 187 (LSB), byte 188 (MSB)
    u_led_vl2_b2 = fields.TwoByteField()  # - byte 189 (LSB), byte 190 (MSB)
    u_led_vl3_b2 = fields.TwoByteField()  # - byte 191 (LSB), byte 192 (MSB)
    u_led_vl4_b2 = fields.TwoByteField()  # - byte 193 (LSB), byte 194 (MSB)
    u_led_vl5_b2 = fields.TwoByteField()  # - byte 195 (LSB), byte 196 (MSB)
    u_led_vl6_b2 = fields.TwoByteField()  # - byte 197 (LSB), byte 198 (MSB)

    # /i CRC parameters
    # TODO: ask/look around for algorithm to try to calculate yourself from inputs of other fields?
    crc_2b = fields.TwoByteField()  # - byte 199 (LSB), byte 200 (MSB)
    # ! based on bytes 128-198

    # /i unknown parameters?
    reserved_version_2b = fields.TwoByteField(
        default=0)  # - byte 169 (LSB), byte 170 (MSB)
    length_block1_1b = fields.OneByteField(default=18)  # - byte 201
    vf_short_threshold_fast = fields.OneByteField()  # - byte 206
    vf_short_threshold_slow = fields.OneByteField()  # - byte 207

    def update_dimming_curve(self, dimlist):
        self.dimming_curve_14_2b = dimlist[0]
        self.dimming_curve_28_2b = dimlist[1]
        self.dimming_curve_34_2b = dimlist[2]
        self.dimming_curve_41_2b = dimlist[3]
        self.dimming_curve_48_2b = dimlist[4]
        self.dimming_curve_52_2b = dimlist[5]
        self.dimming_curve_55_2b = dimlist[6]
        self.dimming_curve_66_2b = dimlist[7]

    @ property
    def dimming_curve(self):
        ret = [self.dimming_curve_14_2b, self.dimming_curve_28_2b, self.dimming_curve_34_2b, self.dimming_curve_41_2b,
               self.dimming_curve_48_2b, self.dimming_curve_52_2b, self.dimming_curve_55_2b, self.dimming_curve_66_2b]
        return ret

    def update_full_flux(self, flux):
        self.flux_comp_m25_1b = flux
        self.flux_comp_0_1b = flux
        self.flux_comp_25_1b = flux
        self.flux_comp_50_1b = flux
        self.flux_comp_75_1b = flux
        self.flux_comp_max_1b = flux

    @ property
    def flux_analysis(self):
        ret = self.flux_comp_m25_1b if self.flux_comp_m25_1b == self.flux_comp_0_1b == self.flux_comp_25_1b == self.flux_comp_50_1b == self.flux_comp_75_1b == self.flux_comp_max_1b else "Varying!"
        return ret

    def update_nominal_voltage(self, volt):
        """ volt is in (V) unit, whether to use 1 byte field or 2 byte field is autodetected """
        if volt <= 25.5:
            self.nominal_voltage_1b = round(volt * 10)
            self.nominal_voltage_2b = 65535
        else:
            self.nominal_voltage_1b = 255
            self.nominal_voltage_2b = round(volt * 100)

    @ property
    def real_nom_voltage(self):
        if self.nominal_voltage_2b == 65535:
            return self.nominal_voltage_1b / 10
        else:
            return self.nominal_voltage_2b / 100

    def _get_full_file(self):
        release_info = [self.rel_year_1b, self.rel_week_1b, self.rel_ver_1b, self.rel_not_used_1b,
                        self.inv_rel_year_1b, self.inv_rel_week_1b, self.inv_rel_ver_1b, self.inv_rel_not_used_1b]
        dimming_curve = split_2b(self.dimming_curve_14_2b) + split_2b(self.dimming_curve_28_2b) + split_2b(self.dimming_curve_34_2b) + split_2b(self.dimming_curve_41_2b) + \
            split_2b(self.dimming_curve_48_2b) + split_2b(self.dimming_curve_52_2b) + \
            split_2b(self.dimming_curve_55_2b) + \
            split_2b(self.dimming_curve_66_2b)
        flux_comp = [self.flux_comp_m25_1b, self.flux_comp_0_1b, self.flux_comp_25_1b,
                     self.flux_comp_50_1b, self.flux_comp_75_1b, self.flux_comp_max_1b]
        programming_date = [self.year_1b,
                            self.month_1b, self.day_1b, self.hour_1b]
        depr1 = split_2b(self.led_pwm_l1_b2) + split_2b(self.led_pwm_l2_b2) + split_2b(self.led_pwm_l3_b2) + \
            split_2b(self.led_pwm_l4_b2) + split_2b(self.led_pwm_l5_b2) + \
            split_2b(self.led_pwm_l6_b2)
        depr2 = split_2b(self.u_led_vl1_b2) + split_2b(self.u_led_vl2_b2) + split_2b(self.u_led_vl3_b2) + \
            split_2b(self.u_led_vl4_b2) + split_2b(self.u_led_vl5_b2) + \
            split_2b(self.u_led_vl6_b2)
        full = [self.short_name] + [255] * 128 + release_info + [self.type_1b] + split_2b(self.nominal_current_2b) + [self.nominal_voltage_1b] + [self.thermal_resistance_1b] + [self.max_junction_temp_1b] + [
            self.flux_bin_info_1b] + [self.color_1b] + [self.fitting_type_1b] + [self.number_of_leds_1b] + [self.led_revision_1b] + dimming_curve + flux_comp + split_2b(self.reserved_version_2b) + programming_date + depr1 + depr2 + split_2b(self.crc_2b) + [self.length_block1_1b] + split_2b(self.min_lin_dim_2b) + split_2b(self.digital_dim_freq_2b) + [
            self.vf_short_threshold_fast] + [self.vf_short_threshold_slow] + split_2b(self.min_on_time_2b) + split_2b(self.nominal_voltage_2b) + [self.load_type_1b] + [self.ak_power_1window_1b] + [self.ak_power_2window_1b] + [self.dual_mon_1b] + [255] * 40
        return full

    def create_file(self, target_dir):
        output = [str(e) for e in self._get_full_file()]
        full_path = Path(target_dir, self.csv_name).resolve()
        with open(full_path, "w") as f:
            f.write(",".join(output))
            f.write("\n")
        return full_path

    def get_relevent_list(self):
        temp = [int(e) for e in self._get_full_file()[129:217]]
        keys = list(range(128, 216, 1))
        print(len(temp), len(keys))
        ret = dict(zip(keys, temp))
        ret["csv_name"] = self.csv_name
        ret["short_name"] = self.short_name
        ret["category"] = self.category
        return ret

    def __str__(self):
        return self.short_name

    def load_params_from_256_list(self, l):
        self.rel_year_1b = l[128]
        self.rel_week_1b = l[129]
        self.rel_ver_1b = l[130]
        self.rel_not_used_1b = l[131]
        self.inv_rel_year_1b = l[132]
        self.inv_rel_week_1b = l[133]
        self.inv_rel_ver_1b = l[134]
        self.inv_rel_not_used_1b = l[135]
        self.type_1b = l[136]
        self.nominal_current_2b = merge_2b(l[137], l[138])
        self.nominal_voltage_1b = l[139]
        self.thermal_resistance_1b = l[140]
        self.max_junction_temp_1b = l[141]
        self.flux_bin_info_1b = l[142]
        self.color_1b = l[143]
        self.fitting_type_1b = l[144]
        self.number_of_leds_1b = l[145]
        self.led_revision_1b = l[146]
        self.dimming_curve_14_2b = merge_2b(l[147], l[148])
        self.dimming_curve_28_2b = merge_2b(l[149], l[150])
        self.dimming_curve_34_2b = merge_2b(l[151], l[152])
        self.dimming_curve_41_2b = merge_2b(l[153], l[154])
        self.dimming_curve_48_2b = merge_2b(l[155], l[156])
        self.dimming_curve_52_2b = merge_2b(l[157], l[158])
        self.dimming_curve_55_2b = merge_2b(l[159], l[160])
        self.dimming_curve_66_2b = merge_2b(l[161], l[162])
        self.flux_comp_m25_1b = l[163]
        self.flux_comp_0_1b = l[164]
        self.flux_comp_25_1b = l[165]
        self.flux_comp_50_1b = l[166]
        self.flux_comp_75_1b = l[167]
        self.flux_comp_max_1b = l[168]
        self.reserved_version_2b = merge_2b(l[169], l[170])
        self.year_1b = l[171]
        self.month_1b = l[172]
        self.day_1b = l[173]
        self.hour_1b = l[174]
        self.led_pwm_l1_b2 = merge_2b(l[175], l[176])
        self.led_pwm_l2_b2 = merge_2b(l[177], l[178])
        self.led_pwm_l3_b2 = merge_2b(l[179], l[180])
        self.led_pwm_l4_b2 = merge_2b(l[181], l[182])
        self.led_pwm_l5_b2 = merge_2b(l[183], l[184])
        self.led_pwm_l6_b2 = merge_2b(l[185], l[186])
        self.u_led_vl1_b2 = merge_2b(l[187], l[188])
        self.u_led_vl2_b2 = merge_2b(l[189], l[190])
        self.u_led_vl3_b2 = merge_2b(l[191], l[192])
        self.u_led_vl4_b2 = merge_2b(l[193], l[194])
        self.u_led_vl5_b2 = merge_2b(l[195], l[196])
        self.u_led_vl6_b2 = merge_2b(l[197], l[198])
        self.crc_2b = merge_2b(l[199], l[200])
        self.length_block1_1b = l[201]
        self.min_lin_dim_2b = merge_2b(l[202], l[203])
        self.digital_dim_freq_2b = merge_2b(l[204], l[205])
        self.vf_short_threshold_fast = l[206]
        self.vf_short_threshold_slow = l[207]
        self.min_on_time_2b = merge_2b(l[208], l[209])
        self.nominal_voltage_2b = merge_2b(l[210], l[211])
        self.load_type_1b = l[212]
        self.ak_power_1window_1b = l[213]
        self.ak_power_2window_1b = l[214]
        self.dual_mon_1b = l[215]

    def get_four_way_tuple(self):
        ret = []
        colors = {"relprog": "#e95b0b", "led": "#ed7103",
                  "dimming": "#f8b123", "flux": "#e8b135", "varia": "#f49b01"}
        ret.append(("Rel year", "128", self.rel_year_1b, colors["relprog"]))
        ret.append(("Rel week", "129", self.rel_week_1b, colors["relprog"]))
        ret.append(("Rel version", "130", self.rel_ver_1b, colors["relprog"]))
        ret.append(("Rel not used", "131", self.rel_not_used_1b,
                    colors["relprog"]))
        ret.append(("Rel year inv", "132", self.inv_rel_year_1b,
                    colors["relprog"]))
        ret.append(("Rel week inv", "133", self.inv_rel_week_1b,
                    colors["relprog"]))
        ret.append(("Rel version inv", "134", self.inv_rel_ver_1b,
                    colors["relprog"]))
        ret.append(("Rel not used inv", "135",
                    self.inv_rel_not_used_1b, colors["relprog"]))
        ret.append(("Type", "136", self.type_1b, colors["varia"]))
        ret.append(("Nom current (mA)", "137 & 138",
                    self.nominal_current_2b, colors["led"]))
        ret.append(("Nom voltage (x100mV) (1b)", "139",
                    self.nominal_voltage_1b, colors["led"]))
        ret.append(("Therm res (°C/W)", "140",
                    self.thermal_resistance_1b, colors["varia"]))
        ret.append(("Max junc temp (°C)", "141",
                    self.max_junction_temp_1b, colors["varia"]))
        ret.append(("Flux bin info", "142", self.flux_bin_info_1b,
                    colors["varia"]))
        ret.append(("Color", "143", self.color_1b, colors["varia"]))
        ret.append(("Fitting type", "144", self.fitting_type_1b,
                    colors["varia"]))
        ret.append(("Number of LEDs", "145",
                    self.number_of_leds_1b, colors["led"]))
        ret.append(("LED revision", "146", self.led_revision_1b,
                    colors["led"]))
        ret.append(("DC 1.4A (mA)", "147 & 148",
                    self.dimming_curve_14_2b, colors["dimming"]))
        ret.append(("DC 2.8A (mA)", "149 & 150",
                    self.dimming_curve_28_2b, colors["dimming"]))
        ret.append(("DC 3.4A (mA)", "151 & 152",
                    self.dimming_curve_34_2b, colors["dimming"]))
        ret.append(("DC 4.1A (mA)", "153 & 154",
                    self.dimming_curve_41_2b, colors["dimming"]))
        ret.append(("DC 4.8A (mA)", "155 & 156",
                    self.dimming_curve_48_2b, colors["dimming"]))
        ret.append(("DC 5.2A (mA)", "157 & 158",
                    self.dimming_curve_52_2b, colors["dimming"]))
        ret.append(("DC 5.5A (mA)", "159 & 160",
                    self.dimming_curve_55_2b, colors["dimming"]))
        ret.append(("DC 6.6A (mA)", "161 & 162",
                    self.dimming_curve_66_2b, colors["dimming"]))
        ret.append(("Flux comp m25°C (%)", "163",
                    self.flux_comp_m25_1b, colors["flux"]))
        ret.append(("Flux comp 0°C (%)", "164",
                    self.flux_comp_0_1b, colors["flux"]))
        ret.append(("Flux comp 25°C (%)", "165",
                    self.flux_comp_25_1b, colors["flux"]))
        ret.append(("Flux comp 50°C (%)", "166",
                    self.flux_comp_50_1b, colors["flux"]))
        ret.append(("Flux comp 75°C (%)", "167",
                    self.flux_comp_75_1b, colors["flux"]))
        ret.append(("Flux comp Max (%)", "168",
                    self.flux_comp_max_1b, colors["flux"]))
        ret.append(("Reserved version", "169 & 170",
                    self.reserved_version_2b, colors["varia"]))
        ret.append(("Prog year", "171", self.year_1b, colors["relprog"]))
        ret.append(("Prog month", "172", self.month_1b, colors["relprog"]))
        ret.append(("Prog date", "173", self.day_1b, colors["relprog"]))
        ret.append(("Prog hour", "174", self.hour_1b, colors["relprog"]))
        ret.append(("LED PWM level 1", "175 & 176",
                    self.led_pwm_l1_b2, colors["varia"]))
        ret.append(("LED PWM level 2", "177 & 178",
                    self.led_pwm_l2_b2, colors["varia"]))
        ret.append(("LED PWM level 3", "179 & 180",
                    self.led_pwm_l3_b2, colors["varia"]))
        ret.append(("LED PWM level 4", "181 & 182",
                    self.led_pwm_l4_b2, colors["varia"]))
        ret.append(("LED PWM level 5", "183 & 184",
                    self.led_pwm_l5_b2, colors["varia"]))
        ret.append(("LED PWM level 6", "185 & 186",
                    self.led_pwm_l6_b2, colors["varia"]))
        ret.append(("U LED level 1", "187 & 188",
                    self.u_led_vl1_b2, colors["varia"]))
        ret.append(("U LED level 2", "189 & 190",
                    self.u_led_vl2_b2, colors["varia"]))
        ret.append(("U LED level 3", "191 & 192",
                    self.u_led_vl3_b2, colors["varia"]))
        ret.append(("U LED level 4", "193 & 194",
                    self.u_led_vl4_b2, colors["varia"]))
        ret.append(("U LED level 5", "195 & 196",
                    self.u_led_vl5_b2, colors["varia"]))
        ret.append(("U LED level 6", "197 & 198",
                    self.u_led_vl6_b2, colors["varia"]))
        ret.append(("CRC", "199 & 200", self.crc_2b, colors["varia"]))
        ret.append(("Length block 1", "201", self.length_block1_1b,
                    colors["varia"]))
        ret.append(("Min lin dim (mA)", "202 & 203",
                    self.min_lin_dim_2b, colors["led"]))
        ret.append(("Dig dim freq (Hz)", "204 & 205",
                    self.digital_dim_freq_2b, colors["led"]))
        ret.append(("Vf treshold fast", "206",
                    self.vf_short_threshold_fast, colors["varia"]))
        ret.append(("Vf threshold slow", "207",
                    self.vf_short_threshold_slow, colors["varia"]))
        ret.append(("Min on time (ns)", "208 & 209",
                    self.min_on_time_2b, colors["varia"]))
        ret.append(("Nom voltage (x10mV)", "210 & 211",
                    self.nominal_voltage_2b, colors["led"]))
        ret.append(("Load type", "212", self.load_type_1b, colors["led"]))
        ret.append(("AK power 1 win (W)", "213",
                    self.ak_power_1window_1b, colors["varia"]))
        ret.append(("AK power 2 win (W)", "214",
                    self.ak_power_2window_1b, colors["varia"]))
        ret.append(("Dual monitoring", "215", self.dual_mon_1b, colors["led"]))
        return ret

    def update_data_without_save(self, update):
        self.rel_year_1b = update["Relyear"]
        self.rel_week_1b = update["Relweek"]
        self.rel_ver_1b = update["Relversion"]
        self.rel_not_used_1b = update["Relnotused"]
        self.inv_rel_year_1b = update["Relyearinv"]
        self.inv_rel_week_1b = update["Relweekinv"]
        self.inv_rel_ver_1b = update["Relversioninv"]
        self.inv_rel_not_used_1b = update["Relnotusedinv"]
        self.type_1b = update["Type"]
        self.nominal_current_2b = update["NomcurrentmA"]
        self.nominal_voltage_1b = update["NomvoltageV1b"]
        self.thermal_resistance_1b = update["ThermresCW"]
        self.max_junction_temp_1b = update["MaxjunctempC"]
        self.flux_bin_info_1b = update["Fluxbininfo"]
        self.color_1b = update["Color"]
        self.fitting_type_1b = update["Fittingtype"]
        self.number_of_leds_1b = update["NumberofLEDs"]
        self.led_revision_1b = update["LEDrevision"]
        self.dimming_curve_14_2b = update["DC14AmA"]
        self.dimming_curve_28_2b = update["DC28AmA"]
        self.dimming_curve_34_2b = update["DC34AmA"]
        self.dimming_curve_41_2b = update["DC41AmA"]
        self.dimming_curve_48_2b = update["DC48AmA"]
        self.dimming_curve_52_2b = update["DC52AmA"]
        self.dimming_curve_55_2b = update["DC55AmA"]
        self.dimming_curve_66_2b = update["DC66AmA"]
        self.flux_comp_m25_1b = update["Fluxcompm25C"]
        self.flux_comp_0_1b = update["Fluxcomp0C"]
        self.flux_comp_25_1b = update["Fluxcomp25C"]
        self.flux_comp_50_1b = update["Fluxcomp50C"]
        self.flux_comp_75_1b = update["Fluxcomp75C"]
        self.flux_comp_max_1b = update["FluxcompMax"]
        self.reserved_version_2b = update["Reservedversion"]
        self.year_1b = update["Progyear"]
        self.month_1b = update["Progmonth"]
        self.day_1b = update["Progdate"]
        self.hour_1b = update["Proghour"]
        self.led_pwm_l1_b2 = update["LEDPWMlevel1"]
        self.led_pwm_l2_b2 = update["LEDPWMlevel2"]
        self.led_pwm_l3_b2 = update["LEDPWMlevel3"]
        self.led_pwm_l4_b2 = update["LEDPWMlevel4"]
        self.led_pwm_l5_b2 = update["LEDPWMlevel5"]
        self.led_pwm_l6_b2 = update["LEDPWMlevel6"]
        self.u_led_vl1_b2 = update["ULEDlevel1"]
        self.u_led_vl2_b2 = update["ULEDlevel2"]
        self.u_led_vl3_b2 = update["ULEDlevel3"]
        self.u_led_vl4_b2 = update["ULEDlevel4"]
        self.u_led_vl5_b2 = update["ULEDlevel5"]
        self.u_led_vl6_b2 = update["ULEDlevel6"]
        self.crc_2b = update["CRC"]
        self.length_block1_1b = update["Lengthblock1"]
        self.min_lin_dim_2b = update["MinlindimmA"]
        self.digital_dim_freq_2b = update["DigdimfreqHz"]
        self.vf_short_threshold_fast = update["Vftresholdfast"]
        self.vf_short_threshold_slow = update["Vfthresholdslow"]
        self.min_on_time_2b = update["Minontimens"]
        self.nominal_voltage_2b = update["NomvoltageV"]
        self.load_type_1b = update["Loadtype"]
        self.ak_power_1window_1b = update["AKpower1winW"]
        self.ak_power_2window_1b = update["AKpower2winW"]
        self.dual_mon_1b = update["Dualmonitoring"]
