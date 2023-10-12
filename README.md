# streamlit-app-ict-realtime
Streamlit application to show realtime alerts in Telegram and gmail.

## Clone the repositoru

````
git clone https://github.com/angel88c/streamlit-app-ict-realtime
````

go to the folder

## Setup

Create a virtual environment with the command:

```
python -m venv env
```
env will be our virtual environment

Install the requirements:

```
pip install -r requirements.txt
```

Once installed requirements, Proceed to setup the base of Telegram bot and gmail.

## Setup Telegram bot
To set up the telegram bot, follow next useful guide in order to create the bot, and generate our **api_token** and **chat_id_group**

https://www.shellhacks.com/python-send-message-to-telegram/#:~:text=To%20send%20a%20message%20to,API%20and%20send%20the%20message.

https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token

replace your api_token number got in api_token variable, and replace your chat_id_group with yur number obtained. 

```python
    api_token = 'YYYYYYYYYY:ZZZZZ'
        
    get_chat_id(api_token)
        
    chat_id_group = '-XXXXXXXXX'
        
    max_fails_reached = st.session_state["max_fails"] 
```

## Setup Email service
To set up the email service, follow next useful guide in order to create the automated service.

[https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/](https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/)


You need to enable less secure apps permissions to your web browser, access from here: [myaccount.google.com/lesssecureapps](myaccount.google.com/lesssecureapps)


Set the source and destination gmail account in order to setup the service.

```python
from_address = '<your_source_address>88@gmail.com'
to_address = '<your_destination_address>@ibtest.com'
    
subject = f'Alert automatic from streamlit - {project_name}'
message = f'Subject: {subject} \n{max_fails_reached} critical failures detected while running production series.\n\n'
message = f'{message}  Project: {project_name}\n\n'
message = f'{message}  Machine: {machine_name}\n\n'
message = f'{message}Component: {component}\n\n'
```


Finally, you can run the application with command: 

```
streamlit run data_runtime_streamlit.py
```

this will open a new web browser window with the app running on it.

Select the type of notification alert to send, Email or Telegram.

Select the Project name and machine name in the sidebar, and also select the maximum number of failures that will cause the notifications send.

![streamlit_runtime_app](/assets/streamlit_realtime_app.png "App running").


The Simulate Failures will increment the number of failures and when this number of failures reach the Maximum number of failures set, the notification will be sent via Email or Telegram depending on the selected type of alert.

Enjoy!
