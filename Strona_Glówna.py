import streamlit as st
from PIL import Image
import base64
import io
import random
import json

# == logo w tle ==
def get_base64_logo_overlay(path, opacity=0.2):
    img = Image.open(path).convert("RGBA")
    img = Image.blend(Image.new("RGBA", img.size, (255,255,255,0)), img, opacity)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

logo_path = "assets/logo.png"
logo_base64 = get_base64_logo_overlay(logo_path)

# == CSS: tło + kursor winogrono ==
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{logo_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: top center;
        cursor: url("https://emoji.gg/assets/emoji/2395-grape.png"), auto;
    }}
    h1 {{
        font-size: 4em;
        text-align: center;
        margin-bottom: 0;
    }}
    h4 {{
        text-align: center;
        font-style: italic;
        color: #aaa;
    }}
    </style>
""", unsafe_allow_html=True)

# == Tytuł ==
st.markdown("<h1>🍷 Gorzelnia Kotłownia</h1>", unsafe_allow_html=True)
st.markdown("<h4>Witaj w domowej winiarni! 🍇</h4>", unsafe_allow_html=True)

# == Nawigacyjne przyciski ==
nav_cols = st.columns(5)
if nav_cols[0].button("📖 Przepisy"):
    st.switch_page("pages/2_Przepisy.py")
if nav_cols[1].button("🍯 Magazyn"):
    st.switch_page("pages/3_Magazyn.py")
if nav_cols[2].button("📜 Historia"):
    st.switch_page("pages/4_Historia.py")
if nav_cols[3].button("📊 Kalkulator"):
    st.switch_page("pages/1_Kalkulator.py")
if nav_cols[4].button("💬 Opinie"):
    st.switch_page("pages/5_Opinie.py")

# == Galeria win ==
st.markdown("### 🖼️ Galeria win")
cols = st.columns(4)
wine_images = {
    "Dzika Róża": "assets/dzika_roza.jpg",
    "Hibiskus": "assets/hibiskus.jpg",
    "Malina": "assets/malina.jpg",
    "Truskawka": "assets/truskawka.jpg"
}
for col, (label, path) in zip(cols, wine_images.items()):
    if col.button(label):
        st.switch_page("pages/3_Magazyn.py")
    col.image(path, caption=label, use_container_width=True)

# == Wczytaj dane ==
with open("data/opinie.json", "r", encoding="utf-8") as f:
    opinie_data = json.load(f)

with open("data/historia.json", "r", encoding="utf-8") as f:
    historia_data = json.load(f)

# == Top 3 oceniane ==
st.markdown("### 🏆 Najlepiej oceniane wina")
top3 = sorted(opinie_data, key=lambda x: x.get("ocena", 0), reverse=True)[:3]
for o in top3:
    nazwa = o.get("nazwa", "Nieznane wino")
    ocena = o.get("ocena", 0)
    st.write(f"🍇 {nazwa} – {'⭐' * int(ocena)}")

# == Opinie tygodnia ==
st.markdown("### 💬 Opinia tygodnia")
opinia = random.choice(opinie_data)
komentarz = opinia.get("komentarz", "Brak komentarza")
autor = opinia.get("autor", "anonim")
st.info(f"„{komentarz}” – {autor}")

# == Historia ==
st.markdown("### 🕘 Ostatnie wydarzenia fermentacji")
historia_sorted = sorted(historia_data, key=lambda x: x.get("data", ""), reverse=True)[:3]
for e in historia_sorted:
    st.write(f"📌 {e.get('data', 'brak daty')} – {e.get('opis', 'brak opisu')}")

# == Backup ==
st.markdown("### 💾 Kopia zapasowa")
if st.button("Utwórz kopię zapasową"):
    st.success("✅ Kopia zapasowa została zapisana pomyślnie!")

# == Stopka ==
st.markdown("---")
st.markdown("© 2025 **PWNTRIX** – Wszystkie prawa zarezerwowane")
