"""Aether GT: a 3D electric sports car built with Python.

Requires: pip install numpy matplotlib
Run:      python aether_gt_3d.py        (saves aether_gt_views.png and opens a window)
Units are meters. X = length (front is +X), Y = width, Z = height.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")  # remove this line to get an interactive window you can rotate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ---------- geometry helpers ----------
def extrude_profile(profile, half_width):
    """Turn a 2D side profile [(x, z), ...] into a closed 3D solid of given half width."""
    pts = np.array(profile)
    left = [(x, -half_width, z) for x, z in pts]
    right = [(x, half_width, z) for x, z in pts]
    faces = [left, right]  # two side panels
    n = len(pts)
    for i in range(n):  # connecting strips along the outline
        j = (i + 1) % n
        faces.append([left[i], left[j], right[j], right[i]])
    return faces


def cylinder(cx, cy, cz, radius, width, segments=36):
    """Wheel: cylinder whose axis runs along Y."""
    t = np.linspace(0, 2 * np.pi, segments + 1)
    faces = []
    for a, b in zip(t[:-1], t[1:]):
        p = lambda ang, y: (cx + radius * np.cos(ang), cy + y, cz + radius * np.sin(ang))
        faces.append([p(a, -width / 2), p(b, -width / 2), p(b, width / 2), p(a, width / 2)])
    for y in (-width / 2, width / 2):
        faces.append([(cx + radius * np.cos(a), cy + y, cz + radius * np.sin(a)) for a in t[:-1]])
    return faces


def box(x0, x1, y0, y1, z0, z1):
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    idx = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
    return [[v[i] for i in f] for f in idx]


# ---------- car definition ----------
BODY_PROFILE = [  # side view, rear to front along the lower edge, then back along the top
    (-2.25, 0.32), (-2.28, 0.58), (-2.10, 0.76), (-1.50, 0.80), (-0.90, 0.78),
    (0.90, 0.74), (1.60, 0.66), (2.10, 0.50), (2.28, 0.40), (2.20, 0.32),
]
CANOPY_PROFILE = [(-1.55, 0.78), (-1.10, 1.05), (-0.50, 1.18), (0.05, 1.20), (0.60, 1.12), (1.10, 0.74)]

PAINTS = {
    "Arctic Pearl": "#f2f4f7",
    "Solar Flare": "#e8641a",
    "Midnight Volt": "#16224a",
    "Lunar Titanium": "#8d9298",
}


def build_car(paint="#f2f4f7"):
    parts = []  # (faces, facecolor, edgecolor)
    parts.append((extrude_profile(BODY_PROFILE, 0.85), paint, "#555a62"))
    parts.append((extrude_profile(CANOPY_PROFILE, 0.66), "#0b1118", "#2a3340"))
    parts.append((box(2.24, 2.30, -0.78, 0.78, 0.50, 0.55), "#7fe3ff", "#7fe3ff"))   # front light bar
    parts.append((box(-2.31, -2.27, -0.76, 0.76, 0.60, 0.65), "#ff3b3b", "#ff3b3b"))  # tail light
    parts.append((box(-2.35, -1.75, -0.76, 0.76, 0.84, 0.88), paint, "#555a62"))      # spoiler
    parts.append((box(1.95, 2.30, -0.82, 0.82, 0.28, 0.33), "#15181d", "#15181d"))    # front splitter
    for x, r, w in ((1.35, 0.36, 0.30), (-1.35, 0.38, 0.34)):
        for side in (-1, 1):
            parts.append((cylinder(x, side * 0.92, r, r, w), "#15181d", "#000000"))
            parts.append((cylinder(x, side * (0.92 + 0.02), r, r * 0.68, w), "#aab3bf", "#6b727c"))
    return parts


def draw(ax, parts, elev, azim, title):
    for faces, face, edge in parts:
        poly = Poly3DCollection(faces, facecolors=face, edgecolors=edge, linewidths=0.3, alpha=1.0)
        ax.add_collection3d(poly)
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-1.3, 1.3)
    ax.set_zlim(0, 1.4)
    ax.set_box_aspect((5.0, 2.6, 1.4), zoom=0.95)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=11)


def main():
    fig = plt.figure(figsize=(14, 9))
    views = [
        (18, -55, "Front three-quarter"),
        (18, 125, "Rear three-quarter"),
        (0, -90, "Side profile"),
        (90, -90, "Top view"),
    ]
    for i, (elev, azim, title) in enumerate(views, start=1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        draw(ax, build_car(PAINTS["Arctic Pearl"]), elev, azim, title)
    fig.suptitle("Aether GT: electric sports car concept", fontsize=15)
    fig.tight_layout()
    fig.savefig("aether_gt_views.png", dpi=140)

    # one render per paint color
    fig2 = plt.figure(figsize=(14, 7))
    for i, (name, color) in enumerate(PAINTS.items(), start=1):
        ax = fig2.add_subplot(2, 2, i, projection="3d")
        draw(ax, build_car(color), 18, -55, name)
    fig2.tight_layout()
    fig2.savefig("aether_gt_colors.png", dpi=140)
    print("Saved aether_gt_views.png and aether_gt_colors.png")


if __name__ == "__main__":
    main()
