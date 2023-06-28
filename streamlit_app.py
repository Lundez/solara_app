from dataclasses import dataclass
import streamlit as st
import polars as pl
import plotly.express as px

def Page():
    st.markdown("# Streamlit Example App (Starbucks Data)")
    file = st.file_uploader("Upload a file")
    if file is not None:
        df = pl.read_csv(file, null_values="-").drop_nulls()
        DFViews(df)
    else:
        st.write("Make sure to upload a file")

@dataclass
class FilterValues:
    sodium: tuple[int, int]
    carb: tuple[int, int]

def Filters(df: pl.DataFrame) -> FilterValues:
    with st.form("df_filer"):
        st.write("**Filter DataFrame**")
        carbs = (df["Carb. (g)"].min(), df["Carb. (g)"].max())
        sodium = (df["Sodium"].min(), df["Sodium"].max())
        carbs = st.slider("Carb. (g)", min_value=carbs[0], max_value=carbs[1], value=carbs)
        sodium = st.slider("Sodium", min_value=sodium[0], max_value=sodium[1], value=sodium)
        
        st.form_submit_button("Submit")
    return FilterValues(sodium, carbs)

def FilteredPage(df: pl.DataFrame, filter_values: FilterValues):
    df = df.filter(pl.col("Sodium").is_between(filter_values.sodium[0], filter_values.sodium[1]) &
                   pl.col("Carb. (g)").is_between(filter_values.carb[0], filter_values.carb[1]))
    DFVis(df)

def DFVis(df: pl.DataFrame):
    st.markdown(f"## DataFrame")
    st.dataframe(df.to_pandas())
    st.write(px.histogram(df, x=["Carb. (g)", "Sodium"]))

def DFViews(df: pl.DataFrame):
    filters = Filters(df)
    c1, c2 = st.columns(2)
    with c1:
        DFVis(df)
    with c2:
        FilteredPage(df, filters)

Page()