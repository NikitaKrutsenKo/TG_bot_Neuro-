from bot_logic.database.models import User, NeuroType, NeuralNetwork
from bot_logic.database.models import async_session
from sqlalchemy import select


#=============================================================== Користувачі cr(ud)
async def set_user(telegram_id: int):
    async with async_session() as session:
        async with session.begin():            
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                new_user = User(telegram_id=telegram_id, premium_expiration_date=None, is_bot_admin=False)
                session.add(new_user)
                await session.commit()


async def get_user(telegram_id: int) -> User:
    async with async_session() as session:
        async with session.begin():            
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
            return user
#===============================================================              


#===============================================================Нейронки читання
async def get_neuro_types():
    async with async_session() as session:
        return await session.scalars(select(NeuroType))
    

async def get_neuro_type_by_id(neuro_type_id):
    async with async_session() as session:
        return await session.scalar(select(NeuroType).where(NeuroType.id == neuro_type_id))


async def get_networks_by_type(neuro_type: int):
    async with async_session() as session:

        neural_networks = await session.scalars(select(NeuralNetwork)
        .where(NeuralNetwork.neuro_type == neuro_type and NeuralNetwork.is_available))

        return neural_networks


async def get_network_by_id(neuro_id: int):
    async with async_session() as session:
        
        neural_network = await session.scalar(select(NeuralNetwork)
        .where(NeuralNetwork.id == neuro_id and NeuralNetwork.is_available))

        return neural_network
#===============================================================

#=============================================================== Нейронки запис у БД
async def write_neuro_type_to_DB(neuro_type: NeuroType):
    async with async_session() as session:
        session.add(neuro_type)
        await session.commit()


async def write_network_to_DB(neural_network: NeuralNetwork):
    async with async_session() as session:
        session.add(neural_network)
        await session.commit()
#===============================================================





