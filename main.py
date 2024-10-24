from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from numpy import poly1d
from math import factorial

app = FastAPI()

@app.get("/math/arithmetic/")
def basic_arithmetic(x: float):
    return {
        "log": np.log(x),
        "exp": np.exp(x)
    }

@app.get("/math/progression/")
def progression(n: int, a: float, r: float, type: str):
    if type == 'arithmetic':
        sum_arithmetic = (n / 2) * (2 * a + (n - 1) * r)
        return {"sum": sum_arithmetic}
    elif type == 'geometric':
        sum_geometric = a * (1 - r**n) / (1 - r) if r != 1 else a * n
        return {"sum": sum_geometric}

@app.post("/math/polynomial/")
def polynomial_operations(coefficients: list):
    poly = poly1d(coefficients)
    return {
        "evaluation": poly(1),  # Evaluate at x=1
        "derivative": poly.deriv().c  # Coefficients of the derivative
    }

@app.get("/math/bases/{base_from}/{base_to}/")
def convert_base(value: str, base_from: int, base_to: int):
    base_10_value = int(value, base_from)
    return {"converted_value": np.base_repr(base_10_value, base=base_to)}

@app.get("/math/primes/")
def sieve_of_eratosthenes(n: int):
    sieve = [True] * (n + 1)
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    primes = [i for i in range(2, n) if sieve[i]]
    return {"primes": primes}

@app.get("/math/combinatorics/")
def combinatorial(n: int, k: int):
    binom = factorial(n) // (factorial(k) * factorial(n - k))
    catalan = binom // (k + 1)
    return {"binomial": binom, "catalan": catalan}

@app.get("/math/geometry/")
def pythagorean(a: float, b: float):
    return {"hypotenuse": (a**2 + b**2)**0.5}

@app.get("/math/game-theory/")
def minimax(game_state):
    return {"message": "Minimax algorithm not implemented yet."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
