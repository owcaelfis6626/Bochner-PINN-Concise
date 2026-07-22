"""Regenerate the Bochner PINN field figures (fig05 snapshots, fig07 errors) from the real ensemble
fields -- replacing the old 'Spectral PINN'-labelled versions. Heston-VG 2D SPDE, 3 channels."""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({"font.family": "serif", "font.size": 10, "figure.dpi": 150})
NPZ = "/home/hubi/spde/results_spectral_v24/results_spectral_v24/ensemble_fields.npz"
OUT = "/home/hubi/research/useful/papers/paper1_bochner_pinn/figures/"
d = np.load(NPZ)
x, t = d["x_grid"], d["t_grid"]
EXT = [t.min(), t.max(), x.min(), x.max()]
CH = [("Z", r"price $z(x,t)$"), ("Y", r"volatility $y(x,t)$"), ("P", r"jump intensity $p(x,t)$")]


def hm(ax, fld, vmin, vmax, cmap="RdBu_r"):
    return ax.imshow(fld, extent=EXT, origin="lower", aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)


# ---- fig05: Bochner PINN mean field vs FD reference (3 channels x 2) ----
fig, ax = plt.subplots(3, 2, figsize=(8.4, 8.0))
for i, (c, lab) in enumerate(CH):
    pm, rf = d[c + "_mean"], d[c + "_ref"]
    vmax = max(abs(rf).max(), abs(pm).max()); vmin = -vmax if rf.min() < -1e-6 else rf.min()
    im = hm(ax[i, 0], pm, vmin, vmax); hm(ax[i, 1], rf, vmin, vmax)
    ax[i, 0].set_ylabel(lab + "\n\n$x$", fontsize=10)
    fig.colorbar(im, ax=ax[i, :].tolist(), fraction=0.025, pad=0.02)
    rel = np.linalg.norm(pm - rf) / np.linalg.norm(rf)
    ax[i, 0].set_title(f"Bochner PINN  (rel. $L^2$ {rel:.3f})" if i == 0 else f"Bochner PINN  (rel. $L^2$ {rel:.3f})", fontsize=10)
    ax[i, 1].set_title("finite-difference reference", fontsize=10)
for j in range(2):
    ax[2, j].set_xlabel("$t$")
fig.suptitle("Bochner PINN reconstructs the Heston-VG fields (ensemble mean vs FD reference)",
             fontsize=12, fontweight="bold", y=0.995)
fig.savefig(OUT + "fig05_field_snapshots_spectral.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig05_field_snapshots_spectral.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# ---- fig07: pointwise absolute error |Bochner mean - FD| (1 x 3) ----
fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
for i, (c, lab) in enumerate(CH):
    err = np.abs(d[c + "_mean"] - d[c + "_ref"])
    im = hm(ax[i], err, 0, err.max(), cmap="magma")
    ax[i].set_title(lab + f"\n max $|u_\\theta-u_{{\\mathrm{{FD}}}}|$ = {err.max():.3f}", fontsize=10)
    ax[i].set_xlabel("$t$"); fig.colorbar(im, ax=ax[i], fraction=0.046, pad=0.03)
ax[0].set_ylabel("$x$")
fig.suptitle("Bochner PINN pointwise error: concentrated at jump cores, bulk field within MC noise",
             fontsize=12, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig(OUT + "fig07_field_errors_spectral.pdf", bbox_inches="tight")
fig.savefig(OUT + "fig07_field_errors_spectral.png", dpi=130, bbox_inches="tight")
plt.close(fig)
print("regenerated fig05 (field snapshots) + fig07 (field errors) with Bochner naming")
