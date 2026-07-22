"""New method-comparison figure for the Bochner PINN paper -- replaces the old 'Spectral PINN'-labelled
ones. The Bochner (distributional) loss vs the plain L2 loss, across TWO neural architectures: the PINN
and the Fourier Neural Operator. Real metrics, 8-seed PINN + multi-seed FNO; variance ratio (ideal = 1).
Architecture = panel; loss = legend (named once) -- so 'Bochner' appears twice, not on every bar."""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"font.family": "serif", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "grid.color": "#e7e7e7",
                     "axes.axisbelow": True, "figure.dpi": 150})
VAN, BOC = "#9a9a9a", "#D55E00"                                   # vanilla L2 / Bochner loss
EVAL = "/home/hubi/research/useful/code/spde-inne/results_eval/summary.json"
SFNO = "/home/hubi/research/potentially_useful/spde-inne_results_spectral_fno/summary_eval.json"
OUT = "/home/hubi/research/useful/papers/paper1_bochner_pinn/figures/"

# --- load PINN (8-seed) and FNO variance ratios from the real eval JSONs ---
pinn = json.load(open(EVAL))
PINN_PROB = {"burgers_vg": "Burgers-VG", "heston_vg": "Heston-VG"}
pinn_rows = [(lab,
              pinn[k]["vanilla"]["var_ratio"]["mean"], pinn[k]["vanilla"]["var_ratio"]["std"],
              pinn[k]["spectral"]["var_ratio"]["mean"], pinn[k]["spectral"]["var_ratio"]["std"])
             for k, lab in PINN_PROB.items()]

fno = json.load(open(SFNO))
FNO_PROB = {"burgers": "Burgers", "heston": "Heston", "bs_levy": "BS-Lévy", "fpl": "FPL", "ns2d": "NS-2D"}
fno_rows = [(lab, fno[k]["vanilla"]["var_ratio_mean"], fno[k]["vanilla"]["var_ratio_std"],
             fno[k]["spectral"]["var_ratio_mean"], fno[k]["spectral"]["var_ratio_std"])
            for k, lab in FNO_PROB.items()]


def panel(ax, rows, title):
    x = np.arange(len(rows)); w = 0.38
    vm = [r[1] for r in rows]; vs = [r[2] for r in rows]
    bm = [r[3] for r in rows]; bs = [r[4] for r in rows]
    ax.bar(x - w / 2, vm, w, yerr=vs, color=VAN, edgecolor="#444", lw=0.6, capsize=3, label="plain $L^2$ loss")
    ax.bar(x + w / 2, bm, w, yerr=bs, color=BOC, edgecolor="#5a2a00", lw=0.6, capsize=3, label="Bochner loss")
    for xi, v in zip(x, vm):                                       # flag total variance collapse (bar ~ 0)
        if v < 0.05:
            ax.annotate("$\\approx\\!0$\n(collapse)", xy=(xi - w / 2, 0.005), xytext=(xi - w / 2, 0.20),
                        fontsize=7.5, ha="center", color="#444", arrowprops=dict(arrowstyle="-", color="#999", lw=0.7))
    ax.axhline(1.0, color="#222", ls=(0, (5, 3)), lw=1.0)
    ax.text(len(rows) - 0.5, 1.02, "ideal (var. matched)", fontsize=8, ha="right", color="#222")
    ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows], fontsize=9)
    ax.set_ylim(0, 1.25); ax.set_title(title, fontsize=12, fontweight="bold")
    ax.grid(axis="y"); ax.set_axisbelow(True)


fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [2, 5]})
panel(ax[0], pinn_rows, "(a) PINN  (physics-only, no data)")
panel(ax[1], fno_rows, "(b) Fourier Neural Operator  (data-driven)")
ax[0].set_ylabel("variance ratio  $\\widehat{\\mathrm{Var}}\\,/\\,\\mathrm{Var}_{\\mathrm{ref}}$")
ax[1].legend(loc="lower right", fontsize=9.5, framealpha=0.95, ncol=2)
fig.suptitle("The Bochner loss closes the variance gap across architectures "
             "(plain $L^2$ collapses it; the Bochner loss restores var. ratio $\\to 1$)",
             fontsize=12.5, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig(OUT + "fig_method_comparison_new.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig_method_comparison_new.png", dpi=160, bbox_inches="tight")
print("saved fig_method_comparison_new.{pdf,png}")
print("PINN  var-ratio:", [(r[0], round(r[1], 2), round(r[3], 2)) for r in pinn_rows])
print("FNO   var-ratio:", [(r[0], round(r[1], 2), round(r[3], 2)) for r in fno_rows])
