import streamlit as st
import numpy as np
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# No title/header/caption to avoid markdown rendering.
st.set_page_config(page_title="Stars", layout="centered")

PALETTE = ["#FFB3BA","#FFDFBA","#FFFFBA","#BAFFC9","#BAE1FF","#E2BAFF"]

def draw_star(ax, center, size, color, wobble=0.0):
    num_points = 5
    outer_points, inner_points = [], []
    for i in range(num_points * 2):
        angle = np.pi / num_points * i
        radius = size if i % 2 == 0 else size * 0.4
        radius *= random.uniform(1 - wobble, 1 + wobble)
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        (outer_points if i % 2 == 0 else inner_points).append((x, y))
    pts = []
    for i in range(num_points):
        pts.append(outer_points[i])
        pts.append(inner_points[i])
    pts.append(outer_points[0])
    x_vals, y_vals = zip(*pts)
    ax.fill(x_vals, y_vals, color=color, alpha=0.8)

def render(fig_w=8, fig_h=8, n_stars=15, size_min=0.3, size_max=0.8,
           wobble_min=0.02, wobble_max=0.1, xlim=(0,10), ylim=(0,10), seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal'); ax.axis('off')
    for _ in range(n_stars):
        x = random.uniform(xlim[0]+0.5, xlim[1]-0.5)
        y = random.uniform(ylim[0]+0.5, ylim[1]-0.5)
        size = random.uniform(size_min, size_max)
        color = random.choice(PALETTE)
        wobble = random.uniform(wobble_min, wobble_max)
        draw_star(ax, (x, y), size, color, wobble=wobble)
    return fig

# Minimal sidebar controls with short labels
n_stars = st.sidebar.slider("n", 1, 100, 15, 1)
size_min, size_max = st.sidebar.slider("size", 0.1, 2.0, (0.3, 0.8), 0.05)
wobble_min, wobble_max = st.sidebar.slider("wobble", 0.0, 0.5, (0.02, 0.1), 0.01)
fig_w = st.sidebar.slider("w", 4, 16, 8, 1)
fig_h = st.sidebar.slider("h", 4, 16, 8, 1)
use_seed = st.sidebar.checkbox("seed", value=False)
seed_val = st.sidebar.number_input("s", min_value=0, max_value=10000000, value=42, step=1, disabled=not use_seed)
st.sidebar.button("go")

fig = render(fig_w=fig_w, fig_h=fig_h, n_stars=n_stars, size_min=size_min, size_max=size_max,
             wobble_min=wobble_min, wobble_max=wobble_max, seed=(seed_val if use_seed else None))

st.pyplot(fig, clear_figure=True)
plt.close(fig)
