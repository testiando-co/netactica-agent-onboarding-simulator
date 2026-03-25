from sqlalchemy import Column, Integer, String

from app.database import Base


class PhoneTI(Base):
    __tablename__ = "phone_ti"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    phone_number = Column(String, nullable=False, index=True)
    ti_number = Column(Integer, nullable=False)
    email = Column(String, nullable=True)
