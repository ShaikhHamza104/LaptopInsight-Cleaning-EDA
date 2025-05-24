import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

class BivariateAnalysis:
    def __init__(self, df):
        self.df = df
        self.numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].apply(lambda x: str(x) if not isinstance(x, str) else x)

    def column_vs_column_display(self):
        st.title("📊 Bivariate Analysis with Plotly")
        st.write("Explore relationships between two variables interactively.")

        columtype = st.selectbox("Select Column Type", 
                                 ("Numerical vs Numerical", 
                                  "Categorical vs Categorical", 
                                  "Numerical vs Categorical"))

        if columtype == "Numerical vs Numerical":
            self.numerical_vs_numerical()
        elif columtype == "Categorical vs Categorical":
            self.categorical_vs_categorical()
        elif columtype == "Numerical vs Categorical":
            self.numerical_vs_categorical()

    def numerical_vs_numerical(self):
        col1 = st.selectbox("Select 1st Numerical Column", self.numerical_columns, key='num1')
        col2 = st.selectbox("Select 2nd Numerical Column", self.numerical_columns, key='num2')
        rows = st.selectbox("Select number of rows to display", options=[len(self.df), 5], 
                            format_func=lambda x: "All Rows" if x == len(self.df) else str(x))
        plot_type = st.selectbox("Select Plot Type", ['Scatterplot', 'Lineplot', 'Boxplot', 'Densityplot', 'Heatmap'])

        st.subheader(f'{col1} vs {col2}')
        df_display = self.df if rows == len(self.df) else self.df.head(rows)

        if plot_type == 'Scatterplot':
            fig = px.scatter(df_display, x=col1, y=col2)
        elif plot_type == 'Lineplot':
            fig = px.line(df_display, x=col1, y=col2)
        elif plot_type == 'Boxplot':
            fig = px.box(df_display, x=col1, y=col2)
        elif plot_type == 'Densityplot':
            fig = px.density_contour(df_display, x=col1, y=col2)
        elif plot_type == 'Heatmap':
            corr = df_display[[col1, col2]].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='Viridis',
                zmin=-1, zmax=1
            ))

        st.plotly_chart(fig, use_container_width=True)

    def categorical_vs_categorical(self):
        col1 = st.selectbox("Select 1st Categorical Column", self.categorical_columns, key='cat1')
        col2 = st.selectbox("Select 2nd Categorical Column", self.categorical_columns, key='cat2')
        rows = st.selectbox("Select number of rows to display", options=[len(self.df), 5],
                            format_func=lambda x: "All Rows" if x == len(self.df) else str(x))
        plot_type = st.selectbox("Select Plot Type", ['Countplot', 'Heatmap'])

        st.subheader(f'{col1} vs {col2}')
        df_display = self.df if rows == len(self.df) else self.df.head(rows)
        cross_tab = pd.crosstab(df_display[col1], df_display[col2])

        if plot_type == 'Countplot':
            fig = px.bar(cross_tab, barmode='stack')
        elif plot_type == 'Heatmap':
            fig = px.imshow(cross_tab, text_auto=True, color_continuous_scale='Blues')

        st.plotly_chart(fig, use_container_width=True)

    def numerical_vs_categorical(self):
        num_col = st.selectbox("Select Numerical Column", self.numerical_columns, key='num_cat1')
        cat_col = st.selectbox("Select Categorical Column", self.categorical_columns, key='num_cat2')
        rows = st.selectbox("Select number of rows to display", options=[len(self.df), 5],
                            format_func=lambda x: "All Rows" if x == len(self.df) else str(x))
        plot_type = st.selectbox("Select Plot Type", ['Boxplot', 'Violinplot', 'Barplot'])

        st.subheader(f'{num_col} vs {cat_col}')
        df_display = self.df if rows == len(self.df) else self.df.head(rows)

        if plot_type == 'Boxplot':
            fig = px.box(df_display, x=cat_col, y=num_col)
        elif plot_type == 'Violinplot':
            fig = px.violin(df_display, x=cat_col, y=num_col, box=True, points='all')
        elif plot_type == 'Barplot':
            grouped = df_display.groupby(cat_col)[num_col].mean().reset_index()
            fig = px.bar(grouped, x=cat_col, y=num_col)

        st.plotly_chart(fig, use_container_width=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/master/laptop_cleaning.csv')

# Run app
if __name__ == "__main__":
    df = load_data()
    app = BivariateAnalysis(df)
    app.column_vs_column_display()
