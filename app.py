with st.container():
    # --- PESTAÑA “Tu Mood Ideal” ---
    tabs = st.tabs(T["tabs_main"][lang])

    with tabs[0]:
        subtabs = st.tabs(T["subtabs_mood"][lang])

        # 🎧 Recomendaciones
        with subtabs[0]:
            st.header(T["labels"][lang]["song_rec"])
            mbti = st.selectbox(T["labels"][lang]["mbti_select"], list(mbti_profiles.keys()), key="mbti1")
            profile = mbti_profiles[mbti]
            wine = profile["wine"]
            desc = profile["description"][lang]

            st.markdown(f"""
                <div style='background-color:{profile["color"]}; padding:15px; border-radius:10px'>
                    <h2>{mbti} — {desc}</h2>
                    <h4>{T['labels'][lang]['ideal_wine']} <i>{wine}</i></h4>
                </div>
            """, unsafe_allow_html=True)

            st.subheader(T["labels"][lang]["song_rec"])
            canciones = spotify_df[(spotify_df["valence_%"] >= 50) & (spotify_df["energy_%"] >= 50)].sample(3)
            for _, row in canciones.iterrows():
                st.markdown(f"- **{row['track_name']}** — *{row['artist(s)_name']}*")

            st.subheader(T["labels"][lang]["wine_rec"])
            vinos_filtrados = wine_df[wine_df["variety"].fillna("").str.contains(wine, case=False)]
            if vinos_filtrados.empty:
                st.warning(T["labels"][lang]["no_wines"])
            else:
                for _, row in vinos_filtrados.head(3).iterrows():
                    titulo = row.get("title", "Vino")
                    puntos = row.get("points", "N/A")
                    pais = row.get("country", "País desconocido")
                    descripcion = row.get("description", "Sin descripción.")
                    st.markdown(f"**{titulo}** — ⭐ {puntos} — {pais}")
                    st.caption(f"*{descripcion}*")

        # 🚀 Interactivo
        with subtabs[1]:
            st.header("🚀 Explora tu mood musical y vinícola")
            tipo = st.selectbox("1️⃣ ¿Cuál es tu tipo de personalidad MBTI?", list(mbti_profiles.keys()), key="mbti2")
            perfil = mbti_profiles[tipo]
            vino = perfil["wine"]

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

            # Mostrar vinos sugeridos también aquí
            st.subheader(T["labels"][lang]["wine_rec"])
            vinos_filtrados = wine_df[wine_df["variety"].fillna("").str.contains(vino, case=False)]
            if vinos_filtrados.empty:
                st.warning(T["labels"][lang]["no_wines"])
            else:
                for _, row in vinos_filtrados.head(3).iterrows():
                    titulo = row.get("title", "Vino")
                    puntos = row.get("points", "N/A")
                    pais = row.get("country", "País desconocido")
                    descripcion = row.get("description", "Sin descripción.")
                    st.markdown(f"**{titulo}** — ⭐ {puntos} — {pais}")
                    st.caption(f"*{descripcion}*")
