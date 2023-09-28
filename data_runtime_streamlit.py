from datetime import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import sys
import os

from PIL import Image
from streamlit.runtime import get_instance
#from streamlit.web.server import Server
from streamlit.runtime.scriptrunner import get_script_run_ctx
from hreader_module.hreader import *

#get instance
runtime = get_instance()

#get run context
ctx = get_script_run_ctx()

#get session id
session_id = ctx.session_id

#get_session_info
session_info = runtime._session_mgr.get_session_info(session_id)
session = session_info.session

ROOT_FOLDER_CSV = r"\\192.168.0.23\shared\IBTEST_BCM901\CSV"
watched_files = os.listdir(ROOT_FOLDER_CSV)

# Keep the list in the session state
if 'number_of_failed' not in st.session_state: 
    st.session_state['number_of_failed'] = 0
    
if 'selection' not in st.session_state:
    st.session_state['selection'] = 0

logo = Image.open(".\Logo\iBtest.png")

#register_watcher
#for watched in watched_files:
session._local_sources_watcher._register_watcher(os.path.join(ROOT_FOLDER_CSV, r"1%c310.csv"), "C310")

st.title("Ejemplo de monitoreo de datos en tiempo real.")
st.sidebar.image(logo, width=250)
st.sidebar.header("Options")

#remove extensions
options = [os.path.splitext(watched)[0] for watched in watched_files]
option = st.sidebar.selectbox("Seleccione una prueba", options, index = st.session_state['selection'])

st.text(dt.now())

if option in options:
    st.header(option)
    df = pd.read_csv(os.path.join(f'{ROOT_FOLDER_CSV}', f'{option}.csv'), sep=",", decimal=".")
    
    fig = px.scatter(df, y=["measurement", "high_limit", "low_limit"])

    promedio = df["measurement"].mean()
    
    # if df["measurement"] < df["low_limit"] or df["measurement"] > df["low_limit"]:
    #     st.session_state.update["number_of_failures"] += 1
    #     st.write(f"failed: {st.session_state['number_of_failures']}")
    
    st.metric(label="Promedio", value=f'{promedio:.3e}')
    #st.line_chart(df, y=["measurement", "high_limit", "low_limit"])
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    st.subheader("Distribution")
    p = ff.create_distplot([df.loc[:,"measurement"]], group_labels=["measurement"], bin_size=[0.1])
    st.plotly_chart(p, use_container_width=True)
    
    st.subheader("Box Plot")
    box = px.box(df, y=["measurement", "high_limit", "low_limit"])
    st.plotly_chart(box, theme="streamlit", use_container_width=True)