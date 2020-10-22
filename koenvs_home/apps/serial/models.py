from django.db import models

# Create your models here.


class Converter(models.Model):
    # Suppliers
    SUPPLIERS = [
        ("CG", "Connect Group"),
        ("SVI", "SVI"),
        ("ELE", "Elemaster"),
        ("PG", "Page")
    ]
    CONV_TYPES = [
        ("LCC_1c", "Low Cost Converter 1con"),
        ("LCC_2c", "Low Cost Converter 2con"),
        ("FO4_1c", "Fail Open Converter v4.1 1con"),
        ("FO4_2c", "Fail Open Converter v4.1 2con"),
        ("HPC4", "High Power Converter v4.x"),
        ("HPC5", "High Power Converter v5.x"),
        ("HPC6", "High Power Converter v6.x"),
        ("FO3.5_1c", "Fail Open Converter v3.5 1con"),
        ("FO3.5_2c", "Fail Open Converter v3.5 1con"),
        ("Unknown", "Unknown converter"),
    ]
    name = models.TextField()
    pid = models.IntegerField(blank=False)
    supplier = models.CharField(max_length=3, choices=SUPPLIERS)
    conv_type = models.CharField(
        max_length=10, choices=CONV_TYPES, blank=False, default=("Unknown"))
    remark = models.TextField(default="no remarks")


class LedCalib(models.Model):
    CHANNELS = [
        ("1", "LED channel A - binary 001 (1)"),
        ("4", "LED channel B - binary 100 (4)"),
    ]
    conv_id = models.ForeignKey(Converter, on_delete=models.CASCADE)
    ledcalib_low = models.IntegerField()
    ledcalib_high = models.IntegerField()
    channel = models.CharField(max_length=1, choices=CHANNELS)


class CcrCalib(models.Model):
    CHANNELS = [
        ("1", "1con - one channel"),
        ("A", "2con - channel A"),
        ("B", "2con - channel B"),
    ]
    conv_id = models.ForeignKey(Converter, on_delete=models.CASCADE)
    calibccrlo = models.IntegerField()
    calibccrhi = models.IntegerField()
    channel = models.CharField(max_length=1, choices=CHANNELS)
