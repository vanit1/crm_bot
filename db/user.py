from .base import BaseModel
import datetime
from sqlalchemy import DATE, Integer, Column, VARCHAR, Text, BigInteger

class ClientOnlyfans(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    name = Column(VARCHAR(length=32), nullable=False)

    info_user = Column(Text, nullable=True)
    
    reg_date = Column(DATE, default=datetime.date.today())
    
    upd_date = Column(DATE, default=datetime.date.today())

    # def __str__(self) -> str:
    #     return f"Наш юзер {self.name}"
    
    