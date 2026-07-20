import json
import os
import re
import pandas as pd
import plotly.express as px
import streamlit as st

# Page setup
st.set_page_config(
    page_title="Pokémon Type Engine", page_icon="⚡", layout="wide"
)

# ---------------------------------------------------------
# 1. LOAD LOCAL DATABASE (pokemonDB.json)
# ---------------------------------------------------------
DB_FILE = "pokemonDB.json"


@st.cache_data
def load_pokemon_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle TinyDB structure (e.g. {"Pokemon": {"1": {...}, "2": {...}}} or direct dict)
    raw_list = []
    if "Pokemon" in data:
        raw_list = list(data["Pokemon"].values())
    elif isinstance(data, dict):
        raw_list = list(data.values())
    elif isinstance(data, list):
        raw_list = data

    # Clean up name whitespace/tabs
    for item in raw_list:
        if "name" in item and item["name"]:
            item["clean_name"] = re.sub(r"[\s\t]+", " ", item["name"]).strip()
        else:
            item["clean_name"] = "Unknown"
    return raw_list


pokemon_db = load_pokemon_db()

# ---------------------------------------------------------
# 2. CONSTANTS, COLOR PALETTE & TYPE ICONS
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

# Vector SVG CDN for Type Icons
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
# 3. HELPER CALCULATORS & HTML BADGE RENDERERS
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
    """Renders a pill badge with type icon and signature color."""
    if not type_name or type_name == "None":
        return ""
    bg = TYPE_COLORS.get(type_name, "#777")
    icon_url = TYPE_ICONS.get(type_name, "")
    return (
        f'<div style="'
        f"display: inline-flex; "
        f"align-items: center; "
        f"background-color: {bg}; "
        f"color: white; "
        f"padding: 4px 12px; "
        f"border-radius: 20px; "
        f"font-weight: bold; "
        f"font-size: 13px; "
        f"margin: 2px; "
        f'box-shadow: 0px 2px 4px rgba(0,0,0,0.2);">'
        f'<img src="{icon_url}" style="width: 15px; height: 15px; margin-right: 6px; filter: drop-shadow(0px 1px 1px rgba(0,0,0,0.5));" />'
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
    if not types_list:
        return
    badges_html = "".join([render_type_badge(t) for t in types_list])
    card_html = (
        f'<div style="'
        f"background-color: {bg_color}; "
        f"border-left: 6px solid {border_color}; "
        f"border-radius: 8px; "
        f"padding: 12px 16px; "
        f"margin-bottom: 12px; "
        f'box-shadow: 0px 1px 3px rgba(0,0,0,0.1);">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">'
        f'<span style="font-size: 14px; font-weight: 700; color: #222;">{title}</span>'
        f'<span style="'
        f"background-color: {border_color}; "
        f"color: white; "
        f"font-size: 10px; "
        f"font-weight: 800; "
        f"padding: 2px 8px; "
        f'border-radius: 10px;">{multiplier_label}</span>'
        f"</div>"
        f"<div>{badges_html}</div>"
        f"</div>"
    )
    st.markdown(card_html, unsafe_allow_html=True)


def get_pokemon_image_url(dex_number: int) -> str:
    """Fetches high-res official artwork from PokéAPI CDN using dex number."""
    if not dex_number:
        return ""
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{dex_number}.png"


# ---------------------------------------------------------
# 4. STREAMLIT INTERFACE
# ---------------------------------------------------------
st.title("⚡ Pokémon Type Balancing Engine")
st.caption("Visualizing Type Synergies, Vulnerabilities, and Database Entries")

tab1, tab2 = st.tabs(
    ["🛡️ Type Defensive Profile", "📊 Interactive 18x18 Matrix"]
)

# ---------------------------------------------------------
# TAB 1: VISUAL CARDS & POKÉMON CAROUSEL
# ---------------------------------------------------------
with tab1:
    # 50/50 Layout: Left side for stacked dropdowns/profile, Right side for Carousel
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("Select Typing")

        # Stacked Dropdowns (Below each other on the left half)
        type1 = st.selectbox(
            "Primary Type:", TYPES, index=TYPES.index("Dark")
        )
        type2_options = ["None"] + [t for t in TYPES if t != type1]
        type2 = st.selectbox(
            "Secondary Type (Optional):",
            type2_options,
            index=type2_options.index("None"),
        )

        # Header Badge Display
        p_badge = render_type_badge(type1)
        s_badge = render_type_badge(type2) if type2 != "None" else ""
        st.markdown(
            f'<div style="margin-top:10px; margin-bottom:15px;">{p_badge}{s_badge}</div>',
            unsafe_allow_html=True,
        )

        # Calculate Defensive Multipliers
        profile = get_defensive_profile(type1, type2)
        q_weak = [t for t, m in profile.items() if m == 4.0]
        weak = [t for t, m in profile.items() if m == 2.0]
        resist = [t for t, m in profile.items() if m == 0.5]
        q_resist = [t for t, m in profile.items() if m == 0.25]
        immune = [t for t, m in profile.items() if m == 0.0]

        # Render Row Cards
        render_row_card(
            "Critical Vulnerabilities", q_weak, "#D32F2F", "#FFEBEE", "4x DAMAGE"
        )
        render_row_card("Weaknesses", weak, "#E53935", "#FFEBEE", "2x DAMAGE")
        render_row_card(
            "Total Immunities", immune, "#1976D2", "#E3F2FD", "0x DAMAGE"
        )
        render_row_card(
            "Double Resistances", q_resist, "#388E3C", "#E8F5E9", "0.25x DAMAGE"
        )
        render_row_card(
            "Resistances", resist, "#4CAF50", "#E8F5E9", "0.5x DAMAGE"
        )

        neutral = [t for t, m in profile.items() if m == 1.0]
        with st.expander("Show Neutral Damage Types (1.0x)"):
            st.markdown(
                "".join([render_type_badge(t) for t in neutral]),
                unsafe_allow_html=True,
            )

    with right_col:
        st.subheader("Matching Pokémon Carousel")

        # Filter database for matching species
        matched_pokemon = []
        for p in pokemon_db:
            p_type1 = p.get("primary_type")
            p_type2 = p.get("secondary_type") or "None"

            # Match exact dual or single type combination (bidirectional)
            if type2 == "None":
                if p_type1 == type1 and (
                    p_type2 is None or p_type2 == "None" or p_type2 == ""
                ):
                    matched_pokemon.append(p)
            else:
                if (p_type1 == type1 and p_type2 == type2) or (
                    p_type1 == type2 and p_type2 == type1
                ):
                    matched_pokemon.append(p)

        if not matched_pokemon:
            st.info(
                f"No Pokémon found in `pokemonDB.json` matching type: **{type1}{'/' + type2 if type2 != 'None' else ''}**"
            )
        else:
            st.write(
                f"Found **{len(matched_pokemon)}** Pokémon matching this typing."
            )

            # Interactive Carousel / Card Selector using session state
            if "carousel_index" not in st.state_session if False else True:
                pass  # State handling

            # Carousel Pagination Control
            carousel_key = f"car_{type1}_{type2}"
            if carousel_key not in st.session_state:
                st.session_state[carousel_key] = 0

            # Carousel Navigation Buttons
            btn_prev, btn_info, btn_next = st.columns([1, 2, 1])
            with btn_prev:
                if st.button("⬅️ Prev", key=f"prev_{carousel_key}"):
                    st.session_state[carousel_key] = (
                        st.session_state[carousel_key] - 1
                    ) % len(matched_pokemon)
            with btn_next:
                if st.button("Next ➡️", key=f"next_{carousel_key}"):
                    st.session_state[carousel_key] = (
                        st.session_state[carousel_key] + 1
                    ) % len(matched_pokemon)

            curr_idx = st.session_state[carousel_key]
            with btn_info:
                st.markdown(
                    f"<div style='text-align: center; font-weight: bold; padding-top: 5px;'>Entry {curr_idx + 1} of {len(matched_pokemon)}</div>",
                    unsafe_allow_html=True,
                )

            # Selected Pokémon Card
            poke = matched_pokemon[curr_idx]
            dex_num = poke.get("dex_number")
            img_url = get_pokemon_image_url(dex_num)
            stats = poke.get("stats", {})

            # Render Card Container
            st.markdown(
                f"""
            <div style="
                background-color: #f8f9fa;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 18px;
                text-align: center;
                margin-top: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            ">
                <h3 style="margin-bottom:2px; color: #111;">{poke.get('clean_name')}</h3>
                <p style="color: #666; font-size: 13px; margin-bottom: 10px;">National Dex #{dex_num if dex_num else 'N/A'}</p>
                <img src="{img_url}" style="width: 210px; height: 210px; object-fit: contain; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.15));" />
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Stat Breakdown Metrics
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("HP", stats.get("HP", "N/A"))
            m_col2.metric("Attack", stats.get("ATA", "N/A"))
            m_col3.metric("Defense", stats.get("DEF", "N/A"))
            m_col4.metric("BST", stats.get("BST", "N/A"))

            # Details
            st.caption(
                f"**Abilities:** {', '.join(poke.get('abilities', []))} | **Height:** {poke.get('height')}m | **Weight:** {poke.get('weight')}kg"
            )

# ---------------------------------------------------------
# TAB 2: POLISHED HEATMAP
# ---------------------------------------------------------
with tab2:
    st.write(
        "Read **Rows** as Attacking Types, and **Columns** as Defending Types."
    )

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
            [0.0, "#1E88E5"],
            [0.25, "#4CAF50"],
            [0.5, "#F5F5F5"],
            [1.0, "#E53935"],
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

    st.plotly_chart(fig, width="stretch")