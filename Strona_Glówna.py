import streamlit as st
from PIL import Image
import base64
import io
import random
import json
import time
import os
from streamlit_extras.switch_page_button import switch_page

# === USTAWIENIA ===
INTRO_TIME = 3
CITATY = [
    "Winem nie naprawisz życia, ale możesz je chwilowo zbuforować.",
    "Dobre wino – złe decyzje.",
    "Kieliszek dziennie trzyma smutki z daleka!",
    "Wino nie zdradzi. Co najwyżej przewróci cię w kuchni.",
    "Czerwone? Białe? Ważne, żeby było. Reszta to szczegóły.",
    "Gdyby wino było walutą, już dawno byłbym milionerem.",
    "Czerwone na stres, białe na relaks, różowe na imprezę. Wino zna wszystkie odpowiedzi.",
    "Nie jestem alkoholikiem, tylko koneserem taniego wina.",
    "Wino nie pyta, wino rozumie.",
    "Nie jesteś tu przez przypadek. Wino też nie."
]

# === LOGO W TLE ===
def get_base64_logo_overlay(path, opacity=0.2):
    img = Image.open(path).convert("RGBA")
    img = Image.blend(Image.new("RGBA", img.size, (255,255,255,0)), img, opacity)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

logo_path = "assets/logo.png"
logo_base64 = get_base64_logo_overlay(logo_path)

# === CSS ===
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{logo_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: top center;
        font-family: 'Georgia', serif;
        color: #f2e8d5;
    }}
    h1, h4 {{ text-align: center; }}

    /* ZAMIANA TUTAJ 👇 */
    .stButton > button {{
        width: 120px;
        height: 60px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.08);  /* przezroczysty */
        color: #f2e8d5;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }}

    .wine-gallery {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }}
    .wine-card {{
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
    }}
    .note-box {{
        background-color: rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 2rem;
    }}
    </style>
""", unsafe_allow_html=True)


# === INTRO ===
if "intro_played" not in st.session_state:
    st.session_state.intro_played = True
    st.image("https://media.giphy.com/media/GyJ8p0Um850ic/giphy.gif", use_container_width=True)
    st.markdown(f"<h4>{random.choice(CITATY)}</h4>", unsafe_allow_html=True)
    time.sleep(INTRO_TIME)
    st.rerun()

# === TYTUŁ ===
st.markdown("<h1>🍷 Gorzelnia Kotłownia</h1>", unsafe_allow_html=True)
st.markdown("<h4>Witaj w domowej winiarni! 🍇</h4>", unsafe_allow_html=True)

# === MENU ===
nav = [
    ("📊 Kalkulator", "1_Kalkulator.py"),
    ("📖 Przepisy", "2_Przepisy.py"),
    ("🍯 Magazyn", "3_Magazyn.py"),
    ("📜 Historia", "4_Historia.py"),
    ("📏Przelicznik", "5_Przelicznik.py"),
    ("🍾 Butelki", "6_Butelki.py"),
    ("⚗️Kalkulator winiarski", "7_Kalkulator_winiarski.py"),
    ("💬 Opinie", "10_Opinie.py"),
    ("🖼️ Galeria", "11_Galeria.py"),
    ("📔 Notatki", "8_Notatki.py"),
    ("🏷️ Etykiety", "9_Etykiety.py"),
    ("🧪Wstawione", "12_Wstawione.py")
]

rows = [nav[i:i+6] for i in range(0, len(nav), 6)]
for row in rows:
    cols = st.columns(6)
    for col, (label, page) in zip(cols, row):
        with col:
            if st.button(label, key=label):
                st.switch_page(f"pages/{page}")

# === GALERIA WIN ===
if os.path.exists("data/magazyn.json"):
    with open("data/magazyn.json", encoding="utf-8") as f:
        magazyn = json.load(f)

    st.markdown("### 🍶 Dostępne wina w magazynie")

    for nazwa, dane in magazyn.items():
        img = dane.get("img", "")
        if img:
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(f"assets/{img}", width=120)
                with col2:
                    if st.button(nazwa, key=nazwa):
                        st.switch_page("pages/3_Magazyn.py")
                    st.markdown(f"📦 **{dane.get('ilosc', 0)} butelek**")
                    st.markdown(f"🍬 Styl: `{dane.get('smak', '-')}`")
                    st.markdown(f"💥 Alk: `{dane.get('alk', '-')}`")

# == Opinia tygodnia ==

# === Wczytaj dane ===
with open("data/opinie.json", "r", encoding="utf-8") as f:
    opinie_data = json.load(f)

with open("data/historia.json", "r", encoding="utf-8") as f:
    historia_data = json.load(f)

st.markdown("### 💬 Opinia tygodnia")
if opinie_data:
    opinia = random.choice(opinie_data)
    wino = opinia.get("wino", "Nieznane wino")
    komentarz = opinia.get("komentarz", "Brak komentarza")
    autor = opinia.get("autor", "anonim")
    st.info(f"🍇 **{wino}** – „{komentarz}” – _{autor}_")

# == Historia fermentacji ==
st.markdown("### 🕘 Ostatnie wydarzenia fermentacji")
historia_sorted = sorted(historia_data, key=lambda x: x.get("data", ""), reverse=True)[:3]
for e in historia_sorted:
    data = e.get("data", "brak daty")
    opis = e.get("opis", "brak opisu")
    st.write(f"📌 `{data}` – {opis}")


# === NOTATKA ===
import json
from datetime import datetime

st.markdown("### 🍃 Dodaj notatkę")

NOTATKI_FILE = "data/notatki.json"
os.makedirs("data", exist_ok=True)

# Wczytaj istniejące notatki
if os.path.exists(NOTATKI_FILE):
    with open(NOTATKI_FILE, "r") as f:
        notatki = json.load(f)
else:
    notatki = []

# Formularz
with st.form("notka"):
    tytul = st.text_input("Tytuł notatki")
    tresc = st.text_area("Treść notatki")
    submitted = st.form_submit_button("Zapisz notatkę")

    if submitted:
        if tytul and tresc:
            nowa = {
                "tytul": tytul,
                "tresc": tresc,
                "data": datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            notatki.append(nowa)
            with open(NOTATKI_FILE, "w", encoding="utf-8") as f:
                json.dump(notatki, f, indent=2, ensure_ascii=False)
            st.success("✅ Notatka została zapisana.")
        else:
            st.warning("⚠️ Wpisz zarówno tytuł, jak i treść.")

#MEMMMYYYY
st.markdown("## Kociołek prawdy")
st.caption("Trochę humoru z piwnicy – tak dla równowagi fermentacyjnej 🍷")

os.makedirs("uploaded_memes", exist_ok=True)
MEME_META_FILE = "data/memy.json"
os.makedirs("data", exist_ok=True)

# === Wczytaj opisy memów ===
if os.path.exists(MEME_META_FILE):
    with open(MEME_META_FILE, "r", encoding="utf-8") as f:
        memy = json.load(f)
else:
    memy = {}

# === Dodawanie mema (bez hasła) ===
with st.expander("➕ Dodaj własnego mema z cytatem"):
    uploaded = st.file_uploader("📸 Wybierz obrazek (meme)", type=["png", "jpg", "jpeg"])
    podpis = st.text_input("✍️ Śmieszny cytat do mema")

    if uploaded and podpis:
        file_path = os.path.join("uploaded_memes", uploaded.name)
        with open(file_path, "wb") as f:
            f.write(uploaded.read())
        memy[uploaded.name] = podpis
        with open(MEME_META_FILE, "w", encoding="utf-8") as f:
            json.dump(memy, f, indent=2, ensure_ascii=False)
        st.success("✅ Dodano mema z cytatem! Odśwież stronę by go zobaczyć.")
        st.experimental_rerun()

# === Pokaz memy ===
if memy:
    st.markdown("### 🎞️ Galeria memów z kotłowni")

    if "wybrany_mem" not in st.session_state:
        st.session_state["wybrany_mem"] = random.choice(list(memy.keys()))

    wybrane = st.selectbox("📂 Wybierz mem:", list(memy.keys()), index=list(memy.keys()).index(st.session_state["wybrany_mem"]))
    st.image(f"uploaded_memes/{wybrane}", caption=f"🍇 {memy[wybrane]}", use_container_width=True)

    # Usuwanie mema – z hasłem
    with st.expander("🗑️ Usuń ten mem"):
        haslo_usun = st.text_input("Podaj hasło do usunięcia:", type="password", key="usun_mema")
        if haslo_usun == "gorzelnia25":
            if st.button("❌ Potwierdź usunięcie"):
                os.remove(f"uploaded_memes/{wybrane}")
                memy.pop(wybrane)
                with open(MEME_META_FILE, "w", encoding="utf-8") as f:
                    json.dump(memy, f, indent=2, ensure_ascii=False)
                st.success("✅ Mem został usunięty.")
                st.experimental_rerun()
        elif haslo_usun:
            st.error("❌ Nieprawidłowe hasło.")
else:
    st.info("Brak memów. Dodaj pierwszy, by rozpocząć fermentację śmiechu 😄")

# === STOPKA ===
st.markdown("---")
st.markdown("<p style='text-align:center;'>© 2025 <b>PWNTRIX</b> – Wszystkie prawa zarezerwowane</p>", unsafe_allow_html=True)
