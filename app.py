#parte 1

import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

st.set_page_config(page_title="MBTI x Music x Wine", layout="wide")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Fredoka', sans-serif;
    background-color: #fffaf3;
    color: #333333;
}
h1, h2, h3 {
    color: #D86F84;
    font-weight: 600;
    text-align: center;
}
.stButton>button {
    background-color: #ffa07a;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-10px);}
    to {opacity: 1; transform: translateY(0);}
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
.titulo-intro {
    position: relative;
    text-align: center;
    padding: 60px 40px;
    background: linear-gradient(120deg, #fceef5, #fff7e6, #e0f7fa);
    border-radius: 30px;
    margin-top: 40px;
    margin-bottom: 60px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    animation: fadeIn 1.5s ease-in-out;
}
.titulo-intro h1 {
    font-size: 52px;
    color: #D86F84;
    font-weight: bold;
    margin-bottom: 20px;
}
.titulo-intro p {
    font-size: 18px;
    color: #555;
    line-height: 1.6;
    max-width: 700px;
    margin: auto;
    white-space: pre-wrap;
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
""", unsafe_allow_html=True)

#✅ PARTE 2 — Funciones, idioma y textos introductorios

# --- FUNCIONES DE TEXTO ---
def normalize_text(text):
    text = text.lower()
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').strip()

def contains_word(text, word):
    return normalize_text(word) in normalize_text(text)

# --- SELECTOR DE IDIOMA ---
language = st.selectbox("🌐 Language / Idioma", ["Español", "English"])
lang = "es" if language == "Español" else "en"

# --- TEXTOS MULTILINGÜES ---
T = {
    "intro": {
        "title": {
            "es": "Bienvenidx a Wine & Music Explorer 🍷🎶",
            "en": "Welcome to Wine & Music Explorer 🍷🎶"
        },
        "text": {
            "es": """¿Te imaginas que tu personalidad tenga su propia playlist… y una copa de vino perfecta para acompañarla?

¡Aquí lo hacemos realidad! Sumérgete en una experiencia interactiva donde el MBTI, la música y el vino se combinan para brindarte una aventura sensorial única.

Nuestra app se divide en dos mundos por explorar:

🔸 **Experiencia personalizada – Descubre tu maridaje ideal entre notas musicales y sabores.**  
🔸 **Exploración de datos – Navega por insights que conectan tipos de personalidad con preferencias musicales y vinícolas.**

🎧🍇 ¡Dale play, sirve tu copa y empieza a explorar!""",
            "en": """Can you imagine your personality having its own playlist... and the perfect glass of wine to pair it with?

We make it a reality here! Immerse yourself in an interactive experience where MBTI, music, and wine combine to provide you with a unique sensory adventure.

Our app is divided into two worlds to explore:

🔸 **Personalized Experience – Discover your ideal pairing of musical notes and flavors.**  
🔸 **Data Exploration – Browse insights that connect personality types with musical and wine preferences.**

🎧🍇 Press play, pour your glass, and start exploring!"""
        }
    }
}


#✅ PARTE 3 — Bloque visual de bienvenida

st.markdown(f"""
<div class='titulo-intro'>
    <img src='https://raw.githubusercontent.com/Angelina0207/p-gina-web-final/main/images/gato.jpg'
         style='width: 120px; display: block; margin: 0 auto 20px; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.2); animation: float 4s ease-in-out infinite;' />
    <h1 style='margin-bottom: 20px;'>{T['intro']['title'][lang]}</h1>
    <p>{T['intro']['text'][lang].replace(chr(10), "<br>")}</p>
</div>
""", unsafe_allow_html=True)

#✅ PARTE 4 — Carga de datos, perfiles MBTI y estructura de pestañas

#🔹 A) Carga de datos
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip')

# Limpieza rápida
wine_df.columns = wine_df.columns.str.strip()
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")

#🔹 B) Diccionario de perfiles MBTI
mbti_profiles = {
    "INFP": {"description": {"es": "Soñador(a/e), sensible, introspectivx", "en": "Dreamy, sensitive, introspective"}, "wine": "Pinot Noir", "color": "#e6ccff"},
    "ENFP": {"description": {"es": "Espontánex, creativx, sociable", "en": "Spontaneous, creative, sociable"}, "wine": "Sauvignon Blanc", "color": "#ffe680"},
    "INTJ": {"description": {"es": "Analíticx, reservadx, estratégicx", "en": "Analytical, reserved, strategic"}, "wine": "Cabernet Sauvignon", "color": "#c2f0c2"},
    "ISFJ": {"description": {"es": "Cálidx, protector(a/e), leal", "en": "Warm, protective, loyal"}, "wine": "Merlot", "color": "#f0d9b5"},
    "ENTP": {"description": {"es": "Innovador(a/e), conversador(a/e), curiosx", "en": "Innovative, talkative, curious"}, "wine": "Rosé", "color": "#ffcce6"},
    "ESFP": {"description": {"es": "Alegre, impulsivx, enérgicx", "en": "Cheerful, impulsive, energetic"}, "wine": "Espumante", "color": "#ffcccc"},
    "INFJ": {"description": {"es": "Visionarix, intuitivx, profundx", "en": "Visionary, intuitive, deep"}, "wine": "Syrah", "color": "#d9d2e9"},
    "ISTJ": {"description": {"es": "Tradicional, metódicx, prácticx", "en": "Traditional, methodical, practical"}, "wine": "Malbec", "color": "#d9ead3"}
}
# --- ETIQUETAS MULTILINGÜES ---
T["labels"] = {
    "es": {
        "mbti_select": "Selecciona tu tipo MBTI",
        "ideal_wine": "Tu vino ideal es:",
        "song_rec": "Canciones recomendadas",
        "wine_rec": "Vinos sugeridos",
        "no_wines": "No se encontraron vinos que coincidan.",
        "no_songs": "No se encontraron canciones que coincidan.",
        "energy": "Nivel de energía",
        "happiness": "Nivel de felicidad (valence)",
        "danceability": "Nivel de bailabilidad"
    },
    "en": {
        "mbti_select": "Select your MBTI type",
        "ideal_wine": "Your ideal wine is:",
        "song_rec": "Recommended Songs",
        "wine_rec": "Suggested Wines",
        "no_wines": "No matching wines found.",
        "no_songs": "No matching songs found.",
        "energy": "Energy level",
        "happiness": "Happiness level (valence)",
        "danceability": "Danceability level"
    }
}

#🔹 C) Títulos de pestañas multilingües
T["tabs_main"] = {
    "es": ["🎧 Tu Mood Ideal", "🎼 Explorar canciones", "📈 Estadísticas Spotify", "🌍 Mapa mundial de vinos"],
    "en": ["🎧 Your Ideal Mood", "🎼 Explore Songs", "📈 Spotify Stats", "🌍 Global Wine Map"]
}
T["subtabs_mood"] = {
    "es": ["🎧 Recomendaciones", "🚀 Interactivo"],
    "en": ["🎧 Recommendations", "🚀 Interactive"]
}
# --- TEXTOS DE LA PESTAÑA DE CANCIONES ---
T["songs_tab"] = {
    "header": {
        "es": "🎼 Explora canciones por año y popularidad",
        "en": "🎼 Explore songs by year and popularity"
    },
    "year": {
        "es": "Selecciona el año de lanzamiento",
        "en": "Select release year"
    },
    "streams": {
        "es": "Rango de reproducciones",
        "en": "Stream range"
    },
    "sort": {
        "es": "Ordenar por",
        "en": "Sort by"
    },
    "filtered": {
        "es": "Canciones filtradas:",
        "en": "Filtered Songs:"
    },
    "artists": {
        "es": "Top artistas más frecuentes",
        "en": "Top frequent artists"
    },
    "energy_valence": {
        "es": "Distribución de energía y felicidad",
        "en": "Energy and happiness distribution"
    },
    "no_data": {
        "es": "No hay datos disponibles para mostrar.",
        "en": "No data available to display."
    }
}
# --- TEXTOS DE LA PESTAÑA DE ESTADÍSTICAS DE SPOTIFY ---
T["spotify_stats"] = {
    "header": {
        "es": "📈 Estadísticas de Spotify",
        "en": "📈 Spotify Statistics"
    },
    "bpm": {
        "es": "Distribución de BPM (Beats por minuto)",
        "en": "BPM Distribution (Beats per Minute)"
    },
    "energy_dance": {
        "es": "Relación entre energía y bailabilidad",
        "en": "Energy vs Danceability"
    },
    "top_streams": {
        "es": "Canciones más populares por número de streams",
        "en": "Most Popular Songs by Stream Count"
    },
    "source": {
        "es": "Fuente: dataset de Spotify 2023",
        "en": "Source: Spotify 2023 dataset"
    }
}

T["wine_map"] = {
    "header": {
        "es": "🌍 Mapa mundial de vinos",
        "en": "🌍 Global Wine Map"
    },
    "no_data": {
        "es": "No se encontraron datos suficientes para mostrar el mapa.",
        "en": "Not enough data found to display the map."
    }
}


#🔹 D) Crear las pestañas principales
tabs = st.tabs(T["tabs_main"][lang])

#✅ PARTE 5 — Pestaña "Tu Mood Ideal" (Recomendaciones + Interactivo)

with tabs[0]:  # 🎧 Tu Mood Ideal
    subtabs = st.tabs(T["subtabs_mood"][lang])

    # --- 🎧 Subpestaña 1: Recomendaciones ---
    with subtabs[0]:
        st.header("🎧 " + ( "Recomendaciones musicales y de vino" if lang == "es" else "Music & Wine Recommendations"))
        mbti = st.selectbox(T["labels"][lang]["mbti_select"], list(mbti_profiles.keys()), key="mbti1")
        profile = mbti_profiles[mbti]
        wine = profile["wine"]
        desc = profile["description"][lang]
# Explicación del MBTI
        explicacion_mbti = {
            "es": """<p style='font-size:16px; line-height:1.6;'>
        El <b>MBTI</b> (Indicador de Tipos de Myers-Briggs) es una herramienta que clasifica las personalidades en 16 tipos distintos según cómo percibes el mundo y tomas decisiones.  
        Esta clasificación ayuda a entender tus preferencias y cómo te conectas con el entorno, ¡incluso con la música y el vino que podrías disfrutar más!
        </p>""",
            "en": """<p style='font-size:16px; line-height:1.6;'>
        The <b>MBTI</b> (Myers-Briggs Type Indicator) is a tool that categorizes personalities into 16 distinct types based on how you perceive the world and make decisions.      
        It helps you understand your preferences and how you connect with your surroundings — even the music and wine you might enjoy the most!
        </p>"""
        }

# Mostrar la explicación antes del selector
st.markdown(explicacion_mbti[lang], unsafe_allow_html=True)

# Mostrar la explicación antes del selector
st.markdown(explicacion_mbti[lang], unsafe_allow_html=True)

        st.markdown(f"""
            <div style='background-color:{profile["color"]}; padding:15px; border-radius:10px'>
                <h2>{mbti} — {desc}</h2>
                <h4>{T['labels'][lang]['ideal_wine']} <i>{wine}</i></h4>
            </div>
        """, unsafe_allow_html=True)

        # Canciones recomendadas (aleatorias)
        st.subheader(T["labels"][lang]["song_rec"])
        canciones = spotify_df[
            (spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)
        ].sample(3)
        for _, row in canciones.iterrows():
            st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

        # Vinos recomendados
        st.subheader(T["labels"][lang]["wine_rec"])
        vinos_filtrados = wine_df[wine_df["variety"].fillna("").str.contains(wine, case=False)]
if vinos_filtrados.empty:
    mensaje_personalizado = (
        "No hay vinos para ti por lo dulce y agrio que eres 😜" if lang == "es"
        else "No wines for you because you're too sweet and sour 😜"
    )
    st.warning(mensaje_personalizado)
else:
    for _, row in vinos_filtrados.head(3).iterrows():
        titulo = row.get("title", "Vino")
        puntos = row.get("points", "N/A")
        pais = row.get("country", "País desconocido" if lang == "es" else "Unknown")
        descripcion = row.get("description", "Sin descripción." if lang == "es" else "No description.")
        st.markdown(f"**{titulo}** — ⭐ {puntos} — {pais}")
        st.caption(f"*{descripcion}*")

    # --- 🚀 Subpestaña 2: Interactivo ---
    with subtabs[1]:
        st.header("🚀 " + ("Explora tu mood musical y vinícola" if lang == "es" else "Explore your musical & wine mood"))

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

#✅ PARTE 6 — Pestaña 2: "🎼 Explorar canciones"

with tabs[1]:
    st.header(T["songs_tab"]["header"][lang])

    spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")
    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

    if not spotify_clean.empty:
        año = st.selectbox(T["songs_tab"]["year"][lang], sorted(spotify_clean["released_year"].unique()))

        max_streams_val = spotify_clean["streams"].max()
        max_streams = int(max_streams_val) if pd.notna(max_streams_val) else 50_000_000

        min_s, max_s = st.slider(
            T["songs_tab"]["streams"][lang],
            0,
            max_streams,
            (1_000_000, 10_000_000),
            step=500_000
        )

        orden = st.selectbox(
            T["songs_tab"]["sort"][lang],
            ["streams", "valence_%", "energy_%", "danceability_%"]
        )

        filtrado = spotify_clean[
            (spotify_clean["released_year"] == año) &
            (spotify_clean["streams"] >= min_s) &
            (spotify_clean["streams"] <= max_s)
        ].sort_values(orden, ascending=False).head(20)

        st.subheader(T["songs_tab"]["filtered"][lang])
        st.dataframe(filtrado[["track_name", "artist(s)_name", "streams"]])
        st.download_button("⬇️ Descargar CSV", filtrado.to_csv(index=False), "canciones_filtradas.csv")

        st.subheader(T["songs_tab"]["artists"][lang])
        top_artistas = spotify_df["artist(s)_name"].value_counts().head(10)
        fig = px.bar(
            x=top_artistas.index,
            y=top_artistas.values,
            labels={"x": "Artista", "y": "Número de canciones"},
            title="Top 10 artistas más presentes" if lang == "es" else "Top 10 Most Frequent Artists"
        )
        st.plotly_chart(fig)

        st.subheader(T["songs_tab"]["energy_valence"][lang])
        fig2 = px.scatter(
            spotify_clean.sample(300),
            x="valence_%",
            y="energy_%",
            hover_data=["track_name", "artist(s)_name"],
            color="energy_%"
        )
        st.plotly_chart(fig2)
    else:
        st.warning(T["songs_tab"]["no_data"][lang])

#✅ PARTE 7 — Estadísticas de Spotify
with tabs[2]:
    st.header(T["spotify_stats"]["header"][lang])

    # --- Histograma de BPM ---
    st.subheader(T["spotify_stats"]["bpm"][lang])
    fig_bpm = px.histogram(
        spotify_df, 
        x="bpm", 
        nbins=30, 
        title=T["spotify_stats"]["bpm"][lang], 
        labels={"bpm": "Beats Per Minute"}
    )
    st.plotly_chart(fig_bpm)

    # --- Dispersión Energía vs Danceability ---
    st.subheader(T["spotify_stats"]["energy_dance"][lang])
    fig_energy_dance = px.scatter(
        spotify_df.sample(300),
        x="energy_%",
        y="danceability_%",
        hover_data=["track_name", "artist(s)_name"],
        color="danceability_%",
        labels={"energy_%": "Energía", "danceability_%": "Bailabilidad"},
        title="Energía vs Bailabilidad"
    )
    st.plotly_chart(fig_energy_dance)

    # --- Top 10 canciones por streams ---
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

    # --- Fuente de datos ---
    st.caption(T["spotify_stats"]["source"][lang])

#PARTE 8 — Mapa mundial de vinos

with tabs[3]:
    st.header(T["wine_map"]["header"][lang])

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
            title=T["wine_map"]["header"][lang]
        )
        fig.update_geos(showcoastlines=True, projection_type="natural earth")
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(T["wine_map"]["no_data"][lang])
