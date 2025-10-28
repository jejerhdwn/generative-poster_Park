Python 3.11.2 (v3.11.2:878ead1ac1, Feb  7 2023, 10:02:41) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt
from io import BytesIO

# --- 페이지 설정
st.set_page_config(
    page_title="Pastel Stars",
    page_icon="⭐",
    layout="centered",
)

st.title("🎨 Pastel Stars Generator (matplotlib)")

# --- 파스텔톤 팔레트 (기존과 동일)
PASTEL_COLORS = [
    "#FFB3BA",  # pastel pink
    "#FFDFBA",  # pastel orange
    "#FFFFBA",  # pastel yellow
    "#BAFFC9",  # pastel green
    "#BAE1FF",  # pastel blue
    "#E2BAFF",  # pastel purple
]

def draw_star(ax, center, size, color, wobble=0.0):
    num_points = 5  # 5-pointed star
    outer_points, inner_points = [], []

    for i in range(num_points * 2):
        angle = np.pi / num_points * i
        radius = size if i % 2 == 0 else size * 0.4
        radius *= random.uniform(1 - wobble, 1 + wobble)
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        if i % 2 == 0:
            outer_points.append((x, y))
        else:
            inner_points.append((x, y))

    points = []
    for i in range(num_points):
        points.append(outer_points[i])
        points.append(inner_points[i])
    points.append(outer_points[0])

    x_vals, y_vals = zip(*points)
    ax.fill(x_vals, y_vals, color=color, alpha=0.8)

def render(fig_w=8, fig_h=8, n_stars=15, size_min=0.3, size_max=0.8,
           wobble_min=0.02, wobble_max=0.1, xlim=(0,10), ylim=(0,10), seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')

    for _ in range(n_stars):
        x = random.uniform(xlim[0]+0.5, xlim[1]-0.5)
        y = random.uniform(ylim[0]+0.5, ylim[1]-0.5)
        size = random.uniform(size_min, size_max)
        color = random.choice(PASTEL_COLORS)
        wobble = random.uniform(wobble_min, wobble_max)
        draw_star(ax, (x, y), size, color, wobble=wobble)

    return fig

# --- Sidebar: 컨트롤
st.sidebar.header("Controls")
n_stars = st.sidebar.slider("Number of stars", 1, 100, 15, 1)
... size_min, size_max = st.sidebar.slider("Star size range", 0.1, 2.0, (0.3, 0.8), 0.05)
... wobble_min, wobble_max = st.sidebar.slider("Wobble range", 0.0, 0.5, (0.02, 0.1), 0.01)
... fig_w = st.sidebar.slider("Figure width (inches)", 4, 16, 8, 1)
... fig_h = st.sidebar.slider("Figure height (inches)", 4, 16, 8, 1)
... 
... use_seed = st.sidebar.checkbox("Use fixed random seed (reproducible)", value=False)
... seed_val = st.sidebar.number_input("Seed", min_value=0, max_value=10_000_000, value=42, step=1, disabled=not use_seed)
... 
... regen = st.sidebar.button("🔄 Regenerate")
... 
... # --- 그리기
... seed = seed_val if use_seed else None
... fig = render(
...     fig_w=fig_w,
...     fig_h=fig_h,
...     n_stars=n_stars,
...     size_min=size_min,
...     size_max=size_max,
...     wobble_min=wobble_min,
...     wobble_max=wobble_max,
...     seed=seed if (use_seed or regen) else None,  # 버튼 누를 때마다 갱신
... )
... 
... st.pyplot(fig)
... 
... # --- 다운로드 버튼 (PNG)
... png_buf = BytesIO()
... fig.savefig(png_buf, format="png", dpi=200, bbox_inches="tight")
... png_buf.seek(0)
... st.download_button(
...     label="⬇️ Download PNG",
...     data=png_buf,
...     file_name="pastel_stars.png",
...     mime="image/png",
... )
