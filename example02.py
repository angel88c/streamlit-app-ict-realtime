import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import os
import json
import streamlit as st
import orm_sqlite
from datetime import datetime as dt

class ICT_Data(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)
    part_number = orm_sqlite.StringField()
    serial_number = orm_sqlite.StringField()
    status = orm_sqlite.IntegerField()
    field_data = orm_sqlite.StringField()
    created_date = orm_sqlite.StringField()


from PIL import Image
from streamlit.runtime import get_instance
#from streamlit.web.server import Server
from streamlit.runtime.scriptrunner import get_script_run_ctx
from hreader_module.hreader import *

def has_valid_format(file: str):
    
    if ".ds_store" in file.lower():
        return False
    
    if os.path.isdir(file):
        return False
    
    data_read = ''
    with open(file, mode='r') as f:
        data_read = f.read()
        print("***")
        print(data_read)
        print("***")
        
    if "batch" in data_read.lower():
        return True
    
    return False

#get instance
runtime = get_instance()

#get run context
ctx = get_script_run_ctx()

#get session id
session_id = ctx.session_id

#get_session_info
session_info = runtime._session_mgr.get_session_info(session_id)
session = session_info.session

ROOT_FOLDER = r"/Users/c_angel/Documents/python/Shared/IBTEST01"
watched_files = os.listdir(ROOT_FOLDER)

# Keep the list in the session state
if 'number_of_failed' not in st.session_state: 
    st.session_state['number_of_failed'] = 0
    
if 'selection' not in st.session_state:
    st.session_state['selection'] = 0

logo = Image.open(r"./Logo/iBtest.png")

#register_watcher
#for watched in watched_files:
session._local_sources_watcher._register_watcher(os.path.join(ROOT_FOLDER, r"BASE_SERIAL001"), "BASE_SERIAL")

st.title("Monitoreo de datos en tiempo real.")
st.sidebar.image(logo, width=250)
st.sidebar.header("Options")

#remove extensions
serial_numbers = []
for watched in watched_files:
    
    complete_file = os.path.join(ROOT_FOLDER, watched)
    
    if has_valid_format(complete_file):
        data = get_btests(complete_file)
        #print(json.dumps(data, indent=4))
        serial_numbers.append(data[0][0]["id"])
        

options = serial_numbers#[os.path.splitext(watched)[0] for watched in watched_files]
options.sort()
option = st.sidebar.selectbox("Seleccione una prueba", options, index = st.session_state['selection'])

st.text(dt.now())

database_file = "/Users/c_angel/Documents/python/python-sqlite/test_streamlit_database.db"
db = orm_sqlite.Database(database_file)
ICT_Data.objects.backend = db

objects = ICT_Data.objects.all()
st.table(objects)

if option in options:
#    st.header(option)
    
    tests = get_all_tests(os.path.join(ROOT_FOLDER, f'BASE_{option}'))
    #json_string = json.dumps(tests)
    
    #print(tests)
    #test_status = 0
    #for test in tests:
    #    if not evaluate_test(test["measurement"], test["high_limit"], test["low_limit"]):
    #        test_status = 6 #Failed in analogs
    st.write(tests)
    #replace_in_file(new_file, r'%STATUS%', f'{test_status:02d}')
    
    #Insert data to database
    #database_file = "/Users/c_angel/Documents/python/python-sqlite/test_streamlit_database.db"
    #db = orm_sqlite.Database(database_file)
    
    #ICT_Data.objects.backend = db
    
    #ict_data = {
    #    "part_number": "NP001",
    #    "serial_number": serial_number,
    #    "status": (1 if test_status == 0 else 0),
    #    "field_data": json_string,
    #    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    #}
    #ICT_Data.objects.add(ict_data)
    #print("Created data")
    
    #update_files(tests)
#    #df = pd.read_csv(os.path.join(f'{ROOT_FOLDER}', f'{option}.csv'), sep=",", decimal=".")
#    
#    fig = px.scatter(df, y=["measurement", "high_limit", "low_limit"])
#
#    promedio = df["measurement"].mean()
#    
#    # if df["measurement"] < df["low_limit"] or df["measurement"] > df["low_limit"]:
#    #     st.session_state.update["number_of_failures"] += 1
#    #     st.write(f"failed: {st.session_state['number_of_failures']}")
#    
#    st.metric(label="Promedio", value=f'{promedio:.3e}')
#    #st.line_chart(df, y=["measurement", "high_limit", "low_limit"])
#    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#    
#    st.subheader("Distribution")
#    p = ff.create_distplot([df.loc[:,"measurement"]], group_labels=["measurement"], bin_size=[0.1])
#    st.plotly_chart(p, use_container_width=True)
#    
#    st.subheader("Box Plot")
#    box = px.box(df, y=["measurement", "high_limit", "low_limit"])
#    st.plotly_chart(box, theme="streamlit", use_container_width=True)