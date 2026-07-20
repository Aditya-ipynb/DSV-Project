import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Pokémon Type Balancing Engine", page_icon="⚡", layout="wide"
)

# ---------------------------------------------------------
# 1. THE ROCK-PAPER-SCISSORS DATA MATRIX (18 TYPES)
# Matrix format: TYPE_CHART[Attacker][Defender] = Multiplier
# ---------------------------------------------------------
TYPES = [
    "Normal",
    "Fire",
    "Water",
    "Grass",
    "Electric",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
    "Fairy",
]

TYPE_CHART = {
    "Normal": {
        "Rock": 0.5,
        "Ghost": 0,
        "Steel": 0.5,
    },
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
    "Ghost": {
        "Normal": 0,
        "Psychic": 2,
        "Ghost": 2,
        "Dark": 0.5,
    },
    "Dragon": {
        "Dragon": 2,
        "Steel": 0.5,
        "Fairy": 0,
    },
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
# 2. CORE LOGIC ENGINE
# ---------------------------------------------------------
def get_attack_multiplier(atk_type: str, def_type: str) -> float:
    """Returns damage multiplier when atk_type attacks def_type."""
    return TYPE_CHART.get(atk_type, {}).get(def_type, 1.0)


def get_defensive_profile(def_type_1: str, def_type_2: str = "None") -> dict:
    """Calculates defensive weaknesses/resistances against all 18 attacking types."""
    profile = {}
    for atk in TYPES:
        mult1 = get_attack_multiplier(atk, def_type_1)
        mult2 = (
            get_attack_multiplier(atk, def_type_2)
            if def_type_2 != "None"
            else 1.0
        )
        profile[atk] = mult1 * mult2
    return profile


def build_full_matrix_df() -> pd.DataFrame:
    """Generates an 18x18 pandas DataFrame for visualization."""
    matrix = []
    for atk in TYPES:
        row = []
        for df in TYPES:
            row.append(get_attack_multiplier(atk, df))
        matrix.append(row)
    return pd.DataFrame(matrix, index=TYPES, columns=TYPES)


# ---------------------------------------------------------
# 3. STREAMLIT FRONTEND INTERFACE
# ---------------------------------------------------------
st.title("⚡ Pokémon Type Balancing Engine")
st.caption(
    "Demonstrating the fundamental 'Rock-Paper-Scissors' multi-type equilibrium."
)

tab1, tab2 = st.tabs(
    ["🔍 Single / Dual-Type Analyzer", "📊 Complete 18x18 Interactive Matrix"]
)

# ---------------------------------------------------------
# TAB 1: INDIVIDUAL TYPE DEFENSIVE ANALYZER
# ---------------------------------------------------------
with tab1:
    st.subheader("Evaluate Type Defensive Profiles")
    col1, col2 = st.columns(2)

    with col1:
        type1 = st.selectbox(
            "Select Primary Type:", TYPES, index=TYPES.index("Fire")
        )
    with col2:
        type2_options = ["None"] + [t for t in TYPES if t != type1]
        type2 = st.selectbox("Select Secondary Type (Optional):", type2_options)

    # Calculate profile
    profile = get_defensive_profile(type1, type2)

    # Group into categories
    quad_weak = [t for t, m in profile.items() if m == 4.0]
    weak = [t for t, m in profile.items() if m == 2.0]
    neutral = [t for t, m in profile.items() if m == 1.0]
    resist = [t for t, m in profile.items() if m == 0.5]
    quad_resist = [t for t, m in profile.items() if m == 0.25]
    immune = [t for t, m in profile.items() if m == 0.0]

    st.markdown("---")
    st.write(
        f"### Defensive Breakdown for **{type1}{'/' + type2 if type2 != 'None' else ''}**"
    )

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("4x Weaknesses", len(quad_weak))
    m2.metric("2x Weaknesses", len(weak))
    m3.metric("Neutral (1x)", len(neutral))
    m4.metric("Resistances (0.5x)", len(resist))
    m5.metric("4x Resistances", len(quad_resist))
    m6.metric("Immunities (0x)", len(immune))

    # Detailed list columns
    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.error("🚨 Weaknesses")
        if quad_weak:
            st.write(f"**4x Ultra Weak:** {', '.join(quad_weak)}")
        if weak:
            st.write(f"**2x Weak:** {', '.join(weak)}")
        if not quad_weak and not weak:
            st.write("None! Clean defense.")

    with res_col2:
        st.success("🛡️ Resistances & Immunities")
        if immune:
            st.write(f"**0x Immune:** {', '.join(immune)}")
        if quad_resist:
            st.write(f"**0.25x Ultra Resist:** {', '.join(quad_resist)}")
        if resist:
            st.write(f"**0.5x Resist:** {', '.join(resist)}")
        if not immune and not quad_resist and not resist:
            st.write("No resistances.")

    with res_col3:
        st.info("⚖️ Neutral Damage (1.0x)")
        st.write(", ".join(neutral))


# ---------------------------------------------------------
# TAB 2: FULL TYPE MATRIX HEATMAP
# ---------------------------------------------------------
with tab2:
    st.subheader("Full 18x18 Attacking vs. Defending Matrix")
    st.write(
        "Read **Rows** as Attacker Types, and **Columns** as Defender Types."
    )

    df_matrix = build_full_matrix_df()

    # Create Plotly Heatmap
    fig = px.imshow(
        df_matrix,
        labels=dict(x="Defender Type", y="Attacker Type", color="Multiplier"),
        x=TYPES,
        y=TYPES,
        color_continuous_scale=[
            [0.0, "#1f77b4"],  # 0x (Immune - Blue)
            [0.25, "#2ca02c"],  # 0.5x (Resisted - Green)
            [0.5, "#cccccc"],  # 1.0x (Neutral - Light Gray)
            [1.0, "#d62728"],  # 2.0x (Super Effective - Red)
        ],
        aspect="auto",
        text_auto=True,
    )

    fig.update_layout(height=650)
    st.plotly_chart(fig, use_container_width=True)