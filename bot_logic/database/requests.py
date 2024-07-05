from bot_logic.database.models import User, NeuroType, NeuralNetwork
from bot_logic.database.models import async_session
from sqlalchemy import select


async def set_user(telegram_id: int):
    async with async_session() as session:
        async with session.begin():            
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                new_user = User(telegram_id=telegram_id, premium_expiration_date=None, is_bot_admin=False)
                session.add(new_user)
                await session.commit()


#===============================================================Нейронки
async def get_neuro_types():
    async with async_session() as session:
        return await session.scalars(select(NeuroType))
    

async def get_neuro_type_by_id(neuro_type_id):
    async with async_session() as session:
        return await session.scalar(select(NeuroType).where(NeuroType.id == neuro_type_id))


async def get_networks_by_type(neuro_type: int):
    async with async_session() as session:
        neural_networks = await session.scalars(select(NeuralNetwork).where(NeuralNetwork.neuro_type == neuro_type))
        return neural_networks


async def get_neuro_by_id(neuro_id: int):
    async with async_session() as session:
        neural_network = await session.scalar(select(NeuralNetwork).where(NeuralNetwork.id == neuro_id))
        return neural_network
#===============================================================





