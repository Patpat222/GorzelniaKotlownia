import streamlit as st

st.set_page_config(page_title="Przelicznik składników", page_icon="📦")
st.title("📦 Przelicznik podstawowych składników")
st.markdown("Wprowadź dane z oryginalnego przepisu i przelicz je na dowolną objętość 🍷")

st.markdown("### 1️⃣ Objętości")
col1, col2 = st.columns(2)
with col1:
    baza = st.number_input("📦 Przepis bazowy (L)", min_value=0.5, value=25.0, step=0.5)
with col2:
    docelowa = st.number_input("🎯 Docelowa objętość (L)", min_value=0.5, value=5.0, step=0.5)

st.markdown("---")
st.markdown("### 2️⃣ Składniki (dla objętości bazowej)")
col1, col2 = st.columns(2)
with col1:
    owoce = st.number_input("🍇 Owoce (kg)", min_value=0.0, value=5.0, step=0.1)
    cukier = st.number_input("🍬 Cukier (kg)", min_value=0.0, value=4.0, step=0.1)
with col2:
    woda = st.number_input("💧 Woda (L)", min_value=0.0, value=15.0, step=0.1)
    drozdze = st.number_input("🧫 Drożdże (g lub saszetki)", min_value=0.0, value=1.0, step=0.1)

st.markdown("---")

if st.button("📐 Przelicz składniki"):
    skala = docelowa / baza
    st.success(f"Współczynnik przeliczenia: {skala:.2f}")

    st.markdown("### ✅ Przeliczone ilości:")
    st.markdown(f"- 🍇 Owoce: **{owoce * skala:.2f} kg**")
    st.markdown(f"- 💧 Woda: **{woda * skala:.2f} L**")
    st.markdown(f"- 🍬 Cukier: **{cukier * skala:.2f} kg**")
    st.markdown(f"- 🧫 Drożdże: **{drozdze * skala:.2f} g/saszetki**")
