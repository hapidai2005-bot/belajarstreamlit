
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("Dashboard Dataset dari Dosen")

st.write("Upload dataset Excel atau CSV untuk dianalisis.")

file = st.file_uploader(
    "Pilih file dataset",
    type=["xlsx", "csv"]
)

if file is not None:
    try:
        if file.name.lower().endswith(".csv"):
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                file.seek(0)
                df = pd.read_csv(
                    file,
                    encoding="latin-1"
                )
        else:
            df = pd.read_excel(file)

        st.success("Dataset berhasil dibaca!")

        st.subheader("Preview Dataset")
        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Jumlah Baris", len(df))
        col2.metric("Jumlah Kolom", len(df.columns))
        col3.metric(
            "Data Kosong",
            int(df.isna().sum().sum())
        )

        st.subheader("Nama Kolom Dataset")
        st.write(df.columns.tolist())

        st.subheader("Statistik Deskriptif")
        st.dataframe(
            df.describe(include="all").fillna(""),
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Gagal membaca dataset: {e}")
