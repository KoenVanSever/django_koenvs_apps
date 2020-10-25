# Generated by Django 3.1.2 on 2020-10-24 09:44

import apps.params.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(default='default', max_length=50)),
                ('csv_name', models.CharField(default='default.csv', max_length=60)),
                ('category', models.CharField(blank=True, choices=[('OMNI', 'Omnidirectional range application'), ('SL', 'SafeLED application'), ('Sign', 'SafeSign application')], default=None, max_length=50, null=True)),
                ('nominal_voltage_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('nominal_current_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('number_of_leds_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('led_revision_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('min_lin_dim_2b', apps.params.fields.TwoByteField(default=300, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('analog_dim_freq_2b', apps.params.fields.TwoByteField(default=610, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('min_on_time_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('nominal_voltage_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('load_type_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('dual_mon_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('dimming_curve_14_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_27_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_34_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_41_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_48_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_52_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_55_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('dimming_curve_66_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('flux_comp_m25_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('flux_comp_0_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('flux_comp_25_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('flux_comp_50_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('flux_comp_75_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('flux_comp_max_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('ak_power_1window_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('ak_power_2window_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('rel_year_1b', apps.params.fields.OneByteField(default=20, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('rel_week_1b', apps.params.fields.OneByteField(default=43, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('rel_ver_1b', apps.params.fields.OneByteField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('rel_not_used_1b', apps.params.fields.OneByteField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('inv_rel_year_1b', apps.params.fields.OneByteField(default=235, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('inv_rel_week_1b', apps.params.fields.OneByteField(default=212, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('inv_rel_ver_1b', apps.params.fields.OneByteField(default=254, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('inv_rel_not_used_1b', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('year_1b', apps.params.fields.OneByteField(default=20, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('month_1b', apps.params.fields.OneByteField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('day_1b', apps.params.fields.OneByteField(default=23, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('hour_1b', apps.params.fields.OneByteField(default=23, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('type_1b', apps.params.fields.OneByteField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('thermal_resistance_1b', apps.params.fields.OneByteField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('max_junction_temp_1b', apps.params.fields.OneByteField(default=130, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('flux_bin_info_1b', apps.params.fields.OneByteField(default=180, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('color_1b', apps.params.fields.OneByteField(default=156, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('fitting_type_1b', apps.params.fields.OneByteField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('led_pwm_l1_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('led_pwm_l2_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('led_pwm_l3_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('led_pwm_l4_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('led_pwm_l5_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('led_pwm_l6_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('u_led_vl1_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('u_led_vl2_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('u_led_vl3_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('u_led_vl4_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('u_led_vl5_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('u_led_vl6_b2', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('crc_2b', apps.params.fields.TwoByteField(default=65535, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('reserved_version_2b', apps.params.fields.TwoByteField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(65535)])),
                ('length_block1_1b', apps.params.fields.OneByteField(default=18, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('vf_short_threshold_fast', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
                ('vf_short_threshold_slow', apps.params.fields.OneByteField(default=255, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(255)])),
            ],
        ),
    ]