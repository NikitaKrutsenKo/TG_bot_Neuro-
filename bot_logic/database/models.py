from sqlalchemy import String, ForeignKey, BigInteger, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

# модель користувача застосунку
class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id : Mapped[int] = mapped_column(BigInteger)
    premium_expiration_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_bot_admin : Mapped[bool] = mapped_column(Boolean)   

# тип нейронки (для відео, тексту, аудіо...)
class NeuroType(Base):
    __tablename__ = 'neuro_types'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(30))

# нейронна мережа 
class NeuralNetwork(Base):
    __tablename__ = 'neural_networks'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(30))
    description : Mapped[str] = mapped_column(String(300), nullable=True)
    neuro_type : Mapped[int] = mapped_column(ForeignKey('neuro_types.id', ondelete='SET NULL'), nullable=True)
    neuro_video_tutorial : Mapped[str] = mapped_column(String(120), nullable=True)    
    neuro_message_ref : Mapped[str] = mapped_column(String(120), nullable=True)
    neuro_ref : Mapped[str] = mapped_column(String(120))
    is_available : Mapped[bool] = mapped_column()


async def async_db_create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
