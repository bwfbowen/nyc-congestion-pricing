import os
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from taxi import taxi
# from citibike import citibike

def heatmap(pre_start, pre_end, post_start, post_end, start, end, origin, destination, plot, data, clear): 
    
    public = "../frontend/public"
    
    if clear:
        # Load the zip code shapefile
        zipcodes = gpd.read_file('zipcodes/zipcodes.shp')
        
        # Create a folium map centered on NYC
        m = folium.Map(location=[40.7128, -74.0060])
        
        # Add the zip code boundaries to the map
        folium.GeoJson(
            zipcodes,
            name="Zipcodes",
            style_function=lambda x: {
                'fillColor': 'white',
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.25
            },
            tooltip=folium.GeoJsonTooltip(fields=["modzcta"], aliases=["Zipcode:"])  # Replace 'modzcta' with the column for zip codes
        ).add_to(m)
        
        # Add a layer control to toggle the zip codes layer
        folium.LayerControl().add_to(m)

        # Save the map
        file_name = os.path.join(public, "map.html")
        m.save(file_name)
        
        plt.figure(figsize=(10, 6))
        plt.title("Empty Time Distribution")
        plt.xlabel("Duration (minutes)")
        plt.ylabel("Number of Trips")
        plt.xlim(0, 24)  # Assuming 24-hour time scale
        plt.ylim(0, 1)   # Empty y-axis
        distribution_file = os.path.join(public, "time.png")
        plt.savefig(distribution_file)
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.title("Empty Scatter Plot")
        plt.xlabel("Distance (miles)")
        plt.ylabel("Average Duration (minutes)")
        plt.xlim(0, 24)  # Assuming 24-hour time scale
        plt.ylim(0, 1)   # Empty y-axis
        scatter_file = os.path.join(public, "scatter.png")
        plt.savefig(scatter_file)
        plt.close()
    
        return file_name, distribution_file, scatter_file
    
    else: 
        if data == "taxi": 
            taxi(pre_start, pre_end, post_start, post_end, start, end, origin, destination, plot)
            
        # elif data == "citibike": 
        #     citibike(pre_start, pre_end, post_start, post_end, start, end, origin, destination, plot)