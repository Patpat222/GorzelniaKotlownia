import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Kącik notatek winiarza", page_icon="📓")
st.title(" 📓 Kącik notatek winiarza")

NOTATKI_FILE = "data/notatki.json"
os.makedirs("data", exist_ok=True)

# —— Wczytaj notatki ——
if os.path.exists(NOTATKI_FILE):
    with open(NOTATKI_FILE, "r") as f:
        notatki = json.load(f)
else:
    notatki = []

# —— Formularz dodawania ——
st.subheader("➕ Dodaj nową notatkę")
tytul = st.text_input("Tytuł notatki")
tresc = st.text_area("Treść notatki")
data = datetime.now().strftime("%d.%m.%Y %H:%M")

if st.button("✍️ Zapisz notatkę"):
    if tytul and tresc:
        notatki.append({"tytul": tytul, "tresc": tresc, "data": data})
        with open(NOTATKI_FILE, "w") as f:
            json.dump(notatki, f, indent=2)
        st.success("✅ Notatka zapisana!")
        st.rerun()
    else:
        st.warning("⚠️ Uzupełnij tytuł i treść notatki")

# —— Lista notatek ——
st.markdown("---")
st.subheader("📂 Twoje notatki")

if notatki:
    for i, n in reversed(list(enumerate(notatki))):
        with st.expander(f"{n['tytul']} ({n['data']})"):
            st.write(n["tresc"])
            if st.button("🔍 Usuń", key=f"usun_{i}"):
                notatki.pop(i)
                with open(NOTATKI_FILE, "w") as f:
                    json.dump(notatki, f, indent=2)
                st.success("🗑️ Notatka usunięta")
                st.rerun()
else:
    st.info("Brak notatek. Czas coś zapisać! 🍷")
