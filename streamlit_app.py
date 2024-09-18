import streamlit as st
import snowflake.connector
import json

# execute SF queries
def get_sf_dropdown_values(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetch_pandas_all()

def get_request_id(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchone()[0]

def insert_submitted_form_timestamp(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
    
# open snowflake connection
conn = snowflake.connector.connect(**st.secrets["snowflake"])

# populate dropdown values from SF queries - TODO insert more queries

# Dev Roles
sql = "select name from FR_ROLES where name ilike '%_dev_%' UNION SELECT 'OTHER' ORDER BY 1 "
Dev_Func_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES  where name ilike '%_dev_%' ORDER BY 1"
Dev_Prj_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES  where name ilike '%_dev_%' UNION SELECT name from FR_ROLES   where name ilike '%_dev_%' UNION SELECT 'OTHER' ORDER BY 1 "
Dev_FR_PR_Values = get_sf_dropdown_values(sql)

sql = "select name from SVC_ROLES  where name ilike '%_dev_%'  UNION SELECT 'OTHER' ORDER BY 1 "
Dev_Svc_Roles_Values = get_sf_dropdown_values(sql)

# Tst Roles
sql = "select name from FR_ROLES where name ilike '%_tst_%'  UNION SELECT 'OTHER' ORDER BY 1 "
Tst_Func_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES  where name ilike '%_tst_%' ORDER BY 1"
Tst_Prj_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES   where name ilike '%_tst_%' UNION SELECT name from FR_ROLES  where name ilike '%_tst%_' UNION SELECT 'OTHER' ORDER BY 1 "
Tst_FR_PR_Values = get_sf_dropdown_values(sql)

sql = "select name from SVC_ROLES where name ilike '%_tst%_' UNION SELECT 'OTHER' ORDER BY 1 "
Tst_Svc_Roles_Values = get_sf_dropdown_values(sql)

# Prod Roles
sql = "select name from FR_ROLES where name ilike '%_prd_%'  UNION SELECT 'OTHER' ORDER BY 1 "
Prd_Func_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES  where name ilike '%_prd_%' ORDER BY 1"
Prd_Prj_Roles_Values = get_sf_dropdown_values(sql)

sql = "select name from PRJ_ROLES   where name ilike '%_prd_%' UNION SELECT name from FR_ROLES  where name ilike '%_prd_%' UNION SELECT 'OTHER' ORDER BY 1 "
Prd_FR_PR_Values = get_sf_dropdown_values(sql)

sql = "select name from SVC_ROLES where name ilike '%_prd_%' UNION SELECT 'OTHER' ORDER BY 1 "
Prd_Svc_Roles_Values = get_sf_dropdown_values(sql)

# close snowflake connection
conn.close()

# create form
st.header('Snowflake Role Request Form')

selected_environment = st.selectbox(
   "Environment(s)",
   ["DEV", "TST", "PRD"],
   index=None,
   key='db_env'
)

selected_requestType = st.selectbox(
   "Type of Request",
   ("Grant Functional Role(s) to a Project Role", "Grant Functional/Project Role(s) to a Service Role", "Revoke Functional Role(s) from a Project Role", "Grant Functional/Project Role(s) from a Service Role"),
   index=None,
   key='reqtyp'
)


with st.form("form1", clear_on_submit = True):

    col1, col2 = st.columns(2)

    if selected_environment == 'DEV':
       if selected_requestType == 'Grant Functional Role(s) to a Project Role':
          Selected_Source_Values = col1.multiselect(
          "Choose functional role(s)",
          (Dev_Func_Roles_Values),
          placeholder="roles you'd like to add to target project role",
          help="Choose functional roles you'd like to add to your project role"
          )
          Selected_Target_Values = col2.selectbox(
          "Choose a target Project role",
          (Dev_Prj_Roles_Values),
          index=None,
          placeholder="role you'd like to add the additional access",
          help="Choose a target project tole that you'd like to add the additional access"
          )
       elif selected_requestType == 'Grant Functional/Project Role(s) to a Service Role':
          col3, col4 = st.columns(2)
          Selected_Source_Values = col3.multiselect(
          "Choose functional/project role(s)",
          (Dev_FR_PR_Values),
          )	  
          Selected_Target_Values = col4.selectbox(
          "Choose a target Service Acct role",
          (Dev_Svc_Roles_Values),
          index=None,
          )
    elif selected_environment == 'TST':
       if selected_requestType == 'Grant Functional Role(s) to a Project Role':
          Selected_Source_Values = col1.multiselect(
          "Choose functional role(s)",
          (Tst_Func_Roles_Values),
          placeholder="roles you'd like to add to target project role",
          help="Choose functional roles you'd like to add to your project role"
          )
          Selected_Target_Values = col2.selectbox(
          "Choose a target Project role",
          (Tst_Prj_Roles_Values),
          index=None,
          placeholder="role you'd like to add the additional access",
          help="Choose a target project tole that you'd like to add the additional access"
          )
       elif selected_requestType == 'Grant Functional/Project Role(s) to a Service Role':
          col3, col4 = st.columns(2)
          Selected_Source_Values = col3.multiselect(
          "Choose functional/project role(s)",
          (Tst_FR_PR_Values),
          )	  
          Selected_Target_Values = col4.selectbox(
          "Choose a target Service Acct role",
          (Tst_Svc_Roles_Values),
          index=None,
          )
    elif selected_environment == 'PRD':
       if selected_requestType == 'Grant Functional Role(s) to a Project Role':
          Selected_Source_Values = col1.multiselect(
          "Choose functional role(s)",
          (Prd_Func_Roles_Values),
          placeholder="roles you'd like to add to target project role",
          help="Choose functional roles you'd like to add to your project role"
          )
          Selected_Target_Values = col2.selectbox(
          "Choose a target Project role",
          (Prd_Prj_Roles_Values),
          index=None,
          placeholder="role you'd like to add the additional access",
          help="Choose a target project tole that you'd like to add the additional access"
          )
       elif selected_requestType == 'Grant Functional/Project Role(s) to a Service Role':
          col3, col4 = st.columns(2)
          Selected_Source_Values = col3.multiselect(
          "Choose functional/project role(s)",
          (Prd_FR_PR_Values),
          )	  
          Selected_Target_Values = col4.selectbox(
          "Choose a target Service Acct role",
          (Prd_Svc_Roles_Values),
          index=None,
          )


    reasonForRequest = st.text_area(
        "Reason for Request",
        "Please enter a brief description here",
    )

    # TODO - add validation to enforce mandatory fields
    submit = st.form_submit_button("Submit")

    
    # print form responses
    if submit:
        #"Environment: ""DEV"
        #formResponses="Environment:" + str(selected_environment) + "  \n Type of Request:" + str(selected_requestType) + "  \n Selected Source Roles:" + str(Selected_Source_Values)[1:-1] + "  \n Selected Target Roles:" +  str(Selected_Target_Values) + "  \n Reason for Request:" + str(reasonForRequest) 
        #formResponses= "\"" + "Environment " + "\":" + "\"" + str(selected_environment) + "\"" 
        #+ "  \n Type of Request:" + str(selected_requestType) + "  \n Selected Source Roles:" + str(Selected_Source_Values)[1:-1] 
        #                + "  \n Selected Target Roles:" +  str(Selected_Target_Values) + "  \n Reason for Request:" + str(reasonForRequest) 
        
        #formResponses = { "selected_environment" : selected_environment , "selected_requestType" : selected_requestType }
        
        formResponses = { "Environment" : selected_environment , "Type of Request" : selected_requestType , "Selected Source Roles" : Selected_Source_Values[1:-1] , "Selected Target Roles" : Selected_Target_Values ,  "Reason for Request" : reasonForRequest }
        formResponsesStr = json.dumps(formResponses)
        st.write(formResponsesStr)
        # open snowflake connection
        conn = snowflake.connector.connect(**st.secrets["snowflake"])

        # insert new form submitted timestamp to table
        #parse_json(formResponses)

        #sql = "INSERT INTO form_submissions1 (request_id, form_submitted_timestamp) VALUES ( request_id_seq.nextval,DEFAULT)"
        #insert_submitted_form_timestamp(sql)

        
        #sql = "INSERT INTO form_submissions2 (request_id, req_env) select request_id_seq.nextval, " + "'" + selected_environment + "'"
        #insert_submitted_form_timestamp(sql)

        #sql = "INSERT INTO form_submissions (request_id, form_resp) select request_id_seq.nextval, " + "'" + formResponses + "'"
        sql = "INSERT INTO form_submissions3 (form_resp) select parse_json(' " +  formResponsesStr + "')"
        insert_submitted_form_timestamp(sql)
        
        # obtain new request_id sequence
        #sql = "SELECT request_id FROM form_submissions ORDER BY form_submitted_timestamp DESC LIMIT 1"
        #formId = get_request_id(sql)
    
        # close snowflake connection
        conn.close()

        st.header('Form Responses')
        st.write(formResponses)
        #st.write("Environment(s): ", selected_environment)
        #st.write("Type of Request: ", selected_requestType)
        #st.write("Selected Source Roles: ", str(Selected_Source_Values)[1:-1])
        #st.write("Selected Target Roles: ", Selected_Target_Values)
        #st.write("Reason for Request: ", reasonForRequest)
