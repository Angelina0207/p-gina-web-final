import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

st.set_page_config("MBTI x Music x Wine", layout="wide")
st.markdown("""
<style>
.titulo-intro {
    position: relative;
    text-align: center;
    padding: 60px 40px;
    background: linear-gradient(120deg, #fceef5, #fff7e6, #e0f7fa);
    border-radius: 30px;
    margin-top: 40px;
    margin-bottom: 60px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}
.titulo-intro h1 {
    font-size: 52px;
    color: #D86F84;
    font-weight: bold;
    margin-bottom: 20px;
}
.floating-img {
    position: absolute;
    width: 60px;
    animation: float 4s ease-in-out infinite;
    z-index: 1;
}
.img1 { top: -30px; left: 30px; }
.img2 { top: -30px; right: 30px; animation-delay: 2s; }
</style>

<div class='titulo-intro'>
    <img src='https://img.icons8.com/emoji/48/wine-glass.png' class='floating-img img1'/>
    <img src='https://img.icons8.com/emoji/48/musical-note.png' class='floating-img img2'/>
    <h1>Bienvenidx a Wine & Music Explorer 🍷🎶</h1>
    <p>¿Te imaginas que tu personalidad tenga su propia playlist… y una copa de vino perfecta para acompañarla?</p>
</div>
""", unsafe_allow_html=True)
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

# --- FUNCTIONS ---
def normalize_text(text):
    text = text.lower()
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').strip()

def contains_word(text, word):
    return normalize_text(word) in normalize_text(text)

# 🌐 Language selector
language = st.selectbox("🌐 Choose language / Elige idioma:", ["Español", "English"])
lang = "es" if language == "Español" else "en"

# --- MULTILINGUAL TEXTS ---
T = {
    "tabs_main": {
        "es": ["🎧 Tu Mood Ideal", "🎼 Explorar canciones", "📈 Estadísticas Spotify", "🌍 Mapa mundial de vinos"],
        "en": ["🎧 Your Ideal Mood", "🎼 Explore Songs", "📈 Spotify Stats", "🌍 Global Wine Map"]
    },
    "subtabs_mood": {
        "es": ["🎧 Recomendaciones", "🚀 Interactivo"],
        "en": ["🎧 Recommendations", "🚀 Interactive"]
    },
    "labels": {
        "es": {
            "mbti_select": "Selecciona tu tipo de personalidad MBTI:",
            "song_rec": "🎵 Canciones recomendadas",
            "wine_rec": "🍇 Vinos sugeridos",
            "no_wines": "No se encontraron vinos.",
            "energy": "Nivel de energía 🎧",
            "happiness": "Nivel de felicidad 😊",
            "danceability": "¿Qué tan bailable? 💃",
            "no_songs": "No se encontraron canciones con esos parámetros.",
            "ideal_wine": "🍷 Vino ideal:"
        },
        "en": {
            "mbti_select": "Select your MBTI personality type:",
            "song_rec": "🎵 Recommended songs",
            "wine_rec": "🍇 Suggested wines",
            "no_wines": "No wines found.",
            "energy": "Energy level 🎧",
            "happiness": "Happiness level 😊",
            "danceability": "How danceable? 💃",
            "no_songs": "No songs found with these settings.",
            "ideal_wine": "🍷 Ideal wine:"
        }
    },
    "intro": {
        "title": {
            "es": "✨ Bienvenida a *Wine & Music Explorer* 🍷🎶",
            "en": "✨ Welcome to *Wine & Music Explorer* 🍷🎶"
        },
        "text": {
            "es": """¿Sabías que tu personalidad podría tener su propia banda sonora y copa de vino ideal?

Esta app interactiva está dividida en dos secciones principales:

🔸 **Experiencia personalizada**  
🔸 **Exploración de datos**

¡Descorcha, explora y disfruta! 🥂""",
            "en": """Did you know your personality might have its own soundtrack and perfect wine?

This interactive app is divided into two main sections:

🔸 **Personalized Experience**  
🔸 **Data Exploration**

Uncork, explore, and enjoy! 🥂"""
        }
    },
    "songs_tab": {
        "header": {
            "es": "🎼 Explorar canciones por filtros",
            "en": "🎼 Explore Songs by Filters"
        },
        "year": {"es": "Año de lanzamiento", "en": "Release Year"},
        "streams": {"es": "Rango de streams", "en": "Streams Range"},
        "sort": {"es": "Ordenar por", "en": "Sort by"},
        "filtered": {"es": "🎵 Canciones filtradas", "en": "🎵 Filtered Songs"},
        "download": {"es": "⬇️ Descargar CSV", "en": "⬇️ Download CSV"},
        "artists": {"es": "🎤 Artistas más frecuentes", "en": "🎤 Most Frequent Artists"},
        "energy_valence": {"es": "🎵 Energía vs Felicidad", "en": "🎵 Energy vs Happiness"},
        "no_data": {"es": "No hay suficientes datos limpios para mostrar estadísticas.", "en": "Not enough clean data to display statistics."}
    },
    "spotify_stats": {
        "header": {"es": "📈 Estadísticas generales de Spotify", "en": "📈 General Spotify Statistics"},
        "bpm": {"es": "🎶 Distribución de BPM", "en": "🎶 BPM Distribution"},
        "energy_dance": {"es": "📊 Relación entre energía y bailabilidad", "en": "📊 Energy vs Danceability"},
        "top": {"es": "🎧 Canciones más populares por número de streams", "en": "🎧 Most Popular Songs by Streams"},
        "source": {
            "es": "Fuente: Base de datos de Spotify 2023. Valores limpiados para visualización.",
            "en": "Source: Spotify 2023 dataset. Values cleaned for visualization."
        }
    },
    "wine_map": {
        "header": {"es": "🌍 Mapa mundial de vinos por puntuación", "en": "🌍 Global Wine Map by Score"},
        "no_data": {"es": "No hay datos suficientes para generar el mapa.", "en": "Not enough data to generate the map."}
    }
}

# --- INTRO ---
st.markdown(f"### {T['intro']['title'][lang]}")
st.write(T['intro']['text'][lang])

# --- LOAD DATA ---
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip')
wine_df.columns = wine_df.columns.str.strip()
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")

# 💡 Asegúrate de tener esta variable antes de este bloque:
# lang = "es" if language == "Español" else "en"

# --- MBTI PROFILES MULTILINGÜES ---
mbti_profiles = {
    "INFP": {"description": {"es": "Soñador, sensible, introspectivo", "en": "Dreamy, sensitive, introspective"}, "wine": "Pinot Noir", "color": "#e6ccff"},
    "ENFP": {"description": {"es": "Espontáneo, creativo, sociable", "en": "Spontaneous, creative, sociable"}, "wine": "Sauvignon Blanc", "color": "#ffe680"},
    "INTJ": {"description": {"es": "Analítico, reservado, estratégico", "en": "Analytical, reserved, strategic"}, "wine": "Cabernet Sauvignon", "color": "#c2f0c2"},
    "ISFJ": {"description": {"es": "Cálido, protector, leal", "en": "Warm, protective, loyal"}, "wine": "Merlot", "color": "#f0d9b5"},
    "ENTP": {"description": {"es": "Innovador, conversador, curioso", "en": "Innovative, talkative, curious"}, "wine": "Rosé", "color": "#ffcce6"},
    "ESFP": {"description": {"es": "Alegre, impulsivo, enérgico", "en": "Cheerful, impulsive, energetic"}, "wine": "Espumante", "color": "#ffcccc"},
    "INFJ": {"description": {"es": "Visionario, intuitivo, profundo", "en": "Visionary, intuitive, deep"}, "wine": "Syrah", "color": "#d9d2e9"},
    "ISTJ": {"description": {"es": "Tradicional, metódico, práctico", "en": "Traditional, methodical, practical"}, "wine": "Malbec", "color": "#d9ead3"}
}
# --- PESTAÑA “Tu Mood Ideal” ---
tabs = st.tabs(T["tabs_main"][lang])

with tabs[0]:
    subtabs = st.tabs(T["subtabs_mood"][lang])

    # 🎧 Recomendaciones
    with subtabs[0]:
        st.header(T["labels"][lang]["song_rec"])
        mbti = st.selectbox(T["labels"][lang]["mbti_select"], list(mbti_profiles.keys()), key="mbti1")
        profile = mbti_profiles[mbti]
        wine = profile["wine"]
        desc = profile["description"][lang]

        st.markdown(f"""
            <div style='background-color:{profile["color"]}; padding:15px; border-radius:10px'>
                <h2>{mbti} — {desc}</h2>
                <h4>{T['labels'][lang]['ideal_wine']} <i>{wine}</i></h4>
            </div>
        """, unsafe_allow_html=True)

        st.subheader(T["labels"][lang]["song_rec"])
        canciones = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
        for _, row in canciones.iterrows():
            st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

        st.subheader(T["labels"][lang]["wine_rec"])
        vinos_filtrados = wine_df[wine_df["variety"].fillna("").str.contains(wine, case=False)]
        if vinos_filtrados.empty:
            st.warning(T["labels"][lang]["no_wines"])
        else:
            for _, row in vinos_filtrados.head(3).iterrows():
                titulo = row.get("title", "Vino")
                puntos = row.get("points", "N/A")
                pais = row.get("country", "País desconocido" if lang == "es" else "Unknown")
                descripcion = row.get("description", "Sin descripción." if lang == "es" else "No description.")
                st.markdown(f"**{titulo}** — ⭐ {puntos} — {pais}")
                st.caption(f"*{descripcion}*")

    # 🚀 Interactivo
    with subtabs[1]:
        st.header("🚀 " + ( "Explora tu mood musical y vinícola" if lang == "es" else "Explore your musical & wine mood"))

        tipo = st.selectbox("1️⃣ " + T["labels"][lang]["mbti_select"], list(mbti_profiles.keys()), key="mbti2")
        perfil = mbti_profiles[tipo]
        vino = perfil["wine"]

        st.subheader("2️⃣ " + ("Ajusta tu mood musical 🎚️" if lang == "es" else "Adjust your musical mood 🎚️"))
        energia = st.slider(T["labels"][lang]["energy"], 0, 100, (50, 100))
        valence = st.slider(T["labels"][lang]["happiness"], 0, 100, (50, 100))
        bailabilidad = st.slider(T["labels"][lang]["danceability"], 0, 100, (50, 100))

        filtro = spotify_df[
            (spotify_df['valence_%'].between(valence[0], valence[1])) &
            (spotify_df['energy_%'].between(energia[0], energia[1])) &
            (spotify_df['danceability_%'].between(bailabilidad[0], bailabilidad[1]))
        ]

        if not filtro.empty:
            resultado = filtro.sample(1).iloc[0]
            st.markdown(f"🎶 **{resultado['track_name']}** — *{resultado['artist(s)_name']}*")
        else:
            st.warning(T["labels"][lang]["no_songs"])

        st.markdown(f"🍷 **{T['labels'][lang]['ideal_wine']}** {vino}")
        
# 🎼 Explore Songs
with tabs[1]:
    st.header("🎼 Explorar canciones por filtros")

    spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")
    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

    if not spotify_clean.empty:
        año = st.selectbox("Año de lanzamiento", sorted(spotify_clean["released_year"].unique()))

        max_streams_val = spotify_clean["streams"].max()
        max_streams = int(max_streams_val) if pd.notna(max_streams_val) else 50_000_000

        min_s, max_s = st.slider("Rango de streams", 0, max_streams, (1_000_000, 10_000_000), step=500_000)
        orden = st.selectbox("Ordenar por", ["streams", "valence_%", "energy_%", "danceability_%"])

        filtrado = spotify_clean[
            (spotify_clean["released_year"] == año) &
            (spotify_clean["streams"] >= min_s) &
            (spotify_clean["streams"] <= max_s)
        ].sort_values(orden, ascending=False).head(20)

        st.subheader("🎵 Canciones filtradas")
        st.dataframe(filtrado[["track_name", "artist(s)_name", "streams"]])
        st.download_button("⬇️ Descargar CSV", filtrado.to_csv(index=False), "canciones_filtradas.csv")

        st.subheader("🎤 Artistas más frecuentes")
        top_artistas = spotify_df["artist(s)_name"].value_counts().head(10)
        fig = px.bar(
            x=top_artistas.index,
            y=top_artistas.values,
            labels={"x": "Artista", "y": "Número de canciones"},
            title="Top 10 artistas más presentes"
        )
        st.plotly_chart(fig)

        st.subheader("🎵 Energía vs Felicidad")
        fig2 = px.scatter(
            spotify_clean.sample(300),
            x="valence_%",
            y="energy_%",
            hover_data=["track_name", "artist(s)_name"],
            color="energy_%"
        )
        st.plotly_chart(fig2)
    else:
        st.warning("No hay suficientes datos limpios para mostrar estadísticas.")

# 📈 Spotify Stats
with tabs[2]:
    st.header("📈 Estadísticas generales de Spotify")

    st.subheader("🎶 Distribución de BPM")
    fig_bpm = px.histogram(
        spotify_df, 
        x="bpm", 
        nbins=30, 
        title="Distribución de BPM (ritmo)", 
        labels={"bpm": "Beats Per Minute"}
    )
    st.plotly_chart(fig_bpm)

    st.subheader("📊 Relación entre energía y bailabilidad")
    fig_energy_dance = px.scatter(
        spotify_df.sample(300),
        x="energy_%",
        y="danceability_%",
        color="valence_%",
        hover_data=["track_name", "artist(s)_name"],
        title="Energía vs Bailabilidad"
    )
    st.plotly_chart(fig_energy_dance)

    st.subheader("🎧 Canciones más populares por número de streams")
    top_streams = spotify_df.sort_values("streams", ascending=False).head(10)
    fig_top = px.bar(
        top_streams,
        x="track_name",
        y="streams",
        color="artist(s)_name",
        title="Top 10 canciones con más streams",
        labels={"track_name": "Canción", "streams": "Reproducciones"}
    )
    st.plotly_chart(fig_top)

    st.caption("Fuente: Base de datos de Spotify 2023. Los valores se han limpiado para esta visualización.")

# 🌍 Global Wine Map
with tabs[3]:
    st.header("🌍 Mapa mundial de vinos por puntuación")

    wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
    wine_df["country"] = wine_df["country"].fillna("Desconocido")

    mapa_df = wine_df.dropna(subset=["points", "country"])
    mapa_df = mapa_df.groupby("country", as_index=False).agg(
        promedio_puntos=("points", "mean"),
        cantidad_vinos=("points", "count")
    )

    if not mapa_df.empty:
        fig = px.choropleth(
            mapa_df,
            locations="country",
            locationmode="country names",
            color="promedio_puntos",
            hover_name="country",
            hover_data=["promedio_puntos", "cantidad_vinos"],
            color_continuous_scale="YlOrRd",
            title="🌎 Puntuación promedio de vinos por país"
        )
        fig.update_geos(showcoastlines=True, projection_type="natural earth")
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos suficientes para generar el mapa.")
