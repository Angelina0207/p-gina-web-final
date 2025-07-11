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

# --- MAIN TABS ---
tabs = st.tabs(T["tabs_main"][lang])

# 🎧 Your Ideal Mood
with tabs[0]:
    subt = st.tabs(T["subtabs_mood"][lang])

    # Recommendations
    with subt[0]:
        st.header(T["labels"][lang]["song_rec"])
        mbti = st.selectbox(T["labels"][lang]["mbti_select"], list(mbti_profiles.keys()), key="mbti1")
        profile = mbti_profiles[mbti]
        wine = profile["wine"]
        st.markdown(f"<div style='background:{profile['color']};padding:10px;border-radius:8px'><h2>{mbti} — {profile['description']}</h2><h4>{T['labels'][lang]['ideal_wine']} <i>{wine}</i></h4></div>", unsafe_allow_html=True)
        songs = spotify_df[(spotify_df["valence_%"] >= 50)&(spotify_df["energy_%"] >= 50)].sample(3)
        for _, r in songs.iterrows():
            st.markdown(f"- **{r['track_name']}** — *{r['artist(s)_name']}*")
        st.subheader(T["labels"][lang]["wine_rec"])
        fw = wine_df[wine_df["variety"].fillna("").str.contains(wine, case=False)]
        if fw.empty:
            st.warning(T["labels"][lang]["no_wines"])
        else:
            for _, r in fw.head(3).iterrows():
                st.markdown(f"**{r.get('title','Wine')}** — ⭐ {r.get('points','N/A')} — {r.get('country','Unknown')}")
                st.caption(f"*{r.get('description','No description.')}*")

    # Interactive
    with subt[1]:
        st.header(T["subtabs_mood"][lang][1])
        mbti = st.selectbox(T["labels"][lang]["mbti_select"], list(mbti_profiles.keys()), key="mbti2")
        perfil = mbti_profiles[mbti]
        wine = perfil["wine"]
        st.subheader(T["subtabs_mood"][lang][1])
        energy = st.slider(T["labels"][lang]["energy"], 0, 100, (50,100))
        happiness = st.slider(T["labels"][lang]["happiness"], 0, 100, (50,100))
        dance = st.slider(T["labels"][lang]["danceability"], 0, 100, (50,100))
        dfm = spotify_df[spotify_df["valence_%"].between(happiness[0],happiness[1]) & spotify_df["energy_%"].between(energy[0],energy[1]) & spotify_df["danceability_%"].between(dance[0],dance[1])]
        if not dfm.empty:
            r = dfm.sample(1).iloc[0]
            st.markdown(f"🎶 **{r['track_name']}** — *{r['artist(s)_name']}*")
        else:
            st.warning(T["labels"][lang]["no_songs"])
        st.markdown(f"{T['labels'][lang]['ideal_wine']} **{wine}**")

# 🎼 Explore Songs
with tabs[1]:
    st.header(T["songs_tab"]["header"][lang])
    sdf = spotify_df.dropna(subset=["streams","released_year"])
    if not sdf.empty:
        year = st.selectbox(T["songs_tab"]["year"][lang], sorted(sdf["released_year"].unique()))
        ms = int(sdf["streams"].max())
        mn, mx = st.slider(T["songs_tab"]["streams"][lang], 0, ms, (1_000_000, min(ms,10_000_000)), step=500_000)
        sb = st.selectbox(T["songs_tab"]["sort"][lang], ["streams","valence_%","energy_%","danceability_%"])
        filt = sdf[(sdf["released_year"]==year)&(sdf["streams"].between(mn,mx))].sort_values(sb, ascending=False).head(20)
        st.subheader(T["songs_tab"]["filtered"][lang]); st.dataframe(filt[["track_name","artist(s)_name","streams"]]); st.download_button(T["songs_tab"]["download"][lang], filt.to_csv(index=False), "songs.csv")
        st.subheader(T["songs_tab"]["artists"][lang]); fig=px.bar(x=sdf["artist(s)_name"].value_counts().head(10).index,y=sdf["artist(s)_name"].value_counts().head(10).values,labels={"x":"Artist","y":"Count"},title=T["songs_tab"]["artists"][lang]); st.plotly_chart(fig)
        st.subheader(T["songs_tab"]["energy_valence"][lang]); fig2=px.scatter(sdf.sample(300),x="valence_%",y="energy_%",hover_data=["track_name","artist(s)_name"],color="energy_%"); st.plotly_chart(fig2)
    else:
        st.warning(T["songs_tab"]["no_data"][lang])

# 📈 Spotify Stats
with tabs[2]:
    st.header(T["spotify_stats"]["header"][lang])
    st.subheader(T["spotify_stats"]["bpm"][lang]); figb=px.histogram(spotify_df,x="bpm",nbins=30,title=T["spotify_stats"]["bpm"][lang],labels={"bpm":"BPM"}); st.plotly_chart(figb)
    st.subheader(T["spotify_stats"]["energy_dance"][lang]); figd=px.scatter(spotify_df.sample(300),x="energy_%",y="danceability_%",color="valence_%",hover_data=["track_name","artist(s)_name"]); st.plotly_chart(figd)
    st.subheader(T["spotify_stats"]["top"][lang]); fst=spotify_df.sort_values("streams",ascending=False).head(10); figt=px.bar(fst,x="track_name",y="streams",color="artist(s)_name",title=T["spotify_stats"]["top"][lang]); st.plotly_chart(figt)
    st.caption(T["spotify_stats"]["source"][lang])

# 🌍 Global Wine Map
with tabs[3]:
    st.header(T["wine_map"]["header"][lang])
    wine_df["points"]=pd.to_numeric(wine_df["points"],errors="coerce")
    wine_df["country"]=wine_df["country"].fillna("Unknown")
    md=wine_df.dropna(subset=["points","country"]).groupby("country",as_index=False).agg(avg_points=("points","mean"),count=("points","count"))
    if not md.empty:
        figm=px.choropleth(md,locations="country",locationmode="country names",color="avg_points",hover_name="country",hover_data=["avg_points","count"],color_continuous_scale="YlOrRd",title=T["wine_map"]["header"][lang])
        figm.update_geos(showcoastlines=True,projection_type="natural earth"); st.plotly_chart(figm,use_container_width=True)
    else:
        st.warning(T["wine_map"]["no_data"][lang])
