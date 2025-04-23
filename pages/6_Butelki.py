import streamlit as st
import math

st.set_page_config(page_title="Kalkulator butelek", page_icon="🍾")

st.title("🍾 Kalkulator liczby butelek z wina")
st.markdown("Podaj ilość wina i wybierz pojemność butelek, aby obliczyć ile butelek napełnisz.")

# 📦 Dane wejściowe
ilosc_wina_litry = st.number_input("Ilość wina (w litrach):", min_value=0.0, step=0.1, format="%.2f")
rozmiar_butelki_ml = st.selectbox(
    "Rozmiar butelki:",
    [100, 200, 250, 330, 375, 500, 700, 750, 1000, 2000, 3000, 5000],
    index=7  # domyślnie zaznaczone 750 ml
)


# 🔍 Obliczenia
if st.button("📊 Oblicz liczbę butelek"):
    wino_ml = ilosc_wina_litry * 1000
    butelek = math.floor(wino_ml / rozmiar_butelki_ml)
    reszta = round(wino_ml % rozmiar_butelki_ml)

    st.success(f"👉 Z {ilosc_wina_litry:.2f} L wina wypełnisz **{butelek} butelek po {rozmiar_butelki_ml} ml**.")
    if reszta > 0:
        st.info(
            f"🔹 Zostanie Ci jeszcze **{reszta} ml** niewykorzystanego wina.\n\n"
            "🍷 Ktoś będzie musiał to **wypić** – jak mówi Michał:\n"
            "_„Nigdy nie ufaj chudemu kucharzowi i trzeźwemu winiarzowi!”_ 😄"
        )
