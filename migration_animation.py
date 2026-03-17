"""
migration_animation.py
──────────────────────
Renders one GIF per corridor type + one "all types" GIF.
Output files land in data/videos/:
    migration_all.gif
    migration_colonial_language.gif
    migration_colonial_only.gif
    migration_shared_language.gif
    migration_shared_only.gif
    migration_language_only.gif
    migration_no_tie.gif

Then migration-map.html wraps them with a dropdown to swap between them.

Run from your project root:
    python migration_animation.py

Requires cartopy:
    conda install -c conda-forge cartopy
    OR: brew install proj geos && pip install cartopy
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.animation import FuncAnimation, PillowWriter
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
TOP_N_CORRIDORS   = 75
FRAME_DURATION_MS = 900
FPS               = 1.1
OUT_DIR           = "data/videos"
os.makedirs(OUT_DIR, exist_ok=True)

TIE_COLORS = {
    "Direct Colonial Tie + Shared Language":       "#E74C3C",
    "Direct Colonial Tie, No Shared Language":     "#E67E22",
    "Shared Colonial Empire + Shared Language":    "#9B59B6",
    "Shared Colonial Empire, No Shared Language":  "#1A9E8F",
    "Shared Language Only":                        "#2980B9",
    "Same Country":                                "#1ABC9C",
    "No Tie":                                      "#7F8C8D",
}
TIE_SHORT = {
    "Direct Colonial Tie + Shared Language":       "Colonial + Shared Language",
    "Direct Colonial Tie, No Shared Language":     "Colonial, No Shared Language",
    "Shared Colonial Empire + Shared Language":    "Shared Empire + Shared Language",
    "Shared Colonial Empire, No Shared Language":  "Shared Empire, No Shared Language",
    "Shared Language Only":                        "Language Only",
    "Same Country":                                "Once Was Same Country",
    "No Tie":                                      "No Tie",
}

# Which GIFs to render: (filename_slug, filter_value or None for all)
RENDERS = [
    ("all",               None),
    ("colonial_language", "Direct Colonial Tie + Shared Language"),
    ("colonial_only",     "Direct Colonial Tie, No Shared Language"),
    ("shared_language",   "Shared Colonial Empire + Shared Language"),
    ("shared_only",       "Shared Colonial Empire, No Shared Language"),
    ("language_only",     "Shared Language Only"),
    ("no_tie",            "No Tie"),
]

BG_COLOR   = "#0A0E1A"
TEXT_COLOR = "#ECF0F1"

COORDS = {
    "AFG": (67.7,  33.9), "SYR": (38.3,  35.0), "SOM": (46.2,   2.0),
    "IRQ": (43.7,  33.2), "COD": (23.7,  -2.9), "MMR": (96.7,  16.9),
    "SDN": (30.2,  15.6), "SSD": (31.3,   6.9), "ETH": (40.5,   9.1),
    "NGA": (8.7,    9.1), "PAK": (69.3,  30.4), "ZWE": (29.2, -20.0),
    "MLI": (-2.0,  17.6), "CAF": (20.9,   6.6), "LBY": (17.2,  26.3),
    "YEM": (47.6,  15.6), "VEN": (-66.6,  6.4), "COL": (-74.3,  4.6),
    "GTM": (-90.2, 15.8), "HND": (-86.6, 15.2), "SLV": (-88.9, 13.8),
    "DRC": (23.7,  -2.9), "CIV": (-5.6,   7.5), "GHA": (-1.0,   7.9),
    "SEN": (-14.5, 14.5), "CMR": (12.4,   3.9), "TCD": (18.7,  15.5),
    "NER": (8.1,   17.6), "GIN": (-11.3,  11.0), "MOZ": (35.5, -18.7),
    "AGO": (17.9, -11.2), "ERI": (39.8,  15.3), "BDI": (29.9,  -3.4),
    "RWA": (29.9,  -1.9), "UKR": (31.2,  49.0), "VNM": (108.3, 14.1),
    "KHM": (104.9, 12.6), "HTI": (-72.3, 18.9), "CUB": (-79.5, 21.5),
    "GEO": (43.4,  42.3), "ARM": (45.0,  40.2), "AZE": (47.6,  40.1),
    "KAZ": (66.9,  48.0), "UZB": (63.9,  41.4), "TJK": (71.3,  38.9),
    "BGD": (90.4,  23.7), "LKA": (80.7,   7.9), "NPL": (84.1,  28.4),
    "USA": (-98.6, 39.8), "DEU": (10.5,  51.2), "FRA": (2.3,   46.2),
    "GBR": (-3.4,  55.4), "CAN": (-96.8, 56.1), "AUS": (133.8,-25.3),
    "SWE": (18.6,  60.1), "NOR": (8.5,   60.5), "NLD": (5.3,   52.1),
    "BEL": (4.5,   50.5), "ITA": (12.6,  42.8), "ESP": (-3.7,  40.4),
    "CHE": (8.2,   46.8), "AUT": (14.6,  47.7), "DNK": (10.0,  56.3),
    "FIN": (25.7,  61.9), "GRC": (21.8,  39.1), "TUR": (35.2,  39.1),
    "JOR": (36.2,  30.6), "LBN": (35.5,  33.9), "UGA": (32.3,   1.4),
    "KEN": (37.9,  -0.0), "ZAF": (25.1, -29.0), "EGY": (30.8,  26.8),
    "MAR": (-7.1,  31.8), "IND": (78.9,  20.6), "BGD": (90.4,  23.7),
    "BRA": (-51.9,-14.2), "MEX": (-102.6,23.6), "ARG": (-63.6,-38.4),
    "THA": (100.9, 15.9), "MYS": (109.7,  2.5), "IDN": (113.9, -0.8),
    "JPN": (138.3, 36.2), "CHN": (104.2, 35.9), "RUS": (99.0,  61.5),
    "SAU": (45.1,  24.2), "IRN": (53.7,  32.4), "PSE": (35.3,  31.9),
}

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/unhcr_colonial.csv")
df = df[~df["year"].isin([2024, 2025, 2026])].copy()
if "tie_type" not in df.columns:
    raise ValueError("tie_type column missing — run build_colonial_vars.py first")

df = df[df["iso_o"].isin(COORDS) & df["iso_d"].isin(COORDS)].copy()
years = sorted(df["year"].unique())
print(f"Loaded: {df.shape[0]:,} rows | {min(years)}–{max(years)} | {len(years)} frames")

# ─────────────────────────────────────────────────────────────────────────────
# CARTOPY SETUP
# ─────────────────────────────────────────────────────────────────────────────
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    USE_CARTOPY = True
    print("Using cartopy for map background")
except ImportError:
    USE_CARTOPY = False
    print("cartopy not available — install it for a proper map background")

# ─────────────────────────────────────────────────────────────────────────────
# ARC HELPER
# ─────────────────────────────────────────────────────────────────────────────
def great_circle_arc(lon1, lat1, lon2, lat2, n=80):
    lons = np.linspace(lon1, lon2, n)
    lats = np.linspace(lat1, lat2, n)
    t    = np.linspace(0, 1, n)
    lats = lats + 12 * np.sin(np.pi * t)
    return lons, lats

# ─────────────────────────────────────────────────────────────────────────────
# ORIGIN REGION MAPPING
# ─────────────────────────────────────────────────────────────────────────────
REGION_MAP = {
    # Americas
    "USA":"Americas","CAN":"Americas","MEX":"Americas","BRA":"Americas",
    "COL":"Americas","VEN":"Americas","ECU":"Americas","PER":"Americas",
    "BOL":"Americas","ARG":"Americas","CHL":"Americas","GTM":"Americas",
    "HND":"Americas","SLV":"Americas","NIC":"Americas","CRI":"Americas",
    "PAN":"Americas","CUB":"Americas","HTI":"Americas","DOM":"Americas",
    "JAM":"Americas","TTO":"Americas","GUY":"Americas","SUR":"Americas",
    # Africa
    "NGA":"Africa","ETH":"Africa","COD":"Africa","TZA":"Africa",
    "SDN":"Africa","SSD":"Africa","UGA":"Africa","KEN":"Africa",
    "GHA":"Africa","MOZ":"Africa","MDG":"Africa","CMR":"Africa",
    "CIV":"Africa","AGO":"Africa","MLI":"Africa","NER":"Africa",
    "BFA":"Africa","SEN":"Africa","GIN":"Africa","RWA":"Africa",
    "BDI":"Africa","SOM":"Africa","ERI":"Africa","DJI":"Africa",
    "CAF":"Africa","TCD":"Africa","ZWE":"Africa","ZMB":"Africa",
    "MWI":"Africa","ZAF":"Africa","NAM":"Africa","BWA":"Africa",
    "LBR":"Africa","SLE":"Africa","GMB":"Africa","GNB":"Africa",
    "TGO":"Africa","BEN":"Africa","LBY":"Africa","DZA":"Africa",
    "MAR":"Africa","TUN":"Africa","EGY":"Africa","MRT":"Africa",
    "CPV":"Africa","STP":"Africa","COM":"Africa","MUS":"Africa",
    "DRC":"Africa",
    # Europe
    "DEU":"Europe","FRA":"Europe","GBR":"Europe","ITA":"Europe",
    "ESP":"Europe","NLD":"Europe","BEL":"Europe","CHE":"Europe",
    "AUT":"Europe","SWE":"Europe","NOR":"Europe","DNK":"Europe",
    "FIN":"Europe","GRC":"Europe","PRT":"Europe","POL":"Europe",
    "UKR":"Europe","BLR":"Europe","MDA":"Europe","ROU":"Europe",
    "BGR":"Europe","SRB":"Europe","BIH":"Europe","HRV":"Europe",
    "SVN":"Europe","MKD":"Europe","ALB":"Europe","MNE":"Europe",
    "RUS":"Europe","GEO":"Europe","ARM":"Europe","AZE":"Europe",
    "XKX":"Europe",
    # Asia
    "CHN":"Asia","IND":"Asia","PAK":"Asia","BGD":"Asia",
    "AFG":"Asia","IRQ":"Asia","SYR":"Asia","IRN":"Asia",
    "TUR":"Asia","SAU":"Asia","YEM":"Asia","JOR":"Asia",
    "LBN":"Asia","PSE":"Asia","ISR":"Asia","ARE":"Asia",
    "OMN":"Asia","KWT":"Asia","BHR":"Asia","QAT":"Asia",
    "MMR":"Asia","THA":"Asia","VNM":"Asia","KHM":"Asia",
    "LAO":"Asia","MYS":"Asia","IDN":"Asia","PHL":"Asia",
    "SGP":"Asia","BRN":"Asia","TLS":"Asia","LKA":"Asia",
    "NPL":"Asia","BTN":"Asia","MDV":"Asia","MNG":"Asia",
    "KAZ":"Asia","UZB":"Asia","TJK":"Asia","KGZ":"Asia",
    "TKM":"Asia","JPN":"Asia","KOR":"Asia","PRK":"Asia",
    "TWN":"Asia","HKG":"Asia","MAC":"Asia",
    # Oceania
    "AUS":"Oceania","NZL":"Oceania","PNG":"Oceania","FJI":"Oceania",
    "SLB":"Oceania","VUT":"Oceania","WSM":"Oceania","TON":"Oceania",
    "KIR":"Oceania","NRU":"Oceania","PLW":"Oceania","FSM":"Oceania",
    "MHL":"Oceania","TUV":"Oceania",
}

# Which region GIFs to render
REGION_RENDERS = [
    ("region_all",      None),
    ("region_americas", "Americas"),
    ("region_africa",   "Africa"),
    ("region_europe",   "Europe"),
    ("region_asia",     "Asia"),
    ("region_oceania",  "Oceania"),
]

# ─────────────────────────────────────────────────────────────────────────────
# RENDER ONE GIF
# ─────────────────────────────────────────────────────────────────────────────
def render_gif(slug, tie_filter, region_filter=None):
    if region_filter:
        label = f"{region_filter} origins"
    elif tie_filter:
        label = TIE_SHORT.get(tie_filter, tie_filter).replace("\n", " ")
    else:
        label = "All corridor types"
    print(f"\nRendering: {slug}  ({label})")

    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR)

    if USE_CARTOPY:
        # Map occupies left 80%, legend panel gets right 18%
        ax = fig.add_axes([0.0, 0.0, 0.80, 1.0],
                          projection=ccrs.Robinson())
        ax.set_global()
        ax.add_feature(cfeature.LAND,      facecolor="#1A2332", edgecolor="none")
        ax.add_feature(cfeature.OCEAN,     facecolor="#0D1420")
        ax.add_feature(cfeature.BORDERS,   linewidth=0.3, edgecolor="#2C3E50")
        ax.add_feature(cfeature.COASTLINE, linewidth=0.4, edgecolor="#2C3E50")
        TRANSFORM = ccrs.PlateCarree()
    else:
        ax = fig.add_axes([0.0, 0.0, 0.80, 1.0])
        ax.set_facecolor(BG_COLOR)
        ax.set_xlim(-180, 180); ax.set_ylim(-70, 85)
        ax.set_xticks([]); ax.set_yticks([])
        for lon in range(-150, 180, 30):
            ax.axvline(lon, color="#1A2332", lw=0.3, zorder=0)
        for lat in range(-60, 90, 30):
            ax.axhline(lat, color="#1A2332", lw=0.3, zorder=0)
        TRANSFORM = None

    ax.set_facecolor(BG_COLOR)

    # Year label
    year_text = ax.text(
        0.01, 0.97, "", transform=ax.transAxes,
        fontsize=44, fontweight="bold", color=TEXT_COLOR, va="top",
        alpha=0.9, fontfamily="monospace",
        path_effects=[pe.withStroke(linewidth=5, foreground=BG_COLOR)]
    )
    # Subtitle (tie type label)
    ax.text(
        0.01, 0.88, label.upper(), transform=ax.transAxes,
        fontsize=11, color="#95A5A6", va="top", fontfamily="monospace",
        path_effects=[pe.withStroke(linewidth=3, foreground=BG_COLOR)]
    )
    # Top 75 note — white, readable
    ax.text(
        0.99, 0.97, "TOP 75 CORRIDORS ANNUALLY", transform=ax.transAxes,
        fontsize=11, color=TEXT_COLOR, va="top", ha="right", fontfamily="monospace",
        path_effects=[pe.withStroke(linewidth=3, foreground=BG_COLOR)]
    )
    subtitle_text = ax.text(
        0.01, 0.83, "", transform=ax.transAxes,
        fontsize=10, color="#7F8C8D", va="top", fontfamily="monospace"
    )

    # Legend — only show relevant tie types
    active_ties = (
        [t for t in TIE_COLORS if t in df["tie_type"].unique()]
        if tie_filter is None
        else [tie_filter]
    )
    # Legend sits BELOW the map as a separate axes strip
    n_ties   = len(active_ties)
    leg_h    = 0.22   # fixed height — two rows
    legend_ax = fig.add_axes([0.0, 0.0, 1.0, leg_h])
    legend_ax.set_facecolor("#0A0E1A")
    legend_ax.set_xticks([]); legend_ax.set_yticks([])
    for spine in legend_ax.spines.values():
        spine.set_visible(False)

    # Each tie type as a colored line + label, laid out horizontally
    total_items = n_ties + 3   # ties + 3 flow volume items
    col_w = 1.0 / (total_items + 1)
    x = col_w * 0.5

    # Legend: corridor types on left (2 rows of 3), flow volume on right
    flow_items = [("Large", 6), ("Medium", 3), ("Small", 1)]
    n_ties_total = len(active_ties)

    # Divide figure width: 75% for corridors, 25% for flow volume
    tie_cols  = 3
    tie_rows  = (n_ties_total + tie_cols - 1) // tie_cols
    col_w     = 0.75 / tie_cols      # width per tie column
    flow_col_w= 0.25 / len(flow_items)

    # Section headers
    legend_ax.text(0.375, 0.96, "CORRIDOR TYPE",
        transform=legend_ax.transAxes, ha="center", va="center",
        fontsize=12, color="#95A5A6", fontfamily="monospace")
    legend_ax.text(0.875, 0.96, "FLOW VOLUME",
        transform=legend_ax.transAxes, ha="center", va="center",
        fontsize=12, color="#95A5A6", fontfamily="monospace")

    # Divider
    legend_ax.axvline(0.77, color="#1f2d3d", lw=1.5)

    for i, tie in enumerate(active_ties):
        row = i // tie_cols
        col = i % tie_cols
        cx = col_w * (col + 0.5)
        # Two rows: top row y=0.72 swatch 0.52 label, bottom row y=0.35 swatch 0.15 label
        swatch_y = 0.76 if row == 0 else 0.38
        label_y  = 0.58 if row == 0 else 0.20
        color = TIE_COLORS.get(tie, "#888")
        legend_ax.plot([cx - col_w*0.32, cx + col_w*0.32], [swatch_y, swatch_y],
            transform=legend_ax.transAxes, color=color, lw=5, solid_capstyle="round")
        legend_ax.text(cx, label_y, TIE_SHORT.get(tie, tie),
            transform=legend_ax.transAxes, ha="center", va="center",
            fontsize=11, color=TEXT_COLOR, fontfamily="monospace",
            multialignment="center")

    # Flow volume items
    for j, (lbl, lw) in enumerate(flow_items):
        cx = 0.77 + flow_col_w * (j + 0.5)
        legend_ax.plot([cx - flow_col_w*0.3, cx + flow_col_w*0.3], [0.72, 0.72],
            transform=legend_ax.transAxes, color="#9EABB5", lw=lw, solid_capstyle="round")
        legend_ax.text(cx, 0.48, lbl,
            transform=legend_ax.transAxes, ha="center", va="center",
            fontsize=11, color=TEXT_COLOR, fontfamily="monospace")

    leg_h = 0.28

    # Resize map axes to leave room for legend strip
    if USE_CARTOPY:
        ax.set_position([0.0, leg_h, 1.0, 1.0 - leg_h])
    else:
        ax.set_position([0.0, leg_h, 1.0, 1.0 - leg_h])

    drawn = []

    def update(frame_idx):
        nonlocal drawn
        for artist in drawn:
            try: artist.remove()
            except: pass
        drawn = []

        year = years[frame_idx]
        year_df = df[df["year"] == year].copy()
        if tie_filter is not None:
            year_df = year_df[year_df["tie_type"] == tie_filter]
        if region_filter is not None:
            year_df = year_df[year_df["iso_o"].map(REGION_MAP) == region_filter]
        year_df = year_df.nlargest(TOP_N_CORRIDORS, "newarrivals")

        year_text.set_text(str(year))
        if year_df.empty:
            return []

        max_flow = year_df["newarrivals"].max()
        total    = year_df["newarrivals"].sum()
        subtitle_text.set_text(f"{len(year_df)} corridors  ·  {total:,.0f} arrivals")

        dest_inflow = year_df.groupby("iso_d")["newarrivals"].sum()
        origin_flow = year_df.groupby("iso_o")["newarrivals"].sum()

        for _, row in year_df.iterrows():
            o, d = row["iso_o"], row["iso_d"]
            if o not in COORDS or d not in COORDS: continue
            lon_o, lat_o = COORDS[o]
            lon_d, lat_d = COORDS[d]
            flow  = row["newarrivals"]
            color = TIE_COLORS.get(row.get("tie_type", "No Tie"), "#7F8C8D")
            alpha = 0.25 + 0.65 * (flow / max_flow) ** 0.5
            lw    = 0.5  + 4.5  * (flow / max_flow) ** 0.6

            arc_lons, arc_lats = great_circle_arc(lon_o, lat_o, lon_d, lat_d)
            trim = int(len(arc_lons) * 0.12)
            arc_lons_draw = arc_lons[:-trim]
            arc_lats_draw = arc_lats[:-trim]

            plot_kw = dict(color=color, linewidth=lw, alpha=alpha,
                           solid_capstyle="round", zorder=3)
            if USE_CARTOPY:
                line, = ax.plot(arc_lons_draw, arc_lats_draw,
                                transform=TRANSFORM, **plot_kw)
            else:
                line, = ax.plot(arc_lons_draw, arc_lats_draw, **plot_kw)
            drawn.append(line)

            tip_lon,  tip_lat  = arc_lons_draw[-1], arc_lats_draw[-1]
            tail_lon, tail_lat = arc_lons_draw[-4], arc_lats_draw[-4]
            arrow_kw = dict(color=color, alpha=min(alpha+0.2, 1.0),
                            arrowstyle="-|>", lw=0.8,
                            mutation_scale=9 + 9*(flow/max_flow)**0.5)
            if USE_CARTOPY:
                arr = ax.annotate("", xy=(tip_lon, tip_lat),
                    xytext=(tail_lon, tail_lat), arrowprops=arrow_kw, zorder=4,
                    xycoords=TRANSFORM._as_mpl_transform(ax),
                    textcoords=TRANSFORM._as_mpl_transform(ax))
            else:
                arr = ax.annotate("", xy=(tip_lon, tip_lat),
                    xytext=(tail_lon, tail_lat), arrowprops=arrow_kw, zorder=4)
            drawn.append(arr)

        for iso, flow in origin_flow.items():
            if iso not in COORDS: continue
            lon, lat = COORDS[iso]
            size = 20 + 350 * (flow / max_flow) ** 0.55
            kw = dict(s=size, color="white", alpha=0.85,
                      edgecolors="white", linewidths=0.6, zorder=6)
            sc = ax.scatter(lon, lat, transform=TRANSFORM, **kw) if USE_CARTOPY \
                 else ax.scatter(lon, lat, **kw)
            drawn.append(sc)
            if flow > max_flow * 0.12:
                lkw = dict(fontsize=9, color=TEXT_COLOR, fontweight="bold",
                           va="bottom", ha="center", zorder=7,
                           fontfamily="monospace",
                           path_effects=[pe.withStroke(linewidth=2, foreground=BG_COLOR)])
                t = ax.text(lon, lat+2, iso, transform=TRANSFORM, **lkw) if USE_CARTOPY \
                    else ax.text(lon, lat+2, iso, **lkw)
                drawn.append(t)

        for iso, flow in dest_inflow.items():
            if iso not in COORDS: continue
            lon, lat = COORDS[iso]
            size = 15 + 280 * (flow / max_flow) ** 0.55
            kw = dict(s=size, color="white", alpha=0.85,
                      edgecolors="white", linewidths=0.6, zorder=5)
            sc = ax.scatter(lon, lat, transform=TRANSFORM, **kw) if USE_CARTOPY \
                 else ax.scatter(lon, lat, **kw)
            drawn.append(sc)
            if flow > max_flow * 0.10:
                lkw = dict(fontsize=9, color="#AED6F1", fontweight="bold",
                           va="top", ha="center", zorder=7,
                           fontfamily="monospace",
                           path_effects=[pe.withStroke(linewidth=2, foreground=BG_COLOR)])
                t = ax.text(lon, lat-2.5, iso, transform=TRANSFORM, **lkw) if USE_CARTOPY \
                    else ax.text(lon, lat-2.5, iso, **lkw)
                drawn.append(t)

        return drawn

    anim = FuncAnimation(fig, update, frames=len(years),
                         interval=FRAME_DURATION_MS, blit=False, repeat=True)

    gif_path = os.path.join(OUT_DIR, f"migration_{slug}.gif")
    anim.save(gif_path, writer=PillowWriter(fps=FPS),
              dpi=110, savefig_kwargs={"facecolor": BG_COLOR})
    print(f"  ✓  {gif_path}")
    plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# RUN ALL RENDERS
# ─────────────────────────────────────────────────────────────────────────────
# Render by tie type
for slug, tie_filter in RENDERS:
    render_gif(slug, tie_filter)

# Render by origin region
for slug, region_filter in REGION_RENDERS:
    render_gif(slug, None, region_filter)

print("\n✓ All GIFs saved to data/videos/")
print("  Now open migration-map.html in your browser.")