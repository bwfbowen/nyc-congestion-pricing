import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from heatmap import heatmap

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"NYC Congestion Pricing Dashboard"}

@app.get("/map")
async def get(
    pre: str = Query(..., title="Pre Date Range (DD-MM-YYYY, DD-MM-YYYY)"), 
    post: str = Query(..., title="Post Date Range (DD-MM-YYYY, DD-MM-YYYY)"),
    start: int = Query(..., title="Start Time"), 
    end: int = Query(..., title="End Time"), 
    origin: str = Query(..., title="Origin"), 
    destination: str = Query(..., title="Destination"), 
    plot: str = Query(..., title="Plot Type (Origin/Destination)"), 
    data: str = Query(..., title="Data Type (Taxi/Citibike)"),
    clear: int = Query(0, title="Clear (1 for empty map)")
):
    """
    Endpoint to generate taxi data visualization.
    """
    # Split date ranges
    pre_start, pre_end = pre.split(",")
    post_start, post_end = post.split(",")

    # Call heatmap function with parsed dates
    heatmap(pre_start, pre_end, post_start, post_end, start, end, origin, destination, plot, data, clear)