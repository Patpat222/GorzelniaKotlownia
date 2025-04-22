import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import os

st.set_page_config(page_title="Opinie o winach", page_icon="💬")

st.title("💬 Opinie o winach")
st.markdown("Zostaw swoją recenzję lub zobacz co myślą inni 🍷")

OPINIE_FILE = "data/opinie.json"
MAGAZYN_FILE = "data/magazyn.json"

# === ZAPIS / ODCZYT ===
def load_opinie():
    if os.path.exists(OPINIE_FILE):
        with open(OPINIE_FILE, "r") as f:
            return json.load(f)
    return []

def save_opinie(lista):
    with open(OPINIE_FILE, "w") as f:
        json.dump(lista, f, indent=2)

# === AUTOMATYCZNE WCZYTANIE MAGAZYNU, JEŚLI NIE ISTNIEJE W SESJI ===
if "magazyn" not in st.session_state:
    if os.path.exists(MAGAZYN_FILE):
        with open(MAGAZYN_FILE, "r") as f:
            st.session_state["magazyn"] = json.load(f)
    else:
        st.warning("Brak pliku magazyn.json – nie można dodać opinii.")
        st.stop()

# 📋 Lista win do wyboru
wina = list(st.session_state["magazyn"].keys())

# 📝 Opinie
if "opinie" not in st.session_state:
    st.session_state["opinie"] = load_opinie()

# === Formularz opinii ===
st.subheader("➕ Dodaj opinię")

col1, col2 = st.columns([2, 1])
with col1:
    wybrane_wino = st.selectbox("🍷 Wybierz wino:", wina)
    komentarz = st.text_area("✍️ Twoja opinia")
    imie = st.text_input("👤 Twoje imię lub pseudonim")

with col2:
    ocena = st.slider("⭐ Ocena", 1, 5, 4)
    st.markdown(f"**{ocena} / 5 gwiazdek**")

if st.button("✅ Dodaj opinię"):
    if wybrane_wino and imie and komentarz:
        nowa_opinia = {
            "wino": wybrane_wino,
            "ocena": ocena,
            "komentarz": komentarz,
            "autor": imie
        }
        st.session_state["opinie"].append(nowa_opinia)
        save_opinie(st.session_state["opinie"])
        st.success("✅ Opinia dodana!")
    else:
        st.warning("⚠️ Wypełnij wszystkie pola!")

st.markdown("---")

# === Wyświetlanie opinii ===
st.subheader("📚 Opinie użytkowników")

opinie_do_pokazania = st.session_state["opinie"]

if not opinie_do_pokazania:
    st.info("Brak jeszcze żadnych opinii – bądź pierwsza/y!")
else:
    for op in reversed(opinie_do_pokazania):
        st.markdown(f"""
        ### {op['wino']}  
        ⭐ **{op['ocena']} / 5**  
        ✍️ _{op['komentarz']}_  
        👤 _{op['autor']}_
        ---
        """)

# === ŚREDNIE OCENY I WYKRES ===
if opinie_do_pokazania:
    st.markdown("## 🏆 Top 3 najlepiej oceniane wina")

    suma = defaultdict(int)
    liczba = defaultdict(int)

    for op in opinie_do_pokazania:
        suma[op["wino"]] += op["ocena"]
        liczba[op["wino"]] += 1

    srednie = {w: round(suma[w] / liczba[w], 2) for w in suma}
    top3 = sorted(srednie.items(), key=lambda x: x[1], reverse=True)[:3]

    if top3:
        wina_top = [w[0] for w in top3]
        oceny_top = [w[1] for w in top3]

        fig, ax = plt.subplots()
        bars = ax.bar(wina_top, oceny_top, color="darkgreen")
        ax.set_ylim(0, 5)
        ax.set_ylabel("Średnia ocena")
        ax.set_title("Top 3 najlepiej oceniane wina")

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5), textcoords="offset points", ha='center', va='bottom')

        fig.tight_layout()
        st.pyplot(fig)
