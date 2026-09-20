from datetime import date, time, datetime

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Date, Time, DateTime


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = {'comment': '实验室预约表'}

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), comment='预约人', nullable=False)
    lab_id: Mapped[int] = mapped_column(ForeignKey('labs.id'), comment='实验室', nullable=False)
    date: Mapped[date] = mapped_column(Date, comment='预约日期', nullable=False)
    start_time: Mapped[time] = mapped_column(Time, comment='开始时间', nullable=False)
    end_time: Mapped[time] = mapped_column(Time, comment='结束时间', nullable=False)
    purpose: Mapped[str] = mapped_column(String(500), comment='用途说明', nullable=False)
    status: Mapped[str] = mapped_column(String(20), comment='状态:pending待审核/approved已通过/rejected已驳回/cancelled已取消', nullable=False, default='pending')
    review_comment: Mapped[str | None] = mapped_column(String(500), comment='审核意见')
    reviewer_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), comment='审核人')
    review_time: Mapped[datetime | None] = mapped_column(DateTime, comment='审核时间')
