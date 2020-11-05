from django.db import models
from pathlib import Path
from pandas import read_pickle

# Create your models here.
MATERIAL_CHOICES = [
    ("MPP", "Moly Permalloy Power"),
    ("HF", "High Flux"),
    ("HFspec", "High Flux special core"),
    ("Edge", "Edge"),
    ("Kmu HF", "Koolmu High Frequency"),
    ("Kmu", "Koolmu"),
    ("XFlux", "XFlux"),
    ("75S", "75 Series"),
    ("Kmu M", "Koolmu MAX"),
    ("Kmu E-U-Bl", "Koolmu E-core, U-core, block"),
    ("XF E-U-Bl", "XFlux E-core, U-core, block"),
    ("HF EQ-LP", "High Flux EQ & LP"),
    ("Kmu EQ-LP", "Koolmu Flux EQ & LP"),
    ("XF EQ-LP", "XFlux Flux EQ & LP"),
]

# PANDAS
STATIC_DIR = Path(__file__, "..", "..", "..", "static").resolve()
RELMU_VS_H = read_pickle(
    Path(STATIC_DIR, "data", "magnetics", "mu_perc_vs_H.pkl"))
B_VS_H = read_pickle(
    Path(STATIC_DIR, "data", "magnetics", "B_vs_H.pkl"))
PC_VS_B = read_pickle(
    Path(STATIC_DIR, "data", "magnetics", "Pc_vs_B-fsw.pkl"))


def generate_core_from_pd(df):
    subset = df[["Material", "Initial Permeability"]]
    print(subset[subset.duplicated(keep=False)])


class Core(models.Model):
    material = models.CharField(max_length=10,
                                choices=MATERIAL_CHOICES, blank=False, null=False)
    init_perm = models.PositiveSmallIntegerField(blank=False, null=False)

    def __str__(self):
        return f"Material: {self.get_material_display()}, initial permeability: {self.init_perm}"


class DCBiasFactors(models.Model):
    """ 
        DB contains the factors for the calculation of relative permeability %mi in function of excitation H [Oersted]
        Formula: %µi = (1 / (a + b * H**c ))
    """
    core_id = models.OneToOneField(Core, on_delete=models.CASCADE)
    a = models.FloatField(blank=False, null=False)
    b = models.FloatField(blank=False, null=False)
    c = models.FloatField(blank=False, null=False)


class CoreLossFactors(models.Model):
    """ 
        DB contains the factors for the calculation of core loss density Pl in function of flux density B [T] and switching frequency f [kHz]
        Formula: Pl = (a * B**b * f**c)
    """
    core_id = models.OneToOneField(Core, on_delete=models.CASCADE)
    a = models.FloatField(blank=False, null=False)
    b = models.FloatField(blank=False, null=False)
    c = models.FloatField(blank=False, null=False)


class FluxFactors(models.Model):
    """ 
        DB contains the factors for the calculation of flux density B [T] in function of excitation H [Oersted]
        Formula: B = ( ( a + b * H + c * H**2 ) / ( 1 + d * H + e * H**2 ) )**x
    """
    core_id = models.OneToOneField(Core, on_delete=models.CASCADE)
    a = models.FloatField(blank=False, null=False)
    b = models.FloatField(blank=False, null=False)
    c = models.FloatField(blank=False, null=False)
    d = models.FloatField(blank=False, null=False)
    e = models.FloatField(blank=False, null=False)
    x = models.FloatField(blank=False, null=False)
