import os
import pandas as pd
import pyarrow.parquet as pq
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import numpy as np
import glob
from codes import codes

def taxi(pre_start, pre_end, post_start, post_end, start, end, origin, destination, plot):
    public = "../frontend/public"
    
    origin_filter = codes.get(origin.lower(), set())
    destination_filter = codes.get(destination.lower(), set())

    def load(start_date, end_date):
        start_day, start_month, start_year = map(int, start_date.split("-"))
        end_day, end_month, end_year = map(int, end_date.split("-"))

        lst = [] 
        
        for year in range(start_year, end_year + 1):
            for month in range(start_month, end_month + 1):
                
                month_directory = f"processed/{year}/{month:02}"
                
                if not os.path.exists(month_directory):
                    continue
                
                files = glob.glob(os.path.join(month_directory, "*.parquet"))
                if not files:
                    continue
                
                for file in files: 
                    df = pq.read_table(file).to_pandas()
                    df = df[(df["pickup"].dt.day >= start_day) & (df["pickup"].dt.day <= end_day)]
                    df = df[(df["pickup"].dt.hour >= start) & (df["pickup"].dt.hour <= end)] 
                    df = df[df["origin"].isin(origin_filter) & df["destination"].isin(destination_filter)] 
                    lst.append(df) 
                    
            if lst: 
                data = pd.concat(lst, ignore_index=True)
            else: 
                data = pd.DataFrame() 
            return data

    pre_data = load(pre_start, pre_end)
    post_data = load(post_start, post_end)

    pre_data["duration"] = (pre_data['dropoff'] - pre_data['pickup']).dt.total_seconds() / 60
    post_data["duration"] = (post_data['dropoff'] - post_data['pickup']).dt.total_seconds() / 60

    nyc = gpd.read_file("taxi_zones/taxi_zones.shp")
    nyc = nyc.to_crs("EPSG:4326")
    
    key = "destination" if plot == "destination" else "origin"

    zone_names = {}
    name_columns = [col for col in nyc.columns if any(term in col.lower() for term in ['name', 'zone', 'borough'])]
    if name_columns:
        zone_names = dict(zip(nyc["LocationID"], nyc[name_columns[0]]))

    pre_counts = pre_data[key].value_counts().rename("pre_count")
    post_counts = post_data[key].value_counts().rename("post_count")

    diff_counts = post_counts.sub(pre_counts, fill_value=0).reset_index()
    diff_counts.columns = [key, "difference"]

    taxi_zones = nyc[["LocationID", "geometry"]].rename(columns={"LocationID": key})
    diff_counts = diff_counts.merge(taxi_zones, on=key, how="left")

    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12.5)

    gdf = gpd.GeoDataFrame(diff_counts, geometry="geometry")

    folium.Choropleth(
        geo_data=gdf,
        name="Difference Heatmap",
        data=gdf,
        columns=[key, "difference"],
        key_on=f"feature.properties.{key}",
        fill_color="RdYlGn_r",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Difference in Taxi Trips", 
    ).add_to(m)

    heatmap_file = os.path.join(public, "map.html")
    m.save(heatmap_file)
    
    top_zones = pd.concat([
        pre_data[key].value_counts().head(5),
        post_data[key].value_counts().head(5)
    ]).index.unique()[:5]  
    
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs = axs.flatten()
    bins = np.arange(0, 100, 5)
    width = 2
    
    axs[0].bar(bins[:-1], np.histogram(pre_data["duration"], bins=bins)[0], 
            width=width, alpha=0.7, label="Pre-Congestion Pricing", color="blue", align="edge")
    axs[0].bar(bins[:-1] + width, np.histogram(post_data["duration"], bins=bins)[0], 
            width=width, alpha=0.7, label="Post-Congestion Pricing", color="red", align="edge")
    
    axs[0].set_xlabel("Duration (minutes)")
    axs[0].set_ylabel("Number of Trips")
    axs[0].set_title("Overall Trip Distribution")
    axs[0].set_xticks(bins[::2])
    axs[0].legend()
    
    for i, zone_id in enumerate(top_zones):
        zone_name = zone_names.get(zone_id, f"Zone {zone_id}")
        
        pre_zone = pre_data[pre_data[key] == zone_id]
        post_zone = post_data[post_data[key] == zone_id]
        
        axs[i+1].bar(bins[:-1], np.histogram(pre_zone["duration"], bins=bins)[0], 
                   width=width, alpha=0.7, label="Pre-Congestion Pricing", color="blue", align="edge")
        axs[i+1].bar(bins[:-1] + width, np.histogram(post_zone["duration"], bins=bins)[0], 
                   width=width, alpha=0.7, label="Post-Congestion Pricing", color="red", align="edge")
        
        axs[i+1].set_xlabel("Duration (minutes)")
        axs[i+1].set_ylabel("Number of Trips")
        axs[i+1].set_title(f"{zone_name}")
        axs[i+1].set_xticks(bins[::2])
        axs[i+1].legend()
    
    for i in range(len(top_zones)+1, len(axs)):
        axs[i].set_visible(False)
    
    plt.tight_layout()
    time_dist_file = os.path.join(public, "time.png")
    plt.savefig(time_dist_file)
    plt.close()
    
    pre_average_time = pre_data.groupby("distance")["duration"].mean().reset_index()
    post_average_time = post_data.groupby("distance")["duration"].mean().reset_index()

    merged_data = pd.merge(pre_average_time, post_average_time, on="distance", suffixes=("_pre", "_post"), how="outer") 
    merged_data = merged_data[merged_data["distance"] <= 100] 
    merged_data = merged_data[(merged_data["duration_pre"] <= 500) & (merged_data["duration_post"] <= 500)]

    plt.figure(figsize=(6, 4))
    plt.scatter(merged_data["distance"], merged_data["duration_pre"], color="blue", alpha=0.5, label="Pre-Congestion Pricing")
    plt.scatter(merged_data["distance"], merged_data["duration_post"], color="red", alpha=0.5, label="Post-Congestion Pricing")
    plt.xlabel("Distance (miles)")
    plt.ylabel("Average Duration (minutes)")
    plt.title("Average Duration vs. Distance")
    plt.legend()
    plt.grid(True)
    
    scatter = os.path.join(public, "scatter.png")
    plt.savefig(scatter) 
    plt.close() 

    return heatmap_file 