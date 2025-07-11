#🔹 BLOQUE 1/3 — Setup inicial, carga de datos y bienvenida
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import unicodedata

# CONFIGURACIÓN GENERAL
st.set_page_config(page_title="MBTI x Música x Vino", layout="wide")

# ESTILO PERSONALIZADO
st.markdown("""
<style>
body {
    background-color: #fffaf3;
    color: #333333;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #ff7043;
}
.sidebar .sidebar-content {
    background-color: #fff4ec;
}
</style>
""", unsafe_allow_html=True)

# CARGA DE DATOS
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip', low_memory=False)
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
wine_df["variety"] = wine_df["variety"].astype(str).str.strip().str.lower()

# PERFILES MBTI
mbti_perfiles = {
    "INFP": {"descripcion": "Soñador, sensible, introspectivo", "vino": "pinot noir", "color": "#e6ccff"},
    "ENFP": {"descripcion": "Espontáneo, creativo, sociable", "vino": "rosé", "color": "#ffe680"},
    "INTJ": {"descripcion": "Analítico, reservado, estratégico", "vino": "cabernet sauvignon", "color": "#c2f0c2"},
    "ESFP": {"descripcion": "Alegre, impulsivo, enérgico", "vino": "sparkling blend", "color": "#ffcccc"},
}

# TABS PRINCIPALES
tabs = st.tabs(["🏠 Inicio", "🎧 Recomendaciones", "🔍 Buscador", "📊 Estadísticas"])

# TAB 1: INICIO
with tabs[0]:
    st.title("🎵 MBTI x Música x Vino 🍷")
    st.markdown("Bienvenid@ a esta app interactiva donde podrás descubrir qué música y vino combinan mejor con tu personalidad MBTI. Basado en datos reales de Spotify 2023 y WineMag.")
    st.image("https://images.unsplash.com/photo-1606788075762-0d990bc7efac", use_column_width=True)
    st.markdown("---")
    st.markdown("Selecciona tu tipo de personalidad MBTI y explora qué sabores y sonidos se alinean contigo. 🎶🍷")


#🔹 BLOQUE 2/3 — Sección de Recomendaciones por MBTI
# TAB 2: RECOMENDACIONES
with tabs[1]:
    st.header("🎧 Tus recomendaciones personalizadas")

    tipo = st.selectbox("Selecciona tu tipo de personalidad MBTI:", list(mbti_perfiles.keys()))
    perfil = mbti_perfiles[tipo]
    color_fondo = perfil["color"]
    vino = perfil["vino"]

    st.markdown(f"""
    <div style='background-color:{color_fondo}; padding:15px; border-radius:10px; margin-bottom:10px'>
        <h2 style='margin-bottom:5px;'>{tipo} — {perfil["descripcion"]}</h2>
        <h4>🍷 Vino sugerido: <i>{vino.title()}</i></h4>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎵 Canciones que van contigo")
    canciones_filtradas = spotify_df[
        (spotify_df["valence_%"] >= 50) & 
        (spotify_df["energy_%"] >= 50)
    ]
    sugeridas = canciones_filtradas.sample(3)
    for _, row in sugeridas.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

    st.subheader("🍇 Vinos compatibles con tu perfil")
    vinos_filtrados = wine_df[wine_df["variety"].str.contains(vino.lower())]

    if vinos_filtrados.empty:
        st.warning("No se encontraron vinos compatibles.")
    else:
        top_vinos = vinos_filtrados.sort_values("points", ascending=False).head(3)
        for _, vino_row in top_vinos.iterrows():
            nombre = vino_row.get("title", "Vino sin nombre")
            puntos = vino_row.get("points", "N/A")
            pais = vino_row.get("country", "Desconocido")
            descripcion = vino_row.get("description", "Sin descripción.")
            st.markdown(f"**🍷 {nombre}**  \n⭐ {puntos} puntos — 🌍 {pais}  \n📝 *{descripcion}*")
            st.markdown("---")
#datosd de canciones:
with tabs[2]:
    st.header("🎼 Explorar canciones por datos")

    st.subheader("📅 Filtros de búsqueda")
    año = st.selectbox("Selecciona un año de lanzamiento", sorted(spotify_df["released_year"].dropna().unique()))
    min_streams, max_streams = st.slider("Filtrar por streams", 0, int(spotify_df["streams"].max()), (1_000_000, 50_000_000), step=1_000_000)

    orden = st.selectbox("Ordenar resultados por:", ["streams", "valence_%", "energy_%", "danceability_%"])

    filtrado = spotify_df[
        (spotify_df["released_year"] == año) &
        (spotify_df["streams"] >= min_streams) &
        (spotify_df["streams"] <= max_streams)
    ].sort_values(orden, ascending=False).head(20)

    st.subheader("🎧 Canciones encontradas:")
    st.dataframe(filtrado[["track_name", "artist(s)_name", "streams", "valence_%", "energy_%"]])

    st.download_button(
        label="⬇️ Descargar CSV filtrado",
        data=filtrado.to_csv(index=False),
        file_name="canciones_filtradas.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader("📊 Artistas con más canciones en el top")
    top_artistas = spotify_df["artist(s)_name"].value_counts().head(10)
    fig1 = px.bar(
        x=top_artistas.index,
        y=top_artistas.values,
        labels={'x': 'Artista', 'y': 'Número de canciones'},
        color=top_artistas.values,
        title="Top 10 artistas más repetidos",
        color_continuous_scale="tealrose"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🎵 Energía vs Felicidad (valence)")
    fig2 = px.scatter(
        spotify_df.dropna(subset=["energy_%", "valence_%"]).sample(300),
        x="valence_%",
        y="energy_%",
        hover_data=["track_name", "artist(s)_name"],
        color="energy_%",
        color_continuous_scale="sunset",
        title="Canciones por felicidad y energía"
    )
    st.plotly_chart(fig2, use_container_width=True)
#🔹 BLOQUE 3/3 — Buscador + Estadísticas + Pie final
# TAB 3: BUSCADOR
with tabs[2]:
    st.header("🔍 Buscador de canciones")
    query = st.text_input("Escribe una palabra clave, canción o artista:")

    if query:
        resultados = spotify_df[
            spotify_df["track_name"].str.contains(query, case=False, na=False) |
            spotify_df["artist(s)_name"].str.contains(query, case=False, na=False)
        ]
        if not resultados.empty:
            st.markdown("### Resultados encontrados:")
            for _, row in resultados.head(5).iterrows():
                st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")
        else:
            st.warning("No se encontraron resultados con esa palabra.")

# TAB 4: ESTADÍSTICAS
with tabs[3]:
    st.header("📊 Estadísticas musicales")

    st.subheader("😊 Top 5 canciones más felices")
    top_valence = spotify_df.sort_values("valence_%", ascending=False).dropna(subset=["valence_%"]).head(5)
    for _, row in top_valence.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}* (valence: {row['valence_%']:.1f})")

    st.subheader("⚡ Distribución de energía en las canciones")
    energia = spotify_df["energy_%"].dropna()
    fig, ax = plt.subplots()
    ax.hist(energia, bins=20, color="#ff7043", edgecolor="white")
    ax.set_xlabel("Nivel de energía")
    ax.set_ylabel("Cantidad de canciones")
    ax.set_title("Histograma de energía en Spotify 2023")
    st.pyplot(fig)

# PIE DE PÁGINA
st.markdown("---")
st.info("App creada por Angelina Alessandra Contreras Bravo 💖 — Datos: Spotify 2023 & WineMag.")
