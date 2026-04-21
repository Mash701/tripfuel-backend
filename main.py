from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Updated Request Model
# -----------------------------
class FuelRequest(BaseModel):
    distance_km: float
    fuel_efficiency_km_per_litre: float
    fuel_price_per_litre: float
    ac_on: bool
    passenger_weight_kg: float
    luggage_weight_kg: float
    city_ratio: float
    idle_minutes: float
    vehicle_type: str


# -----------------------------
# Calculation Logic
# -----------------------------
@app.post("/calculate_fuel")
def calculate_fuel(data: FuelRequest):

    # Base fuel needed
    base_fuel = data.distance_km / data.fuel_efficiency_km_per_litre

    # AC penalty
    ac_penalty = 0.1 if data.ac_on else 0.0

    # Weight penalty (simple model)
    weight_penalty = (data.passenger_weight_kg + data.luggage_weight_kg) * 0.0002

    # City driving penalty
    city_penalty = data.city_ratio * 0.15

    # Idle fuel consumption (litres per minute)
    idle_fuel = data.idle_minutes * 0.02

    # Total fuel needed
    total_fuel = base_fuel * (1 + ac_penalty + weight_penalty + city_penalty) + idle_fuel

    # Total cost
    total_cost = total_fuel * data.fuel_price_per_litre

    return {
        "fuel_needed_litres": round(total_fuel, 2),
        "fuel_cost": round(total_cost, 2)
    }


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Trip Fuel Backend is running"}
