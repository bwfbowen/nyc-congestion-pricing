# NYC Congestion Pricing Dashboard 
## Overview 
This interactive dashboard compares taxi trips after the New York City Congestion Pricing Program was implemented in January 2025 with its corresponding day of the week in January 2024. 
By filtering [Taxi & Limousine Commission (TLC) Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) by: 
1. Range of dates:
   * Before congestion pricing
   * After congestion pricing 
2. Hour of the day (0 - 23):
   * Start time
   * End time 
3. Location:
   * Origin
   * Destination  

The dashboard will produce:
* A heatmap of changes in the number of taxi trips across NYC taxi zones
* Histograms of the time distributions of all taxi trips and the top five areas with the most changes in time distribution after congestion pricing
* A scatter plot of the average taxi trip duration (minutes) against each taxi trip (miles)

## Usage 
1. Install the required dependencies for both the frontend and backend directories ('**requirements.txt**').
2. Navigate to the backend directory and start the backend using:

   ```uvicorn main:app --reload```
   
3. In a new terminal, navigate to the frontend directory and start the frontend using:

   ```npm start```
 
4. Scroll to the bottom of the sidebar to choose filters, then click '**Generate**'. Due to the amount of data, the dashboard may take a while.
5. Click '**Clear**' to clear the dashboard.  
