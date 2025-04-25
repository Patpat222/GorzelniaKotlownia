import streamlit as st
import os
import json
import subprocess

st.set_page_config(page_title="Magazyn Win", page_icon="🍾")
st.title("🍾 Magazyn Gorzelniany")
st.markdown("Tu śledzimy ile butelek jest jeszcze na stanie 🍇📦")

MAGAZYN_FILE = "data/magazyn.json"

def load_magazyn():
    if os.path.exists(MAGAZYN_FILE):
        with open(MAGAZYN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_magazyn(magazyn):
    with open(MAGAZYN_FILE, "w") as f:
        json.dump(magazyn, f, indent=2, ensure_ascii=False)
    try:
        subprocess.run(["git", "add", MAGAZYN_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Aktualizacja magazynu"], check=True)
        subprocess.run(["git", "push"], check=True)
        st.info("🚀 Zmiany zapisane w GitHubie")
    except Exception as e:
        st.warning(f"⚠️ Nie udało się wykonać push: {e}")

if "magazyn" not in st.session_state:
    st.session_state["magazyn"] = load_magazyn()

# === Dodawanie nowego wina ===
with st.expander("➕ Dodaj nowe wino do magazynu"):
    nazwa = st.text_input("🍷 Nazwa wina")
    img = st.text_input("🖼️ Nazwa pliku zdjęcia (np. moje_wino.jpg)")
    rocznik = st.text_input("📅 Rocznik (np. 12.2025)")
    alk = st.text_input("💥 Procent alkoholu (np. 14%)")
    ml = st.number_input("🧪 Objętość (ml)", min_value=100, max_value=2000, step=50, value=750)
    ilosc = st.number_input("📦 Ilość butelek", min_value=1, step=1)
    smak = st.selectbox("🍬 Styl wina", ["Słodkie", "Półsłodkie", "Wytrawne"])
    drozdze = st.text_input("🧫 Rodzaj drożdży (np. Bayanus)")

    if st.button("✅ Dodaj wino"):
        if nazwa and img:
            st.session_state["magazyn"][nazwa] = {
                "img": img, "rocznik": rocznik, "alk": alk,
                "ml": ml, "ilosc": ilosc, "smak": smak, "drozdze": drozdze
            }
            save_magazyn(st.session_state["magazyn"])
            st.success(f"🍾 Dodano: {nazwa}")
        else:
            st.warning("⚠️ Podaj przynajmniej nazwę i zdjęcie")

st.divider()

# === WIZUALNY MAGAZYN ===
for nazwa, dane in list(st.session_state["magazyn"].items()):
    with st.container():
        st.markdown(f"## {nazwa}")
        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.image(f"assets/{dane['img']}", use_container_width=True)

        with col2:
            st.markdown(f"📅 Rocznik: `{dane.get('rocznik', '-')}`")
            st.markdown(f"🍷 Alkohol: `{dane.get('alk', '-')}`")
            st.markdown(f"🧪 Objętość: `{dane.get('ml', '-')} ml`")
            st.markdown(f"🧫 Drożdże: `{dane.get('drozdze', '-')}`")
            st.markdown(f"🍬 Styl: `{dane.get('smak', '-')}`")
            st.markdown(f"📦 Na stanie: **{dane.get('ilosc', 0)} butelek**")

            if dane["ilosc"] == 1:
                st.warning("🟡 Ostatnia butelka!")
            elif dane["ilosc"] == 0:
                st.error("🔴 Brak w magazynie!")

            if st.button(f"➖ Wziąłem 1", key=f"{nazwa}_wez"):
                if dane["ilosc"] > 0:
                    dane["ilosc"] -= 1
                    save_magazyn(st.session_state["magazyn"])

            with st.expander("✏️ Edytuj / Usuń"):
                nowe_img = st.text_input(f"🖼️ Zdjęcie ({nazwa})", value=dane["img"], key=f"{nazwa}_img")
                nowe_rocznik = st.text_input(f"📅 Rocznik", value=dane["rocznik"], key=f"{nazwa}_roc")
                nowe_alk = st.text_input(f"💥 Alkohol", value=dane["alk"], key=f"{nazwa}_alk")
                nowe_ml = st.number_input(f"🧪 Objętość (ml)", value=dane["ml"], step=50, key=f"{nazwa}_ml")
                nowe_ilosc = st.number_input(f"📦 Ilość", value=dane["ilosc"], min_value=0, key=f"{nazwa}_ilosc")
                nowe_smak = st.selectbox(f"🍬 Styl", ["Słodkie", "Półsłodkie", "Wytrawne"], index=["Słodkie", "Półsłodkie", "Wytrawne"].index(dane["smak"]), key=f"{nazwa}_smak")
                nowe_drozdze = st.text_input(f"🧫 Drożdże", value=dane["drozdze"], key=f"{nazwa}_dro")

                if st.button(f"💾 Zapisz zmiany ({nazwa})"):
                    st.session_state["magazyn"][nazwa] = {
                        "img": nowe_img,
                        "rocznik": nowe_rocznik,
                        "alk": nowe_alk,
                        "ml": nowe_ml,
                        "ilosc": nowe_ilosc,
                        "smak": nowe_smak,
                        "drozdze": nowe_drozdze
                    }
                    save_magazyn(st.session_state["magazyn"])
                    st.success("✅ Zapisano zmiany!")

                if st.button(f"🗑️ Usuń {nazwa}", key=f"{nazwa}_usun"):
                    st.session_state["magazyn"].pop(nazwa)
                    save_magazyn(st.session_state["magazyn"])
                    st.warning(f"❌ Usunięto {nazwa}")
                    st.experimental_rerun()

    st.divider()
