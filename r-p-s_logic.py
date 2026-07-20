import pandas as pd
import plotly.express as px
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Pokémon Type Engine", page_icon="⚡", layout="wide"
)

# ---------------------------------------------------------
# 1. CONSTANTS, COLOR PALETTE & TYPE ICONS
# ---------------------------------------------------------
TYPE_COLORS = {
    "Normal": "#A8A77A",
    "Fire": "#EE8130",
    "Water": "#6390F0",
    "Electric": "#F7D02C",
    "Grass": "#7AC74C",
    "Ice": "#96D9D6",
    "Fighting": "#C22E28",
    "Poison": "#A33EA1",
    "Ground": "#E2BF65",
    "Flying": "#A98FF3",
    "Psychic": "#F95587",
    "Bug": "#A6B91A",
    "Rock": "#B6A136",
    "Ghost": "#735797",
    "Dragon": "#6F35FC",
    "Dark": "#705746",
    "Steel": "#B7B7CE",
    "Fairy": "#D685AD",
}

TYPES = list(TYPE_COLORS.keys())

# Reliable SVG CDN for Pokémon Type Icons
TYPE_ICONS = {
    t: f"https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/{t.lower()}.svg"
    for t in TYPES
}

TYPE_CHART = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2,
        "Ice": 2,
        "Bug": 2,
        "Rock": 0.5,
        "Dragon": 0.5,
        "Steel": 2,
    },
    "Water": {
        "Fire": 2,
        "Water": 0.5,
        "Grass": 0.5,
        "Ground": 2,
        "Rock": 2,
        "Dragon": 0.5,
    },
    "Grass": {
        "Fire": 0.5,
        "Water": 2,
        "Grass": 0.5,
        "Poison": 0.5,
        "Ground": 2,
        "Flying": 0.5,
        "Bug": 0.5,
        "Rock": 2,
        "Dragon": 0.5,
        "Steel": 0.5,
    },
    "Electric": {
        "Water": 2,
        "Grass": 0.5,
        "Electric": 0.5,
        "Ground": 0,
        "Flying": 2,
        "Dragon": 0.5,
    },
    "Ice": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2,
        "Ice": 0.5,
        "Ground": 2,
        "Flying": 2,
        "Dragon": 2,
        "Steel": 0.5,
    },
    "Fighting": {
        "Normal": 2,
        "Ice": 2,
        "Poison": 0.5,
        "Flying": 0.5,
        "Psychic": 0.5,
        "Bug": 0.5,
        "Rock": 2,
        "Ghost": 0,
        "Dark": 2,
        "Steel": 2,
        "Fairy": 0.5,
    },
    "Poison": {
        "Grass": 2,
        "Poison": 0.5,
        "Ground": 0.5,
        "Rock": 0.5,
        "Ghost": 0.5,
        "Steel": 0,
        "Fairy": 2,
    },
    "Ground": {
        "Fire": 2,
        "Grass": 0.5,
        "Electric": 2,
        "Poison": 2,
        "Flying": 0,
        "Bug": 0.5,
        "Rock": 2,
        "Steel": 2,
    },
    "Flying": {
        "Grass": 2,
        "Electric": 0.5,
        "Fighting": 2,
        "Bug": 2,
        "Rock": 0.5,
        "Steel": 0.5,
    },
    "Psychic": {
        "Fighting": 2,
        "Poison": 2,
        "Psychic": 0.5,
        "Dark": 0,
        "Steel": 0.5,
    },
    "Bug": {
        "Fire": 0.5,
        "Grass": 2,
        "Fighting": 0.5,
        "Poison": 0.5,
        "Flying": 0.5,
        "Psychic": 2,
        "Ghost": 0.5,
        "Dark": 2,
        "Steel": 0.5,
        "Fairy": 0.5,
    },
    "Rock": {
        "Fire": 2,
        "Ice": 2,
        "Fighting": 0.5,
        "Ground": 0.5,
        "Flying": 2,
        "Bug": 2,
        "Steel": 0.5,
    },
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {
        "Fighting": 0.5,
        "Psychic": 2,
        "Ghost": 2,
        "Dark": 0.5,
        "Fairy": 0.5,
    },
    "Steel": {
        "Fire": 0.5,
        "Water": 0.5,
        "Electric": 0.5,
        "Ice": 2,
        "Rock": 2,
        "Steel": 0.5,
        "Fairy": 2,
    },
    "Fairy": {
        "Fire": 0.5,
        "Fighting": 2,
        "Poison": 0.5,
        "Dragon": 2,
        "Dark": 2,
        "Steel": 0.5,
    },
}


# ---------------------------------------------------------
# 2. HELPER CALCULATORS & HTML RENDERERS
# ---------------------------------------------------------
def get_attack_multiplier(atk: str, df: str) -> float:
    return TYPE_CHART.get(atk, {}).get(df, 1.0)


def get_defensive_profile(type1: str, type2: str = "None") -> dict:
    profile = {}
    for atk in TYPES:
        m1 = get_attack_multiplier(atk, type1)
        m2 = get_attack_multiplier(atk, type2) if type2 != "None" else 1.0
        profile[atk] = m1 * m2
    return profile


def render_type_badge(type_name: str) -> str:
    """Creates a clean HTML badge with working SVG icons."""
    bg = TYPE_COLORS.get(type_name, "#777")
    icon_url = TYPE_ICONS.get(type_name, "")
    return (
        f'<div style="'
        f"display: inline-flex; "
        f"align-items: center; "
        f"background-color: {bg}; "
        f"color: white; "
        f"padding: 5px 12px; "
        f"border-radius: 16px; "
        f"font-weight: bold; "
        f"font-size: 13px; "
        f"margin: 3px; "
        f'box-shadow: 0px 2px 4px rgba(0,0,0,0.25);">'
        f'<img src="{icon_url}" style="width: 16px; height: 16px; margin-right: 6px; filter: drop-shadow(0px 1px 1px rgba(0,0,0,0.5));" />'
        f"{type_name.upper()}"
        f"</div>"
    )


def render_row_card(
    title: str,
    types_list: list,
    border_color: str,
    bg_color: str,
    multiplier_label: str,
):
    """Renders a visual card ONLY if types exist for this category."""
    if not types_list:
        return

    badges_html = "".join([render_type_badge(t) for t in types_list])

    card_html = (
        f'<div style="'
        f"background-color: {bg_color}; "
        f"border-left: 6px solid {border_color}; "
        f"border-radius: 8px; "
        f"padding: 14px 18px; "
        f"margin-bottom: 14px; "
        f'box-shadow: 0px 1px 3px rgba(0,0,0,0.1);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
        f'<span style="font-size: 15px; font-weight: 700; color: #222;">{title}</span>'
        f'<span style="'
        f"background-color: {border_color}; "
        f"color: white; "
        f"font-size: 11px; "
        f"font-weight: 800; "
        f"padding: 2px 8px; "
        f'border-radius: 10px;">{multiplier_label}</span>'
        f"</div>"
        f"<div>{badges_html}</div>"
        f"</div>"
    )
    st.markdown(card_html, unsafe_allow_html=True)


# ---------------------------------------------------------
# 3. STREAMLIT INTERFACE
# ---------------------------------------------------------
st.title("⚡ Pokémon Type Balancing Engine")
st.caption("Visualizing Type Synergies, Vulnerabilities, and Equilibrium")

tab1, tab2 = st.tabs(
    ["🛡️ Type Defensive Profile", "📊 Interactive 18x18 Matrix"]
)

# ---------------------------------------------------------
# TAB 1: VISUAL ROW CARDS
# ---------------------------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        type1 = st.selectbox(
            "Primary Type:", TYPES, index=TYPES.index("Grass")
        )
    with col2:
        type2_options = ["None"] + [t for t in TYPES if t != type1]
        type2 = st.selectbox(
            "Secondary Type (Optional):",
            type2_options,
            index=type2_options.index("Steel") if "Steel" in type2_options else 0,
        )

    profile = get_defensive_profile(type1, type2)

    # Filter categories
    q_weak = [t for t, m in profile.items() if m == 4.0]
    weak = [t for t, m in profile.items() if m == 2.0]
    resist = [t for t, m in profile.items() if m == 0.5]
    q_resist = [t for t, m in profile.items() if m == 0.25]
    immune = [t for t, m in profile.items() if m == 0.0]

    st.markdown("---")

    # Header display using type badges
    selected_badge = render_type_badge(type1) + (
        render_type_badge(type2) if type2 != "None" else ""
    )
    st.markdown(
        f'<div style="margin-bottom: 15px;"><h3 style="display:inline; margin-right: 10px;">Defensive Profile for:</h3>{selected_badge}</div>',
        unsafe_allow_html=True,
    )

    # Render Visual Row Cards (Only shows rows that have items)
    render_row_card("Critical Vulnerabilities", q_weak, "#D32F2F", "#FFEBEE", "4x DAMAGE")
    render_row_card("Weaknesses", weak, "#E53935", "#FFEBEE", "2x DAMAGE")
    render_row_card("Total Immunities", immune, "#1976D2", "#E3F2FD", "0x DAMAGE")
    render_row_card("Double Resistances", q_resist, "#388E3C", "#E8F5E9", "0.25x DAMAGE")
    render_row_card("Resistances", resist, "#4CAF50", "#E8F5E9", "0.5x DAMAGE")

    # Show neutral compactly at the bottom
    neutral = [t for t, m in profile.items() if m == 1.0]
    with st.expander("Show Neutral Damage Types (1.0x)"):
        st.markdown(
            "".join([render_type_badge(t) for t in neutral]),
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# TAB 2: POLISHED HEATMAP
# ---------------------------------------------------------
with tab2:
    st.write(
        "Read **Rows** as Attacking Types, and **Columns** as Defending Types."
    )

    # Build matrix dataframe
    matrix_data = []
    text_data = []
    for atk in TYPES:
        m_row = []
        t_row = []
        for df in TYPES:
            val = get_attack_multiplier(atk, df)
            m_row.append(val)
            if val == 2.0:
                t_row.append("2x")
            elif val == 0.5:
                t_row.append("½x")
            elif val == 0.0:
                t_row.append("0x")
            else:
                t_row.append("")
        matrix_data.append(m_row)
        text_data.append(t_row)

    df_matrix = pd.DataFrame(matrix_data, index=TYPES, columns=TYPES)

    fig = px.imshow(
        df_matrix,
        labels=dict(x="Defender Type", y="Attacker Type", color="Multiplier"),
        x=TYPES,
        y=TYPES,
        color_continuous_scale=[
            [0.0, "#1E88E5"],  # Immune (Blue)
            [0.25, "#4CAF50"],  # Resisted (Green)
            [0.5, "#F5F5F5"],  # Neutral (Soft Gray)
            [1.0, "#E53935"],  # Weakness (Red)
        ],
        text_auto=False,
        aspect="auto",
    )

    fig.update_traces(
        text=text_data,
        texttemplate="%{text}",
        textfont={"size": 12, "weight": "bold"},
    )
    fig.update_layout(height=650, margin=dict(l=20, r=20, t=20, b=20))

    # Updated 'width="stretch"' to resolve deprecation warnings
    st.plotly_chart(fig, width="stretch")