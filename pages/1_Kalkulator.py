import streamlit as st

st.set_page_config(page_title="Kalkulator cukru", page_icon="📐")

st.title("📐 Kalkulator cukru do nastawu")
st.markdown("Oblicz ile cukru należy dodać na podstawie ilości owoców, wody i planowanego %. 🍇💧")

# 🫐 Lista bazowych składników (owoce, zioła, napary itd.)
owoc = st.selectbox("Wybierz składnik bazowy:", [
    "Winogrona",
    "Jabłka",
    "Gruszki",
    "Śliwki",
    "Porzeczki (czarne)",
    "Porzeczki (czerwone)",
    "Truskawki",
    "Maliny",
    "Żurawina",
    "Borówki",
    "Czereśnie",
    "Wiśnie",
    "Banany",
    "Pomarańcze",
    "Mandarynki",
    "Ananas",
    "Mango",
    "Aronia",
    "Agrest",
    "Hibiskus",
    "Zielona herbata",
    "Mieszanka lekarska",
    "Kwiaty dzikiego bzu",
    "Inny (ręcznie dopisany)"
])

# ✍️ Wpisanie własnego składnika
if owoc == "Inny (ręcznie dopisany)":
    inny_owoc = st.text_input("Wpisz nazwę składnika:")
    owoc = inny_owoc if inny_owoc else "Nieznany składnik"

# ⚖️ Ilość składników
ilosc_owocow = st.number_input("Ilość owoców (w kg):", min_value=0.0, step=0.1, format="%.2f")
ilosc_wody = st.number_input("Ilość dodanej wody (w litrach):", min_value=0.0, step=0.1, format="%.2f")

# 🎯 Docelowy % alkoholu
procent = st.slider("Planowana zawartość alkoholu (%):", 5, 18, 12)

# ☑️ Tryb dokładny
dokladnie = st.checkbox("Użyj dokładnego przelicznika 17.2g (zamiast 17g)", value=False)

# 🔘 Przycisk liczenia
if st.button("🔍 Oblicz ilość cukru"):
    suma = ilosc_owocow + ilosc_wody
    mnoznik = 17.2 if dokladnie else 17
    wynik = round(suma * procent * mnoznik)

    st.success(f"👉 Dla składnika **{owoc}** i objętości {suma:.2f} L dodaj około **{wynik} gramów cukru**.")
    st.caption(f"Obliczenie: {suma:.2f} L × {procent}% × {mnoznik}g")

# 📎 Dodatkowe informacje (opcjonalne)
st.markdown("---")
st.caption("🍷 Wzór przybliżony, błąd może wynosić do ±1%. Smacznego nastawu!")
