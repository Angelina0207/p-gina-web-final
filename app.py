#📌 Parte 1: Configuración, estilos y carga de datos
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configuración
st.set_page_config("MBTI x Música x Vino", layout="wide")

# Estilos
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #fff8f0;
        color: #333;
    }
    h1, h2, h3 {
        color: #c94f4f;
    }
    .stButton>button {
        background-color: #ff6666;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Datos
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", on_bad_lines='skip', low_memory=False)
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
wine_df["variety"] = wine_df["variety"].fillna("")

# Perfiles MBTI
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

#📌 Parte 2: Pestañas principales y recomendaciones
# Pestañas
tabs = st.tabs(["🏠 Inicio", "🎧 Recomendaciones", "🎼 Explorar canciones", "🔍 Buscador", "📊 Estadísticas"])

# Inicio
with tabs[0]:
    st.title("MBTI × Música × Vino 🍷🎶")
    st.markdown("Descubre la música y el vino ideal según tu personalidad MBTI.")

# Recomendaciones
with tabs[1]:
    st.header("🎧 Tus recomendaciones personalizadas")
    tipo = st.selectbox("Selecciona tu tipo de personalidad MBTI:", list(mbti_perfiles.keys()))
    perfil = mbti_perfiles[tipo]
    vino = perfil["vino"]

    st.markdown(f"""
    <div style='background-color:{perfil["color"]}; padding:15px; border-radius:10px'>
        <h2>{tipo} — {perfil["descripcion"]}</h2>
        <h4>🍷 Vino sugerido: <i>{vino}</i></h4>
    </div>
    """, unsafe_allow_html=True)

    canciones = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
    st.subheader("🎵 Canciones recomendadas")
    for _, row in canciones.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

    st.subheader("🍇 Vinos sugeridos")
    vinos_filtrados = wine_df[wine_df["variety"].str.contains(vino, case=False)]
    if vinos_filtrados.empty:
        st.warning("No se encontraron vinos.")
    else:
        for _, row in vinos_filtrados.head(3).iterrows():
            # Obtener título adecuado
            if pd.notna(row.get('title')) and row['title'].strip() != "":
                titulo = row['title']
            elif pd.notna(row.get('designation')) and row['designation'].strip() != "":
                titulo = row['designation']
            elif pd.notna(row.get('variety')) and row['variety'].strip() != "":
                titulo = row['variety']
            elif pd.notna(row.get('winery')) and row['winery'].strip() != "":
                titulo = row['winery']
            else:
                titulo = "Vino sin nombre 🍷"

            st.markdown(f"**{titulo}** — ⭐ {row['points']} puntos — {row.get('country', 'País desconocido')}")
            st.caption(f"*{row.get('description', 'Sin descripción.')}*")
            st.markdown("---")
# Pestañas
tab1, tab2, tab3 = st.tabs(["🎧 Recomendaciones", "🚀 Interactivo", "📈 Estadísticas Spotify"])

# 📌 Parte 3: Explorador musical interactivo
with tab3:
    st.header("📈 Explorar canciones por filtros")

    # Asegurar que la columna 'streams' es numérica
    if "streams" in spotify_df.columns:
        spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")

        # Limpiar NaN
        spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

        if not spotify_clean.empty:
            # Selectbox para año
            año = st.selectbox("Año de lanzamiento", sorted(spotify_clean["released_year"].unique()))

            # Rango dinámico de streams
            max_streams_val = spotify_clean["streams"].dropna().max()
            max_streams = int(max_streams_val) if pd.notna(max_streams_val) else 50_000_000
            min_s, max_s = st.slider("🎧 Rango de streams", 0, max_streams, (1_000_000, 10_000_000), step=500_000)

            # Orden por métrica
            orden = st.selectbox("Ordenar por", ["streams", "valence_%", "energy_%", "danceability_%"])

            # Filtro
            filtrado = spotify_clean[
                (spotify_clean["released_year"] == año) &
                (spotify_clean["streams"] >= min_s) &
                (spotify_clean["streams"] <= max_s)
            ].sort_values(orden, ascending=False).head(20)

            # Mostrar tabla
            st.dataframe(filtrado[["track_name", "artist(s)_name", "streams"]])
            st.download_button("⬇️ Descargar CSV", filtrado.to_csv(index=False), "filtrado.csv")

            # Gráfico: Artistas más frecuentes
            st.subheader("🎤 Artistas más frecuentes")
            top_artistas = spotify_clean["artist(s)_name"].value_counts().head(10)
            fig = px.bar(
                x=top_artistas.index,
                y=top_artistas.values,
                labels={"x": "Artista", "y": "Número de canciones"},
                title="Top 10 artistas más presentes"
            )
            st.plotly_chart(fig)

            # Gráfico: Energía vs Felicidad
            st.subheader("🎵 Energía vs Felicidad")
            fig2 = px.scatter(
                spotify_clean.sample(300),
                x="valence_%", y="energy_%",
                hover_data=["track_name", "artist(s)_name"],
                color="energy_%",
                title="Canciones: Valence vs Energía"
            )
            st.plotly_chart(fig2)
        else:
            st.warning("No hay datos suficientes en Spotify para mostrar estadísticas.")
    else:
        st.error("La columna 'streams' no está disponible en el CSV.")
        
# --- Pestaña de estadísticas ---
with tab3:
    st.header("📈 Análisis de Canciones Populares en Spotify")

    # Limpiar datos vacíos
    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

    # Rango para filtrar streams
    min_streams = 1_000_000
    max_streams = int(spotify_clean["streams"].dropna().max())

    rango_streams = st.slider("🎧 Filtrar por número de streams", min_value=min_streams, max_value=max_streams, value=(min_streams, 50_000_000), step=1_000_000)

    # Filtrar canciones según streams
    filtrado = spotify_clean[spotify_clean["streams"].between(rango_streams[0], rango_streams[1])]

    if not filtrado.empty:
        st.subheader("🔢 Total de Streams por Año")
        resumen_por_año = filtrado.groupby("released_year")["streams"].sum().reset_index()
        fig_bar = px.bar(resumen_por_año, x="released_year", y="streams", title="📅 Streams por Año de Lanzamiento", labels={"streams": "Reproducciones", "released_year": "Año"})
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("🎶 Energía vs Popularidad")
        fig_scatter = px.scatter(
            filtrado,
            x="energy_%",
            y="streams",
            size="valence_%",
            color="released_year",
            hover_data=["track_name", "artist(s)_name"],
            title="⚡ Energía vs Streams (Tamaño: Felicidad)",
            labels={"energy_%": "Energía", "streams": "Reproducciones"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No se encontraron canciones en ese rango.")
