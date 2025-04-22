import streamlit as st
import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Rejestracja czcionki z polskimi znakami
pdfmetrics.registerFont(TTFont("DejaVu", "assets/DejaVuSans.ttf"))

st.set_page_config(page_title="Przepisy", page_icon="📒")
st.title("📒 Przepisy na wina domowe")

PRZEPISY_FILE = "data/przepisy.json"
PDF_DIR = "data/pdf"
os.makedirs(PDF_DIR, exist_ok=True)

def load_przepisy():
    if os.path.exists(PRZEPISY_FILE):
        with open(PRZEPISY_FILE, "r") as f:
            return json.load(f)
    return []

def save_przepisy(lista):
    with open(PRZEPISY_FILE, "w") as f:
        json.dump(lista, f, indent=2)

def generuj_pdf(przepis):
    filename = f"{PDF_DIR}/{przepis['nazwa'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("DejaVu", 16)
    c.drawString(50, y, przepis["nazwa"])
    y -= 30

    c.setFont("DejaVu", 12)
    c.drawString(50, y, f"🍬 Styl: {przepis.get('styl', '-')}")
    y -= 20
    c.drawString(50, y, f"🍇 Kolor: {przepis.get('kolor', '-')}")
    y -= 30

    c.setFont("DejaVu", 13)
    c.drawString(50, y, "📋 Składniki:")
    y -= 20
    c.setFont("DejaVu", 11)
    for s in przepis["skladniki"]:
        c.drawString(60, y, f"- {s}")
        y -= 15
        if y < 100:
            c.showPage()
            c.setFont("DejaVu", 11)
            y = height - 50

    y -= 20
    c.setFont("DejaVu", 13)
    c.drawString(50, y, "🧪 Przygotowanie:")
    y -= 20
    c.setFont("DejaVu", 11)
    for line in przepis["przygotowanie"].split("\n"):
        c.drawString(60, y, line)
        y -= 15
        if y < 100:
            c.showPage()
            c.setFont("DejaVu", 11)
            y = height - 50

    c.save()
    return filename

if "przepisy" not in st.session_state:
    st.session_state["przepisy"] = load_przepisy()

# === Dodawanie nowego przepisu ===
with st.expander("➕ Dodaj nowy przepis"):
    nazwa = st.text_input("🍷 Nazwa przepisu")
    skladniki = st.text_area("📋 Składniki (każdy w nowej linii)")
    przygotowanie = st.text_area("🧪 Sposób przygotowania")
    styl = st.selectbox("🍬 Styl wina", ["Słodkie", "Półsłodkie", "Wytrawne"])
    kolor = st.selectbox("🍇 Kolor wina", ["Czerwone", "Białe", "Różowe"])
    zdjecie = st.text_input("🖼️ Nazwa pliku zdjęcia (opcjonalnie)")

    if st.button("✅ Dodaj przepis"):
        if nazwa and skladniki and przygotowanie:
            nowy = {
                "nazwa": nazwa,
                "skladniki": skladniki.strip().split("\n"),
                "przygotowanie": przygotowanie,
                "styl": styl,
                "kolor": kolor,
                "zdjecie": zdjecie.strip()
            }
            st.session_state["przepisy"].append(nowy)
            save_przepisy(st.session_state["przepisy"])
            st.success("✅ Przepis dodany!")
        else:
            st.warning("⚠️ Uzupełnij wszystkie pola oprócz zdjęcia.")

st.markdown("---")

# === Filtry ===
st.markdown("### 🔍 Filtruj przepisy")

filtr_styl = st.selectbox("🍬 Styl wina", ["Wszystkie", "Słodkie", "Półsłodkie", "Wytrawne"])
filtr_kolor = st.selectbox("🍇 Kolor wina", ["Wszystkie", "Czerwone", "Białe", "Różowe"])

def pasuje(przepis):
    if filtr_styl != "Wszystkie" and przepis.get("styl") != filtr_styl:
        return False
    if filtr_kolor != "Wszystkie" and przepis.get("kolor") != filtr_kolor:
        return False
    return True

# === Lista przepisów ===
przepisy_do_wyswietlenia = [p for p in st.session_state["przepisy"] if pasuje(p)]

if przepisy_do_wyswietlenia:
    for i, przepis in enumerate(przepisy_do_wyswietlenia):
        st.subheader(f"📖 {przepis['nazwa']}")

        if przepis.get("zdjecie"):
            st.image(f"assets/{przepis['zdjecie']}", width=300)

        st.markdown("**📋 Składniki:**")
        for s in przepis["skladniki"]:
            st.markdown(f"- {s}")
        st.markdown("**🧪 Przygotowanie:**")
        st.markdown(przepis["przygotowanie"])
        st.markdown(f"**🍬 Styl:** {przepis.get('styl', '-')}")
        st.markdown(f"**🍇 Kolor:** {przepis.get('kolor', '-')}")

        # 📥 PDF
        if st.button(f"📥 Pobierz jako PDF", key=f"pdf_{i}"):
            pdf_path = generuj_pdf(przepis)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Pobierz PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

        # ✏️ Edycja w expanderze
        with st.expander("✏️ Edytuj przepis"):
            e_nazwa = st.text_input("🍷 Nazwa", value=przepis["nazwa"], key=f"nazwa_{i}")
            e_skladniki = st.text_area("📋 Składniki", value="\n".join(przepis["skladniki"]), key=f"skl_{i}")
            e_przygotowanie = st.text_area("🧪 Przygotowanie", value=przepis["przygotowanie"], key=f"prep_{i}")
            e_styl = st.selectbox("🍬 Styl", ["Słodkie", "Półsłodkie", "Wytrawne"],
                                  index=["Słodkie", "Półsłodkie", "Wytrawne"].index(przepis.get("styl", "Półsłodkie")),
                                  key=f"styl_{i}")
            e_kolor = st.selectbox("🍇 Kolor", ["Czerwone", "Białe", "Różowe"],
                                   index=["Czerwone", "Białe", "Różowe"].index(przepis.get("kolor", "Czerwone")),
                                   key=f"kolor_{i}")
            e_zdjecie = st.text_input("🖼️ Zdjęcie", value=przepis.get("zdjecie", ""), key=f"img_{i}")

            col_edit, col_del = st.columns(2)
            with col_edit:
                if st.button("💾 Zapisz zmiany", key=f"zapisz_{i}"):
                    idx = st.session_state["przepisy"].index(przepis)
                    st.session_state["przepisy"][idx] = {
                        "nazwa": e_nazwa,
                        "skladniki": e_skladniki.strip().split("\n"),
                        "przygotowanie": e_przygotowanie,
                        "styl": e_styl,
                        "kolor": e_kolor,
                        "zdjecie": e_zdjecie.strip()
                    }
                    save_przepisy(st.session_state["przepisy"])
                    st.success("✅ Przepis zaktualizowany!")
                    st.experimental_rerun()

            with col_del:
                if st.button("🗑️ Usuń przepis", key=f"usun_{i}"):
                    st.session_state["przepisy"].remove(przepis)
                    save_przepisy(st.session_state["przepisy"])
                    st.warning("❌ Przepis usunięty.")
                    st.experimental_rerun()
else:
    st.info("Brak pasujących przepisów. Spróbuj innego filtra lub dodaj pierwszy!")
