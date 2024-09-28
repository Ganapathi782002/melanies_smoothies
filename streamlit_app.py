# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Input for name on order
name_on_order = st.text_input('Name on Smoothie ')
st.write('The name on your smoothie will be: ', name_on_order)

# Establish session
cnx = st.connection("snowflake")
session = cnx.session()

# Get available fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Select ingredients for the smoothie
ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe,max_selections = 5)

if ingredients_list:
    # Convert selected ingredients into a string
    ingredients_string = ' '

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    # Safely format the SQL insert statement
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{name_on_order}')"""

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    # Only proceed if 'Submit Order' is clicked
    if time_to_insert:
        # Execute the SQL insert statement
        session.sql(my_insert_stmt).collect()

        # Show success message
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
