import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

class UnivariateAnalysis:

    def __init__(self, df):
        self.df = df
        self.selected_column = None
        self.selected_plot_type = None
        self.rows = 5

    def display(self):
        st.title("📊 Univariate Analysis")
        st.write("This app performs univariate analysis on a selected column of the dataset.")
        
        column_type = st.selectbox('Select column type', ['Numeric', 'Categorical'])

        st.write("### Data Preview")
        if column_type == 'Numeric':
            numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            if not numeric_cols.empty:
                self.selected_column = st.selectbox("Select a numeric column", numeric_cols)
                st.write(self.df[self.selected_column].describe())
        else:
            self.rows = st.number_input("Number of rows to display", min_value=1, max_value=len(self.df), value=5)
            cat_cols = self.df.select_dtypes(include=['object']).columns
            if not cat_cols.empty:
                self.selected_column = st.selectbox("Select a categorical column", cat_cols)
                st.write(self.df[self.selected_column].value_counts().head(self.rows))

        if self.selected_column:
            st.write("### Plot Preview")
            self.generate_plot(column_type)

    def generate_plot(self, column_type):
        fig, ax = plt.subplots()
        if column_type == 'Numeric':
            self.selected_plot_type = st.selectbox(
                "Select plot type", ["Histogram", "Boxplot", "Lineplot", "Scatterplot", "Density"]
            )
            if self.selected_plot_type == "Histogram":
                sns.histplot(self.df[self.selected_column], bins=30, ax=ax)
            elif self.selected_plot_type == "Boxplot":
                sns.boxplot(x=self.df[self.selected_column], ax=ax)
            elif self.selected_plot_type == "Lineplot":
                sns.lineplot(y=self.df[self.selected_column], x=self.df.index, ax=ax)
            elif self.selected_plot_type == "Scatterplot":
                sns.scatterplot(x=self.df.index, y=self.df[self.selected_column], ax=ax)
            elif self.selected_plot_type == "Density":
                sns.kdeplot(self.df[self.selected_column], ax=ax)
        else:
            self.selected_plot_type = st.selectbox(
                "Select plot type", ["Countplot", "Pie chart", "Barplot"]
            )
            data_counts = self.df[self.selected_column].value_counts().head(self.rows)
            if self.selected_plot_type == "Countplot":
                sns.countplot(x=self.df[self.selected_column], order=data_counts.index, ax=ax)
            elif self.selected_plot_type == "Pie chart":
                fig, ax = plt.subplots()
                ax.pie(data_counts.values, labels=data_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
                st.pyplot(fig)
                return  # Don't call st.pyplot() again below
            elif self.selected_plot_type == "Barplot":
                sns.barplot(x=data_counts.index, y=data_counts.values, ax=ax)

        ax.set_title(f"{self.selected_plot_type} of {self.selected_column}")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        st.pyplot(fig)

# Run app
if __name__ == "__main__":
    df = pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')
    univariate_analysis = UnivariateAnalysis(df)
    univariate_analysis.display()
