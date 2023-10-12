from datetime import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import requests
import json
import smtplib
import os

from PIL import Image
from streamlit.runtime import get_instance
#from streamlit.web.server import Server
from streamlit.runtime.scriptrunner import get_script_run_ctx
from hreader_module.hreader import *

def get_chat_id(api_token):

    #api_token = '5669323375:AAGsoWz_itZlsOs4vFOF_QSl_gfmU43vUBs'
    url = f"https://api.telegram.org/bot{api_token}/getUpdates"

    print(url)
    print(json.dumps(requests.get(url).json(), indent=4))
    
def send_alert(alert_type):
    
    project_name = st.session_state.selected_project
    machine_name = st.session_state.selected_machine
            
    if alert_type.lower() == "email":
        st.warning('Sending email notification')
        
        max_fails_reached = st.session_state["max_fails"] 

        component = st.session_state.selected_component.replace("%", ":")

        from_address = 'cc.angel88@gmail.com'
        to_address = 'angel.carreon@ibtest.com'
        
        subject = f'Alert automatic from streamlit - {project_name}'
        message = f'Subject: {subject} \n{max_fails_reached} critical failures detected while running production series.\n\n'
        message = f'{message}  Project: {project_name}\n\n'
        message = f'{message}  Machine: {machine_name}\n\n'
        message = f'{message}Component: {component}\n\n'
        
        username = 'angel.carreon@ibtest.com'
        password = 'programacion2'

        try:
            server_gmail = smtplib.SMTP('smtp.gmail.com:587')
            server_gmail.starttls()
            reply = server_gmail.login(username, password)
            
            if reply[0] == 235:
                print('Authentication successfull.')
            
            elif reply[0] == 503:
                print('Already Authenticated.')
            
            err = server_gmail.sendmail(from_address, to_address, message)
            print(err)
            
            server_gmail.quit()
            if err == {}:
                return True
            else:
                return err

        except smtplib.SMTPException as e:
            return (f'[ERROR] - {e}')
    else:
        st.success('Sending Telegram notification')
            
        api_token = '5669323375:AAGsoWz_itZlsOs4vFOF_QSl_gfmU43vUBs'
        
        get_chat_id(api_token)
        
        chat_id = '5212122181'
        chat_id_group = '-837331912'
        
        max_fails_reached = st.session_state["max_fails"] 
        
        component = st.session_state.selected_component.replace("%", ":")
        
        message = f'{max_fails_reached} critical failures detected while running production series.\n\n'
        message = f'{message}  Project: {project_name}\n'
        message = f'{message}  Machine: {machine_name}\n'
        message = f'{message}Component: {component}\n'
        #message = message.encode('utf-8')
        
        url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chat_id_group}&text={message}"
        response = requests.get(url).json() # this sends the message
        print(response)
        if response['ok'] == True:
            return True
        else:
           return 'Error in sending Telegram notification'
        
def raise_failure(alert_type):
    if 'number_of_failed' not in st.session_state: 
        st.session_state['number_of_failed'] = 1
    else:
        st.session_state['number_of_failed'] += 1

    if st.session_state['number_of_failed'] >= st.session_state['max_fails']:

        res = send_alert(alert_type)
        if res == True:
            st.success("Max number of failures reached. Notification sent.", icon="✅")
            
            st.session_state.selected = 1
            st.session_state['max_failures'] = st.session_state.selected
            st.session_state['number_of_failed'] = 0
            
        else:
            st.error(res)
            
failures = {}
option = ''
#get instance
runtime = get_instance()

#get run context
ctx = get_script_run_ctx()

#get session id
session_id = ctx.session_id

#get_session_info
session_info = runtime._session_mgr.get_session_info(session_id)
session = session_info.session

ROOT_FOLDER_CSV = r"./IBTEST01/CSV"
watched_files = os.listdir(ROOT_FOLDER_CSV)

# Keep the list in the session state
if 'number_of_failed' not in st.session_state: 
    st.session_state['number_of_failed'] = 0
    
if 'selection' not in st.session_state:
    st.session_state['selection'] = 0
    
if 'max_fails' not in st.session_state:
    st.session_state['max_fails'] = -1

logo = Image.open(r"./assets/iBtest.png")

#register_watcher
#for watched in watched_files:
session._local_sources_watcher._register_watcher(os.path.join(ROOT_FOLDER_CSV, r"1%c310.csv"), "C310")

st.title("Alerts and Realtime monitoring example app.")
st.sidebar.image(logo, width=250)
st.sidebar.header("Options")


st.sidebar.selectbox("Project Name", options=["IBT_BCM09", "IBT_KEY01", "IBT_K4120", "IBT_T23"], index=0, key="selected_project")
st.sidebar.selectbox("Machine Name", options=["ICT21", "ICT22", "ICT23", "ICT24"], index=0, key="selected_machine")
st.sidebar.text("Select Max failures to send alert.")
st.sidebar.selectbox("Number of failures", list(range(1,11)), key="selected")

alert_type = st.sidebar.selectbox("Alert type",['Telegram', 'Email'])

st.session_state["max_fails"] = st.session_state.selected

#remove extensions
options = [os.path.splitext(watched)[0] for watched in watched_files]
#st.session_state['selected_component'] = st.sidebar.selectbox("Seleccione una prueba", options, index = st.session_state['selection'], key='selected_component')
st.sidebar.selectbox("Select a component Test", options, index = st.session_state['selection'], key='selected_component')
option = st.session_state.selected_component

st.text(dt.now())
button = st.button("Simulate Failure.", on_click=raise_failure, type="primary", args=[alert_type])
st.metric("Number of failures", st.session_state['number_of_failed'])

if option in options:
    st.header(option)
    df = pd.read_csv(os.path.join(f'{ROOT_FOLDER_CSV}', f'{option}.csv'), sep=",", decimal=".")
    
    fig = px.scatter(df, y=["measurement", "high_limit", "low_limit"])

    promedio = df["measurement"].mean()
    st.metric(label="Promedio", value=f'{promedio:.3e}')
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    st.subheader("Distribution")
    p = ff.create_distplot([df.loc[:,"measurement"]], group_labels=["measurement"], bin_size=[0.1])
    st.plotly_chart(p, use_container_width=True)
    
    st.subheader("Box Plot")
    box = px.box(df, y=["measurement", "high_limit", "low_limit"])
    st.plotly_chart(box, theme="streamlit", use_container_width=True)