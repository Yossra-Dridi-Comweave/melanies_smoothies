
# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
# Write directly to the app
st.title(f"Customize Your Smoothie :balloon: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """
)

# import streamlit as st
name_on_order  = st.text_input('Name on Smoothies:')
st.write('The name on your Smoothie will be:', name_on_order)
# option= st.selectbox(
#     'What is your favorite fruit?',('Banana', 'Strawberries', 'Peaches')
# )
# st.write('Your favorite fruit is', option)

import streamlit as st
import snowflake.connector

# Récupérer les secrets
sf = st.secrets["snowflake"]

# Connexion Snowflake
cnx = snowflake.connector.connect(
    user=sf["user"],
    password=sf["password"],
    account=sf["account"],
    role=sf["role"],
    warehouse=sf["warehouse"],
    database=sf["database"],
    schema=sf["schema"],
    client_session_keep_alive=sf["client_session_keep_alive"]
)

# Ici on crée la "session" pour exécuter les requêtes
session = cnx.cursor()

# Exemple d'utilisation
session.execute("SELECT CURRENT_DATE;")
date = session.fetchone()[0]

st.write("Connexion réussie ! Date actuelle : ", date)

# N'oublie pas de fermer le curseur et la connexion à la fin
session.close()
cnx.close()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").to_pandas()
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect("Choose up to 5 ingredients: ", my_dataframe["FRUIT_NAME"].tolist(), max_selections=5)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen
    st.write(ingredients_string) 
    my_insert_stmt = """insert into smoothies.public.orders (ingredients,name_on_order) values ('""" + ingredients_string+ """','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!')
        
