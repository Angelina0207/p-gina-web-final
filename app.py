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
spotify_df = pd.read_csv("spotify-2023.csv")
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
            st.markdown(f"**{row.get('title', 'Vino')}** — ⭐ {row['points']} puntos — {row.get('country', 'País desconocido')}")
            st.caption(f"*{row.get('description', 'Sin descripción.')}*")
            st.markdown("---")

#📌 Parte 3: Explorador musical interactivo
with tabs[2]:
    st.header("🎼 Explorar canciones por filtros")

    spotify_clean = spotify_df.dropna(subset=["streams", "released_year"])
    if not spotify_clean.empty:
        año = st.selectbox("Año de lanzamiento", sorted(spotify_clean["released_year"].unique()))
        max_streams = int(spotify_clean["streams"].max())
        min_s, max_s = st.slider("Rango de streams", 0, max_streams, (1000000, 10000000), step=500000)
        orden = st.selectbox("Ordenar por", ["streams", "valence_%", "energy_%", "danceability_%"])

        filtrado = spotify_clean[
            (spotify_clean["released_year"] == año) &
            (spotify_clean["streams"] >= min_s) &
            (spotify_clean["streams"] <= max_s)
        ].sort_values(orden, ascending=False).head(20)

        st.dataframe(filtrado[["track_name", "artist(s)_name", "streams"]])
        st.download_button("⬇️ Descargar CSV", filtrado.to_csv(index=False), "filtrado.csv")

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

#📌 Parte 4: Buscador y Estadísticas
with tabs[3]:
    st.header("🔍 Buscador de canciones")
    q = st.text_input("Busca por canción o artista")
    if q:
        res = spotify_df[
            spotify_df["track_name"].str.contains(q, case=False, na=False) |
            spotify_df["artist(s)_name"].str.contains(q, case=False, na=False)
        ]
        if not res.empty:
            st.write(res[["track_name", "artist(s)_name", "streams"]].head(10))
        else:
            st.warning("No se encontró nada 😢")

with tabs[4]:
    st.header("📊 Estadísticas musicales")
    top_val = spotify_df.sort_values("valence_%", ascending=False).dropna(subset=["valence_%"]).head(5)
    st.subheader("😊 Canciones más felices")
    for _, row in top_val.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}* (valence: {row['valence_%']:.1f})")

    energia = spotify_df["energy_%"].dropna()
    fig, ax = plt.subplots()
    ax.hist(energia, bins=20, color="#ff7043", edgecolor="white")
    ax.set_title("Distribución de energía")
    st.pyplot(fig)
