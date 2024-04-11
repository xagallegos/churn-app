import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(layout="wide")
st.title("Churn App")

dict_input = {}

col1, col2, col3, col4, col5 = st.columns(5)

# Numerical data
with col1:
    st.subheader('Service Costs:')
    dict_input['tenure'] = int(st.number_input('Tenure'))
    dict_input['MonthlyCharges'] = float(st.number_input('Monthly Charges'))
    dict_input['TotalCharges'] = float(st.number_input('Total Charges'))

with col2:
    st.subheader('Personal information:')
    gender = st.radio('Gender', ['Male', 'Female'])
    dict_input['gender_Female'] = True if gender == 'Female' else False
    dict_input['gender_Male'] = not dict_input['gender_Female']

    senior_citizens = st.checkbox('Senior Citizen')
    dict_input['SeniorCitizen'] = 1 if senior_citizens else 0

    partner = st.checkbox('Partner')
    dict_input['Partner_Yes'] = True if partner else False
    dict_input['Partner_No'] = not dict_input['Partner_Yes']

    dependents = st.checkbox('Dependents')
    dict_input['Dependents_Yes'] = True if dependents else False
    dict_input['Dependents_No'] = not dict_input['Dependents_Yes']

with col3:
    st.subheader('Phone service')
    phone_service = st.checkbox('Phone Service')
    dict_input['PhoneService_Yes'] = True if phone_service else False
    dict_input['PhoneService_No'] = not dict_input['PhoneService_Yes']

    multiple_lines = st.checkbox('Multiple phone lines', disabled=not phone_service)

    dict_input['MultipleLines_Yes'] = True if multiple_lines and phone_service else False
    dict_input['MultipleLines_No'] = True if not multiple_lines and phone_service else False
    dict_input['MultipleLines_No_phone_service'] = True if not phone_service else False

with col4:
    st.subheader('Internet service')
    internet_service = st.radio('Type of Internet Service', ['No service', 'DSL', 'Fiber Optic'])

    dict_input['InternetService_No'] = True if internet_service == 'No service' else False
    dict_input['InternetService_DSL'] = True if internet_service == 'DSL' else False
    dict_input['InternetService_Fiber_optic'] = True if internet_service == 'Fiber Optic' else False

    online_services = {}
    has_internet = True if internet_service != 'No service' else False

    online_services['OnlineSecurity'] = st.checkbox('Online Security', disabled=not has_internet)
    online_services['OnlineBackup'] = st.checkbox('Online Backup', disabled=not has_internet)
    online_services['DeviceProtection'] = st.checkbox('Device Protection', disabled=not has_internet)
    online_services['TechSupport'] = st.checkbox('Tech Support', disabled=not has_internet)
    online_services['StreamingTV'] = st.checkbox('Streaming TV', disabled=not has_internet)
    online_services['StreamingMovies'] = st.checkbox('Streaming Movies', disabled=not has_internet)

    for service, status in online_services.items():
        dict_input[f'{service}_Yes'] = True if status and has_internet else False
        dict_input[f'{service}_No'] = True if not status and has_internet else False
        dict_input[f'{service}_No_internet_service'] = True if not has_internet else False

with col5:
    st.subheader('Contract and Billing:')
    paperless = st.checkbox('Paperless Billing')
    dict_input['PaperlessBilling_Yes'] = True if paperless else False
    dict_input['PaperlessBilling_No'] = not dict_input['PaperlessBilling_Yes']

    contract = st.radio('Type of contract', ['Month to month', 'One year', 'Two year'])
    dict_input['Contract_Month_to_month'] = True if contract == 'Month to month' else False
    dict_input['Contract_One_year'] = True if contract == 'One year' else False
    dict_input['Contract_Two_year'] = True if contract == 'Two year' else False

    payment = st.radio('Payment method', ['Bank transfer', 'Credit card', 'Electronic check', 'Mailed check'])
    dict_input['PaymentMethod_Bank_transfer'] = True if payment == 'Bank transfer' else False
    dict_input['PaymentMethod_Credit_card'] = True if payment == 'Credit card' else False
    dict_input['PaymentMethod_Electronic_check'] = True if payment == 'Electronic check' else False
    dict_input['PaymentMethod_Mailed_check'] = True if payment == 'Mailed check' else False


df_input = pd.DataFrame(dict_input, index=[0])
st.divider()

cola, colb = st.columns([0.1,0.9])

with cola:
    pred = st.button('Predict')

with colb:
    if pred:
        url = 'http://churn-api:5000/api/v1/classify?api_key=ChurnModel-2024$*'
        payload = json.dumps(dict_input)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=payload)
        st.subheader(response.json()['prediction'])
