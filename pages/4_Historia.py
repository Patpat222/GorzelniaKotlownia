import streamlit as st
from datetime import date, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import os

st.set_page_config(page_title="Historia Przebiegu", page_icon="📜")
st.title("📜 Historia przebiegu fermentacji")
st.markdown("Zapisuj postępy, pomiary i działania wykonane przy każdej partii 🍷")

HISTORIA_FILE = "data/historia.json"

# 🔁 Odczyt danych
def load_historia():
    if os.path.exists(HISTORIA_FILE):
        with open(HISTORIA_FILE, "r") as f:
            return json.load(f)
    return []

# 💾 Zapis danych
def save_historia(lista):
    with open(HISTORIA_FILE, "w") as f:
        json.dump(lista, f, indent=2)

if "wpisy" not in st.session_state:
    st.session_state["wpisy"] = load_historia()

# === Dodawanie nowego wpisu ===
with st.expander("➕ Dodaj wpis do historii"):
    partie = sorted(set([w["nazwa"] for w in st.session_state["wpisy"]]))
    wybrana_partia = st.selectbox("🍷 Wybierz partię:", partie + ["➕ Dodaj nową"])

    if wybrana_partia == "➕ Dodaj nową":
        nowa_partia = st.text_input("📌 Wpisz nową nazwę partii:")
        final_partia = nowa_partia if nowa_partia else "Nowa partia"
    else:
        final_partia = wybrana_partia

    data_wpisu = st.date_input("📅 Data zdarzenia", value=date.today())
    opis_wpisu = st.text_area("🧪 Co się działo?")

    if st.button("📌 Dodaj wpis"):
        nowy_wpis = {
            "nazwa": final_partia,
            "data": data_wpisu.strftime("%d.%m.%Y"),
            "opis": opis_wpisu
        }
        st.session_state["wpisy"].append(nowy_wpis)
        save_historia(st.session_state["wpisy"])
        st.success(f"✅ Dodano wpis do: {final_partia}")

# === Przegląd historii ===
st.markdown("---")
st.subheader("📂 Zobacz historię konkretnej partii")

dostepne_partie = sorted(set([w["nazwa"] for w in st.session_state["wpisy"]]))
wybor_partii = st.selectbox("🔍 Wybierz partię:", dostepne_partie)

filtr = [w for w in st.session_state["wpisy"] if w["nazwa"] == wybor_partii]

# 🔁 Sortowanie i filtrowanie
sortuj_rosnaco = st.checkbox("⬆️ Pokaż od najstarszego wpisu", value=False)
tylko_blg = st.checkbox("🔬 Pokaż tylko wpisy z BLG")

wpisy_do_pokazania = filtr if sortuj_rosnaco else list(reversed(filtr))
if tylko_blg:
    wpisy_do_pokazania = [w for w in wpisy_do_pokazania if "BLG" in w["opis"]]

if wpisy_do_pokazania:
    for i, wpis in enumerate(wpisy_do_pokazania):
        st.markdown(f"""
        📅 **{wpis['data']}**  
        ✍️ {wpis['opis']}
        """)
        with st.expander("✏️ Edytuj wpis"):
            e_data = st.date_input("📅 Data", value=datetime.strptime(wpis["data"], "%d.%m.%Y"), key=f"data_{i}")
            e_opis = st.text_area("🧪 Opis", value=wpis["opis"], key=f"opis_{i}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Zapisz zmiany", key=f"zapisz_{i}"):
                    wpis["data"] = e_data.strftime("%d.%m.%Y")
                    wpis["opis"] = e_opis
                    save_historia(st.session_state["wpisy"])
                    st.success("✅ Zmieniono wpis.")
                    st.experimental_rerun()
            with col2:
                if st.button("🗑️ Usuń wpis", key=f"usun_{i}"):
                    st.session_state["wpisy"].remove(wpis)
                    save_historia(st.session_state["wpisy"])
                    st.warning("❌ Wpis usunięty.")
                    st.experimental_rerun()
        st.markdown("---")
else:
    st.info("Brak wpisów do wyświetlenia.")

# 📝 Notatka do partii (tymczasowa)
with st.expander("📝 Notatka do tej partii"):
    st.text_area("Dodatkowe uwagi lub plany (niedługo zrobimy zapis!)")

# 📈 Wykres BLG
blg_data = []
for w in filtr:
    if "BLG" in w["opis"]:
        try:
            wartosc = int(w["opis"].split("BLG")[0].strip())
            data_blg = datetime.strptime(w["data"], "%d.%m.%Y")
            blg_data.append((data_blg, wartosc))
        except:
            pass

if blg_data:
    blg_data.sort()
    daty = [d[0] for d in blg_data]
    wartosci = [d[1] for d in blg_data]

    st.markdown("### 📉 Wykres fermentacji (BLG)")
    fig, ax = plt.subplots()
    ax.plot(daty, wartosci, marker='o', color='darkred', linewidth=2)
    ax.set_xlabel("Data")
    ax.set_ylabel("BLG")
    ax.set_title(f"BLG – {wybor_partii}")
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)
