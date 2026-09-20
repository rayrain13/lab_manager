from datetime import date, time

from pydantic import BaseModel


class ReservationCreate(BaseModel):
    lab_id: int
    date: date
    start_time: time
    end_time: time
    purpose: str


class ReviewRequest(BaseModel):
    review_comment: str | None = None


class ReservationOut(BaseModel):
    id: int
    user_id: int
    lab_id: int
    date: str
    start_time: str
    end_time: str
    purpose: str
    status: str
    review_comment: str | None = None
    reviewer_id: int | None = None
    review_time: str | None = None
    user_name: str | None = None
    lab_name: str | None = None
    lab_location: str | None = None
    reviewer_name: str | None = None
