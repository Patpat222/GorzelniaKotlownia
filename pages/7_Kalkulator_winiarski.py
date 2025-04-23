import streamlit as st
import math

st.set_page_config(page_title="Kalkulator winiarski", page_icon="🍷")
st.title("Kalkulator winiarski")

st.markdown("""
## 🍇 Chcesz zrobić wino w domu, ale nie wiesz jak?\n
Nasz kalkulator to jak pomocnik z winnicy – tylko nie narzeka i nie pije zapasów.\n
Wybierz owoce, podaj ile litrów i jaki procent – reszta zrobi się niemal sama.\n
Czekaj na fermentacyjne czary-mary i zostań bohaterem każdej kolacji 🍷✨
""")

# === Dane bazowe ===
przepisy = {
    "Wiśnie": {"cukier": 3.6, "woda": 6.0, "drozdze": "Fermivin, Fermicru LS2, Enovin, Enovin WS", "procent": 12},
    "Jabłka": {"cukier": 3.4, "woda": 8.0, "drozdze": "Fermivin, Tokay, Sherry, Enovin WS", "procent": 12},
    "Maliny": {"cukier": 4.4, "woda": 6.6, "drozdze": "Fermivin, Fermicru LS2, Enovin WS", "procent": 14},
    "Truskawki": {"cukier": 3.2, "woda": 6.6, "drozdze": "Fermivin, Enovin WS, Tokay", "procent": 14},
    "Czarny Bez": {"cukier": 4.6, "woda": 7.2, "drozdze": "Fermivin, Fermicru VR5, Tokay", "procent": 16},
    "Agrest": {"cukier": 3.6, "woda": 9.6, "drozdze": "Fermivin, Tokay, Madera", "procent": 12},
    "Czereśnie": {"cukier": 3.6, "woda": 5.6, "drozdze": "Fermivin, Fermicru LS2, Enovin", "procent": 12},
    "Brzoskwinia": {"cukier": 3.4, "woda": 6.6, "drozdze": "Fermivin, Fermicru LS2, Sauternes", "procent": 14},
    "Aronia": {"cukier": 4.4, "woda": 9.6, "drozdze": "Fermicru VR5, Malaga", "procent": 14},
    "Dzika Róża": {"cukier": 4.4, "woda": 12.4, "drozdze": "Fermivin, Tokay, Sauternes", "procent": 14},
    "Jeżyny": {"cukier": 4.4, "woda": 5.6, "drozdze": "Fermivin, Bordeaux, Enovin", "procent": 14},
    "Jagody": {"cukier": 4.4, "woda": 5.6, "drozdze": "Fermivin, Enovin WS", "procent": 14},
}

# === Formularz ===
st.header("Wybierz owoce na wino")
wybrane = st.multiselect("Zaznacz owoce, które chcesz użyć", options=list(przepisy.keys()))

litry = st.number_input("Podaj ile litrów wina chcesz zrobić:", min_value=1.0, step=1.0)

rodzaj = st.radio("Wybierz rodzaj wina:", ["wytrawne", "półwytrawne", "półsłodkie", "słodkie"])
procent = st.slider("Planowana moc wina (%)", 11, 18, 14)

# === Wyniki ===
if wybrane and litry:
    st.subheader("📈 Składniki na Twoje wino")
    suma_cukru = 0
    suma_wody = 0
    suma_kwasu = 0
    st.write(f"### 🍇 Owoce: {', '.join(wybrane)}")
    for owoc in wybrane:
        baza = przepisy[owoc]
        cukier = baza["cukier"] * (litry / 20)
        woda = baza["woda"] * (litry / 20)
        kwas = 0.1 * (litry / 20) if procent >= 15 else 0
        st.markdown(f"**{owoc}**: cukier {cukier:.1f} kg, woda {woda:.1f} L, kwas cytrynowy {kwas:.1f} g")
        suma_cukru += cukier
        suma_wody += woda
        suma_kwasu += kwas

    drozdze = set(przepisy[o]["drozdze"] for o in wybrane)
    st.markdown(f"**🍬 Łącznie cukru**: {suma_cukru:.1f} kg")
    st.markdown(f"**💧 Łącznie wody**: {suma_wody:.1f} L")
    st.markdown(f"**🧪 Drożdże**: {', '.join(drozdze)}")

    st.markdown("""
    ---
    #### 🔧 Przepis krok po kroku:
    1. Przygotuj owoce, umyj i rozdrobnij.
    2. Odmierz odpowiednie ilości cukru i wody wg wskazań powyżej.
    3. Podgrzej wodę do ~40°C, rozpuść w niej cukier i pozostaw do ostygnięcia.
    4. Połącz owoce, wodę z cukrem, drożdże i pożywkę w balonie fermentacyjnym.
    5. Pozostaw do fermentacji na 2-4 tygodnie, potem zlej z nad osadu i klaruj.
    """)

    st.caption("Dane bazowe na podstawie tabel z alkohole-domowe.com - dziękujemy! 🙏")
