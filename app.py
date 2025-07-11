import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

st.set_page_config("MBTI x Music x Wine", layout="wide")

# --- CUSTOM STYLE ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Fredoka', sans-serif;
        background-color: #fffaf3;
        color: #333333;
    }
    h1, h2, h3 {
        color: #ff7043;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #ffa07a;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES ---
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.strip()

def contiene_palabra(texto, palabra):
    texto_norm = normalizar_texto(texto)
    palabra_norm = normalizar_texto(palabra)
    return palabra_norm in texto_norm

# 🌐 Language selector
idioma = st.selectbox("🌐 Choose language / Elige idioma:", ["Español", "English"])
lang = "es" if idioma == "Español" else "en"

# --- TEXTOS MULTILINGÜES ---
TEXTOS = {
    "titulo": {
        "es": "✨ Bienvenida a *Wine & Music Explorer* 🍷🎶",
        "en": "✨ Welcome to *Wine & Music Explorer* 🍷🎶"
    },
    "intro": {
        "es": "¿Sabías que tu personalidad podría tener su propia banda sonora y copa de vino ideal?",
        "en": "Did you know your personality might have its own soundtrack and perfect wine?"
    },
    "detalle": {
        "es": """
Esta app interactiva está dividida en dos secciones principales:

🔸 **Experiencia personalizada**: descubre qué vino y canción van contigo según tu tipo MBTI.  
🔸 **Exploración de datos**: analiza tendencias musicales, explora canciones según filtros, y observa un mapa global del vino.

¡Descorcha, explora y disfruta! 🥂
""",
        "en": """
This interactive app is divided into two main sections:

🔸 **Personalized Experience**: find out which wine and song match your MBTI type.  
🔸 **Data Exploration**: analyze musical trends, filter songs by mood, and explore a global wine map.

Uncork, explore, and enjoy! 🥂
"""
    }
}

# --- INTRODUCCIÓN DINÁMICA ---
st.markdown(f"### {TEXTOS['titulo'][lang]}")
st.write(TEXTOS["intro"][lang])
st.markdown(TEXTOS["detalle"][lang])
# --- MBTI + Wine ---
mbti_profiles = {
    "INFP": {"description": "Dreamy, sensitive, introspective", "wine": "Pinot Noir", "color": "#e6ccff"},
    "ENFP": {"description": "Spontaneous, creative, outgoing", "wine": "Sauvignon Blanc", "color": "#ffe680"},
    "INTJ": {"description": "Analytical, reserved, strategic", "wine": "Cabernet Sauvignon", "color": "#c2f0c2"},
    "ISFJ": {"description": "Warm, protective, loyal", "wine": "Merlot", "color": "#f0d9b5"},
    "ENTP": {"description": "Innovative, talkative, curious", "wine": "Rosé", "color": "#ffcce6"},
    "ESFP": {"description": "Cheerful, impulsive, energetic", "wine": "Sparkling", "color": "#ffcccc"},
    "INFJ": {"description": "Visionary, intuitive, deep", "wine": "Syrah", "color": "#d9d2e9"},
    "ISTJ": {"description": "Traditional, methodical, practical", "wine": "Malbec", "color": "#d9ead3"}
}

# --- LOAD DATA ---
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip')
wine_df.columns = wine_df.columns.str.strip()
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")

# 🧩 MAIN TABS
main_tabs = st.tabs(["🎧 Your Ideal Mood", "🎼 Explore Songs", "📈 Spotify Stats", "🌍 Global Wine Map"])

# === 🎧 MINI-TABS INSIDE “Your Ideal Mood” ===
with main_tabs[0]:
    subtabs = st.tabs(["🎧 Recommendations", "🚀 Interactive"])

    # --- Subtab: MBTI Recommendations ---
    with subtabs[0]:
        st.header("🎧 Your Personalized Recommendations")
        mbti_type = st.selectbox("Select your MBTI personality type:", list(mbti_profiles.keys()), key="mbti1")
        profile = mbti_profiles[mbti_type]
        wine = profile["wine"]

        st.markdown(f"""
        <div style='background-color:{profile["color"]}; padding:15px; border-radius:10px'>
            <h2>{mbti_type} — {profile["description"]}</h2>
            <h4>🍷 Suggested Wine: <i>{wine}</i></h4>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🎵 Recommended Songs")
        songs = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
        for _, row in songs.iterrows():
            st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

        st.subheader("🍇 Suggested Wines")
        filtered_wines = wine_df[wine_df["variety"].fillna("").str.contains(wine, case=False)]
        if filtered_wines.empty:
            st.warning("No wines found.")
        else:
            for _, row in filtered_wines.head(3).iterrows():
                title = row.get("title", "Wine")
                points = row.get("points", "N/A")
                country = row.get("country", "Unknown Country")
                description = row.get("description", "No description.")
                st.markdown(f"**{title}** — ⭐ {points} points — {country}")
                st.caption(f"*{description}*")
                st.markdown("---")

    # --- Subtab: Interactive Mood ---
    with subtabs[1]:
        st.header("🚀 Explore your musical & wine mood")
        mbti_type = st.selectbox("1️⃣ What's your MBTI personality type?", list(mbti_profiles.keys()), key="mbti2")
        profile = mbti_profiles[mbti_type]
        wine = profile["wine"]

        st.subheader("2️⃣ Adjust your musical mood 🎚️")
        energy = st.slider("Energy Level 🎧", 0, 100, (50, 100))
        valence = st.slider("Happiness Level 😊", 0, 100, (50, 100))
        danceability = st.slider("How danceable? 💃", 0, 100, (50, 100))

        filtered = spotify_df[
            (spotify_df['valence_%'].between(valence[0], valence[1])) &
            (spotify_df['energy_%'].between(energy[0], energy[1])) &
            (spotify_df['danceability_%'].between(danceability[0], danceability[1]))
        ]

        if not filtered.empty:
            result = filtered.sample(1).iloc[0]
            st.markdown(f"🎶 **{result['track_name']}** — *{result['artist(s)_name']}*")
        else:
            st.warning("No songs found with these parameters.")

        st.markdown(f"🍷 **Ideal Wine:** {wine}")

# 🎼 PART 3: Song Explorer
with main_tabs[1]:
    st.header("🎼 Explore Songs by Filters")

    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

    if not spotify_clean.empty:
        year = st.selectbox("Release Year", sorted(spotify_clean["released_year"].unique()))

        max_streams_val = spotify_clean["streams"].max()
        max_streams = int(max_streams_val) if pd.notna(max_streams_val) else 50_000_000

        min_s, max_s = st.slider("Streams Range", 0, max_streams, (1_000_000, 10_000_000), step=500_000)
        sort_by = st.selectbox("Sort by", ["streams", "valence_%", "energy_%", "danceability_%"])

        filtered = spotify_clean[
            (spotify_clean["released_year"] == year) &
            (spotify_clean["streams"] >= min_s) &
            (spotify_clean["streams"] <= max_s)
        ].sort_values(sort_by, ascending=False).head(20)

        st.subheader("🎵 Filtered Songs")
        st.dataframe(filtered[["track_name", "artist(s)_name", "streams"]])
        st.download_button("⬇️ Download CSV", filtered.to_csv(index=False), "filtered_songs.csv")

        st.subheader("🎤 Most Frequent Artists")
        top_artists = spotify_df["artist(s)_name"].value_counts().head(10)
        fig = px.bar(
            x=top_artists.index,
            y=top_artists.values,
            labels={"x": "Artist", "y": "Number of Songs"},
            title="Top 10 Most Frequent Artists"
        )
        st.plotly_chart(fig)

        st.subheader("🎵 Energy vs Happiness")
        fig2 = px.scatter(
            spotify_clean.sample(300),
            x="valence_%", y="energy_%",
            hover_data=["track_name", "artist(s)_name"],
            color="energy_%"
        )
        st.plotly_chart(fig2)
    else:
        st.warning("Not enough clean data to display statistics.")

# 📈 PART 4: Spotify Stats
with main_tabs[2]:
    st.header("📈 General Spotify Statistics")

    st.subheader("🎶 BPM Distribution")
    fig_bpm = px.histogram(
        spotify_df, 
        x="bpm", 
        nbins=30, 
        title="BPM (Beats Per Minute) Distribution", 
        labels={"bpm": "Beats Per Minute"}
    )
    st.plotly_chart(fig_bpm)

    st.subheader("📊 Energy vs Danceability")
    fig_energy_dance = px.scatter(
        spotify_df.sample(300),
        x="energy_%",
        y="danceability_%",
        color="valence_%",
        hover_data=["track_name", "artist(s)_name"],
        title="Energy vs Danceability"
    )
    st.plotly_chart(fig_energy_dance)

    st.subheader("🎧 Most Popular Songs by Streams")
    top_streams = spotify_df.sort_values("streams", ascending=False).head(10)
    fig_top = px.bar(
        top_streams,
        x="track_name",
        y="streams",
        color="artist(s)_name",
        title="Top 10 Most Streamed Songs",
        labels={"track_name": "Song", "streams": "Streams"}
    )
    st.plotly_chart(fig_top)

    st.caption("Source: Spotify 2023 dataset. Values cleaned for this visualization.")

# 🌍 PART 5: Global Wine Map
with main_tabs[3]:
    st.header("🌍 Global Wine Map by Score")

    wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
    wine_df["country"] = wine_df["country"].fillna("Unknown")

    map_df = wine_df.dropna(subset=["points", "country"])
    map_df = map_df.groupby("country", as_index=False).agg(
        avg_points=("points", "mean"),
        wine_count=("points", "count")
    )

    if not map_df.empty:
        fig = px.choropleth(
            map_df,
            locations="country",
            locationmode="country names",
            color="avg_points",
            hover_name="country",
            hover_data=["avg_points", "wine_count"],
            color_continuous_scale="YlOrRd",
            title="🌎 Average Wine Score by Country"
        )
        fig.update_geos(showcoastlines=True, projection_type="natural earth")
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Not enough data to generate the map.")
