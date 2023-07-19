import streamlit as st
import requests
import json


#startup directions:
#https://docs.streamlit.io/knowledge-base/using-streamlit/how-do-i-run-my-streamlit-script
#streamlit run finch_project.py

#function for the dispay after a company is chosen
def master_direct(auth):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Company Directory")
        comp_directory()


    with col2:
        st.header("Company")
        company_direct(auth)


    with col3:
        st.header("Employee")
        employee_buttons(auth)

#Function for the data that is used to create the buttons found in employee_buttons(auth)
def employee_direct(auth):
    headers = {
        "Finch-API-Version": "2020-09-17",
        'Authorization':'Bearer' +' '+ auth,
        'Accept': 'application/json',
        }

    response = requests.get('https://sandbox.tryfinch.com/api/employer/directory', headers=headers)
    return response.json()


#Function for the data that is seen under the 'Individual Information'
def ind_employee(auth,emp_id):
    url = "https://sandbox.tryfinch.com/api/employer/individual"
    payload = { "requests": [ { "individual_id": emp_id }] }
    headers = {
    "Finch-API-Version": "2020-09-17",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer" + ' ' + auth
}

    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    json_to_string = (json.dumps(response).replace('null', '"No Data"'))
    response = json.loads(json_to_string)
    return response

#Function for the data that is seen under the 'Employee Information'
def emp_employee(auth,emp_id):
    url = "https://sandbox.tryfinch.com/api/employer/employment"

    payload = { "requests": [{ "individual_id": emp_id}] }
    headers = {
        "Finch-API-Version": "2020-09-17",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer"  + ' ' + auth
        }

    response = requests.post(url, json=payload, headers=headers)

    response = response.json()
    json_to_string = (json.dumps(response).replace('null', '"No Data"'))
    response = json.loads(json_to_string)
    return response

#Function for company information after a button is picked on the previous step
def company_direct(auth):
    headers = {
        "Finch-API-Version": "2020-09-17",
        'Authorization': 'Bearer' + ' ' + auth,
        'Accept': 'application/json',
        }

    response = requests.get('https://sandbox.tryfinch.com/api/employer/company', headers=headers)
    response = response.json()
    json_to_string = (json.dumps(response).replace('null', '"No Data"'))
    response = json.loads(json_to_string)
    for (k,v) in response.items():
       st.markdown(f'<h1 style="color:#FFBF00;font-size:16px">{k}</h1>', unsafe_allow_html=True)
       Json_parse(v)
    return

#Flattens the Json. Does this based on conditionals(sub-lists/sub-dics). Returns a custom message if a 501 error is found
def Json_parse(input):
    if isinstance(input,list):
        for x in range(len(input)):
            for (h,p) in input[x].items():
                st.write(h + ':' + ' '+ str(p))
    elif isinstance(input,dict):
         for (l,m) in input.items():
             st.write(l + ':' + ' ' +str(m))
    else:
         st.write(input)
         if str(input) == '501':
             st.error('This is an error: https://developer.tryfinch.com/docs/reference/1f80003f67f0d-error-types', icon="🚨")

    return


#Function to display what is seen when an employee is selected from the directory. incorporates f strings so that the data is more readable(color/font-size)
def employee_information(index,auth,emp_id):
    employee = employee_direct(auth)
    raw_json = employee['individuals'][index]
    json_to_string = (json.dumps(raw_json).replace('null', '"No Data"'))
    employee_list = json.loads(json_to_string)

    ind_data = ind_employee(auth,emp_id)
    emp_data = (emp_employee(auth,emp_id))
    #make columns that are seen after an employee is selected
    col1, col2, col3, col4 = st.columns(4,gap = "large")
    with col1:
        st.header("Company Directory")
        comp_directory()
    with col2:
        st.header("Company")

        company_direct(auth)
    with col3:
        st.header("Individual Information")
        for (k,v) in ind_data['responses'][0]['body'].items():
            st.markdown(f'<h1 style="color:#DE3163;font-size:16px">{k}</h1>', unsafe_allow_html=True)
            Json_parse(v)
    with col4:
        st.header("Employee Information")
        for (k,v) in emp_data['responses'][0]['body'].items():
           st.markdown(f'<h1 style="color:#CCCCFF;font-size:16px">{k}</h1>', unsafe_allow_html=True)
           Json_parse(v)
    return


#Function for employee button creation
def employee_buttons(auth):
    employee_list = employee_direct(auth)
    for x in range(len(employee_list['individuals'])):
        #parses the JSON to create a button with the employee name + add onlick_click function based on the auth token/position
        st.button(employee_list['individuals'][x]['first_name'] + ' ' + employee_list['individuals'][x]['last_name'] ,key =employee_list['individuals'][x]['id'], on_click = employee_information,args=(x,auth,employee_list['individuals'][x]['id'],),kwargs=None,
    disabled=False)


    return

#function to get access token based on company that is chosen and passes token to the master_direct function
def get_auth(provider_id):
    headers = {
    'Content-Type': 'application/json',
}

    json_data = {
    'provider_id': provider_id,
    'products': [
        'company',
        'directory',
        'individual',
        'employment'
    ],
    'employee_size': 10,
    }

    response = requests.post('https://sandbox.tryfinch.com/api/sandbox/create', headers=headers, json=json_data)
    response = response.json()
    return master_direct(response['access_token'])



#create a new key everytime a company directory is picked. Use this key for other api endpoints until a different company directory is chosen/page reloaded.
def comp_directory():
        bamboohr_b = st.button('bamboohr', key = 'bamboohr',on_click = get_auth,args=("bamboo_hr",),kwargs=None,
    disabled=False)
        justworks_b = st.button('justworks', key = 'justworks',on_click = get_auth,args=("justworks",),kwargs=None,
    disabled=False)
        paychex_flex_b = st.button('paychex_flex', key = 'paychex_flex',on_click = get_auth,args=("paychex_flex",),kwargs=None,
    disabled=False)
        workday_b = st.button('workday', key = 'workday',on_click = get_auth,args=("workday",),kwargs=None,
    disabled=False)
        gusto_b = st.button('gusto', key = 'gusto',on_click = get_auth,args=("gusto",),kwargs=None,
    disabled=False)

        return


#initialization using session_state. Initial screen that is seen
if 's_counter' not in st.session_state:
    st.session_state['s_counter'] = 0



if (st.session_state['s_counter'] <1):
    col1, col2, col3= st.columns(3)
    with col1:
        st.header("Company Directory")
        comp_directory()


    with col2:
        st.header("Company")


    with col3:
        st.header("Employee")
    st.session_state['s_counter'] += 1
