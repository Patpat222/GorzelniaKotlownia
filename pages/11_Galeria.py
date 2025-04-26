import streamlit as st
import os
import json
from PIL import Image
from datetime import date, datetime
import subprocess

# === USTAWIENIA ===
GALERIA_DIR = "galeria"
GALERIA_META = "data/galeria.json"
HASLO_USUWANIA = "gorzelnia25"

os.makedirs(GALERIA_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# === WCZYTYWANIE ZDJĘĆ ===
if os.path.exists(GALERIA_META):
    with open(GALERIA_META, encoding="utf-8") as f:
        galeria = json.load(f)
else:
    galeria = []

# === SORTOWANIE PO DACIE (najświeższe najpierw) ===
def parse_date(entry):
    try:
        return datetime.strptime(entry.get("data", "01.01.1970"), "%d.%m.%Y")
    except:
        return datetime(1970, 1, 1)

galeria.sort(key=parse_date, reverse=True)

# === STAN: index aktywnego zdjęcia ===
if "galeria_index" not in st.session_state:
    st.session_state.galeria_index = 0

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
        font-size: 0.95rem;
        color: #ddd;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    .arrow-btn > button {
        font-size: 2rem !important;
        width: 100%;
        height: 100%;
        padding: 0.25rem;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# === TYTUŁ ===
st.markdown("## 🌞 Galeria Zdjęć")

# === WYŚWIETLANIE ===
if galeria:
    index = st.session_state.galeria_index
    index = max(0, min(index, len(galeria) - 1))
    zdjecie = galeria[index]
    plik = os.path.join(GALERIA_DIR, zdjecie["plik"])

    nav = st.columns([1, 6, 1])
    with nav[0]:
        if st.button("⬅️", key="prev") and index > 0:
            st.session_state.galeria_index -= 1
            st.rerun()
    with nav[2]:
        if st.button("➡️", key="next") and index < len(galeria) - 1:
            st.session_state.galeria_index += 1
            st.rerun()

    if os.path.exists(plik):
        st.image(plik, use_container_width=True, output_format="PNG")
    else:
        st.warning("❌ Obrazek nie został znaleziony.")

    st.markdown(
        f"<div class='caption'>{zdjecie.get('tytul', 'Bez tytułu')} ({zdjecie.get('data', 'brak daty')})</div>",
        unsafe_allow_html=True
    )

    # === USUWANIE ===
    with st.expander("🧹 Usuń to zdjęcie"):
        haslo = st.text_input("Podaj hasło", type="password")
        if haslo == HASLO_USUWANIA:
            if st.button("❌ Potwierdź usunięcie"):
                try:
                    os.remove(plik)
                except FileNotFoundError:
                    pass
                galeria.pop(index)
                with open(GALERIA_META, "w", encoding="utf-8") as f:
                    json.dump(galeria, f, indent=2, ensure_ascii=False)

                try:
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(["git", "commit", "-m", f"Usunięto zdjęcie {zdjecie['plik']}", "--allow-empty"], check=True)
                    subprocess.run(["git", "push"], check=True)
                except Exception as e:
                    st.warning(f"⚠️ Push nieudany: {e}")

                st.success("✅ Zdjęcie zostało usunięte.")
                st.session_state.galeria_index = max(0, index - 1)
                st.rerun()
        elif haslo:
            st.error("❌ Nieprawidłowe hasło.")
else:
    st.info("📅 Brak zdjęć w galerii.")

# === DODAWANIE ===
with st.expander("➕ Dodaj nowe zdjęcie"):
    uploaded = st.file_uploader("📸 Wybierz zdjęcie", type=["png", "jpg", "jpeg"])
    tytul = st.text_input("📄 Tytuł zdjęcia", max_chars=50)
    data_zdjecia = st.date_input("📅 Data zdjęcia", value=date.today(), format="DD.MM.YYYY")

    if uploaded and tytul:
        filename = uploaded.name.replace(" ", "_")
        save_path = os.path.join(GALERIA_DIR, filename)

        # zapisz zdjęcie
        with open(save_path, "wb") as f:
            f.write(uploaded.read())

        galeria.append({
            "plik": filename,
            "tytul": tytul,
            "data": data_zdjecia.strftime("%d.%m.%Y")
        })

        with open(GALERIA_META, "w", encoding="utf-8") as f:
            json.dump(galeria, f, indent=2, ensure_ascii=False)

        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Dodano zdjęcie {filename}", "--allow-empty"], check=True)
            subprocess.run(["git", "push"], check=True)
            st.info("🚀 Zdjęcie zapisane w repozytorium GitHub.")
        except Exception as e:
            st.warning(f"⚠️ Push nieudany: {e}")

        st.success("✅ Zdjęcie zostało dodane!")
        st.rerun()

# === STOPKA ===
st.markdown("---")
st.markdown("<p style='text-align:center;'>© 2025 <b>PWNTRIX</b> – Gorzelnia Kotłownia</p>", unsafe_allow_html=True)