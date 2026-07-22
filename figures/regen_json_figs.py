"""Regenerate fig03 (spectrum matching), fig16 (Bochner PINN vs Bochner FNO variance), fig17 (log-PSD)
from the real eval JSONs, with Bochner naming. Companions to fig02 (variance)."""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"font.family": "serif", "font.size": 10.5, "axes.spines.top": False,
                     "axes.spines.right": False, "grid.color": "#e7e7e7", "figure.dpi": 150})
EV = json.load(open("/home/hubi/research/useful/code/spde-inne/results_eval/summary.json"))
FN = json.load(open("/home/hubi/research/potentially_useful/spde-inne_results_spectral_fno/summary_eval.json"))
OUT = "/home/hubi/research/useful/papers/paper1_bochner_pinn/figures/"
VAN, BOC, BFNO = "#9a9a9a", "#D55E00", "#0072B2"
PL = {"burgers_vg": "Burgers-VG", "heston_vg": "Heston-VG"}

# ---- fig03: spectrum matching (log-spatial-PSD error) vanilla vs Bochner, log y ----
fig, ax = plt.subplots(figsize=(5.4, 4.0)); x = np.arange(len(PL)); w = 0.38
van = [EV[k]["vanilla"]["sp_err"]["mean"] for k in PL]; vs = [EV[k]["vanilla"]["sp_err"]["std"] for k in PL]
boc = [EV[k]["spectral"]["sp_err"]["mean"] for k in PL]; bs = [EV[k]["spectral"]["sp_err"]["std"] for k in PL]
ax.bar(x - w / 2, van, w, yerr=vs, color=VAN, edgecolor="#444", lw=0.6, capsize=3, label="plain $L^2$ loss")
ax.bar(x + w / 2, boc, w, yerr=bs, color=BOC, edgecolor="#5a2a00", lw=0.6, capsize=3, label="Bochner loss")
ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(list(PL.values()))
ax.set_ylabel("log-spatial-PSD MSE  (lower better)"); ax.legend(fontsize=9.5)
ax.set_title("Spectrum matching: the Bochner loss\ncuts the PSD error $3$--$50\\times$", fontsize=11, fontweight="bold")
ax.grid(axis="y", which="both"); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(OUT + "fig03_logpsd_bars.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig03_logpsd_bars.png", dpi=140, bbox_inches="tight"); plt.close(fig)

# ---- fig16 + fig17: Bochner PINN vs Bochner FNO (the loss is architecture-agnostic) ----
COMMON = {"burgers": "Burgers", "heston": "Heston"}                # benchmarks both ran
pinn_key = {"burgers": "burgers_vg", "heston": "heston_vg"}


def pinn_fno(metric_pinn, metric_fno):
    pinn = [EV[pinn_key[k]]["spectral"][metric_pinn]["mean"] for k in COMMON]
    fno = [FN[k]["spectral"][metric_fno] for k in COMMON]
    return pinn, fno


for fid, (mp, mf, ylab, title, logy) in {
    "fig16_spectral_fno_var": ("var_ratio", "var_ratio_mean", "variance ratio (ideal $=1$)",
                               "The Bochner loss lifts variance fidelity on both;\nthe data-driven FNO reaches higher on hard Heston", False),
    "fig17_spectral_fno_logpsd": ("sp_err", "log_sp_mse_mean", "log-spatial-PSD MSE (lower better)",
                                  "Spectrum fidelity, Bochner PINN vs Bochner FNO", True)}.items():
    pinn, fno = pinn_fno(mp, mf)
    fig, ax = plt.subplots(figsize=(5.2, 4.0)); x = np.arange(len(COMMON)); w = 0.38
    ax.bar(x - w / 2, pinn, w, color=BOC, edgecolor="#5a2a00", lw=0.6, label="Bochner PINN")
    ax.bar(x + w / 2, fno, w, color=BFNO, edgecolor="#003c5e", lw=0.6, label="Bochner FNO")
    if not logy:
        ax.axhline(1.0, color="#222", ls=(0, (5, 3)), lw=1.0); ax.set_ylim(0, 1.25)
    else:
        ax.set_yscale("log")
    ax.set_xticks(x); ax.set_xticklabels(list(COMMON.values())); ax.set_ylabel(ylab)
    ax.legend(fontsize=9.5); ax.set_title(title, fontsize=11, fontweight="bold")
    ax.grid(axis="y", which="both"); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(OUT + fid + ".pdf", bbox_inches="tight")
    fig.savefig(OUT + fid + ".png", dpi=140, bbox_inches="tight"); plt.close(fig)

print("regenerated fig03, fig16, fig17")
print("  fig03 sp_err van/boc:", [(k, round(EV[k]["vanilla"]["sp_err"]["mean"], 2), round(EV[k]["spectral"]["sp_err"]["mean"], 2)) for k in PL])
print("  fig16 var PINN/FNO:", list(zip(*pinn_fno("var_ratio", "var_ratio_mean"))))
