# Import python packages
import streamlit as st
import snowflake.connector
import pandas as pd

# Write directly to the app
st.title(f"Customize Your Smoothie :balloon: {st.__version__}")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Input for name on order
name_on_order = st.text_input('Name on Smoothies:')
st.write('The name on your Smoothie will be:', name_on_order)

# -------------------------------
# Connect to Snowflake
# -------------------------------
sf = st.secrets["snowflake"]
import requests
cnx = snowflake.connector.connect(
    user=sf["user"],
    password=sf["password"],
    account=sf["account"],
    role=sf["role"],
    warehouse=sf["warehouse"],
    database=sf["database"],
    schema=sf["schema"],
    client_session_keep_alive=True
)

# Create a cursor
cur = cnx.cursor()

# Retrieve fruit options
cur.execute("SELECT FRUIT_NAME, SEARCH_ON FROM smoothies.public.fruit_options")
my_dataframe = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
st.dataframe(my_dataframe)
pd_df = my_dataframe 


# -------------------------------
# Smoothie order logic
# -------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients: ", 
    my_dataframe, 
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Ingredients selected:", ingredients_string)

    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (?, ?)
    """

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        cur.execute(my_insert_stmt, (ingredients_string, name_on_order))
        cnx.commit()
        st.success('Your Smoothie is ordered!')
    for fruit_chosen in ingredients_list :
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ',fruit_chosen, ' is ',search_on,'.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
        


# Close cursor and connection at the end
cur.close()
cnx.close()

