import os
import pandas as pd
import pyarrow.parquet as pq
import geopandas as gpd
import folium
import matplotlib.pyplot as plt

def taxi(date, pu_borough, do_borough, plot, hours, clear):
    
    static_dir = "static"

    if clear == 1:
        m = folium.Map(location=[40.7128, -74.0060])
        file_name = os.path.join(static_dir, "nyc.html")
        m.save(file_name)
        
        plt.figure(figsize=(10, 6))
        plt.title("Empty Time Distribution")
        plt.xlabel("Time")
        plt.ylabel("Frequency")
        plt.xlim(0, 24)  # Assuming 24-hour time scale
        plt.ylim(0, 1)   # Empty y-axis
        distribution_file = os.path.join(static_dir, "time.png")
        plt.savefig(distribution_file)
        plt.close()
    
        return file_name, distribution_file
    
    month, year = date.split("-")
    
    codes = {
        "crz": {50, 48, 163, 230, 161, 162, 229, 246, 68, 100, 
                186, 90, 164, 234, 170, 233, 107, 137, 224, 158, 
                249, 113, 114, 79, 4, 125, 211, 144, 148, 232, 
                231, 45, 209, 13, 261, 87, 88, 12},
        "bronx": {200, 240, 259, 254, 81, 51, 184, 220, 241, 174, 
                  18, 20, 31, 32, 3, 185, 242, 183, 58, 136, 
                  94, 235, 169, 47, 78, 59, 60, 248, 182, 212, 
                  250, 213, 208, 46, 119, 247, 69, 167, 159, 147, 
                  126, 199, 168},
        "brooklyn": {55, 29, 150, 154, 108, 123, 210, 21, 149, 155, 
                     11, 22, 14, 67, 26, 133, 227, 111, 257, 228, 
                     178, 165, 89, 85, 71, 91, 39, 222, 76, 63, 
                     77, 35, 72, 188, 62, 190, 181, 106, 40, 195, 
                     54, 52, 33, 25, 65, 66, 34, 97, 49, 189, 
                     61, 177, 225, 17, 217, 256, 80, 37, 36, 255, 
                     112},
        "manhattan": {153, 128, 127, 243, 120, 244, 116, 42, 152, 166, 
                      41, 74, 194, 24, 151, 238, 239, 143, 142, 43, 
                      75, 236, 263, 262, 237, 141, 140, 202},
        "queens": {27, 201, 117, 86, 2, 132, 124, 219, 203, 180, 
                   216, 10, 218, 219, 203, 139, 205, 215, 130, 197, 
                   258, 96, 134, 28, 131, 122, 191, 38, 19, 101, 
                   64, 175, 98, 9, 16, 15, 252, 171, 73, 192, 
                   135, 121, 93, 253, 92, 53, 57, 56, 95, 196, 
                   160, 198, 102, 157, 83, 82, 173, 70, 129, 138, 
                   207, 223, 8, 179, 193, 146, 145, 226, 260, 157, 
                   7},
        "staten_island": {44, 204, 5, 84, 109, 110, 176, 172, 214, 6, 
                          221, 115, 245, 206, 251, 187, 156, 23, 118, 99}
        }
    
    pu_filter = codes.get(pu_borough.lower(), set())
    do_filter = codes.get(do_borough.lower(), set())
        
    directory = f"data/{year}/{month}"
    
    df_list = []
    for file in sorted(os.listdir(directory)):
        if file.endswith(".parquet"):
            color = file[0]
            if color == "y":
                pickup = 'tpep_pickup_datetime'
                dropoff = 'tpep_dropoff_datetime'
            elif color == "g":
                pickup = 'lpep_pickup_datetime'
                dropoff = 'lpep_dropoff_datetime'
            elif color == "f":
                pickup = 'pickup_datetime'
                dropoff = 'dropOff_datetime'
            columns = [pickup, dropoff, 'PULocationID', 'DOLocationID']
            filepath = os.path.join(directory, file)
            df = pq.read_table(filepath, columns=columns).to_pandas()
            
            df[pickup] = pd.to_datetime(df[pickup])
            is_weekend = df[pickup].dt.dayofweek > 4
            if hours == "Peak":
                df = df[
                    ((is_weekend) & (df[pickup].dt.hour.between(9, 20))) |
                    ((~is_weekend) & (df[pickup].dt.hour.between(5, 20)))
                ]
            elif hours == "Overnight":
                df = df[
                    ((is_weekend) & ((df[pickup].dt.hour >= 21) | (df[pickup].dt.hour < 9))) |
                    ((~is_weekend) & ((df[pickup].dt.hour >= 21) | (df[pickup].dt.hour < 5)))
                ]
            
            df_list.append(df)
            
    taxi_data = pd.concat(df_list, ignore_index=True)
    
    taxi_data["trip_duration"] = (taxi_data[dropoff] - taxi_data[pickup]).dt.total_seconds() / 60
    taxi_data = taxi_data[taxi_data["PULocationID"].isin(pu_filter)]
    taxi_data = taxi_data[taxi_data["DOLocationID"].isin(do_filter)]
    
    nyc = gpd.read_file("taxi_zones/taxi_zones.shp")
    
    heatmap = "PULocationID" if plot == "Pickup" else "DOLocationID"
    trip_type = "Pickups" if plot == "Pickup" else "Drop-offs"
    
    taxi_zones = nyc[["LocationID", "geometry"]].rename(columns={"LocationID": heatmap})
    trip_count = taxi_data[heatmap].value_counts().reset_index(name="count")
    trip_count = trip_count.merge(taxi_zones, on=heatmap, how="left")
    
    m = folium.Map(location=[40.7128, -74.0060])
    
    gdf = gpd.GeoDataFrame(trip_count, geometry="geometry")
    
    folium.Choropleth(
        geo_data=gdf,
        name=f"{trip_type} Heatmap",
        data=gdf,
        columns=[heatmap, "count"],
        key_on=f"feature.properties.{heatmap}",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"Number of {trip_type}",
    ).add_to(m)

    file_name = os.path.join(static_dir, "nyc.html")
    m.save(file_name)
    
    print(f"Saved as '{file_name}' showing number of {trip_type}.")
    
    # Generate trip duration distribution
    plt.figure(figsize=(10, 6))
    taxi_data["trip_duration"].hist(bins=50)
    plt.title(f"Trip Duration Distribution: {pu_borough.capitalize()} to {do_borough.capitalize()} ({hours} hours)")
    plt.xlabel("Trip Duration (minutes)", fontsize=16)
    plt.ylabel(f"{plot} Frequency", fontsize=16)
    distribution_file = os.path.join(static_dir, "time.png")
    plt.savefig(distribution_file)
    plt.close()
    
    print(f"Trip duration distribution saved as '{distribution_file}'")
    
    return (file_name, distribution_file)