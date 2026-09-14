from datetime import date, datetime

from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    customer_id: int
    professional_id: int
    service_id: int
    start_time: datetime = Field(..., description="Data e hora de início (ISO 8601)")


class AppointmentResponse(BaseModel):
    id: int
    customer_id: int
    professional_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: str

    model_config = {"from_attributes": True}


class BusySlot(BaseModel):
    start: datetime
    end: datetime


class AvailabilityResponse(BaseModel):
    professional_id: int
    date: date
    busy_slots: list[BusySlot]
