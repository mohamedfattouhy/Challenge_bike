import folium
import webbrowser
import json
import pandas as  pd
import altair as alt
from altair import Chart, load_dataset
import numpy as np
import requests, zipfile, io


# Import data
zip_file_url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_Archives.zip"
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("")


# Create a dataframe from location
df_cd = pd.DataFrame(np.array([[43.60969924926758, 3.896939992904663], 
                        [43.5907, 3.81324], [43.61465, 3.8336], [43.57926, 3.93327],
                        [43.6157418, 3.9096322], [43.6138841, 3.8684671]]),
                         columns=['lon', 'lat'])



# Read json files
with open('MMM_EcoCompt_X2H19070220_Archive2020.json') as f:
        j1 = json.loads("[" + 
        f.read().replace("}\n{", "},\n{") + "]")
with open('MMM_EcoCompt_X2H20042632_Archive2020.json') as f:
        j2 = json.loads("[" + 
        f.read().replace("}\n{", "},\n{") + "]")
with open('MMM_EcoCompt_X2H20042633_Archive2020.json') as f:
        j3 = json.loads("[" + 
        f.read().replace("}\n{", "},\n{") + "]")
with open('MMM_EcoCompt_X2H20042634_Archive2020.json') as f:
        j4 = json.loads("[" + 
        f.read().replace("}\n{", "},\n{") + "]")
with open('MMM_EcoCompt_X2H20063161_Archive2020.json') as f:
        j5 = json.loads("[" + 
        f.read().replace("}\n{", "},\n{") + "]")
with open('MMM_EcoCompt_X2H20063162_Archive2020.json') as f:
        j6 = json.loads("[" + 
        f.read().replace("}\n{", "},\n{") + "]")





df_1 = pd.DataFrame.from_dict(j1)
df_1 = df_1.drop(columns = ['laneId', 'location', 'id', 'type', 'vehicleType', 'reversedLane'])
df_1['dateObserved'] = pd.Series(df_1['dateObserved'], dtype="string")

# Other point
df_2 = pd.DataFrame.from_dict(j2)
df_2 = df_2.drop(columns = ['laneId', 'location', 'id', 'type', 'vehicleType', 'reversedLane'])
df_2['dateObserved'] = pd.Series(df_2['dateObserved'], dtype="string")

df_3 = pd.DataFrame.from_dict(j3)
df_3 = df_3.drop(columns = ['laneId', 'location', 'id', 'type', 'vehicleType', 'reversedLane'])
df_3['dateObserved'] = pd.Series(df_3['dateObserved'], dtype="string")

df_4 = pd.DataFrame.from_dict(j4)
df_4 = df_4.drop(columns = ['laneId', 'location', 'id', 'type', 'vehicleType', 'reversedLane'])
df_4['dateObserved'] = pd.Series(df_4['dateObserved'], dtype="string")

df_5 = pd.DataFrame.from_dict(j5)
df_5 = df_5.drop(columns = ['laneId', 'location', 'id', 'type', 'vehicleType', 'reversedLane'])
df_5['dateObserved'] = pd.Series(df_5['dateObserved'], dtype="string")


df_6 = pd.DataFrame.from_dict(j6)
df_6 = df_6.drop(columns = ['laneId', 'location', 'id', 'type', 'vehicleType', 'reversedLane'])
df_6['dateObserved'] = pd.Series(df_6['dateObserved'], dtype="string")



def formatting(df):

    for i in range(df.shape[0]):
        df.loc[i, 'dateObserved'] = df.loc[i, 'dateObserved'][:10]

    return df


df_1 = formatting(df_1)
df_1['dateObserved'] = pd.to_datetime(df_1['dateObserved'])
df_1 = df_1.rename(columns={"intensity": "Intensity_bike"})
dg_1 = df_1.groupby(pd.Grouper(key='dateObserved', freq='1M')).sum()


# Other point
df_2 = formatting(df_2)
df_2['dateObserved'] = pd.to_datetime(df_2['dateObserved'])
df_2 = df_2.rename(columns={"intensity": "Intensity_bike"})
dg_2 = df_2.groupby(pd.Grouper(key='dateObserved', freq='1M')).sum()

df_3 = formatting(df_3)
df_3['dateObserved'] = pd.to_datetime(df_3['dateObserved'])
df_3 = df_3.rename(columns={"intensity": "Intensity_bike"})
dg_3 = df_3.groupby(pd.Grouper(key='dateObserved', freq='1M')).sum()

df_4 = formatting(df_4)
df_4['dateObserved'] = pd.to_datetime(df_4['dateObserved'])
df_4 = df_4.rename(columns={"intensity": "Intensity_bike"})
dg_4 = df_4.groupby(pd.Grouper(key='dateObserved', freq='1M')).sum()


df_5 = formatting(df_5)
df_5['dateObserved'] = pd.to_datetime(df_5['dateObserved'])
df_5 = df_5.rename(columns={"intensity": "Intensity_bike"})
dg_5 = df_5.groupby(pd.Grouper(key='dateObserved', freq='1M')).sum()

df_6= formatting(df_6)
df_6['dateObserved'] = pd.to_datetime(df_6['dateObserved'])
df_6 = df_6.rename(columns={"intensity": "Intensity_bike"})
dg_6 = df_6.groupby(pd.Grouper(key='dateObserved', freq='1M')).sum()


tooltip = "Click me!"

# Create map
m = folium.Map(location=[df_cd.iloc[0, 0], df_cd.iloc[0, 1]], zoom_start=12.5, tiles='OpenStreetMap', 
control_scale=True, attr="My attr")


# Create a circle on map

folium.CircleMarker(
    location=[df_cd.iloc[0, 0], df_cd.iloc[0, 1]],
    radius=60,
    popup="Hi, i'm X2H19070220 counter, you can see what i've recorded, enjoy ! \n Information: 1009 bikes pass here on average per day !",
    color="red",
    fill=True,
    fill_color="#e41a1c",
    tooltip=tooltip
).add_to(m)

# Other point

folium.CircleMarker(
    location=[df_cd.iloc[1, 0],df_cd.iloc[1, 1]],
    radius=35,
    popup="Hi, i'm X2H20042632 counter, you can see what i've recorded, enjoy ! \n Information: 221 bikes pass here on average per day !",
    color="blue",
    fill=True,
    fill_color="blue",
    tooltip=tooltip
).add_to(m)


folium.CircleMarker(
    location=[df_cd.iloc[2, 0],df_cd.iloc[2, 1]],
    radius=48,
    popup="Hi, i'm X2H20042633 counter, you can see what i've recorded, enjoy ! \n Information: 583 bikes pass here on average per day !",
    color="purple",
    fill=True,
    fill_color="purple",
    tooltip=tooltip
).add_to(m)


folium.CircleMarker(
    location=[df_cd.iloc[3, 0],df_cd.iloc[3, 1]],
    radius=20,
    popup="Hi, i'm X2H20042634 counter, you can see what i've recorded, enjoy ! \n Information: 98 bikes pass here on average per day !",
    color="green",
    fill=True,
    fill_color="green",
    tooltip=tooltip
).add_to(m)


folium.CircleMarker(
    location=[df_cd.iloc[4, 0], df_cd.iloc[4, 1]],
    radius=30,
    popup="Hi, i'm X2H20063161 counter, you can see what i've recorded, enjoy ! \n Information: 206 bikes pass here on average per day !",
    color="black",
    fill=True,
    fill_color="black",
    tooltip=tooltip
).add_to(m)



folium.CircleMarker(
    location=[df_cd.iloc[5, 0], df_cd.iloc[5, 1]],
    radius=55,
    popup="Hi, i'm X2H20063162 counter, you can see what i've recorded, enjoy ! \n Information: 925 bikes pass here on average per day !",
    color="orange",
    fill=True,
    fill_color="orange",
    tooltip=tooltip
).add_to(m)



# Create graphs

base = (alt.Chart(df_1, title="This is an (interactive) flux of trafic bicycle").mark_line()
.encode(alt.X('dateObserved', axis=alt.Axis(title='Date')),
alt.Y('Intensity_bike', axis=alt.Axis(title='Intensity')))
.configure_mark(opacity=0.8, color='red').properties(width=600, height=300).interactive())


vega = folium.features.VegaLite(base, width=700, height=50)
graph_popup = folium.Popup()  # Create a popup
vega.add_to(graph_popup)  # Add graph to popup
marker = folium.features.Marker([df_cd.iloc[0, 0], df_cd.iloc[0, 1]], icon=folium.Icon(color='white', icon='bicycle', icon_color="red", prefix='fa')).add_to(m)
graph_popup.add_to(marker)
marker.add_to(m)



# Other point

base = (alt.Chart(df_2, title="This is an (interactive) bicycle flow").mark_line()
.encode(alt.X('dateObserved', axis=alt.Axis(title='Date')),
alt.Y('Intensity_bike', axis=alt.Axis(title='Number of bikes')))
.configure_mark(opacity=0.8, color='blue').properties(width=600, height=300).interactive())
 
vega = folium.features.VegaLite(base, width=700, height=50)
graph_popup = folium.Popup()  # Create a popup
vega.add_to(graph_popup)  # Add graph to popup
marker = folium.features.Marker([df_cd.iloc[1, 0],df_cd.iloc[1, 1]], icon=folium.Icon(color='white', icon='bicycle', icon_color="blue", prefix='fa')).add_to(m)
graph_popup.add_to(marker) 
marker.add_to(m)


base = (alt.Chart(df_3, title="This is an (interactive) bicycle flow").mark_line()
.encode(alt.X('dateObserved', axis=alt.Axis(title='Date')),
alt.Y('Intensity_bike', axis=alt.Axis(title='Number of bikes')))
.configure_mark(opacity=0.8, color='purple').properties(width=600, height=300).interactive())


vega = folium.features.VegaLite(base, width=700, height=50)
graph_popup = folium.Popup()  # Create a popup
vega.add_to(graph_popup)  # Add graph to popup
marker = folium.features.Marker([df_cd.iloc[2, 0],df_cd.iloc[2, 1]], icon=folium.Icon(color='white', icon='bicycle', icon_color="purple", prefix='fa')).add_to(m)
graph_popup.add_to(marker)
marker.add_to(m)


base = (alt.Chart(df_4, title="This is an (interactive) bicycle flow").mark_line()
.encode(alt.X('dateObserved', axis=alt.Axis(title='Date')),
alt.Y('Intensity_bike', axis=alt.Axis(title='Number of bikes')))
.configure_mark(opacity=0.8, color='green').properties(width=600, height=300).interactive())


vega = folium.features.VegaLite(base, width=700, height=50)
graph_popup = folium.Popup()  # Create a popup
vega.add_to(graph_popup)  # Add graph to popup
marker = folium.features.Marker([df_cd.iloc[3, 0],df_cd.iloc[3, 1]],icon=folium.Icon(color='white', icon='bicycle', icon_color="green", prefix='fa')).add_to(m)
graph_popup.add_to(marker)
marker.add_to(m)


base = (alt.Chart(df_5, title="This is an (interactive) bicycle flow").mark_line()
.encode(alt.X('dateObserved', axis=alt.Axis(title='Date')),
alt.Y('Intensity_bike', axis=alt.Axis(title='Number of bikes')))
.configure_mark(opacity=0.8, color='black').properties(width=600, height=300).interactive())


vega = folium.features.VegaLite(base, width=700, height=50)
graph_popup = folium.Popup()  # Create a popup
vega.add_to(graph_popup)  # Add graph to popup
marker = folium.features.Marker([df_cd.iloc[4, 0],df_cd.iloc[4, 1]], icon=folium.Icon(color='white', icon='bicycle', icon_color="black", prefix='fa')).add_to(m)
graph_popup.add_to(marker)
marker.add_to(m)


base = (alt.Chart(df_6, title="This is an (interactive) bicycle flow").mark_line()
.encode(alt.X('dateObserved', axis=alt.Axis(title='Date')),
alt.Y('Intensity_bike', axis=alt.Axis(title='Number of bikes')))
.configure_mark(opacity=0.8, color='orange').properties(width=600,height=300).interactive())


vega = folium.features.VegaLite(base, width=700, height=50)
graph_popup = folium.Popup()  # Create a popup
vega.add_to(graph_popup)  # Add graph to popup
marker = folium.features.Marker([df_cd.iloc[5, 0],df_cd.iloc[5, 1]], icon=folium.Icon(color='white', icon='bicycle', icon_color="orange", prefix='fa')).add_to(m)
graph_popup.add_to(marker)
marker.add_to(m)

# Linking markers
my_Polygone = folium.Polygon(locations=df_cd, weight=4, color='yellow', opacity=1)
m.add_child(my_Polygone)



folium.TileLayer(
    tiles='Stamen Terrain', name='Stamen Terrain', show=True
).add_to(m)
folium.TileLayer(
    tiles='cartodb positron', name='cartodb positron', show=True
).add_to(m)
folium.TileLayer(  
    tiles="stamentonerbackground", name="stamentoner background", show=True
).add_to(m)



# Add a title

title_html = '''
             <h3 align="center" style="color:purple;background-color:#2AAE67;font-size:210%"> <b>Montpellier's bicycle counters</b> </h3>
             '''
m.get_root().html.add_child(
    folium.Element(title_html)
)


folium.LayerControl().add_to(m)


# Save and display the map

m.save("map.html")
webbrowser.open("map.html")
