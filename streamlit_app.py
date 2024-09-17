import streamlit as st
import snowflake.connector

# execute SF queries
def get_sf_dropdown_values(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetch_pandas_all()
        
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
          FrRoleValues = col1.multiselect(
          "Choose functional role(s)",
          (Dev_Func_Roles_Values),
          placeholder="roles you'd like to add to target project role",
          help="Choose functional roles you'd like to add to your project role"
          )
          PrjRoleValues = col2.selectbox(
          "Choose a target Project role",
          (Dev_Prj_Roles_Values),
          index=None,
          placeholder="role you'd like to add the additional access",
          help="Choose a target project tole that you'd like to add the additional access"
          )
       elif selected_requestType == 'Grant Functional/Project Role(s) to a Service Role':
          col3, col4 = st.columns(2)
          FrPrRoleValues = col3.multiselect(
          "Choose functional/project role(s)",
          (Dev_FR_PR_Values),
          )	  
          SvcRoleValues = col4.selectbox(
          "Choose a target Service Acct role",
          (Dev_Svc_Roles_Values),
          index=None,
          )
    elif selected_environment == 'TST':
       if selected_requestType == 'Grant Functional Role(s) to a Project Role':
          FrRoleValues = col1.multiselect(
          "Choose functional role(s)",
          (Tst_Func_Roles_Values),
          placeholder="roles you'd like to add to target project role",
          help="Choose functional roles you'd like to add to your project role"
          )
          PrjRoleValues = col2.selectbox(
          "Choose a target Project role",
          (Tst_Prj_Roles_Values),
          index=None,
          placeholder="role you'd like to add the additional access",
          help="Choose a target project tole that you'd like to add the additional access"
          )
       elif selected_requestType == 'Grant Functional/Project Role(s) to a Service Role':
          col3, col4 = st.columns(2)
          FrPrRoleValues = col3.multiselect(
          "Choose functional/project role(s)",
          (Tst_FR_PR_Values),
          )	  
          SvcRoleValues = col4.selectbox(
          "Choose a target Service Acct role",
          (Tst_Svc_Roles_Values),
          index=None,
          )
    elif selected_environment == 'PRD':
       if selected_requestType == 'Grant Functional Role(s) to a Project Role':
          FrRoleValues = col1.multiselect(
          "Choose functional role(s)",
          (Prd_Func_Roles_Values),
          placeholder="roles you'd like to add to target project role",
          help="Choose functional roles you'd like to add to your project role"
          )
          PrjRoleValues = col2.selectbox(
          "Choose a target Project role",
          (Prd_Prj_Roles_Values),
          index=None,
          placeholder="role you'd like to add the additional access",
          help="Choose a target project tole that you'd like to add the additional access"
          )
       elif selected_requestType == 'Grant Functional/Project Role(s) to a Service Role':
          col3, col4 = st.columns(2)
          FrPrRoleValues = col3.multiselect(
          "Choose functional/project role(s)",
          (Prd_FR_PR_Values),
          )	  
          SvcRoleValues = col4.selectbox(
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
        st.header('Form Responses')
        st.write("Environment(s): ", selected_environment)
        st.write("Type of Request: ", seelcted_requestType)
        # TODO add role options 
    
        st.write("Reason for Request: ", reasonForRequest)
