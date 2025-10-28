import streamlit as st
import numpy as np
import random
import math
import colorsys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO

# ---------------- Page config ----------------
st.set_page_config(page_title="Generative Star Poster", layout="centered")

# ---------------- Palette ----------------
def hsv_to_rgb_tuple(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (r, g, b)

def random_palette(k=6, mode="vivid", seed=None):
    """
    Generate k colors based on palette mode.
    - pastel: low saturation, high value
    - vivid: high saturation, high value
    - mixed: varied saturation/value
    """
    if seed is not None:
        rnd = random.Random(seed)
        np.random.seed(seed)
    else:
        rnd = random

    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = rnd.random()
            s = rnd.uniform(0.2, 0.4)
            v = rnd.uniform(0.9, 1.0)
            cols.append(hsv_to_rgb_tuple(h, s, v))
        elif mode == "vivid":
            h = rnd.random()
            s = rnd.uniform(0.8, 1.0)
            v = rnd.uniform(0.8, 1.0)
            cols.append(hsv_to_rgb_tuple(h, s, v))
        else:  # mixed
            h = rnd.random()
            s = rnd.uniform(0.4, 1.0)
            v = rnd.uniform(0.6, 1.0)
            cols.append(hsv_to_rgb_tuple(h, s, v))
    return cols

# ---------------- Geometry ----------------
def star_shape(center=(0.5, 0.5), r_outer=0.3, r_inner=0.15, num_points=5, wobble=0.1, rnd=None):
    """
    Generate one star polygon with alternating radii and small wobble.
    Returns arrays x, y.
    """
    if rnd is None:
        rnd = random

    angles = np.linspace(0, 2 * math.pi, num_points * 2, endpoint=False)
    radii = np.empty_like(angles)

    for i in range(len(angles)):
        base_r = r_outer if i % 2 == 0 else r_inner
        radii[i] = base_r * (1 + wobble * (rnd.random() - 0.5))

    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def render_poster(
    n_layers=7,
    palette_mode="vivid",
    fig_w=7,
    fig_h=10,
    bg=(0.98, 0.98, 0.97),
    seed=None
):
    rnd = random.Random(seed) if seed is not None else random

    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = plt.gca()
    ax.axis("off")
    ax.set_facecolor(bg)

    palette = random_palette(6, mode=palette_mode, seed=seed)

    for _ in range(n_layers):
        cx, cy = rnd.random(), rnd.random()
        outer_r = rnd.uniform(0.15, 0.4)
        inner_r = outer_r * rnd.uniform(0.4, 0.7)
        points = rnd.choice([5, 6, 7])
        wobble = rnd.uniform(0.05, 0.25)

        x, y = star_shape(
            center=(cx, cy),
            r_outer=outer_r,
            r_inner=inner_r,
            num_points=points,
            wobble=wobble,
            rnd=rnd
        )
        color = rnd.choice(palette)
        alpha = rnd.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# ---------------- Sidebar Controls ----------------
st.sidebar.subheader("Controls")
n_layers = st.sidebar.slider("Number of layers", 1, 50, 7, 1)
palette_mode = st.sidebar.selectbox("Palette", ["vivid", "pastel", "mixed"], index=0)
fig_w = st.sidebar.slider("Figure width (inches)", 4, 20, 7, 1)
fig_h = st.sidebar.slider("Figure height (inches)", 4, 30, 10, 1)
use_seed = st.sidebar.checkbox("Use fixed seed", value=False)
seed_val = st.sidebar.number_input("Seed", min_value=0, max_value=10_000_000, value=42, step=1, disabled=not use_seed)

title_text = st.sidebar.text_input("Title text", "Generative Star Poster")
subtitle_text = st.sidebar.text_input("Subtitle text", "Week 2 • Arts & Advanced Big Data")
show_text = st.sidebar.checkbox("Show title/subtitle", value=True)

regen = st.sidebar.button("Regenerate")

# ---------------- Render ----------------
seed_to_use = seed_val if use_seed else None
fig = render_poster(
    n_layers=n_layers,
    palette_mode=palette_mode,
    fig_w=fig_w,
    fig_h=fig_h,
    seed=seed_to_use
)

if show_text:
    ax = plt.gca()
    ax.text(0.05, 0.95, title_text, fontsize=18, weight="bold", transform=ax.transAxes)
    ax.text(0.05, 0.91, subtitle_text, fontsize=11, transform=ax.transAxes)

st.pyplot(fig, clear_figure=True)

# ---------------- Download ----------------
png_buf = BytesIO()
fig.savefig(png_buf, format="png", dpi=200, bbox_inches="tight")
png_buf.seek(0)
st.download_button(
    label="Download PNG",
    data=png_buf,
    file_name="generative_star_poster.png",
    mime="image/png",
)

plt.close(fig)
