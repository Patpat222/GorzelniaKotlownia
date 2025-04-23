import streamlit as st

st.set_page_config(page_title="Kalkulator cukru", page_icon="📐")
st.title("📐 Kalkulator cukru do nastawu")

wybor = st.radio("Wybierz tryb kalkulatora:", ["Prosty", "Zaawansowany"], horizontal=True)

# =================== TRYB PROSTY ===================
if wybor == "Prosty":
    st.subheader("🔹 Tryb prosty")

    ilosc_owocow = st.number_input("Ilość owoców (w kg):", min_value=0.0, step=0.1, format="%.2f")
    ilosc_wody = st.number_input("Ilość dodanej wody (w litrach):", min_value=0.0, step=0.1, format="%.2f")
    procent = st.slider("Planowana zawartość alkoholu (%):", 5, 18, 12)
    dokladnie = st.checkbox("Użyj dokładnego przelicznika 17.2g (zamiast 17g)", value=False)

    if st.button("🔍 Oblicz ilość cukru"):
        suma = ilosc_owocow + ilosc_wody
        mnoznik = 17.2 if dokladnie else 17
        wynik = round(suma * procent * mnoznik)

        st.success(f"👉 Łącznie {suma:.2f} L: dodaj około **{wynik} gramów cukru**.")
        st.caption(f"📎 Obliczenie: {suma:.2f} L × {procent}% × {mnoznik}g")
        st.info("🧠 Od podanego wyniku należy odjąć zawartość BLG w soku.")

# =================== TRYB ZAAWANSOWANY ===================
#Michał mnie zmusił, żeby dać opcje zaawansowaną
else:
    st.subheader("🔸 Tryb zaawansowany")

    # zawartość cukru w owocach (g/100ml)
    cukry = {
        "Agrest": 11.6,
        "Czereśnie": 18.4,
        "Dzika róża": 10.0,
        "Jabłka": 21.6,
        "Maliny": 14.6,
        "Morele": 21.6,
        "Wiśnie": 20.0,
        "Porzeczki białe": 10.0,
        "Porzeczki czerwone": 10.0,
        "Rodzynki": 3.0,
        "Winogrona czarne": 18.0,
        "Truskawki": 21.6,
        "Aronia": 9.8,
        "Czarna jagoda": 17.2,
        "Czarny bez": 11.2,
        "Jeżyny": 17.0,
        "Śliwki": 18.0,
        "Inny": 0
    }

    owoc = st.selectbox("Wybierz owoc bazowy:", list(cukry.keys()))
    cukier_w_owocu = cukry[owoc]
    if owoc == "Inny":
        cukier_w_owocu = st.number_input("Podaj zawartość cukru w owocu (g/100ml):", min_value=0.0, step=0.1)

    ilosc_owocow = st.number_input("Ilość owoców (w kg):", min_value=0.0, step=0.1)
    ilosc_wody = st.number_input("Ilość dodanej wody (w litrach):", min_value=0.0, step=0.1)
    procent = st.slider("Planowana zawartość alkoholu (%):", 5, 18, 12)
    dokladnie = st.checkbox("Użyj dokładnego przelicznika 17.2g (zamiast 17g)", value=False)

    if st.button("📊 Oblicz z uwzględnieniem cukru z owoców"):
        mnoznik = 17.2 if dokladnie else 17
        calosc = ilosc_owocow + ilosc_wody
        wymagany_cukier = calosc * procent * mnoznik / 1000  # w kg
        cukier_z_owocu = (cukier_w_owocu * ilosc_owocow) / 10  # w kg
        do_dodania = max(0, wymagany_cukier - cukier_z_owocu)

        st.success(f"👉 Łącznie potrzebujesz: **{wymagany_cukier:.2f} kg** cukru")
        st.write(f"Z czego cukier z owoców: **{cukier_z_owocu:.2f} kg**")
        st.write(f"**➡️ Dodaj: {do_dodania:.2f} kg cukru**")

        st.caption(f"📎 Obliczenie: ({calosc:.2f} L × {procent}% × {mnoznik}) ÷ 1000 = {wymagany_cukier:.2f} kg")
        st.caption(f"📎 Cukier w owocach: {cukier_w_owocu}g/100ml × {ilosc_owocow}kg = {cukier_z_owocu:.2f} kg")
        st.info("🧠 Od podanego wyniku należy odjąć zawartość BLG w soku.")
