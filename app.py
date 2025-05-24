import streamlit as st
import pandas as pd
import overview
import univariate_analysis
df = pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')

st.title('EDA Dashboard : Univariate & Bivariate analysis')

# Sidebar for navigation
st.sidebar.title("📊 Laptop Analyzer")
analysis_type = st.sidebar.selectbox("Select Analysis Type", ("Overview","Univariate Analysis", "Bivariate Analysis"))

# --- Dataset overiew ---
if analysis_type == 'Overview':
    overview = overview.Overview(df)
    
# --- Univariate Analysis ---
elif analysis_type == "Univariate Analysis":
    univariate = univariate_analysis.UnivariateAnalysis(df)
    univariate_analysis = univariate_analysis.UnivariateAnalysis(df)
    univariate_analysis.display()

# --- Bivariate Analysis ---
elif analysis_type == "Bivariate Analysis":
    st.write("Bivariate Analysis is under construction. Please check back later.")