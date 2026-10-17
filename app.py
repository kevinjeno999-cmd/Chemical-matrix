from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mendeleev import element

app = FastAPI(title="Periodic Table AI Agent", description="An agent that retrieves and explains element properties.")

class ElementQuery(BaseModel):
    element_name: str

@app.get("/")
def home():
    return {"message": "Welcome to the Periodic Table AI Agent! Send a POST request to /element with an element name."}

@app.post("/element")
def get_element_properties(query: ElementQuery):
    try:
        # Fetch element data using mendeleev library (case-insensitive search)
        el = element(query.element_name.capitalize())
        
        if not el:
            raise HTTPException(status_code=404, detail="Element not found in the periodic table.")
        
        # Extract characteristic properties
        properties = {
            "name": el.name,
            "symbol": el.symbol,
            "atomic_number": el.atomic_number,
            "atomic_weight": el.atomic_weight,
            "category": el.group_id, # or block, series, etc.
            "phase": el.phase,
            "melting_point": el.melting_point,
            "boiling_point": el.boiling_point,
            "density": el.density,
            "discovery_year": el.discovery_year,
            "electron_configuration": el.electron_configuration,
            "summary": f"{el.name} is a {el.phase} element with atomic number {el.atomic_number} and symbol {el.symbol}."
        }
        
        return {
            "status": "success",
            "data": properties
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))