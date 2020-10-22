from django.db import models
from . import fields
# from django.core.validators import MinValueValidator, MaxValueValidator

# ! Create your models here.


class Parameter(models.Model):
    # /i  intro parameters
    nominal_voltage_1b = fields.OneByteField()
    nominal_current_1b = fields.OneByteField()

    # /i dimming curve paramters
    dimming_curve_14_2b = fields.TwoByteField()
    dimming_curve_27_2b = fields.TwoByteField()
    dimming_curve_34_2b = fields.TwoByteField()
    dimming_curve_41_2b = fields.TwoByteField()
    dimming_curve_48_2b = fields.TwoByteField()
    dimming_curve_52_2b = fields.TwoByteField()
    dimming_curve_55_2b = fields.TwoByteField()
    dimming_curve_66_2b = fields.TwoByteField()

    # /i flux compensation curve parameters
    flux_comp_m50_1b = fields.OneByteField()
    flux_comp_m25_1b = fields.OneByteField()
    flux_comp_0_1b = fields.OneByteField()
    flux_comp_25_1b = fields.OneByteField()
    flux_comp_50_1b = fields.OneByteField()
    flux_comp_75_1b = fields.OneByteField()
    flux_comp_max_1b = fields.OneByteField()
