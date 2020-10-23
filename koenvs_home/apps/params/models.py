from django.db import models
from . import fields
# from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


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

    # * NON INTEGER FIELDS
    short_name = models.CharField(max_length=50, default="default")
    csv_name = models.CharField(max_length=60, default="default.csv")
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
    led_revision_1b = fields.OneByteField()  # - byte 146
    # ! LED revision 0: shortLED not mounted, LED revision 1: shortLED mounted
    min_lin_dim_2b = fields.TwoByteField(
        default=300)  # - byte 202 (LSB), byte 203 (MSB)
    analog_dim_freq_2b = fields.TwoByteField(
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
    dimming_curve_27_2b = fields.TwoByteField()  # - byte 149 (LSB), byte 150 (MSB)
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
    rel_year_1b = fields.OneByteField(default=20)  # - byte 171
    rel_week_1b = fields.OneByteField(default=43)  # - byte 172
    rel_ver_1b = fields.OneByteField(default=1)  # - byte 173
    rel_not_used_1b = fields.OneByteField(default=0)  # - byte 174
    inv_rel_year_1b = fields.OneByteField(default=235)  # - byte 171
    inv_rel_week_1b = fields.OneByteField(default=212)  # - byte 172
    inv_rel_ver_1b = fields.OneByteField(default=254)  # - byte 173
    inv_rel_not_used_1b = fields.OneByteField(default=255)  # - byte 174
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
