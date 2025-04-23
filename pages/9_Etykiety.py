import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Generator Etykiet", page_icon="🏷️")
st.title("🏷️ Generator etykiet na butelki")

# === Formularz danych ===
st.markdown("### ✏️ Wypełnij dane do etykiety")
nazwa = st.text_input("Nazwa wina:", "Jabłko-Malina")
typ = st.selectbox("Rodzaj wina:", ["Wino wytrawne", "Wino półwytrawne", "Wino półsłodkie", "Wino słodkie"], index=2)
data = st.text_input("Data butelkowania:", "01.2025")
alkohol = st.slider("Zawartość alkoholu (%)", 5, 20, 18)
pojemnosc = st.selectbox("Pojemność butelki:", ["750ML", "500ML", "1000ML", "2000ML"], index=0)
dolny_tekst = st.text_input("Dolny napis (np. NFC):", "NFC")

st.markdown("---")
st.markdown("### 🖨️ Podgląd etykiety")

# Wczytanie logo
try:
    logo = Image.open("assets/logo.png").convert("RGBA")
    logo = logo.resize((120, 120))  # większe logo
except Exception as e:
    st.error(f"Błąd wczytywania logo: {e}")
    st.stop()

# Tło
tlo = Image.new("RGB", (800, 500), "white")
draw = ImageDraw.Draw(tlo)

# Czcionki
font_path = "assets/DejaVuSans.ttf"
font_path_bold = "assets/DejaVuSans-Bold.ttf"
try:
    font_big = ImageFont.truetype(font_path_bold, 56)
    font_medium = ImageFont.truetype(font_path, 32)
    font_small = ImageFont.truetype(font_path, 24)
except Exception as e:
    st.error(f"Błąd wczytywania czcionki: {e}")
    st.stop()

# GORZELNIA i KOTŁOWNIA z liniami i logo w środku
draw.text((100, 30), "GORZELNIA", font=font_small, fill="black")
draw.text((550, 30), "KOTŁOWNIA", font=font_small, fill="black")
# Linie z lewej i prawej strony logo
draw.line((40, 90, 340, 90), fill="black", width=2)
draw.line((460, 90, 760, 90), fill="black", width=2)
# Logo pośrodku
tlo.paste(logo, (340, 30), logo)

# Nazwa wina i typ
text_nazwa = nazwa.upper()
text_typ = typ.upper()
width_nazwa = draw.textlength(text_nazwa, font=font_big)
width_typ = draw.textlength(text_typ, font=font_medium)
draw.text(((800 - width_nazwa) / 2, 180), text_nazwa, font=font_big, fill="black")
draw.text(((800 - width_typ) / 2, 270), text_typ, font=font_medium, fill="black")

# Data i linia
width_data = draw.textlength(data, font=font_small)
draw.text(((800 - width_data) / 2, 320), data, font=font_small, fill="black")
# Linia pod datą, nie na całą szerokość
draw.line((200, 350, 600, 350), fill="black", width=2)

# Dolne informacje
draw.text((140, 420), dolny_tekst, font=font_small, fill="black")
draw.text((360, 420), f"{alkohol}%", font=font_small, fill="black")
draw.text((580, 420), pojemnosc, font=font_small, fill="black")

# Podgląd
st.image(tlo, caption="Podgląd etykiety", use_container_width=True)

# Zapis
buf = io.BytesIO()
tlo.save(buf, format="PNG")
st.download_button("💾 Pobierz etykietę jako PNG", buf.getvalue(), file_name=f"etykieta_{nazwa}.png", mime="image/png")
