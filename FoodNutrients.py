import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from pandas import json_normalize
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

DATA_URL = (
     'https://bitbucket.org/DanielleLaur/food_db/raw/4f223e4c1aa997fb02e6dc6f544a6cda4d283cd5/USDA_data_2020_wide152.csv'
 )
DATA_URL1 = (
     'https://bitbucket.org/DanielleLaur/food_db/raw/4f223e4c1aa997fb02e6dc6f544a6cda4d283cd5/openfood_data_clean_nodup.csv'
 )
DATA_URL2 = (
     'https://bitbucket.org/DanielleLaur/food_db/raw/4f223e4c1aa997fb02e6dc6f544a6cda4d283cd5/Fao_food_data_mod.csv'
     )
    
st.title("Food Nutrients")
## Put the logo image
img = 'nutrients.png'
st.sidebar.image(Image.open(img))
st.sidebar.subheader("About")
st.sidebar.markdown("This application can be used "
            "to find foods with highest or lowest content of some nutrients.")

st.header("Find Foods rich in some nutrients")
st.write("Are you looking for foods rich in Iron or Fiber or another nutrient?\nCheck out this!")

@st.cache_data
def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    return data

def convert():
    ''' convert the 100g of nutrient to your food weight'''
    nut = st.number_input("Enter the nutrient amount for 100g: ", 10)
    food = st.number_input("Enter the food weight: ", 20)

    return (nut*food)/100    


def print_data(data, L):

    st.header("Top 10 Foods")
    st.markdown("The barplot shows only the top 10, if you want more look at the table below.")
    select = st.selectbox('Select a compound', L)
    
    
    st.subheader("Top 10 Foods rich in %s" % (select)) 
    st.write("***Hover on a bar**")
    chart_data = data[['Product', select]]
    fig = px.bar(chart_data.sort_values(select, ascending=False).head(10), x=select, y='Product',
     labels = {"Product":"", select: select + ' (in 100g)'}, orientation='h', width=650)
    fig.update_yaxes(tickfont=dict(family='Rockwell', color='crimson', size=10))
    for data in fig.data:
        data["width"] = 0.15
           
    st.write(fig)
    cat_base = st.radio("Which type are you looking for?",
                        ('Foods rich', 'Foods poor')) 
    
    if cat_base == 'Foods rich':

        st.subheader("Table of Foods rich in %s" % (select))
        chart_data1 = chart_data.fillna(0).sort_values(select, ascending=False).head(10)
        fig1 = go.Figure(data=[go.Table(
            columnwidth = [150, 50],
        header=dict(values=list(chart_data1.columns),
                    fill_color='royalblue',
                    align='left',
                    font=dict(color='white', size=14)),
        cells=dict(values=[chart_data1.Product, chart_data1[select]],
                   fill_color='lavender',
                   align='left'))])
        st.write(fig1)
    #st.text('If your are you looking foods poor in that nutrient click below')
    else:
        st.subheader("Table of Foods poor in %s" % (select))
        chart_data1 = chart_data.fillna(0).sort_values(select, ascending=False).tail(10)
        fig2 = go.Figure(data=[go.Table(
            columnwidth = [150, 50],
        header=dict(values=list(chart_data1.columns),
                    fill_color='royalblue',
                    align='left',
                    font=dict(color='white', size=14)),
        cells=dict(values=[chart_data1.Product, chart_data1[select]],
                   fill_color='lavender',
                   align='left'))])
        st.plotly_chart(fig2)
                
    return 'Have fun!!'            


st.sidebar.markdown("## Search your nutrient")
data_base = st.sidebar.radio(
     "Select your database",
    ('USDA', 'OpenFood', 'FAO'))   

if data_base == 'USDA':
    us_data = load_data(DATA_URL)  
    st.write(print_data(us_data, [col for col in us_data.columns if col != 'Product']))
elif data_base == 'OpenFood':
    op_data = load_data(DATA_URL1)
    st.write(print_data(op_data, [col for col in op_data.columns if col not in ('Product', 'Quantity','Brands')]))    
else:
    fao_data = load_data(DATA_URL2)
    st.write(print_data(fao_data, [col for col in fao_data.columns if col != 'Product']))     


st.markdown("The amount reported is for 100g of food. "
                "If what you consume is not 100g calculate below the real amount")

res = convert()
if st.button('Calculate'):
    st.write('Your food contains %s g of this nutrient' % (res)) 


with st.sidebar.expander("*Data Sources*"):
     st.write(""" 
        - [USDA](https://ndb.nal.usda.gov/ndb/)  
        - [Openfood](https://world.openfoodfacts.org/)  
        - [Fao](http://www.fao.org/infoods/infoods/tables-and-databases/en/)
        
---
        """)    


st.write('''
    Note:  
    DVs are the recommended amounts of nutrients to consume or 
    not to exceed each day. The %DV is how much a nutrient in a single 
    serving of an individual packaged food or dietary supplement contributes 
    to your daily diet. Below is a table of DV of the most important nutrients according to the FDA.
    \n Are you looking for another nutrient? Check [here](https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels)''')

dv = pd.DataFrame({
     'Nutrients': ['Energy', 'Total fat', 'Saturated Fat', 'Carbohydrate', 
                   'Total sugars', 'Dietary Fiber', 'Protein', 'Salt'],
     'Daily Value': ['8400kJ/2000kcal', '65g', '20g', '300g', '90g', '25g',
                      '50g', '6g']})

tab = go.Figure(data=[go.Table(
                columnwidth = [50, 45],
            header=dict(values=list(dv.columns),
                        fill_color='darkslategray',
                        align='left',
                        font=dict(color='white', size=14)),
            cells=dict(values=[dv.Nutrients, dv['Daily Value']],
                       fill_color='white',
                       align='left'))])

st.write(tab)


st.sidebar.markdown('''
    -------
    By Danielle Taneyo  
    [Linkedin](https://www.linkedin.com/in/danielletaneyosaa/)''')
          
