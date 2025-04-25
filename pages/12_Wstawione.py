import streamlit as st
import json
import os
import subprocess
from datetime import datetime

st.set_page_config(page_title="Wstawione Wina", page_icon="🧪")
st.title("🧪 Dziennik wstawionych win")

FILE_PATH = "data/wstawione.json"
os.makedirs("data", exist_ok=True)

# === Wczytaj dane ===
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        wstawione = json.load(f)
else:
    wstawione = []

# === Zapis z automatycznym pushowaniem ===
def save_wstawione(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    try:
        subprocess.run(["git", "add", FILE_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "Aktualizacja wstawionych win"], check=True)
        subprocess.run(["git", "push"], check=True)
        st.info("🚀 Zmiany wysłane na GitHuba")
    except Exception as e:
        st.warning(f"⚠️ Nie udało się wykonać push: {e}")

# === Dodawanie nowego wina ===
st.subheader("➕ Dodaj nowe wino")
nazwa = st.text_input("🍇 Nazwa / Skład wina")
data = st.date_input("📅 Data wstawienia", value=datetime.today()).strftime("%d.%m.%Y")
alk = st.slider("💥 Planowana moc (%)", 8, 18, 14)
styl = st.selectbox("🍬 Styl wina", ["Słodkie", "Półsłodkie", "Wytrawne"])
drozdze = st.text_input("🧫 Użyte drożdże", value="Bayanus G995")
objetosc = st.number_input("📦 Objętość (L)", 1.0, 100.0, step=0.5)
status = st.selectbox("🟢 Status", ["Fermentuje", "Klaruje się", "Zabutelkowane"])
uwagi = st.text_area("📓 Dodatkowe uwagi")

if st.button("✅ Zapisz wino"):
    if nazwa:
        wstawione.append({
            "nazwa": nazwa,
            "data": data,
            "alk": alk,
            "styl": styl,
            "drozdze": drozdze,
            "objetosc": objetosc,
            "status": status,
            "uwagi": uwagi
        })
        save_wstawione(wstawione)
        st.success("🍷 Wino dodane do dziennika!")
        st.rerun()
    else:
        st.warning("⚠️ Podaj nazwę wina!")

# === Lista wstawionych win ===
st.markdown("---")
st.subheader("📜 Lista wstawionych win")

if wstawione:
    for i, w in reversed(list(enumerate(wstawione))):
        with st.expander(f"{w['nazwa']} ({w['data']}) - {w['status']}"):
            st.markdown(f"**Alkohol:** {w['alk']}%")
            st.markdown(f"**Styl:** {w['styl']}")
            st.markdown(f"**Drożdże:** {w['drozdze']}")
            st.markdown(f"**Objętość:** {w['objetosc']} L")
            st.markdown(f"**Uwagi:** {w['uwagi'] if w['uwagi'] else '-'}")

            if st.button(f"🗑️ Usuń ({w['nazwa']})", key=f"usun_{i}"):
                wstawione.pop(i)
                save_wstawione(wstawione)
                st.success("🗑️ Wpis usunięty")
                st.rerun()
else:
    st.info("Brak wstawionych win. Dodaj pierwszy wpis!")
