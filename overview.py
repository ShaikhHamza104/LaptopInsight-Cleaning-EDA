import streamlit as st
import io
import pandas as pd
import plotly.express as px

class Overview:

    def __init__(self, df):
        self.df = df
        self.create_overview()

    def create_overview(self):
        st.header("📊 Overview")
        st.write("This dashboard provides an overview of the Laptop dataset.")

        # First 5 rows
        st.subheader("🔹 First 5 Rows")
        st.write(self.df.head())

        # Last 5 rows
        st.subheader("🔹 Last 5 Rows")
        st.write(self.df.tail())

        # Summary statistics
        st.subheader("📈 Summary Statistics")
        st.write(self.df.describe())

        # Shape of the dataset
        st.subheader("📐 Dataset Shape")
        st.write(f"Rows: {self.df.shape[0]}")
        st.write(f"Columns: {self.df.shape[1]}")

        # Dataset information
        st.subheader("ℹ️ Dataset Info")
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        # Missing values
        st.subheader("⚠️ Missing Values")
        missing = self.df.isnull().sum()
        st.write(missing)
        st.write(f"Total missing values: {missing.sum()}")

        # Data types
        st.subheader("🧬 Data Types")
        st.write(self.df.dtypes)

        # Value counts for categorical columns
        st.subheader("🔠 Value Counts for Categorical Columns")
        categorical_cols = self.df.select_dtypes(include='object').columns
        for col in categorical_cols:
            st.markdown(f"**{col}**")
            st.write(self.df[col].value_counts())

        # Correlation matrix using Plotly
        st.subheader("📊 Correlation Matrix (Heatmap)")
        corr = self.df.select_dtypes(include=['int64', 'float64']).corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', title="Feature Correlation Heatmap")
        st.plotly_chart(fig)


if __name__ == "__main__":
    df = pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')
    overview = Overview(df)
    overview.create_overview()
    st.write("Overview created successfully.")