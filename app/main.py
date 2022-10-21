import streamlit as st
import os
import pandas as pd
import numpy as np

DATA_PATH = "../beijing.csv"
CSS_PATH = "style.css"
st.set_page_config(layout="wide")  # Page layout

# Load css from file (for custom css)
with open(CSS_PATH) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)  # Enable caching of data
def load_data(DATA_PATH, sep, encoding):  # Load data to dataframe and return it
    if os.path.exists(DATA_PATH) and encoding !="" and sep != "":
        data = pd.read_csv(DATA_PATH, sep=sep, encoding=encoding)
        return data
    else:
        st.error("Error while loading csv file!")

data = load_data(DATA_PATH=DATA_PATH, sep=',', encoding='iso-8859-1')  # Load data via function

st.title("Housing prices beijing")
st.write("Link to the Kaggle page: [Dataset](https://www.kaggle.com/datasets/ruiqurm/lianjia)")

st.markdown("---")
st.markdown("## Map visualization")
Mapdata = data.copy()  # Copy of original data
Mapdata = Mapdata[["Lng", "Lat", "price"]]  # Select only for map important data
Mapdata.rename(columns={"Lng":"longitude", "Lat":"latitude"} ,inplace=True)
if st.checkbox("Show map data"):
    st.write(Mapdata)  # Print data
st.map(Mapdata)
st.markdown("---")