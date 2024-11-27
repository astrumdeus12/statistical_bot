
from sqlalchemy import MetaData, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship
from datetime import date

class Base(DeclarativeBase):
    metadata = MetaData()
    
    


class User(Base):
    __tablename__ = 'users'
    
    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    phone_number : Mapped[str] = mapped_column()
    tg_id : Mapped[str] = mapped_column(unique=True)
    name : Mapped[str] = mapped_column()
    sells : Mapped[list['Sells']] = Relationship(back_populates='user',
                                                 uselist=True)
    
    

class Sells(Base):
    __tablename__ = 'sells'
    
    id : Mapped[int] = mapped_column(primary_key=True, unique = True, autoincrement=True)
    user : Mapped['User'] = Relationship(back_populates='sells',
                                            uselist=False)
    
    user_id : Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    
    credits : Mapped[int] = mapped_column(default=0)
    insurance : Mapped[int] = mapped_column(default=0)
    credit_cards : Mapped[int] = mapped_column(default=0)
    deb_cards : Mapped[int] = mapped_column(default=0)
    investition_insurance : Mapped[int] = mapped_column(default=0)
    client_calls : Mapped[int] = mapped_column(default=0)
    day : Mapped[date] = mapped_column(Date)
    
    
