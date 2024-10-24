from fastapi import FastAPI
from pydantic import BaseModel
from scipy.spatial import distance
from typing import List, Tuple

class Point(BaseModel):
    x: float
    y: float

def calculate_distance(point1: Point, point2: Point) -> float:
    return distance.euclidean((point1.x, point1.y), (point2.x, point2.y))

class Rectangle(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

def check_collision(rect1: Rectangle, rect2: Rectangle) -> bool:
    return not (rect1.x1 > rect2.x2 or rect1.x2 < rect2.x1 or 
                rect1.y1 > rect2.y2 or rect1.y2 < rect2.y1)

def polygon_area(vertices: List[Tuple[float, float]]) -> float:
    n = len(vertices)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2.0

app = FastAPI()

@app.post("/calculate-distance")
def api_calculate_distance(point1: Point, point2: Point):
    return {"distance": calculate_distance(point1, point2)}

@app.post("/check-collision")
def api_check_collision(rect1: Rectangle, rect2: Rectangle):
    return {"collision": check_collision(rect1, rect2)}

@app.post("/polygon-area")
def api_polygon_area(vertices: List[Tuple[float, float]]):
    return {"area": polygon_area(vertices)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
