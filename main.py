from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

VEHICLE_PRESETS = {
    "sedan": 14,
    "suv": 10,
    "truck": 6,
    "hybrid": 20,
    "motorcycle": 25
}

class FuelRequest(BaseModel):
    distance_km: float
    fuel_efficiency_km_per_litre: float | None = None
    fuel_price_per_litre: float
    ac_on: bool = False
    passenger_weight_kg: float = 0
    luggage_weight_kg: float = 0
    city_ratio: float = 0.5
    idle_minutes: float = 0
    vehicle_type: str | None = None

@app.post("/calculate_fuel")
def calculate_fuel(data: FuelRequest):

    # If vehicle type is selected, override efficiency
    if data.vehicle_type:
        data.fuel_efficiency_km_per_litre = VEHICLE_PRESETS[data.vehicle_type]

    efficiency = data.fuel_efficiency_km_per_litre

    # AC reduces efficiency by 10%
    if data.ac_on:
        efficiency *= 0.9

    # Weight penalty (max 15%)
    total_weight = data.passenger_weight_kg + data.luggage_weight_kg
    if total_weight > 0:
        efficiency *= (1 - min(total_weight / 1000, 0.15))

    # City vs highway efficiency
    city_eff = efficiency * 0.8
    highway_eff = efficiency * 1.1
    mixed_eff = (city_eff * data.city_ratio) + (highway_eff * (1 - data.city_ratio))

    # Idle fuel burn (1.2 L/hr)
    idle_fuel = (data.idle_minutes / 60) * 1.2

    # Final calculations
    fuel_needed = (data.distance_km / mixed_eff) + idle_fuel
    total_cost = fuel_needed * data.fuel_price_per_litre

    return {
        "fuel_needed_litres": round(fuel_needed, 2),
        "total_cost": round(total_cost, 2),
        "effective_efficiency": round(mixed_eff, 2)
    }
