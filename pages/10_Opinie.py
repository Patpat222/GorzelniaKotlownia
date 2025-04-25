import streamlit as st
import json
import os
import matplotlib.pyplot as plt
from collections import defaultdict

OPINIE_FILE = "data/opinie.json"
os.makedirs("data", exist_ok=True)

# === Wczytaj opinie ===
if os.path.exists(OPINIE_FILE):
    with open(OPINIE_FILE, "r", encoding="utf-8") as f:
        opinie = json.load(f)
else:
    opinie = []

# === Dodawanie nowej opinii ===
st.subheader("➕ Dodaj opinię")

wino = st.text_input("🍷 Nazwa wina")
autor = st.text_input("👤 Twoje imię / pseudonim")
ocena = st.slider("⭐ Ocena", 1, 5, 4)
komentarz = st.text_area("✍️ Komentarz")

if st.button("✅ Zapisz opinię"):
    if wino and autor and komentarz:
        opinie.append({
            "wino": wino,
            "autor": autor,
            "ocena": ocena,
            "komentarz": komentarz,
            "odpowiedzi": []
        })
        with open(OPINIE_FILE, "w", encoding="utf-8") as f:
            json.dump(opinie, f, indent=2, ensure_ascii=False)
        st.success("✅ Opinia zapisana!")
        st.rerun()
    else:
        st.warning("⚠️ Uzupełnij wszystkie pola")

# === Hasło do moderacji ===
st.markdown("---")
st.subheader("📚 Opinie użytkowników")
haslo_dostepu = st.text_input("🔐 Wpisz hasło, aby mieć dostęp do usuwania", type="password")

# === Wyświetlanie opinii ===
for i, opinia in reversed(list(enumerate(opinie))):
    st.markdown(f"### 🍇 {opinia['wino']}")
    st.markdown(f"⭐ {opinia['ocena']} / 5")
    st.markdown(f"✍️ {opinia['komentarz']} — _{opinia['autor']}_")

    # Odpowiedzi
    if opinia.get("odpowiedzi"):
        for odp in opinia["odpowiedzi"]:
            st.markdown(f"🔁 _{odp['autor']}_: {odp['tresc']}")

    with st.expander(f"💬 Odpowiedz na tę opinię"):
        odp_autor = st.text_input(f"🖊️ Twoje imię lub pseudonim (opinia {i})", key=f"odp_autor_{i}")
        odpowiedz = st.text_area(f"✍️ Twoja odpowiedź", key=f"odp_tresc_{i}")
        if st.button(f"📩 Dodaj odpowiedź ({i})"):
            if odp_autor and odpowiedz:
                opinia.setdefault("odpowiedzi", []).append({"autor": odp_autor, "tresc": odpowiedz})
                with open(OPINIE_FILE, "w", encoding="utf-8") as f:
                    json.dump(opinie, f, indent=2, ensure_ascii=False)
                st.success("📬 Odpowiedź dodana!")
                st.rerun()
            else:
                st.warning("⚠️ Podaj imię i treść odpowiedzi")

    # Usuwanie z hasłem
    if haslo_dostepu == "gorzelnia25":
        if st.button(f"🗑️ Usuń opinię ({i})", key=f"usun_op_{i}"):
            opinie.pop(i)
            with open(OPINIE_FILE, "w", encoding="utf-8") as f:
                json.dump(opinie, f, indent=2, ensure_ascii=False)
            st.success("🗑️ Opinia usunięta")
            st.rerun()

# === Wykres ocen ===
srednie = defaultdict(list)
for o in opinie:
    srednie[o["wino"]].append(o["ocena"])

srednie_oceny = {k: round(sum(v)/len(v), 2) for k, v in srednie.items()}

if srednie_oceny:
    st.subheader("📊 Średnia ocena win")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(srednie_oceny.keys(), srednie_oceny.values(), color="orange")
    ax.set_ylabel("Ocena")
    ax.set_ylim(0, 5)
    ax.set_xticklabels(srednie_oceny.keys(), rotation=30, ha="right")
    st.pyplot(fig)
else:
    st.info("Brak ocen do wyświetlenia.")
from utils.git_sync import push_to_github

# ... po zapisaniu danych
st.success("✅ Opinia została zapisana.")
st.info(push_to_github("🗣️ Dodano opinię przez użytkownika"))
