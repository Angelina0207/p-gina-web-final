import streamlit as st
import pandas as pd
import unicodedata
import random

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config("MBTI x Música x Vino", layout="centered")

# --- CARGAR CSVs ---
spotify_df = pd.read_csv("spotify-2023.csv", encoding="latin1")
wine_df = pd.read_csv("winemag-data_first150k.csv", encoding="latin1", on_bad_lines='skip', low_memory=False)

# --- LIMPIEZA DE DATOS ---
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
        "musica": {
            "valence": (30, 60),
            "energy": (20, 50),
            "danceability": (30, 60)
        }
    },
    "ENFP": {
        "descripcion": "Espontáneo, creativo, sociable",
        "color": "#ffe680",
        "vino": "rosé",
        "musica": {
            "valence": (60, 90),
            "energy": (60, 90),
            "danceability": (60, 90)
        }
    },
    "INTJ": {
        "descripcion": "Analítico, reservado, estratégico",
        "color": "#c2f0c2",
        "vino": "cabernet sauvignon",
        "musica": {
            "valence": (20, 50),
            "energy": (30, 60),
            "danceability": (30, 60)
        }
    },
    "ESFP": {
        "descripcion": "Alegre, impulsivo, enérgico",
        "color": "#ffcccc",
        "vino": "sparkling blend",
        "musica": {
            "valence": (70, 100),
            "energy": (70, 100),
            "danceability": (70, 100)
        }
    }
}

# --- SELECCIÓN DEL TIPO MBTI ---
st.image("https://i.imgur.com/dAZnUQO.png", width=300)
st.title("MBTI x Música x Vino")
st.caption("✨ Porque tu personalidad también suena... y sabe único 🍷🎶")

tipo = st.selectbox("Selecciona tu tipo de personalidad MBTI:", list(mbti_perfiles.keys()))
perfil = mbti_perfiles[tipo]

# --- PRESENTACIÓN DE PERFIL ---
st.markdown(f"""
    <div style='background-color:{perfil["color"]}; padding:20px; border-radius:12px;'>
        <h2 style='margin-bottom:10px;'>{tipo} — {perfil['descripcion']}</h2>
        <h4>🍷 Vino sugerido: <span style='color:#444;'>{perfil['vino'].title()}</span></h4>
    </div>
""", unsafe_allow_html=True)

# --- RECOMENDACIÓN MUSICAL ---
st.subheader("🎵 Canciones para tu mood")
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
        nombre = row['track_name']
        artista = row['artist(s)_name']
        st.markdown(f"- **{nombre}** — *{artista}*")
else:
    st.warning("No se encontraron canciones con esos valores.")

# --- RECOMENDACIÓN DE VINOS ---
st.subheader("🍷 Vinos que combinan contigo")

vino_variedad = perfil["vino"].lower().strip()
vinos_filtrados = wine_df[wine_df["variety"].str.contains(vino_variedad, na=False)]

if not vinos_filtrados.empty:
    top_vinos = vinos_filtrados.sort_values("points", ascending=False).head(3)
    for _, row in top_vinos.iterrows():
        titulo = row.get("title", "Vino sin título")
        puntos = row.get("points", "N/A")
        pais = row.get("country", "País desconocido")
        descripcion = row.get("description", "Sin descripción disponible.")
        st.markdown(f"### 🍇 {titulo}")
        st.markdown(f"**Puntuación:** ⭐ {puntos} &nbsp;&nbsp;&nbsp; 🌍 **Origen:** {pais}")
        st.caption(f"📝 *{descripcion}*")
        st.markdown("---")
else:
    st.warning("No se encontraron vinos para este tipo.")

# --- DESPEDIDA ---
st.markdown("#### *Hecho con 💛 por Angelina*")
st.success("¡Explora tu sabor y sonido interior! 🎧🍷")
