
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
import pandas as pd

# Récupérer les secrets
sf = st.secrets["snowflake"]

# Connexion
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

# Créer un curseur
cur = cnx.cursor()

# Exécuter une requête SQL pour récupérer les données
cur.execute("SELECT * FROM smoothies.public.fruit_options")

# Mettre dans un DataFrame pandas
my_dataframe = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

st.dataframe(my_dataframe)

# Fermer curseur et connexion
cur.close()
cnx.close()



#session = get_active_session()
#my_dataframe = session.table("smoothies.public.fruit_options").to_pandas()
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
        
