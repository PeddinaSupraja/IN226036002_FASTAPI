from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# -----------------------------
# DATA MODELS
# -----------------------------

class Appointment(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_name: str
    date: str
    time: str
    status: str = "booked"

class AppointmentUpdate(BaseModel):
    patient_name: Optional[str]
    doctor_name: Optional[str]
    date: Optional[str]
    time: Optional[str]
    status: Optional[str]

appointments = []

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def find_appointment(app_id: int):
    for appo in appointments:
        if appo["id"] == app_id:
            return appo
    return None

# -----------------------------
# GET APIs
# -----------------------------

@app.get("/")
def home():
    return {"message": "Medical Appointment System API"}

@app.get("/appointments")
def get_all():
    return appointments

@app.get("/appointments/{id}")
def get_by_id(id: int):
    appo = find_appointment(id)
    if not appo:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appo

@app.get("/appointments/count")
def count():
    return {"total_appointments": len(appointments)}

# -----------------------------
# POST API
# -----------------------------

@app.post("/appointments", status_code=201)
def create(appo: Appointment):
    new = appo.dict()
    new["id"] = len(appointments) + 1
    appointments.append(new)
    return new

# -----------------------------
# PUT API
# -----------------------------

@app.put("/appointments/{id}")
def update(id: int, updated: AppointmentUpdate):
    appo = find_appointment(id)
    if not appo:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in updated.dict().items():
        if value is not None:
            appo[key] = value

    return appo

# -----------------------------
# DELETE API
# -----------------------------

@app.delete("/appointments/{id}")
def delete(id: int):
    appo = find_appointment(id)
    if not appo:
        raise HTTPException(status_code=404, detail="Not found")

    appointments.remove(appo)
    return {"message": "Deleted successfully"}

# -----------------------------
# MULTI-STEP WORKFLOW
# -----------------------------

@app.post("/appointments/{id}/checkin")
def checkin(id: int):
    appo = find_appointment(id)
    if not appo:
        raise HTTPException(status_code=404, detail="Not found")

    appo["status"] = "checked-in"
    return appo

@app.post("/appointments/{id}/complete")
def complete(id: int):
    appo = find_appointment(id)
    if not appo:
        raise HTTPException(status_code=404, detail="Not found")

    appo["status"] = "completed"
    return appo

@app.get("/appointments/history")
def history():
    return [a for a in appointments if a["status"] == "completed"]

# -----------------------------
# ADVANCED APIs
# -----------------------------

@app.get("/appointments/search")
def search(keyword: Optional[str] = None):
    if keyword:
        return [a for a in appointments if keyword.lower() in a["patient_name"].lower()]
    return appointments

@app.get("/appointments/filter")
def filter_by_status(status: Optional[str] = None):
    if status:
        return [a for a in appointments if a["status"] == status]
    return appointments

@app.get("/appointments/sort")
def sort_by_name(order: str = "asc"):
    return sorted(appointments, key=lambda x: x["patient_name"], reverse=(order=="desc"))

@app.get("/appointments/pagination")
def paginate(skip: int = 0, limit: int = 5):
    return appointments[skip: skip + limit]

@app.get("/appointments/browse")
def browse(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 5
):
    result = appointments

    if keyword:
        result = [a for a in result if keyword.lower() in a["patient_name"].lower()]

    if status:
        result = [a for a in result if a["status"] == status]

    return result[skip: skip + limit]