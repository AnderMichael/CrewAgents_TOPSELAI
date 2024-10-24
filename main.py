from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from scipy.spatial import ConvexHull

app = FastAPI()

# Models for request and response data
class Point(BaseModel):
    x: float
    y: float

class PointsList(BaseModel):
    points: list[Point]

# Compute the convex hull of a set of points
@app.post("/convex_hull/")
async def compute_convex_hull(points_list: PointsList):
    points = np.array([[point.x, point.y] for point in points_list.points])
    hull = ConvexHull(points)
    return {
        "vertices": points[hull.vertices].tolist(),
        "hull_area": hull.volume
    }

# Run the app with: uvicorn main:app --reload
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)