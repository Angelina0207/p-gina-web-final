
# BLOQUE 1/3 — Configuración + Datos + Perfiles MBTI

import streamlit as st
import pandas as pd
import unicodedata
import plotly.express as px
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config("MBTI x Música x Vino", layout="centered")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #fffaf3;
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
hr {
    border: none;
    border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip', low_memory=False)

wine_df.columns = wine_df.columns.str.strip()
wine_df["variety"] = wine_df["variety"].astype(str).str.strip().str.lower()
wine_df["points"] = pd.to_numeric(wine_df["points"], errors="coerce")
wine_df = wine_df.dropna(subset=["variety", "points"])

# --- PERFILES MBTI PERSONALIZADOS ---
mbti_perfiles = {
    "INFP": {
        "descripcion": "Soñador, sensible, introspectivo",
        "color": "#e6ccff",
        "vino": "pinot noir",
        "musica": {"valence": (30, 60), "energy": (20, 50), "danceability": (30, 60)}
    },
    "ENFP": {
        "descripcion": "Espontáneo, creativo, sociable",
        "color": "#ffe680",
        "vino": "rosé",
        "musica": {"valence": (60, 90), "energy": (60, 90), "danceability": (60, 90)}
    },
    "INTJ": {
        "descripcion": "Analítico, reservado, estratégico",
        "color": "#c2f0c2",
        "vino": "cabernet sauvignon",
        "musica": {"valence": (20, 50), "energy": (30, 60), "danceability": (30, 60)}
    },
    "ESFP": {
        "descripcion": "Alegre, impulsivo, enérgico",
        "color": "#ffcccc",
        "vino": "sparkling blend",
        "musica": {"valence": (70, 100), "energy": (70, 100), "danceability": (70, 100)}
    }
}

#🔹 BLOQUE 2/3 — App interactiva completa
# --- PORTADA ---
st.title("🎧 MBTI x Música x Vino 🍷")
st.caption("Descubre tu personalidad en sabores y sonidos. Basado en datos reales de Spotify y WineMag. ✨")

# --- SELECCIÓN DE TIPO MBTI ---
tipo = st.selectbox("Selecciona tu tipo de personalidad MBTI:", list(mbti_perfiles.keys()))
perfil = mbti_perfiles[tipo]

# --- BLOQUE DE PERFIL ---
st.markdown(f"""
<div style='background-color:{perfil["color"]}; padding:20px; border-radius:12px; margin-bottom:20px;'>
    <h2 style='margin-bottom:10px;'>{tipo} — {perfil['descripcion']}</h2>
    <h4>🍷 Vino sugerido: <span style='color:#444;'>{perfil['vino'].title()}</span></h4>
</div>
""", unsafe_allow_html=True)

# --- CANCIONES PERSONALIZADAS ---
st.subheader("🎵 Tus canciones ideales")
val_min, val_max = perfil["musica"]["valence"]
ene_min, ene_max = perfil["musica"]["energy"]
bail_min, bail_max = perfil["musica"]["danceability"]

canciones = spotify_df[
    (spotify_df["valence_%"].between(val_min, val_max)) &
    (spotify_df["energy_%"].between(ene_min, ene_max)) &
    (spotify_df["danceability_%"].between(bail_min, bail_max))
]

if not canciones.empty:
    canciones_mostradas = canciones.sample(3)
    for _, row in canciones_mostradas.iterrows():
        st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")
else:
    st.warning("No se encontraron canciones con esos valores.")

# --- VINOS COMPATIBLES ---
st.subheader("🍇 Vinos que combinan contigo")
vino_variedad = perfil["vino"].lower().strip()
vinos_filtrados = wine_df[wine_df["variety"].str.contains(vino_variedad, na=False)]

if not vinos_filtrados.empty:
    top_vinos = vinos_filtrados.sort_values("points", ascending=False).head(3)
    for _, row in top_vinos.iterrows():
        titulo = row.get("title", "Vino sin título")
        puntos = row.get("points", "N/A")
        pais = row.get("country", "País desconocido")
        descripcion = row.get("description", "Sin descripción disponible.")
        st.markdown(f"### 🍷 {titulo}")
        st.markdown(f"**⭐ Puntuación:** {puntos} &nbsp;&nbsp; 🌍 **Origen:** {pais}")
        st.caption(f"📝 *{descripcion}*")
        st.markdown("---")
else:
    st.warning("No se encontraron vinos para este tipo.")

# --- BUSCADOR DE CANCIONES ---
st.subheader("🔍 Busca una canción o artista")
search = st.text_input("Escribe una palabra clave, nombre de canción o artista:")

if search:
    resultados = spotify_df[spotify_df["track_name"].str.contains(search, case=False, na=False) |
                            spotify_df["artist(s)_name"].str.contains(search, case=False, na=False)]
    if not resultados.empty:
        st.markdown("### Resultados encontrados:")
        for _, row in resultados.head(5).iterrows():
            st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")
    else:
        st.warning("No se encontraron coincidencias.")


#🔹 BLOQUE 3/3 — Datos musicales interesantes + visualización
st.markdown("---")
st.header("📊 Datos interesantes sobre las canciones 🎶")

# --- TOP 5 canciones con mayor valence ---
st.subheader("😊 Top 5 canciones más felices")
top_valence = spotify_df.sort_values("valence_%", ascending=False).dropna(subset=["valence_%"]).head(5)

for _, row in top_valence.iterrows():
    st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}* (valence: {row['valence_%']:.1f})")

# --- HISTOGRAMA DE ENERGÍA ---
st.subheader("⚡ Distribución de energía en todas las canciones")
energia = spotify_df["energy_%"].dropna()

fig, ax = plt.subplots()
ax.hist(energia, bins=20, color='#ff7043', edgecolor='white')
ax.set_xlabel("Nivel de energía")
ax.set_ylabel("Cantidad de canciones")
ax.set_title("Distribución general de energía")
st.pyplot(fig)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.info("App desarrollada por Angelina Alessandra Contreras Bravo ✨. Todos los datos provienen de fuentes reales: Spotify Top (2023) y WineMag. Esta aplicación es una muestra de creatividad, análisis y diseño interactivo basada en datos.")
