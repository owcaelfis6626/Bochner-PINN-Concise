"""Produce the ~20pp 'knapp' (concise) Bochner-loss-only version of Paper 1 from the full main.tex.
Keeps the Bochner-loss core; exiles the 3D extension, the long convergence proofs, the Heston deep-dives,
the finance app, and ~13 figures. Preserves thm:main + thm:levy-ext (referenced in kept text)."""

import re

SRC = "/home/hubi/research/useful/papers/paper1_bochner_pinn/main.tex"
DST = "/home/hubi/research/useful/papers/bochnerknapp/main.tex"

# regex (DOTALL) trims of abstract/contribution prose that advertised now-exiled content;
# applied BEFORE the small ref-replacements so prop:levy-ito etc. still match in original form
REGEX_FIX = [
    (r"structure\); the full law is certified.*?in that regime\.", lambda m: "structure)."),
    (r"FNO benchmarks, and six.*?without retuning\.", lambda m: "FNO benchmarks."),
    (r"\s*We also identify and cure.*?random resampling\.", lambda m: ""),
    (r"\(Proposition~\\ref\{thm:levy-ext\}\), and a full-law bound.*?positivity assumption\.",
     lambda m: r"(Proposition~\ref{thm:levy-ext}); full-law and higher-cumulant extensions are "
               r"given in the extended version."),
    (r"The 3D extension\s*\(Section~\\ref\{sec:3d\}\) uses Neumann boundaries, but more general"
     r".*?non-Cartesian sub-grid; this is open\.",
     lambda m: "The method uses a Cartesian spectral sub-grid; more general non-periodic geometries "
               "(curved, multi-component) require a non-Cartesian sub-grid; this is open."),
    (r"solution that transfers from 2D synthetic SPDEs to 3D extensions and\s*to real-world "
     r"calibrated drivers without further modification\.",
     lambda m: r"solution that applies unchanged across L\'evy-driven SPDE families and across "
               r"architectures (PINN and FNO)."),
    # conclusion recap advertised the cut 3D + six-real-data results -> keep only the FNO point
    (r"Three further validations extend the synthetic-benchmark result\..*?architecture-agnostic\.",
     lambda m: "The same loss applied to a Fourier Neural Operator surrogate closes the variance gap "
               "on four of five problems, demonstrating that the construction is architecture-agnostic."),
]

# line ranges (1-indexed, inclusive) in the ORIGINAL main.tex to remove
CUT_RANGES = [
    (302, 494),    # Intro: "Gap analysis" + "Section roadmap"
    (625, 652),    # Method: "Why this is the right object" (justification)
    (733, 756),    # Method: "Cumulant-matching loss" (an extension beyond the 3 terms)
    (792, 803),    # Method: "Complexity"
    (889, 944),    # theory: "Why the log scale is the right choice" (justification)
    (1105, 1211),  # convergence proof after thm:main + bias-only remark (keep thm:main 1076-1104)
    (1224, 1329),  # extension props 3-4 + proof sketches + Zolotarev remark (keep thm:levy-ext 1212-1223)
    (223, 233),    # contribution item: "Sub-grid overfit diagnosis and fix" (cut content)
    (234, 242),    # contribution item: "Cumulant matching for kurtosis" (cut)
    (243, 250),    # contribution item: "Levy intensity threshold sweep" (cut)
    (271, 281),    # contribution item: "3D extension" (cut)
    (282, 295),    # contribution item: "Real-world calibration on six datasets" (cut)
    (1330, 1359),  # theory: "Heston volatility channel: initial diagnosis"
    (1602, 1726),  # results: "Heston-VG volatility channel: sub-grid overfit diagnosis" (+ fig14, fig18_heston)
    (1727, 1762),  # results: "Qualitative comparison: field snapshots" (fig05/06/07/08)
    (1857, 1871),  # results: "Comparison with concurrent neural-spectral methods"
    (1993, 2202),  # whole "Extension to 3D problems" section (+ fig18_grid, fig20, fig21)
    (2224, 2280),  # discussion: Heston-diagnosed + S-channel deep-dives
]
# broken cross-refs (labels now exiled) -> neutralize to plain text
POST_FIX = [
    ("Proposition~\\ref{prop:levy-ito}", "the full-law extension"),
    ("Proposition~\\ref{cor:berry-esseen}", "the Berry--Esseen result"),
    ("Section~\\ref{subsec:heston-diag}", "the extended version"),
    ("Section~\\ref{sec:3d}", "the extended version"),
    ("Section~\\ref{subsec:levy-ext}", "the extended version"),
    ("Figure~\\ref{fig:snapshots}", "the extended version"),
    ("Figure~\\ref{fig:snapshots_fno}", "the extended version"),
    ("Figure~\\ref{fig:errors_spectral}", "the extended version"),
    ("Section~\\ref{subsec:cumulant-loss}", "the extended version"),
    ("~\\ref{subsec:cumulant-loss}", " (extended version)"),
    ("Section~\\ref{subsec:log-scale}", "the extended version"),
    ("~\\ref{subsec:log-scale}", " (extended version)"),
]
# figures embedded in KEPT sections that we still drop
CULL = {"fig04_y_outlier", "fig07_field_errors_spectral", "fig08_field_errors_fno",
        "fig13_summary_metrics_table", "fig09_fno_vs_pinn_evolution", "fig10_unified_comparison",
        "fig11_comprehensive_spectral", "fig12_comprehensive_fno"}

lines = open(SRC).read().split("\n")
remove = [False] * len(lines)
for a, b in CUT_RANGES:
    for i in range(a - 1, b):
        remove[i] = True

# drop \begin{figure}..\end{figure} blocks containing a culled filename
i = 0
while i < len(lines):
    if "\\begin{figure}" in lines[i]:
        j = i
        while j < len(lines) and "\\end{figure}" not in lines[j]:
            j += 1
        if any(f in " ".join(lines[i:j + 1]) for f in CULL):
            for k in range(i, j + 1):
                remove[k] = True
        i = j + 1
    else:
        i += 1

text = "\n".join(l for k, l in enumerate(lines) if not remove[k])
text = text.replace("\\documentclass[review,12pt]{elsarticle}", "\\documentclass[10pt]{elsarticle}")
for pat, repl in REGEX_FIX:
    text = re.sub(pat, repl, text, flags=re.DOTALL)
for a, b in POST_FIX:
    text = text.replace(a, b)
text = re.sub(r"\. the extended version", ". The extended version", text)  # capitalise after a period
open(DST, "w").write(text)
out = text.split("\n")
print(f"kept {len(out)}/{len(lines)} lines; figures kept: "
      f"{sum('includegraphics' in l for l in out)} (was {sum('includegraphics' in l for l in lines)})")
