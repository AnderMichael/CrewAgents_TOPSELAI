from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scipy import optimize
from scipy.spatial import ConvexHull
import numpy as np
from typing import List

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get("/optimize")
def optimize_function(a: float, b: float):
    """Optimize a simple quadratic function."""
    def objective(x):
        return a * x**2 + b
    
    result = optimize.minimize(objective, 0)
    return {"optimized_x": result.x.tolist(), "optimized_value": result.fun}

@app.post("/convex_hull")
def convex_hull(points: List[List[float]]):
    """Calculate convex hull from a set of points."""
    hull = ConvexHull(points)
    return {"hull_points": hull.vertices.tolist()}

class GaussianEliminationRequest(BaseModel):
    a: List[List[float]]
    b: List[float]

@app.post("/gaussian_elimination")
def gaussian_elim(request: GaussianEliminationRequest):
    """Solve system of linear equations using Gaussian elimination."""
    A = np.array(request.a)
    B = np.array(request.b)
    
    try:
        solution = np.linalg.solve(A, B)
        return {"solution": solution.tolist()}
    except np.linalg.LinAlgError:
        return {"error": "The system does not have a unique solution."}

