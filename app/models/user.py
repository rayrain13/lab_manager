from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'comment':'用户信息表'}

    username:Mapped[str] = mapped_column(String(50),comment='账号',nullable=False)
    password:Mapped[str] = mapped_column(String(128),comment='密码',nullable=False)
    name:Mapped[str] = mapped_column(String(50),comment='名称',nullable=False)
    role:Mapped[str] = mapped_column(String(50),comment='角色',nullable=False)
    email:Mapped[str | None] = mapped_column(String(50),comment='邮箱')
    phone:Mapped[str | None] = mapped_column(String(50),comment='电话')
    