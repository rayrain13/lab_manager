from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey


class Equipment(Base):
    __tablename__ = "equipments"
    __table_args__ = {'comment': '实验室设备表'}

    name: Mapped[str] = mapped_column(String(100), comment='设备名称', nullable=False)
    code: Mapped[str] = mapped_column(String(50), comment='设备编号', nullable=False, unique=True)
    model: Mapped[str | None] = mapped_column(String(100), comment='型号')
    lab_id: Mapped[int] = mapped_column(ForeignKey('labs.id'), comment='所属实验室', nullable=False)
    status: Mapped[str] = mapped_column(String(20), comment='状态:available可用/in_use使用中/maintenance维护中', nullable=False, default='available')
    description: Mapped[str | None] = mapped_column(Text, comment='描述')
