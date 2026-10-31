
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Keuangan Yayasan",
    page_icon="📊",
    layout="wide"
)

# Data simulasi keuangan
data = {
    "Bulan": [
        "Januari", "Februari", "Maret",
        "April", "Mei", "Juni"
    ],
    "Kas Masuk": [
        45000000, 48000000, 52000000,
        47000000, 55000000, 60000000
    ],
    "Kas Keluar": [
        32000000, 35000000, 38000000,
        36000000, 40000000, 43000000
    ]
}

df = pd.DataFrame(data)

# Menghitung arus kas bersih
df["Arus Kas Bersih"] = (
    df["Kas Masuk"] - df["Kas Keluar"]
)

# Sidebar navigasi
st.sidebar.title("Keuangan Yayasan")

menu = st.sidebar.radio(
    "Pilih Menu",
    ["Dashboard", "Data Transaksi", "Laporan"]
)

# Filter bulan
pilihan_bulan = st.sidebar.selectbox(
    "Pilih Bulan",
    ["Semua"] + df["Bulan"].tolist()
)

if pilihan_bulan == "Semua":
    data_filter = df.copy()
else:
    data_filter = df[
        df["Bulan"] == pilihan_bulan
    ].copy()

# Menghitung ringkasan
total_masuk = data_filter["Kas Masuk"].sum()
total_keluar = data_filter["Kas Keluar"].sum()
saldo = total_masuk - total_keluar

def rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# Halaman Dashboard
if menu == "Dashboard":

    st.title("Dashboard Keuangan Yayasan")
    st.write("Monitoring arus kas masuk dan keluar")
    st.info("Data yang ditampilkan adalah data simulasi.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Kas Masuk",
            rupiah(total_masuk)
        )

    with col2:
        st.metric(
            "Total Kas Keluar",
            rupiah(total_keluar)
        )

    with col3:
        st.metric(
            "Arus Kas Bersih",
            rupiah(saldo)
        )

    st.subheader("Grafik Arus Kas Bulanan")

    fig, ax = plt.subplots(figsize=(10, 5))

    x = range(len(data_filter))
    lebar = 0.35

    ax.bar(
        [i - lebar / 2 for i in x],
        data_filter["Kas Masuk"] / 1000000,
        width=lebar,
        label="Kas Masuk"
    )

    ax.bar(
        [i + lebar / 2 for i in x],
        data_filter["Kas Keluar"] / 1000000,
        width=lebar,
        label="Kas Keluar"
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(data_filter["Bulan"])
    ax.set_ylabel("Juta Rupiah")
    ax.set_title("Perbandingan Kas Masuk dan Keluar")
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Halaman Data Transaksi
elif menu == "Data Transaksi":

    st.title("Data Transaksi Keuangan")
    st.dataframe(
        data_filter,
        use_container_width=True,
        hide_index=True
    )

# Halaman Laporan
elif menu == "Laporan":

    st.title("Laporan Arus Kas Yayasan")

    st.dataframe(
        data_filter,
        use_container_width=True,
        hide_index=True
    )

    st.write("Total Kas Masuk:", rupiah(total_masuk))
    st.write("Total Kas Keluar:", rupiah(total_keluar))
    st.write("Arus Kas Bersih:", rupiah(saldo))

    csv = data_filter.to_csv(index=False)

    st.download_button(
        label="Download Laporan CSV",
        data=csv,
        file_name="laporan_keuangan.csv",
        mime="text/csv"
    )
