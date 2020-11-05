from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from pandas import read_pickle
from pathlib import Path

# Create your views here.
# pandas playground
STATIC_DIR = Path(__file__, "..", "..", "..", "static").resolve()
RELMU_VS_H = read_pickle(
    Path(STATIC_DIR, "data", "magnetics", "mu_perc_vs_H.pkl"))
B_VS_H = read_pickle(
    Path(STATIC_DIR, "data", "magnetics", "B_vs_H.pkl"))
PC_VS_B = read_pickle(
    Path(STATIC_DIR, "data", "magnetics", "Pc_vs_B-fsw.pkl"))


def magneticsIndex(request):
    print(RELMU_VS_H[["Material", "Initial Permeability"]])
    return render(request, "magnetics/index.html")
