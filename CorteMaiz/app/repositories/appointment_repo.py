from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.entities import Appointment, Professional, Service, User


class AppointmentRepository:
    @staticmethod
    def check_conflict_and_create(
        db: Session, customer_id: int, professional_id: int, service_id: int, start_time: datetime
    ) -> Appointment:
        if not db.get(User, customer_id):
            raise ValueError("Cliente não encontrado.")
        if not db.get(Professional, professional_id):
            raise ValueError("Profissional não encontrado.")
        service = db.get(Service, service_id)
        if not service:
            raise ValueError("Serviço não encontrado.")

        end_time = start_time + timedelta(minutes=service.duration_minutes)
        conflict = db.query(Appointment).filter(
            and_(
                Appointment.professional_id == professional_id,
                Appointment.status == "scheduled",
                Appointment.start_time < end_time,
                Appointment.end_time > start_time,
            )
        ).first()
        if conflict:
            raise ValueError("O profissional já possui um agendamento neste horário.")

        appointment = Appointment(
            customer_id=customer_id,
            professional_id=professional_id,
            service_id=service_id,
            start_time=start_time,
            end_time=end_time,
            status="scheduled",
        )
        db.add(appointment)
        return appointment
