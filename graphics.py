import streamlit as st
import pandas as pd
import numpy as np

c1, c2 = st.columns(2)

with c1:
    chart_data = pd.DataFrame({
        "col1": list(range(20))*3,
        "col2": np.random.randn(60),
        "col3": ["A"]*20 + ["B"]*20 + ["C"]*20,
    })
    
    #print(list(range(20))*3)
    #print(np.random.randn(60))
    #print(["A"]*30)
    
    st.write(chart_data)
    st.bar_chart(chart_data, x="col1", y="col2", use_container_width=False)
    