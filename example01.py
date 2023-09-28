import smtplib
import json
import requests
import streamlit as st

def get_chat_id(api_token):

    #api_token = '5669323375:AAGsoWz_itZlsOs4vFOF_QSl_gfmU43vUBs'

    url = f"https://api.telegram.org/bot{api_token}/getUpdates"

    print(url)
    print(json.dumps(requests.get(url).json(), indent=4))
    
def send_alert(alert_type):
    
    project_name = 'IBT_BCM901'
            
    if alert_type == "Email":
        st.warning('Sending email notification')


        from_address = 'angel.carreon@ibtest.com'
        to_address = 'cc.angel88@gmail.com'
        subject = f'Automatic alert from streamlit - {project_name}'
        message = f'Subject:{subject} \nUnusual number of failures detected while running production series.\n'
        message = f'{message}Project: IBT_BCM901\n'
        message = f'{message}Machine: ICT091\n'
        message = f'{message}Component: 1%C100, 1%C601\n'
        
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

            if err == {}:
                st.warning('Notification done')
            else:
                st.warning(err)

            server_gmail.quit()
        except smtplib.SMTPException as e:
            print(f'[ERROR] - {e}')
    else:
        st.warning('Sending Telegram notification')
            
        api_token = '5669323375:AAGsoWz_itZlsOs4vFOF_QSl_gfmU43vUBs'
        
        get_chat_id(api_token)
        
        chat_id = '5212122181'
        chat_id_group = '-837331912'
        
        subject = f'Automatic alert from streamlit - {project_name}'
        message = f'Subject: {subject} \n\nUnusual number of failures detected while running production series.\n\n'
        message = f'{message}Project: IBT_BCM901\n'
        message = f'{message}Machine: ICT091\n'
        message = f'{message}Component: 1:C100, 1:C601\n'
        #message = message.encode('utf-8')
        
        url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chat_id_group}&text={message}"
        response = requests.get(url).json() # this sends the message
        print(response)
        if response['ok'] == True:
            st.warning('Sending Telegram notification')
        else:
            st.error('Error in sending Telegram notification')
        
        
st.selectbox("choose an option", ['opcion 1', 'option 2', 'option 3'])

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A1")
    st.write("This is A1")

with col2:
    st.header("A2")
    st.write("This is A2")

with col3:
    st.header("A2")
    st.write("This is A2")
    
st.selectbox("choose an option2", ['opcion 1', 'option 2', 'option 3'])

st.header("Condiciones de falla")

column1, column2 = st.columns(2)

with column1:
    st.slider("Failure", min_value=0, max_value=100)

with column2:
    alert_type = st.selectbox("Alert type",['Email', 'Telegram'])
        
    st.button("Send Alert", on_click=send_alert, args=[alert_type], type="primary")