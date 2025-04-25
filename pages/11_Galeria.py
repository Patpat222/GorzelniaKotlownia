import streamlit as st
import os
import json
from datetime import date
from PIL import Image
import subprocess

st.set_page_config(page_title="Galeria", page_icon="📸")
st.title("📸 Galeria")

FOLDER = "data/zdjecia"
BAZA = "data/galeria.json"
os.makedirs(FOLDER, exist_ok=True)

# === Wczytywanie bazy ===
if os.path.exists(BAZA):
    with open(BAZA, "r") as f:
        galeria = json.load(f)
else:
    galeria = []

# === Funkcja do pushowania do Git ===
def push_to_github(file_path, message):
    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        st.info("🚀 Galeria zaktualizowana w repozytorium GitHub!")
    except Exception as e:
        st.warning(f"⚠️ Nie udało się wykonać push: {e}")

# === Formularz dodawania ===
st.markdown("### ➕ Dodaj nowe zdjęcie")
with st.form("dodaj_zdjecie"):
    zdjecie = st.file_uploader("Wybierz zdjęcie wina", type=["jpg", "jpeg", "png"])
    opis = st.text_input("Opis lub nazwa partii")
    data_zdjecia = st.date_input("Data zdjęcia", value=date.today())
    dodaj = st.form_submit_button("📤 Dodaj do galerii")

    if dodaj and zdjecie:
        nazwa_pliku = zdjecie.name.replace(" ", "_")
        sciezka = os.path.join(FOLDER, nazwa_pliku)
        with open(sciezka, "wb") as f:
            f.write(zdjecie.getbuffer())

        galeria.append({
            "plik": nazwa_pliku,
            "opis": opis,
            "data": data_zdjecia.strftime("%d.%m.%Y")
        })
        with open(BAZA, "w") as f:
            json.dump(galeria, f, indent=2)

        push_to_github(BAZA, f"Dodano zdjęcie: {opis}")
        st.success("✅ Zdjęcie dodane do galerii!")

# === Filtrowanie ===
st.markdown("---")
st.subheader("🔍 Filtruj zdjęcia")

unikalne_opisy = sorted(set([x["opis"] for x in galeria if x["opis"]]))
wybor_opisu = st.selectbox("📌 Wybierz nazwę partii (lub zostaw puste):", ["Wszystkie"] + unikalne_opisy)

filtruj_data = st.date_input("📅 Pokaż zdjęcia od tej daty:", value=None)

filtered = galeria
if wybor_opisu != "Wszystkie":
    filtered = [x for x in filtered if x["opis"] == wybor_opisu]

if filtruj_data:
    filtruj_data_str = filtruj_data.strftime("%d.%m.%Y")
    filtered = [x for x in filtered if x["data"] >= filtruj_data_str]

# === Wyświetlanie ===
st.markdown("---")
st.subheader("🖼️ Zdjęcia")

if filtered:
    obrazy = []
    for item in reversed(filtered):
        sciezka = os.path.join(FOLDER, item["plik"])
        if os.path.exists(sciezka):
            obrazy.append((sciezka, f"{item['opis']} ({item['data']})", item["plik"]))

    if obrazy:
        if "current_slide" not in st.session_state:
            st.session_state.current_slide = 0

        col1, col2, col3 = st.columns([1, 6, 1])

        with col1:
            if st.button("⬅️"):
                st.session_state.current_slide = max(0, st.session_state.current_slide - 1)

        with col3:
            if st.button("➡️"):
                st.session_state.current_slide = min(len(obrazy) - 1, st.session_state.current_slide + 1)

        current = st.session_state.current_slide
        sciezka, podpis, plik = obrazy[current]
        st.image(sciezka, caption=podpis, use_container_width=True)

        with st.expander("🧹 Usuń to zdjęcie"):
            haslo = st.text_input("Podaj hasło, aby usunąć zdjęcie", type="password")
            if st.button("❌ Usuń zdjęcie"):
                if haslo == "gorzelnia25":
                    galeria = [x for x in galeria if x["plik"] != plik]
                    with open(BAZA, "w") as f:
                        json.dump(galeria, f, indent=2)
                    os.remove(os.path.join(FOLDER, plik))
                    push_to_github(BAZA, f"Usunięto zdjęcie: {plik}")
                    st.success("🗑️ Zdjęcie zostało usunięte")
                    st.session_state.current_slide = 0
                    st.rerun()
                else:
                    st.error("❌ Niepoprawne hasło")
else:
    st.info("Brak zdjęć do wyświetlenia w wybranym zakresie.")
