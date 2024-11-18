import streamlit as st
import pandas as pd
import plotly.express as px

# Daftar negara di Asia Tenggara
southeast_asian_countries = [
    "Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", 
    "Myanmar", "Philippines", "Singapore", "Thailand", "Vietnam", "Timor-Leste"
]

# Judul aplikasi
st.title("Analisis Perubahan Pola Konsumsi Ikan dan Makanan Laut (1961–2021)")

# Unggah data
uploaded_file = st.file_uploader("Unggah file CSV Anda", type="csv")

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file)
    
    # Filter hanya negara Asia Tenggara
    df = df[df['Entity'].isin(southeast_asian_countries)]
    
    # Menampilkan preview data
    st.subheader("Data Awal")
    st.dataframe(df.head())

    # Dropdown untuk memilih negara utama dan negara lainnya
    countries = df['Entity'].unique()
    comparison_countries = st.multiselect("Pilih negara lain untuk dibandingkan", countries, default=[c for c in countries][:10])

    # Filter data berdasarkan negara yang dipilih
    filtered_df = df[df['Entity'].isin(comparison_countries)]

    # Visualisasi perubahan konsumsi
    st.subheader("Grafik Perubahan Pola Konsumsi")
    fig = px.line(
        filtered_df,
        x='Year',
        y='Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita',
        color='Entity',
        title="Perubahan Pola Konsumsi Ikan dan Makanan Laut (1961–2021)",
        labels={'Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita': 'Konsumsi per Kapita (kg)', 'Year': 'Tahun'}
    )
    fig.update_layout(legend_title="Negara", xaxis_title="Tahun", yaxis_title="Konsumsi per Kapita (kg)")
    st.plotly_chart(fig)

    # Perbandingan konsumsi rata-rata
    st.subheader("Perbandingan Konsumsi Rata-Rata")
    avg_consumption = filtered_df.groupby('Entity')['Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita'].mean().reset_index()
    avg_consumption.columns = ['Negara', 'Rata-rata Konsumsi per Kapita (kg)']
    st.table(avg_consumption)

    # Dropdown untuk memilih tahun
    st.subheader("Perbandingan Konsumsi Ikan Berdasarkan Tahun")
    selected_year = st.selectbox("Pilih tahun untuk perbandingan", sorted(df['Year'].unique()))

    # Filter data berdasarkan tahun yang dipilih
    yearly_comparison = filtered_df[filtered_df['Year'] == selected_year]

    # Menampilkan tabel konsumsi berdasarkan tahun
    st.write(f"Konsumsi Ikan per Kapita pada Tahun {selected_year}")
    yearly_comparison_table = yearly_comparison[['Entity', 'Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita']]
    yearly_comparison_table.columns = ['Negara', 'Konsumsi per Kapita (kg)']
    st.table(yearly_comparison_table)

else:
    st.info("Silakan unggah file CSV untuk melanjutkan analisis.")
