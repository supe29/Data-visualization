import streamlit as st
import plotly.express as px
import pandas as pd
import pycountry as pc
import pycountry_convert as pcc

drink = pd.read_csv("starbucks_drink.csv")
food = pd.read_csv("starbucks_food.csv")
st.title("Starbucks Growth strategy")

# data inputs
drink = pd.read_csv("starbucks_drink.csv")
food = pd.read_csv("starbucks_food.csv")
health = drink.merge(food, left_on='Calories', right_on='Protein (g)', how='left')
data = pd.read_csv('directory.csv')
consdata = pd.read_csv('CoffeeConsumption.csv')

# data clean
data['Brand'].value_counts().sort_values(ascending=False)
data = data.query('Brand == "Starbucks"')
data['Brand'].value_counts()
data.drop(axis=1, columns=['Store Number', 'Postcode', 'Phone Number', 'Timezone'], inplace=True)
data['Country'].value_counts().sort_values(ascending=False)
data['City'].value_counts().sort_values(ascending=False)
data['State/Province'].value_counts().sort_values(ascending=False)
data.query('Country == "US"')['State/Province'].value_counts().sort_values(ascending=False)
data.query('Country == "US"')['State/Province'].value_counts(normalize=True).apply(lambda x: x * 100).sort_values(
    ascending=False)
data['Country_ISO'] = data['Country']
data['Country'] = data['Country'].apply(lambda country: pc.countries.get(alpha_2=country).name)
data['Continent'] = data['Country_ISO'].apply(lambda country: pcc.country_alpha2_to_continent_code(country)).apply(
    lambda cont: pcc.convert_continent_code_to_continent_name(cont))

# consdata clean
consdata.rename(columns={"country": "Country", "totCons2019": "Total", "perCapitaCons2016": "PerCapita"}, inplace=True)
x = pd.DataFrame(data['Country'].value_counts().rename('Stores_count'))
x.reset_index(inplace=True)
x.rename(columns={'index': 'Country'}, inplace=True)
consdata = consdata.merge(x, on='Country')

fig1 = px.scatter_geo(data, lat='Latitude', lon='Longitude', hover_name='Store Name', size_max=10,
                      title='Starbucks locations worldwide')
st.write(fig1)

st.header('Starbucks Address and Store Name')
fg2_data = data.query('Country_ISO == "US"')
st.write(fg2_data)

st.header('No. of stores per country')
fg3_data = data['Country'].value_counts().rename('Counts')
fg3 = px.scatter_geo(fg3_data, locationmode='country names', locations=fg3_data.index, color='Counts',
                     hover_data=['Counts'], color_continuous_scale='RdBU')
st.write(fg3)

st.header('stores per state')
fg4_data = data.query('Country_ISO == "US"')['State/Province'].value_counts().rename('Counts')
fig3 = px.scatter_geo(fg4_data, locationmode='USA-states', locations=fg4_data.index, size='Counts', color='Counts',
                      hover_data=['Counts'], color_continuous_scale='RdBu', scope='usa',
                      title='No. of stores per state in United States')
st.write(fig3)

fig4 = px.histogram(data, x='Country', color='Ownership Type', labels={'count': 'No. of Stores'},
                    title='Ownership type per country', color_discrete_sequence=px.colors.qualitative.Pastel,
                    log_y=True).update_xaxes(categoryorder='total descending')
st.write(fig4)


st.header('calories consumption')

br_option = drink['Beverage'].unique().tolist()
Beverage = st.multiselect('Select Beverage?', br_option, default=["Coffee"])
drink = drink[drink['Beverage'].isin(Beverage)]
fig5 = px.bar(drink, x='Beverage', y='Calories')
st.write(fig5)

option = food['Food'].unique()
foodselect = st.multiselect('Select food?', option, default=["Plain Bagel"])
st.write(foodselect)
fooda = food[food['Food'].isin(foodselect)]
fig6 = px.bar(fooda, x='Food', y='Calories', color='Food')
st.write(fig6)

st.write(health)
option2= food['Food'].unique()
foodselect1 = st.multiselect('Select food u like?', option2, default=["8-Grain Roll"])
food1 = food[food['Food'].isin(foodselect1)]
fig7 = px.bar(food1, x='Food', y='Protein (g)', color='Food')
st.write(fig7)