"""Regenerate fig06 (Bochner FNO field snapshots) + fig08 (errors) from the re-evaluated FNO fields
(_fno_fields.npz), matching the fig05/fig07 Bochner-PINN layout. Heston-VG 2D SPDE, 3 channels."""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"font.family": "serif", "font.size": 10, "figure.dpi": 150})
F = np.load("/home/hubi/research/useful/papers/paper1_bochner_pinn/figures/_fno_fields.npz")
OUT = "/home/hubi/research/useful/papers/paper1_bochner_pinn/figures/"
x, t = F["x_grid"], F["t_grid"]
EXT = [t.min(), t.max(), x.min(), x.max()]
CH = [("Z", r"price $z(x,t)$"), ("Y", r"volatility $y(x,t)$"), ("P", r"jump intensity $p(x,t)$")]
R = 0                                                          # representative test realization


def hm(ax, fld, vmin, vmax, cmap="RdBu_r"):
    return ax.imshow(fld, extent=EXT, origin="lower", aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)


# ---- fig06: Bochner FNO prediction vs FD reference ----
fig, ax = plt.subplots(3, 2, figsize=(8.4, 8.0))
for i, (c, lab) in enumerate(CH):
    pr, rf = F[c + "_fno"][R], F[c + "_ref"][R]
    vmax = max(abs(rf).max(), abs(pr).max()); vmin = -vmax if rf.min() < -1e-6 else float(rf.min())
    im = hm(ax[i, 0], pr, vmin, vmax); hm(ax[i, 1], rf, vmin, vmax)
    ax[i, 0].set_ylabel(lab + "\n\n$x$", fontsize=10)
    fig.colorbar(im, ax=ax[i, :].tolist(), fraction=0.025, pad=0.02)
    rel = np.linalg.norm(pr - rf) / np.linalg.norm(rf)
    ax[i, 0].set_title(f"Bochner FNO  (rel. $L^2$ {rel:.3f})", fontsize=10)
    ax[i, 1].set_title("finite-difference reference", fontsize=10)
for j in range(2):
    ax[2, j].set_xlabel("$t$")
fig.suptitle("Bochner FNO reconstructs the Heston-VG fields (prediction vs FD reference)",
             fontsize=12, fontweight="bold", y=0.995)
fig.savefig(OUT + "fig06_field_snapshots_fno.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig06_field_snapshots_fno.png", dpi=130, bbox_inches="tight"); plt.close(fig)

# ---- fig08: pointwise absolute error ----
fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
for i, (c, lab) in enumerate(CH):
    err = np.abs(F[c + "_fno"][R] - F[c + "_ref"][R])
    im = hm(ax[i], err, 0, err.max(), cmap="magma")
    ax[i].set_title(lab + f"\n max $|u_\\theta-u_{{\\mathrm{{FD}}}}|$ = {err.max():.3f}", fontsize=10)
    ax[i].set_xlabel("$t$"); fig.colorbar(im, ax=ax[i], fraction=0.046, pad=0.03)
ax[0].set_ylabel("$x$")
fig.suptitle("Bochner FNO pointwise error, same realisation and slices as the FD reference",
             fontsize=12, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig(OUT + "fig08_field_errors_fno.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig08_field_errors_fno.png", dpi=130, bbox_inches="tight"); plt.close(fig)
print("regenerated fig06 + fig08 (Bochner FNO fields)")
for c, lab in CH:
    print(f"  {c}: rel_L2={np.linalg.norm(F[c+'_fno'][R]-F[c+'_ref'][R])/np.linalg.norm(F[c+'_ref'][R]):.3f}")
