import streamlit as st
import pandas as pd
#import balance_book
#import input_field
#import progress


#df = pd.DataFrame({
#  'first column': [1, 2, 3, 4],
#  'second column': [10, 20, 30, 40]
#})
#
#df

import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon=":simile:",
)

st.write("# Welcome to Money App! 👋")

st.sidebar.success("Select an item above.")

st.markdown(
    """
    Money Appは消費者が、使ったお金の集計・可視化をしてお金の使い過ぎを防ぐツールです。
"""
)

