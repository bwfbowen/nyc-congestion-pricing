import os
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from taxi import taxi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nyc-congestion-pricing.onrender.com", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"NYC Congestion Pricing Dashboard"}

@app.get("/taxi")
async def get(
    date: str = Query(..., title="Date (MM-YYYY)"),
    pu_borough: str = Query(..., title="Pickup Borough"),
    do_borough: str = Query(..., title="Dropoff Borough"),
    plot: str = Query(..., title="Plot Type (Pickup/Dropoff)"),
    hours: str = Query(..., title="Hours (Peak/Overnight)"),
    clear: int = Query(0, title="Clear (1 for empty map)")
):
    """
    Endpoint to generate taxi data visualization.
    """
    nyc_html, time_png = taxi(date, pu_borough, do_borough, plot, hours, clear)
    return {
        "nyc_html": f"/static/{os.path.basename(nyc_html)}",
        "time_png": f"/static/{os.path.basename(time_png)}"
    } 