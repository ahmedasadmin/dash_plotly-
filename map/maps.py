import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from colorcet import fire, kbc, bmw, gray
import plotly.express as px

df = pd.read_csv("Crimes_-_2001_to_Present.csv")
dff = df[['Primary Type', 'Latitude', 'Longitude']]
print(dff['Primary Type'].unique())
dff = dff[dff['Primary Type'].isin(['PROSTITUTION'])]
dff.dropna(subset=['Latitude', 'Longitude'], inplace=True)
print(dff.shape)


cvs = ds.Canvas(plot_width=1000, plot_height=1000)
aggs = cvs.points(dff, x='Longitude', y='Latitude')
coords_lat, coords_lon = aggs.coords['Latitude'].values, aggs.coords['Longitude'].values


coordinates = [[coords_lon[0], coords_lat[0]],
               [coords_lon[-1], coords_lat[0]],
               [coords_lon[-1], coords_lat[-1]],
               [coords_lon[0], coords_lat[-1]]]
img = tf.shade(aggs, cmap=fire, how='eq_hist', alpha=255)[::-1].to_pil()
fig = px.scatter_mapbox(dff[:1], lat='Latitude', lon='Longitude', zoom=10)
fig.update_layout(mapbox_style="carto-darkmatter",
                  mapbox_layers=[
                      {
                    "sourcetype": "image",
                    "source": img,
                    "coordinates": coordinates
                      }
                  ]
)
fig.show()