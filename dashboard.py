
#Importing the libraries

import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import locale
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Upload e load of excel file Adidas.xlsx

df = pd.read_excel("dataset/Adidas.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('adidas-logo.jpg')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)
html_title = """
    <style>
    .title-test{
        font-weight:bold;
        padding:5px
        border-radius:6px
    }
    </style>
    <center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)
    
col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Ultima atualização: \n {box_date}")

# Build First Graphic bar 
with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales": "Total Vendas {$}"},
                 title="Total Vendas no Varejo", hover_data=["TotalSales"],
                 template="gridon",height=500)
    st.plotly_chart(fig,use_container_width=True)
    
_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")
    
#Build Second Graphic Line
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", title="Total Vendas Por Data", template="gridon")
    st.plotly_chart(fig1,use_container_width=True)
with view2:
    expander =st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")

st.divider()

#Build Third Graphic Bar and Scatter
result1 = df.groupby(by="State")[["TotalSales","UnitsSold"]].sum().reset_index()

# Add the units sold as a line chart on a secondary y-axis

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode="lines",
                          name="Units Sold", yaxis="y2"))
fig3.update_layout(
    title = "Total Vendas e Unidades Vendidas por Estado",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying = "y", side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1)
)
_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5,0.45,0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data= result1.to_csv().encode("utf-8"),
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

#Building Fourth Graphic Treemap

_, col7 = st.columns([0.1,1])
treemap = df[["Region","City","TotalSales"]].groupby(by= ["Region","City"])["TotalSales"].sum().reset_index()
def format_sales(value):
    if value >=0:
       return '{:.2f} Lakh'.format(value / 1_000_00)
    
treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)
fig4 = px.treemap(treemap, path=["Region","City"], values="TotalSales",
                  hover_name= "TotalSales (Formatted)",
                  hover_data=["TotalSales (Formatted)"],
                  color= "City", height= 700, width= 600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4,use_container_width=True)
    
_, view4, dwn4 = st.columns([0.1,0.45,0.45])
with view4:
    result2 = df[["Region","City","TotalSales"]].groupby(by=["Region","City"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("Get Data", data= result2.to_csv().encode("utf-8"),
                       file_name="Sales_by_Region.csv", mime="text/csv")

st.divider()

#Building Fifth Graphic folium Map

geolocator = Nominatim(user_agent="adidas_sales_dashboard")
_, col8 = st.columns([0.1, 1])
state_sales = df.groupby("State")[["TotalSales", "UnitsSold"]].sum().reset_index()

states_coords = {
    "Alabama": {"lat": 32.806671, "lng": -86.791130},
    "Alaska": {"lat": 61.370716, "lng": -152.404419},
    "Arizona": {"lat": 33.729759, "lng": -111.431221},
    "Arkansas": {"lat": 34.969704, "lng": -92.373123},
    "California": {"lat": 36.116203, "lng": -119.681564},
    "Colorado": {"lat": 39.059811, "lng": -105.311104},
    "Connecticut": {"lat": 41.597782, "lng": -72.755371},
    "Delaware": {"lat": 39.318523, "lng": -75.507141},
    "Florida": {"lat": 27.766279, "lng": -81.686783},
    "Georgia": {"lat": 33.040619, "lng": -83.643074},
    "Hawaii": {"lat": 21.094318, "lng": -157.498337},
    "Idaho": {"lat": 44.299782, "lng": -114.742040},
    "Illinois": {"lat": 40.636770, "lng": -89.398528},
    "Indiana": {"lat": 40.051270, "lng": -85.602364},
    "Iowa": {"lat": 41.125370, "lng": -98.268082},
    "Kansas": {"lat": 38.526600, "lng": -96.726486},
    "Kentucky": {"lat": 37.668140, "lng": -84.670067},
    "Louisiana": {"lat": 31.169546, "lng": -91.867805},
    "Maine": {"lat": 44.693947, "lng": -69.381927},
    "Maryland": {"lat": 39.063946, "lng": -76.802101},
    "Massachusetts": {"lat": 42.230171, "lng": -71.530106},
    "Michigan": {"lat": 43.326618, "lng": -84.536095},
    "Minnesota": {"lat": 45.694454, "lng": -93.900192},
    "Mississippi": {"lat": 32.741646, "lng": -89.678696},
    "Missouri": {"lat": 36.716402, "lng": -93.009202},
    "Montana": {"lat": 46.921925, "lng": -110.454353},
    "Nebraska": {"lat": 41.125370, "lng": -98.268082},
    "Nevada": {"lat": 38.313515, "lng": -117.055374},
    "New Hampshire": {"lat": 43.452492, "lng": -71.563896},
    "New Jersey": {"lat": 40.298904, "lng": -74.521011},
    "New Mexico": {"lat": 34.840515, "lng": -106.248482},
    "New York": {"lat": 40.712776, "lng": -74.005974},
    "North Carolina": {"lat": 35.630066, "lng": -79.806419},
    "North Dakota": {"lat": 47.528912, "lng": -99.784012},
    "Ohio": {"lat": 40.388783, "lng": -82.764915},
    "Oklahoma": {"lat": 35.565342, "lng": -96.928917},
    "Oregon": {"lat": 44.299782, "lng": -114.742040},
    "Pennsylvania": {"lat": 40.590752, "lng": -77.209755},
    "Rhode Island": {"lat": 41.680893, "lng": -71.511780},
    "South Carolina": {"lat": 33.656293, "lng": -80.008774},
    "South Dakota": {"lat": 43.045754, "lng": -94.478828},
    "Tennessee": {"lat": 35.630066, "lng": -79.806419},
    "Texas": {"lat": 31.968598, "lng": -99.901813},
    "Utah": {"lat": 40.113555, "lng": -111.863011},
    "Vermont": {"lat": 44.045876, "lng": -72.710686},
    "Virginia": {"lat": 36.821336, "lng": -75.711751},
    "Washington": {"lat": 47.400902, "lng": -121.490494},
    "West Virginia": {"lat": 38.491226, "lng": -80.954903},
    "Wisconsin": {"lat": 43.075970, "lng": -89.831000},
    "Wyoming": {"lat": 42.755966, "lng": -107.302490}
}

# Criando um mapa de vendas por estado
map_center = [39.8283, -98.5795]  # Defina o centro do mapa com uma latitude/longitude centralizada (pode ser em São Paulo por exemplo)
with col8:
    m = folium.Map(location=map_center, zoom_start=5)

    # Adicionando círculos no mapa para representar vendas por estado e incluindo pop-up com as informações
    for index, row in state_sales.iterrows():
        location = geolocator.geocode(row["State"] + " USA", timeout=5)  # Ajuste na busca pela geolocalização
        if location:
            # Pop-up com as informações de vendas
            popup_text = f"Estado: {row['State']}<br>Total Sales: ${row['TotalSales']:,}<br>Units Sold: {row['UnitsSold']}"
            
            folium.Circle(
                location=[location.latitude, location.longitude],
                radius=row["TotalSales"] / 1000,  # Ajuste o raio conforme necessário
                color="blue",
                fill=True,
                fill_color="blue",
                popup=popup_text  # Adicionando o pop-up
            ).add_to(m)

    st.subheader(":point_right: Total Sales for States in the Map")
    st_folium(m, width=700, height=500)
    
_, view4, dwn4 = st.columns([0.5,0.45,0.45])
with view4:
    result4 = df[["Region","State","City","TotalSales"]].groupby(by=["Region","State"])["TotalSales"].sum().reset_index()
    expander = st.expander("View data for Total Sales by Region and States")
    expander.write(result4)
with dwn4:
    st.download_button("Get Data", data= result4.to_csv().encode("utf-8"),
                       file_name="Total_Sales_Region_States.csv", mime="text/csv")


    