"""Regenerate fig15 (ablation) from the real ablation_summary.json with Bochner naming.
The three Bochner-loss terms (log-spatial PSD, log-temporal PSD, variance ratio): which are needed?
'full' = all three; single-term configs degrade either the variance OR the spectrum; 'vanilla' = none."""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"font.family": "serif", "font.size": 10.5, "axes.spines.top": False,
                     "axes.spines.right": False, "grid.color": "#e7e7e7", "figure.dpi": 150})
d = json.load(open("/home/hubi/research/useful/code/spde-inne/results_eval/ablation_summary.json"))
OUT = "/home/hubi/research/useful/papers/paper1_bochner_pinn/figures/"
ORD = ["full", "var_only", "t_only", "xy_only", "vanilla"]
NAME = {"full": "full\n(all 3)", "var_only": "var. ratio\nonly", "t_only": "temporal\nPSD only",
        "xy_only": "spatial\nPSD only", "vanilla": "plain $L^2$\n(none)"}
HL = "#D55E00"; OT = "#9a9a9a"
cols = [HL if k == "full" else OT for k in ORD]

fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.9))
x = np.arange(len(ORD))
# (a) variance ratio (ideal 1)
vr = [d[k]["var_ratio_mean"] for k in ORD]; vs = [d[k]["var_ratio_std"] for k in ORD]
ax[0].bar(x, vr, yerr=vs, color=cols, edgecolor="#444", lw=0.6, capsize=3)
ax[0].axhline(1.0, color="#222", ls=(0, (5, 3)), lw=1.0); ax[0].set_ylim(0, 1.35)
ax[0].set_ylabel("variance ratio  (ideal $=1$)"); ax[0].set_title("(a) variance fidelity", fontsize=11, fontweight="bold")
# (b) log spatial-PSD MSE (lower better)
sp = [d[k]["log_sp_mse_mean"] for k in ORD]; ss = [d[k]["log_sp_mse_std"] for k in ORD]
ax[1].bar(x, sp, yerr=ss, color=cols, edgecolor="#444", lw=0.6, capsize=3)
ax[1].set_ylabel("log-spatial-PSD MSE  (lower better)"); ax[1].set_title("(b) spectrum fidelity", fontsize=11, fontweight="bold")
for a in ax:
    a.set_xticks(x); a.set_xticklabels([NAME[k] for k in ORD], fontsize=8.5); a.grid(axis="y"); a.set_axisbelow(True)
fig.suptitle("All three Bochner-loss terms are needed: only the full loss is good on BOTH "
             "variance and spectrum", fontsize=11.5, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig(OUT + "fig15_ablation.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig15_ablation.png", dpi=140, bbox_inches="tight")
print("regenerated fig15_ablation; full var=%.2f sp=%.2f | vanilla var=%.2f sp=%.2f" %
      (d["full"]["var_ratio_mean"], d["full"]["log_sp_mse_mean"], d["vanilla"]["var_ratio_mean"], d["vanilla"]["log_sp_mse_mean"]))
