from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.entities import Appointment, Professional
from app.repositories.appointment_repo import AppointmentRepository
from app.schemas.appointments import AppointmentCreate, AppointmentResponse, AvailabilityResponse

router = APIRouter(prefix="/appointments", tags=["Agendamentos"])


def booking_period() -> tuple[date, date]:
    """Retorna o intervalo permitido: hoje até o último dia do próximo mês."""
    today = date.today()
    if today.month == 12:
        first_after_next_month = date(today.year + 1, 2, 1)
    elif today.month == 11:
        first_after_next_month = date(today.year + 1, 1, 1)
    else:
        first_after_next_month = date(today.year, today.month + 2, 1)
    return today, first_after_next_month - timedelta(days=1)


def validate_booking_date(value: date) -> None:
    first_day, last_day = booking_period()
    if not first_day <= value <= last_day:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Escolha uma data entre {first_day:%d/%m/%Y} e {last_day:%d/%m/%Y}.",
        )


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    validate_booking_date(payload.start_time.date())
    try:
        appointment = AppointmentRepository.check_conflict_and_create(db, **payload.model_dump())
        db.commit()
        db.refresh(appointment)
        return appointment
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno.") from exc


@router.get("/professionals/{professional_id}/availability", response_model=AvailabilityResponse)
def get_availability(professional_id: int, target_date: date, db: Session = Depends(get_db)):
    validate_booking_date(target_date)
    if not db.get(Professional, professional_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional não encontrado.")
    start_of_day = datetime.combine(target_date, time.min)
    end_of_day = start_of_day + timedelta(days=1)
    appointments = db.query(Appointment).filter(
        Appointment.professional_id == professional_id,
        Appointment.status == "scheduled",
        Appointment.start_time < end_of_day,
        Appointment.end_time > start_of_day,
    ).order_by(Appointment.start_time).all()
    return {"professional_id": professional_id, "date": target_date,
            "busy_slots": [{"start": item.start_time, "end": item.end_time} for item in appointments]}
