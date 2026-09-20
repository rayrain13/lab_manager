from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text


class Lab(Base):
    __tablename__ = "labs"
    __table_args__ = {'comment': '实验室信息表'}

    name: Mapped[str] = mapped_column(String(100), comment='实验室名称', nullable=False)
    code: Mapped[str] = mapped_column(String(50), comment='实验室编号', nullable=False, unique=True)
    location: Mapped[str] = mapped_column(String(200), comment='位置', nullable=False)
    capacity: Mapped[int] = mapped_column(comment='容纳人数', nullable=False, default=0)
    description: Mapped[str | None] = mapped_column(Text, comment='描述')
    status: Mapped[str] = mapped_column(String(20), comment='状态:available可用/maintenance维护中', nullable=False, default='available')
