import streamlit as st
import os
import json
from PIL import Image
from datetime import date
import subprocess

# === ŚCIEŻKI I USTAWIENIA ===
GALERIA_DIR = "galeria"
GALERIA_META = "data/galeria.json"
HASLO_USUWANIA = "gorzelnia25"

os.makedirs(GALERIA_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# === Wczytaj metadane ===
if os.path.exists(GALERIA_META):
    with open(GALERIA_META, encoding="utf-8") as f:
        galeria = json.load(f)
else:
    galeria = []

# === CSS ===
st.markdown("""
    <style>
    .gallery-img {
        border-radius: 12px;
        max-width: 100%;
        margin-bottom: 0.5rem;
        box-shadow: 0 0 12px rgba(0,0,0,0.4);
    }
    .caption {
        text-align: center;
        font-style: italic;
        font-size: 0.9rem;
        color: #ccc;
        margin-bottom: 1rem;
    }
    .arrow-btn > button {
        font-size: 1.5rem !important;
        padding: 8px;
        width: 100%;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# === TYTUŁ ===
st.markdown("## 🖼️ Zdjęcia")

# === STAN: które zdjęcie aktualnie
if "galeria_index" not in st.session_state:
    st.session_state.galeria_index = 0

# === Galeria główna
if galeria:
    index = st.session_state.galeria_index
    index = max(0, min(index, len(galeria) - 1))
    zdjecie = galeria[index]
    plik = os.path.join(GALERIA_DIR, zdjecie["plik"])

    nav = st.columns([1, 6, 1])
    with nav[0]:
        if st.button("⬅️", key="prev") and index > 0:
            st.session_state.galeria_index -= 1
            st.experimental_rerun()
    with nav[2]:
        if st.button("➡️", key="next") and index < len(galeria) - 1:
            st.session_state.galeria_index += 1
            st.experimental_rerun()

    if os.path.exists(plik):
        st.image(plik, use_column_width=True, output_format="PNG", caption=None)
    else:
        st.warning("❌ Obrazek nie został znaleziony.")

    st.markdown(
        f"<div class='caption'>{zdjecie['tytul']} ({zdjecie['data']})</div>",
        unsafe_allow_html=True
    )

    # === Usuń zdjęcie
    with st.expander("🧹 Usuń to zdjęcie"):
        haslo = st.text_input("Podaj hasło", type="password")
        if haslo == HASLO_USUWANIA:
            if st.button("❌ Usuń zdjęcie permanentnie"):
                try:
                    os.remove(plik)
                except FileNotFoundError:
                    pass
                galeria.pop(index)
                with open(GALERIA_META, "w", encoding="utf-8") as f:
                    json.dump(galeria, f, indent=2, ensure_ascii=False)

                try:
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(["git", "commit", "-m", f"Usunięto zdjęcie {zdjecie['plik']}"], check=True)
                    subprocess.run(["git", "push"], check=True)
                    st.info("✅ Usunięcie zapisane w GitHubie.")
                except Exception as e:
                    st.warning(f"⚠️ Push nieudany: {e}")

                st.success("✅ Zdjęcie zostało usunięte.")
                st.session_state.galeria_index = max(0, index - 1)
                st.experimental_rerun()
        elif haslo:
            st.error("❌ Nieprawidłowe hasło.")
else:
    st.info("📭 Brak zdjęć w galerii.")

# === Dodaj nowe zdjęcie ===
with st.expander("➕ Dodaj nowe zdjęcie do galerii"):
    uploaded = st.file_uploader("📸 Wybierz zdjęcie", type=["png", "jpg", "jpeg"])
    tytul = st.text_input("📝 Tytuł zdjęcia", max_chars=40)
    data_zdjecia = st.date_input("📅 Data", value=date.today(), format="DD.MM.YYYY")

    if uploaded and tytul:
        filename = uploaded.name.replace(" ", "_")
        save_path = os.path.join(GALERIA_DIR, filename)

        # Zapisz plik
        with open(save_path, "wb") as f:
            f.write(uploaded.read())

        # Dodaj do listy
        galeria.append({
            "plik": filename,
            "tytul": tytul,
            "data": data_zdjecia.strftime("%d.%m.%Y")
        })

        # Zapisz JSON
        with open(GALERIA_META, "w", encoding="utf-8") as f:
            json.dump(galeria, f, indent=2, ensure_ascii=False)

        # Git push
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Dodano zdjęcie {filename}"], check=True)
            subprocess.run(["git", "push"], check=True)
            st.info("🚀 Zdjęcie zapisane w GitHubie.")
        except Exception as e:
            st.warning(f"⚠️ Push nieudany: {e}")

        st.success("✅ Zdjęcie zostało dodane.")
        st.experimental_rerun()

# === STOPKA ===
st.markdown("---")
st.markdown("<p style='text-align:center;'>© 2025 <b>PWNTRIX</b> – Gorzelnia Kotłownia</p>", unsafe_allow_html=True)
#działa?