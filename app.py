import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

st.set_page_config("MBTI x Música x Vino", layout="wide")

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

# 🌐 Selector de idioma
idioma = st.selectbox("🌐 Choose language / Elige idioma:", ["Español", "English"])

# 💬 Introducción en el idioma seleccionado
if idioma == "Español":
    st.markdown("""
    ### ✨ Bienvenida a *Wine & Music Explorer* 🍷🎶  
    ¿Sabías que tu personalidad podría tener su propia banda sonora y copa de vino ideal?

    Esta app interactiva está dividida en dos secciones principales:

    🔸 **Experiencia personalizada**: descubre qué vino y canción van contigo según tu tipo MBTI.  
    🔸 **Exploración de datos**: analiza tendencias musicales, explora canciones según filtros, y observa un mapa global del vino.

    ¡Descorcha, explora y disfruta! 🥂
    """)
else:
    st.markdown("""
    ### ✨ Welcome to *Wine & Music Explorer* 🍷🎶  
    Did you know your personality might have its own soundtrack and perfect wine?

    This interactive app is divided into two main sections:

    🔸 **Personalized Experience**: find out which wine and song match your MBTI type.  
    🔸 **Data Exploration**: analyze musical trends, filter songs by mood, and explore a global wine map.

    Uncork, explore, and enjoy! 🥂
    """)
    
# --- MBTI + vino ---
mbti_perfiles = {
    "INFP": {"descripcion": "Soñador, sensible, introspectivo", "vino": "Pinot Noir", "color": "#e6ccff"},
    "ENFP": {"descripcion": "Espontáneo, creativo, sociable", "vino": "Sauvignon Blanc", "color": "#ffe680"},
    "INTJ": {"descripcion": "Analítico, reservado, estratégico", "vino": "Cabernet Sauvignon", "color": "#c2f0c2"},
    "ISFJ": {"descripcion": "Cálido, protector, leal", "vino": "Merlot", "color": "#f0d9b5"},
    "ENTP": {"descripcion": "Innovador, conversador, curioso", "vino": "Rosé", "color": "#ffcce6"},
    "ESFP": {"descripcion": "Alegre, impulsivo, enérgico", "vino": "Espumante", "color": "#ffcccc"},
    "INFJ": {"descripcion": "Visionario, intuitivo, profundo", "vino": "Syrah", "color": "#d9d2e9"},
    "ISTJ": {"descripcion": "Tradicional, metódico, práctico", "vino": "Malbec", "color": "#d9ead3"}
}

# --- CARGA DE DATOS ---
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip')
wine_df.columns = wine_df.columns.str.strip()
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")

#🧩 PARTE 2: Pestaña principal “🎧 Tu Mood Ideal” con mini-tabs
# --- Pestañas principales ---
main_tabs = st.tabs(["🎧 Tu Mood Ideal", "🎼 Explorar canciones", "📈 Estadísticas Spotify", "🌍 Mapa mundial de vinos"])

# === 🎧 MINI-TABS DENTRO DE “Tu Mood Ideal” ===
with main_tabs[0]:
    subtabs = st.tabs(["🎧 Recomendaciones", "🚀 Interactivo"])

    # --- Subtab: Recomendaciones MBTI ---
    with subtabs[0]:
        st.header("🎧 Tus recomendaciones personalizadas")
        tipo = st.selectbox("Selecciona tu tipo de personalidad MBTI:", list(mbti_perfiles.keys()), key="mbti1")
        perfil = mbti_perfiles[tipo]
        vino = perfil["vino"]

        st.markdown(f"""
        <div style='background-color:{perfil["color"]}; padding:15px; border-radius:10px'>
            <h2>{tipo} — {perfil["descripcion"]}</h2>
            <h4>🍷 Vino sugerido: <i>{vino}</i></h4>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🎵 Canciones recomendadas")
        canciones = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
        for _, row in canciones.iterrows():
            st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

        st.subheader("🍇 Vinos sugeridos")
        vinos_filtrados = wine_df[wine_df["variety"].fillna("").str.contains(vino, case=False)]
        if vinos_filtrados.empty:
            st.warning("No se encontraron vinos.")
        else:
            for _, row in vinos_filtrados.head(3).iterrows():
                titulo = row.get("title", "Vino")
                puntos = row.get("points", "N/A")
                pais = row.get("country", "País desconocido")
                descripcion = row.get("description", "Sin descripción.")
                st.markdown(f"**{titulo}** — ⭐ {puntos} puntos — {pais}")
                st.caption(f"*{descripcion}*")
                st.markdown("---")

    # --- Subtab: Interactivo ---
    with subtabs[1]:
        st.header("🚀 Explora tu mood musical y vinícola")
        tipo = st.selectbox("1️⃣ ¿Cuál es tu tipo de personalidad MBTI?", list(mbti_perfiles.keys()), key="mbti2")
        perfil = mbti_perfiles[tipo]
        vino = perfil["vino"]

        st.subheader("2️⃣ Ajusta tu mood musical 🎚️")
        energia = st.slider("Nivel de energía 🎧", 0, 100, (50, 100))
        valence = st.slider("Nivel de felicidad 😊", 0, 100, (50, 100))
        bailabilidad = st.slider("¿Qué tan bailable? 💃", 0, 100, (50, 100))

        filtro = spotify_df[
            (spotify_df['valence_%'].between(valence[0], valence[1])) &
            (spotify_df['energy_%'].between(energia[0], energia[1])) &
            (spotify_df['danceability_%'].between(bailabilidad[0], bailabilidad[1]))
        ]

        if not filtro.empty:
            resultado = filtro.sample(1).iloc[0]
            st.markdown(f"🎶 **{resultado['track_name']}** — *{resultado['artist(s)_name']}*")
        else:
            st.warning("No se encontraron canciones con esos parámetros.")

        st.markdown(f"🍷 **Vino ideal:** {vino}")

#🎼 PARTE 3: Explorador de canciones

with main_tabs[1]:
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

# 📈 PARTE 4: Estadísticas Spotify
with main_tabs[2]:
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

#🌍 PARTE 5: Mapa mundial de vinos
with main_tabs[3]:
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
