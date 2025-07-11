#✅ Estructura general

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración ---
st.set_page_config("MBTI × Música × Vino", layout="wide")

# --- Cargar datos ---
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines="skip")
wine_df.columns = wine_df.columns.str.strip()

# --- Diccionario MBTI ---
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

#🏠 Inicio con mini-tabs

# Pestaña de INICIO
st.markdown("<h1 style='text-align:center;'>MBTI × Música × Vino 🍷🎶</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Descubre la música y el vino ideal según tu personalidad MBTI.</p>", unsafe_allow_html=True)
st.markdown("---")

subtab1, subtab2 = st.tabs(["🎧 Recomendaciones", "🚀 Interactivo"])

with subtab1:
    tipo = st.selectbox("Selecciona tu tipo de personalidad MBTI:", list(mbti_perfiles.keys()))
    perfil = mbti_perfiles[tipo]
    vino = perfil["vino"]

    st.markdown(f"### {tipo} — {perfil['descripcion']}")
    st.markdown(f"🍷 Vino sugerido: **{vino}**")

    st.subheader("🎵 Canciones recomendadas")
    canciones = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
    for _, row in canciones.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

    st.subheader("🍇 Vinos sugeridos")
    vinos_filtrados = wine_df[wine_df["variety"].str.contains(vino, case=False, na=False)]
    for _, row in vinos_filtrados.head(3).iterrows():
        nombre = row.get("title", "Vino")
        st.markdown(f"**{nombre}** — ⭐ {row['points']} puntos — {row.get('country', 'País desconocido')}")
        st.caption(f"*{row.get('description', 'Sin descripción.')}*")
        st.markdown("---")

with subtab2:
    tipo = st.selectbox("1️⃣ ¿Cuál es tu tipo MBTI?", list(mbti_perfiles.keys()), key="int")
    perfil = mbti_perfiles[tipo]
    vino = perfil["vino"]

    energia = st.slider("Nivel de energía 🎧", 0, 100, (50, 100))
    valence = st.slider("Nivel de felicidad 😊", 0, 100, (50, 100))
    bailabilidad = st.slider("¿Qué tan bailable? 💃", 0, 100, (50, 100))

    filtro_canciones = spotify_df[
        (spotify_df["valence_%"].between(valence[0], valence[1])) &
        (spotify_df["energy_%"].between(energia[0], energia[1])) &
        (spotify_df["danceability_%"].between(bailabilidad[0], bailabilidad[1]))
    ]

    if not filtro_canciones.empty:
        sugerida = filtro_canciones.sample(1).iloc[0]
        st.success(f"🎶 **{sugerida['track_name']}** — *{sugerida['artist(s)_name']}*")
    else:
        st.warning("No se encontraron canciones con esos filtros.")
        
        st.subheader("📊 Tu perfil musical según MBTI")

        if "mbti" in spotify_df.columns:
            media_mbti = spotify_df.groupby("mbti")[["valence_%", "energy_%", "danceability_%"]].mean().reset_index()
            tu_mbti_data = media_mbti[media_mbti["mbti"] == tipo]

            if not tu_mbti_data.empty:
                datos = tu_mbti_data.melt(id_vars="mbti", var_name="característica", value_name="porcentaje")
                fig = px.bar(
                    datos,
                    x="característica",
                    y="porcentaje",
                    color="característica",
                    text="porcentaje",
                    title=f"🎼 Perfil emocional musical del tipo {tipo}",
                    range_y=[0, 100]
                )
                st.plotly_chart(fig, use_container_width=True)

#🎼 Explorar canciones (pestaña principal 2)
tab_explorar, tab_estadisticas = st.tabs(["🎼 Explorar canciones", "📈 Estadísticas Spotify"])

with tab_explorar:
    st.header("🎼 Filtra canciones por año y streams")
    spotify_df["streams"] = pd.to_numeric(spotify_df["streams"], errors="coerce")
    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])

    año = st.selectbox("Año de lanzamiento", sorted(spotify_clean["released_year"].unique()))
    max_streams = int(spotify_clean["streams"].max())
    min_s, max_s = st.slider("🎧 Rango de streams", 0, max_streams, (1_000_000, 10_000_000), step=500_000)

    orden = st.selectbox("Ordenar por", ["streams", "valence_%", "energy_%", "danceability_%"])

    filtrado = spotify_clean[
        (spotify_clean["released_year"] == año) &
        (spotify_clean["streams"] >= min_s) &
        (spotify_clean["streams"] <= max_s)
    ].sort_values(orden, ascending=False).head(20)

    st.dataframe(filtrado[["track_name", "artist(s)_name", "streams"]])
    st.download_button("⬇️ Descargar CSV", filtrado.to_csv(index=False), "filtrado.csv")

#📈 Estadísticas Spotify (pestaña principal 3)
with tab_estadisticas:
    st.header("📊 Análisis general de canciones")

    st.subheader("🎤 Artistas más frecuentes")
    top_artistas = spotify_clean["artist(s)_name"].value_counts().head(10)
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
        x="valence_%", y="energy_%",
        hover_data=["track_name", "artist(s)_name"],
        color="energy_%",
        title="Distribución emocional de canciones"
    )
    st.plotly_chart(fig2)

# 📌 Parte 4: Mapa mundial de vinos con análisis
with st.tabs(["🌍 Mapa mundial de vinos"])[0]:
    st.header("🌍 Mapa mundial de vinos por puntuación")

    # Asegurarse de que la columna 'points' sea numérica
    wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")

    if "country" in wine_df.columns and "points" in wine_df.columns:
        mapa_df = wine_df[wine_df["country"].notna() & wine_df["points"].notna()]

        # Agrupar y filtrar por mínimo 10 vinos por país
        mapa_df = mapa_df.groupby("country", as_index=False).agg(
            promedio_puntos=("points", "mean"),
            cantidad_vinos=("points", "count")
        )
        mapa_df = mapa_df[mapa_df["cantidad_vinos"] >= 10]

        if not mapa_df.empty:
            st.subheader("🗺️ Mapa mundial por puntaje promedio")

            fig = px.choropleth(
                mapa_df,
                locations="country",
                locationmode="country names",
                color="promedio_puntos",
                hover_name="country",
                hover_data={"promedio_puntos": True, "cantidad_vinos": True},
                color_continuous_scale="YlOrBr",  # Puedes probar: "Inferno", "Plasma", "Sunsetdark"
                title="🌍 Promedio de puntuación de vinos por país"
            )
            fig.update_geos(showframe=False, showcoastlines=False, projection_type='equirectangular')
            fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)

            st.caption("📌 *Se muestran solo los países con al menos 10 vinos registrados para evitar sesgos.*")

            st.subheader("🏅 Top 10 países con mejor puntuación promedio")
            top_paises = mapa_df.sort_values("promedio_puntos", ascending=False).head(10)
            fig_bar = px.bar(
                top_paises,
                x="country",
                y="promedio_puntos",
                color="promedio_puntos",
                labels={"country": "País", "promedio_puntos": "Puntaje promedio"},
                title="🍷 Países con mejores vinos según puntaje promedio"
            )
            fig_bar.update_layout(xaxis_title="País", yaxis_title="Puntaje")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("⚠️ No hay suficientes países con datos confiables para mostrar el mapa.")
    else:
        st.error("No se encontraron columnas 'country' o 'points' en la base de datos.")
