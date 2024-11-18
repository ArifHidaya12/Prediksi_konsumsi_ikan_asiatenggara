import streamlit as st
import pandas as pd
import plotly.express as px

# Daftar negara di Asia Tenggara
southeast_asian_countries = [
    "Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia",
    "Myanmar", "Philippines", "Singapore", "Thailand", "Vietnam", "Timor-Leste"
]

# Judul aplikasi
st.title("Dashboard Analisis Konsumsi Ikan di Asia Tenggara (1961–2021)")

# Unggah file data
uploaded_file = st.file_uploader("Unggah file CSV Anda", type="csv")

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file)
    
    # Filter hanya negara Asia Tenggara
    df = df[df['Entity'].isin(southeast_asian_countries)]
    
    # Menampilkan data awal sebagai referensi
    st.subheader("Data Awal")
    st.dataframe(df.head())

    # Summary Konsumsi
    st.subheader("Summary Data Konsumsi")
    total_entities = len(df['Entity'].unique())
    avg_consumption_all = df['Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita'].mean()
    st.metric("Jumlah Negara", total_entities)
    st.metric("Rata-rata Konsumsi Ikan", f"{avg_consumption_all:.2f} kg per kapita")

    # Grafik Perubahan Konsumsi
    st.subheader("Grafik Perubahan Pola Konsumsi")
    fig_line = px.line(
        df,
        x='Year',
        y='Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita',
        color='Entity',
        title="Perubahan Pola Konsumsi Ikan dan Makanan Laut (1961–2021)",
        labels={'Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita': 'Konsumsi (kg)', 'Year': 'Tahun'}
    )
    st.plotly_chart(fig_line)

    # Pie Chart untuk Persentase Negara dengan Konsumsi Tinggi
    st.subheader("Distribusi Konsumsi Ikan per Negara")
    latest_year = df['Year'].max()
    latest_data = df[df['Year'] == latest_year]
    fig_pie = px.pie(
        latest_data,
        values='Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita',
        names='Entity',
        title=f"Distribusi Konsumsi Ikan di Tahun {latest_year}",
        labels={'Entity': 'Negara', 'Fish and seafood': 'Konsumsi (kg)'}
    )
    st.plotly_chart(fig_pie)

    # Bar Chart untuk Rata-rata Konsumsi
    st.subheader("Rata-rata Konsumsi per Negara")
    avg_data = df.groupby('Entity')['Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita'].mean().reset_index()
    fig_bar = px.bar(
        avg_data,
        x='Entity',
        y='Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita',
        title="Rata-rata Konsumsi Ikan per Kapita (1961–2021)",
        labels={'Fish and seafood | 00002960 || Food available for consumption | 0645pc || kilograms per year per capita': 'Rata-rata Konsumsi (kg)', 'Entity': 'Negara'}
    )
    st.plotly_chart(fig_bar)
else:
    st.info("Silakan unggah file CSV untuk melihat dashboard.")
