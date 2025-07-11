import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

st.set_page_config("MBTI x Música x Vino", layout="wide")

# --- TRADUCCIONES ---
textos = {
    "Español": {
        "titulo": "Bienvenida a *Wine & Music Explorer* 🍷🎶",
        "intro": "¿Sabías que tu personalidad podría tener su propia banda sonora y copa de vino ideal?",
        "secciones": [
            "🎧 Tu Mood Ideal",
            "🎼 Explorar canciones",
            "📈 Estadísticas Spotify",
            "🌍 Mapa mundial de vinos"
        ],
        "mbti": "Selecciona tu tipo de personalidad MBTI:",
        "recomendaciones": "🎧 Tus recomendaciones personalizadas",
        "canciones_recomendadas": "🎵 Canciones recomendadas",
        "vinos_recomendados": "🍇 Vinos sugeridos",
        "no_vinos": "No se encontraron vinos.",
        "explora_mood": "🚀 Explora tu mood musical y vinícola",
        "pregunta_mbti": "1️⃣ ¿Cuál es tu tipo de personalidad MBTI?",
        "ajusta_mood": "2️⃣ Ajusta tu mood musical 🎚️",
        "energia": "Nivel de energía 🎧",
        "valence": "Nivel de felicidad 😊",
        "bailabilidad": "¿Qué tan bailable? 💃",
        "sin_resultados": "No se encontraron canciones con esos parámetros.",
        "vino_ideal": "🍷 Vino ideal:",
        "explorar_canciones": "🎼 Explorar canciones por filtros",
        "anio": "Año de lanzamiento",
        "rango_streams": "Rango de streams",
        "ordenar": "Ordenar por",
        "canciones_filtradas": "🎵 Canciones filtradas",
        "descargar": "⬇️ Descargar CSV",
        "artistas_frecuentes": "🎤 Artistas más frecuentes",
        "energia_vs_felicidad": "🎵 Energía vs Felicidad",
        "sin_datos": "No hay suficientes datos limpios para mostrar estadísticas.",
        "estadisticas": "📈 Estadísticas generales de Spotify",
        "bpm": "🎶 Distribución de BPM",
        "bpm_titulo": "Distribución de BPM (ritmo)",
        "energia_vs_baila": "📊 Relación entre energía y bailabilidad",
        "top_streams": "🎧 Canciones más populares por número de streams",
        "top10": "Top 10 canciones con más streams",
        "fuente": "Fuente: Base de datos de Spotify 2023. Los valores se han limpiado para esta visualización.",
        "mapa": "🌍 Mapa mundial de vinos por puntuación",
        "no_mapa": "No hay datos suficientes para generar el mapa."
    },
    "English": {
        "titulo": "Welcome to *Wine & Music Explorer* 🍷🎶",
        "intro": "Did you know your personality might have its own soundtrack and perfect wine?",
        "secciones": [
            "🎧 Your Ideal Mood",
            "🎼 Explore Songs",
            "📈 Spotify Statistics",
            "🌍 Global Wine Map"
        ],
        "mbti": "Select your MBTI personality type:",
        "recomendaciones": "🎧 Your Personalized Recommendations",
        "canciones_recomendadas": "🎵 Recommended Songs",
        "vinos_recomendados": "🍇 Suggested Wines",
        "no_vinos": "No wines found.",
        "explora_mood": "🚀 Explore your musical and wine mood",
        "pregunta_mbti": "1️⃣ What is your MBTI personality type?",
        "ajusta_mood": "2️⃣ Adjust your musical mood 🎚️",
        "energia": "Energy level 🎧",
        "valence": "Happiness level 😊",
        "bailabilidad": "How danceable? 💃",
        "sin_resultados": "No songs found with those parameters.",
        "vino_ideal": "🍷 Ideal wine:",
        "explorar_canciones": "🎼 Explore songs by filters",
        "anio": "Release year",
        "rango_streams": "Streams range",
        "ordenar": "Sort by",
        "canciones_filtradas": "🎵 Filtered songs",
        "descargar": "⬇️ Download CSV",
        "artistas_frecuentes": "🎤 Most frequent artists",
        "energia_vs_felicidad": "🎵 Energy vs Happiness",
        "sin_datos": "Not enough clean data to show statistics.",
        "estadisticas": "📈 General Spotify Statistics",
        "bpm": "🎶 BPM Distribution",
        "bpm_titulo": "BPM (Beats Per Minute) Distribution",
        "energia_vs_baila": "📊 Energy vs Danceability",
        "top_streams": "🎧 Most popular songs by streams",
        "top10": "Top 10 most streamed songs",
        "fuente": "Source: Spotify 2023 database. Values have been cleaned for visualization.",
        "mapa": "🌍 Global wine score map",
        "no_mapa": "Not enough data to generate the map."
    }
}

#✅ 2. RECOMENDACIONES + INTERACTIVO (como mini-tabs)
# --- FUNCIONES AUXILIARES ---
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.strip()

def contiene_palabra(texto, palabra):
    texto_norm = normalizar_texto(texto)
    palabra_norm = normalizar_texto(palabra)
    return palabra_norm in texto_norm

# --- PERFILES MBTI ---
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
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines="skip", low_memory=False)
wine_df.columns = wine_df.columns.str.strip()
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")

# --- MINI-TABS: Recomendaciones + Interactivo ---
st.header("💫 Wine & Music Matcher")
tab_rec, tab_inter = st.tabs([textos[idioma]["recomendaciones"], textos[idioma]["interactivo"]])

# --- TAB DE RECOMENDACIONES ---
with tab_rec:
    tipo = st.selectbox(textos[idioma]["selecciona_tipo"], list(mbti_perfiles.keys()), key="rec")
    perfil = mbti_perfiles[tipo]
    vino = perfil["vino"]

    st.markdown(f"""
        <div style='background-color:{perfil["color"]}; padding:15px; border-radius:10px'>
            <h2>{tipo} — {perfil["descripcion"]}</h2>
            <h4>{textos[idioma]["vino_sugerido"]}: <i>{vino}</i></h4>
        </div>
    """, unsafe_allow_html=True)

    canciones = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
    st.subheader(textos[idioma]["canciones_recomendadas"])
    for _, row in canciones.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

    st.subheader(textos[idioma]["vinos_sugeridos"])
    vinos_filtrados = wine_df[wine_df["variety"].astype(str).str.contains(vino, case=False, na=False)]
    if vinos_filtrados.empty:
        st.warning(textos[idioma]["no_vinos"])
    else:
        for _, row in vinos_filtrados.head(3).iterrows():
            st.markdown(f"**{row.get('title', 'Vino')}** — ⭐ {row['points']} puntos — {row.get('country', 'Desconocido')}")
            st.caption(f"*{row.get('description', 'Sin descripción.')}*")
            st.markdown("---")

# --- TAB INTERACTIVO ---
with tab_inter:
    tipo = st.selectbox(textos[idioma]["selecciona_tipo"], list(mbti_perfiles.keys()), key="interactivo")
    perfil = mbti_perfiles[tipo]
    vino = perfil["vino"]

    energia = st.slider("🔋 Energy level", 0, 100, (50, 100))
    valencia = st.slider("😊 Happiness level", 0, 100, (50, 100))
    bailabilidad = st.slider("💃 Danceability", 0, 100, (50, 100))

    filtro_canciones = spotify_df[
        (spotify_df["valence_%"].between(valencia[0], valencia[1])) &
        (spotify_df["energy_%"].between(energia[0], energia[1])) &
        (spotify_df["danceability_%"].between(bailabilidad[0], bailabilidad[1]))
    ]

    if not filtro_canciones.empty:
        sugerencia = filtro_canciones.sample(1).iloc[0]
        st.markdown(f"🎶 **{sugerencia['track_name']}** — *{sugerencia['artist(s)_name']}*")
    else:
        st.warning("No se encontraron canciones con esos parámetros.")

    st.markdown(f"🍷 {textos[idioma]['vino_sugerido']}: **{vino}**")


#✅ 3. ESTADÍSTICAS SPOTIFY (Pestaña independiente)
# --- PARTE 3: ESTADÍSTICAS SPOTIFY ---
with tabs[2]:
    st.header(textos[idioma]["estadisticas_spotify"])  # Ej: "📈 Estadísticas Spotify"

    # Limpieza de datos
    spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")
    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

    # Filtros
    año = st.selectbox("📅 " + textos[idioma]["año_lanzamiento"], sorted(spotify_clean["released_year"].unique()))
    max_streams_val = spotify_clean["streams"].dropna().max()
    max_streams = int(max_streams_val) if pd.notna(max_streams_val) else 50_000_000

    min_s, max_s = st.slider("🎧 " + textos[idioma]["rango_streams"], 0, max_streams, (1_000_000, 10_000_000), step=500_000)
    orden = st.selectbox(textos[idioma]["ordenar_por"], ["streams", "valence_%", "energy_%", "danceability_%"])

    filtrado = spotify_clean[
        (spotify_clean["released_year"] == año) &
        (spotify_clean["streams"] >= min_s) &
        (spotify_clean["streams"] <= max_s)
    ].sort_values(orden, ascending=False).head(20)

    st.dataframe(filtrado[["track_name", "artist(s)_name", "streams"]])
    st.download_button("⬇️ Descargar CSV", filtrado.to_csv(index=False), "canciones_filtradas.csv")

    # Top 10 artistas
    st.subheader("🎤 " + textos[idioma]["top_artistas"])
    top_artistas = spotify_df["artist(s)_name"].value_counts().head(10)
    fig_artistas = px.bar(
        x=top_artistas.index,
        y=top_artistas.values,
        labels={"x": "Artista", "y": "Número de canciones"},
        title=textos[idioma]["top_artistas"]
    )
    st.plotly_chart(fig_artistas)

    # Energía vs felicidad
    st.subheader("🎵 " + textos[idioma]["energia_vs_valence"])
    fig_scatter = px.scatter(
        spotify_clean.sample(300),
        x="valence_%",
        y="energy_%",
        hover_data=["track_name", "artist(s)_name"],
        color="energy_%",
        title=textos[idioma]["energia_vs_valence"]
    )
    st.plotly_chart(fig_scatter)

#✅ 4. MAPA MUNDIAL DE VINOS (Pestaña independiente)
# --- PARTE 4: MAPA MUNDIAL DE VINOS ---
with tabs[3]:
    st.header(textos[idioma]["mapa_vinos"])  # Ej: "🌍 Mapa mundial de vinos por puntuación"

    # Preprocesamiento
    wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
    mapa_df = wine_df[wine_df["country"].notna() & wine_df["points"].notna()]

    if not mapa_df.empty:
        mapa_grouped = mapa_df.groupby("country", as_index=False).agg(
            promedio_puntos=("points", "mean"),
            cantidad_vinos=("points", "count")
        )

        # Visualización con Plotly
        fig_mapa = px.choropleth(
            mapa_grouped,
            locations="country",
            locationmode="country names",
            color="promedio_puntos",
            hover_name="country",
            hover_data={"promedio_puntos": True, "cantidad_vinos": True},
            color_continuous_scale="Oranges",
            title=textos[idioma]["mapa_vinos"]
        )
        fig_mapa.update_geos(fitbounds="locations", visible=False)
        fig_mapa.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        st.plotly_chart(fig_mapa, use_container_width=True)

        st.caption("📌 " + textos[idioma]["mapa_nota"])
    else:
        st.warning("No hay suficientes datos para generar el mapa.")

# --- PIE DE PÁGINA / AGRADECIMIENTOS ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 20px; font-size: 16px; color: gray;'>
    <p>{textos[idioma]["agradecimiento"]}</p>
    <p><b>Streamlit App - {textos[idioma]["nombre_app"]}</b></p>
    <p>© 2025 - Angelina Alessandra Contreras Bravo</p>
</div>
""", unsafe_allow_html=True)
