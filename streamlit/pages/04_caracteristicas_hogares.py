import streamlit as st
import matplotlib.pyplot as plt
from package.data_graphics.individuos import agglomeration_id
from package.data_graphics.hogares import (
    load_hogar_data_04,
    get_available_years,
    get_total_houses,
    get_housing_type_distribution,
    get_floor_material_by_agglomerate,
    get_bathroom_access_by_agglomerate,
    get_villas_by_agglomerate,
    get_habitability_by_agglomerate,
    get_tenure_evolution_named
)

st.title("P4 - Características Hogares")

# Cargar los datos de hogares con las columnas necesarias
try:
    df = load_hogar_data_04()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

# Filtro por año, hago un selectbox para elegir el año o todos
available_years = get_available_years(df)
selected_year = st.selectbox("Año", ["Todos"] + available_years, index=len(available_years))

# Si el año seleccionado no es "Todos", filtro el dataframe por el año seleccionado
if selected_year != "Todos":
    df = df[df["ANO4"] == selected_year]

# 1.4.1
st.subheader("1.4.1 - Cantidad total de viviendas")
st.write("Total de viviendas: ", get_total_houses(df))

# 1.4.2
st.subheader("1.4.2 - Distribución por tipo de vivienda")
type_counts = get_housing_type_distribution(df)
# Creo figura y ejes
fig, ax = plt.subplots()
ax.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%")
ax.set_title("Proporción por tipo de vivienda", fontsize=14)
st.write(fig)

# 1.4.3
st.subheader("1.4.3 - Material predominante en pisos por aglomerado")
st.dataframe(get_floor_material_by_agglomerate(df))

# 1.4.4
st.subheader("1.4.4 - Porcentaje de viviendas con baño dentro del hogar por aglomerado")
st.dataframe(get_bathroom_access_by_agglomerate(df))

# 1.4.5
st.subheader("1.4.5 - Evolución del régimen de tenencia")

# Diccionario y listas de aglomerados
dict_ag_id = agglomeration_id()
dict_name_to_id = {v: int(k) for k, v in dict_ag_id.items()}
agglomerates = sorted(dict_name_to_id.keys())

# Selector de aglomerado
selected_agglomerate_name = st.selectbox("Aglomerado", agglomerates, key="ten_agglom")
selected_agglomerate = dict_name_to_id[selected_agglomerate_name]

# Diccionario de regimen de tenencia
TENENCIA_LABELS = {
    1: "Propietario vivienda y terreno",
    2: "Propietario vivienda solo",
    3: "Inquilino / arrendatario",
    4: "Ocupante por impuestos/expensas",
    5: "Ocupante en relación laboral",
    6: "Ocupante con permiso",
    7: "Ocupante sin permiso",
    8: "Está en sucesión"
}

# Selector de tenencias por nombre
selected_labels = st.multiselect(
    "Tipo(s) de tenencia",
    options=list(TENENCIA_LABELS.values()),
    default=list(TENENCIA_LABELS.values())
)

pivot = get_tenure_evolution_named(df, selected_agglomerate, selected_labels)

if pivot.empty:
    st.warning("No hay datos disponibles para la selección.")
else:
    pivot["Periodo"] = pivot["ANO4"].astype(str) + "-T" + pivot["TRIMESTRE"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#1D2B44')
    ax.set_facecolor('#1D2B44')

    for label in selected_labels:
        if label in pivot.columns:
            ax.plot(pivot["Periodo"], pivot[label], label=label, linewidth=2)

    ax.set_title("Evolución del régimen de tenencia", fontsize=14, color='white')
    ax.set_xlabel("Periodo", fontsize=12, color='white')
    ax.set_ylabel("Viviendas", fontsize=12, color='white')
    ax.tick_params(axis='x', labelrotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    ax.legend(labelcolor='white', facecolor='#1D2B44', frameon=False)
    st.pyplot(fig)

# 1.4.6
st.subheader("1.4.6 - Viviendas en villa de emergencia")
villa_df = get_villas_by_agglomerate(df)
villa_df = villa_df.sort_values(by="Cantidad en Villas", ascending=False)
st.dataframe(villa_df[["Aglomerado", "Cantidad en Villas", "Total", "Porcentaje"]])

# 1.4.7
st.subheader("1.4.7 - Condición de habitabilidad por aglomerado")
hab_df = get_habitability_by_agglomerate(df)
st.dataframe(hab_df[["Aglomerado", "CONDICION_DE_HABITABILIDAD", "Cantidad", "Porcentaje"]])

csv = hab_df.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV", data=csv, file_name="habitabilidad.csv", mime="text/csv")