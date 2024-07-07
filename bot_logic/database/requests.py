from bot_logic.database.models import User, NeuroType, NeuralNetwork
from bot_logic.database.models import async_session
from sqlalchemy import select, update


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
        

async def grant_user_admin(telegram_id: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(is_bot_admin = True)
            )
#===============================================================              


#===============================================================Нейронки читання
async def get_neuro_types():
    async with async_session() as session:
        return await session.scalars(select(NeuroType))
    

async def get_neuro_type_by_id(neuro_type_id):
    async with async_session() as session:
        return await session.scalar(select(NeuroType).where(NeuroType.id == neuro_type_id))


async def get_all_networks():
    async with async_session() as session:
        neural_networks = await session.scalars(select(NeuralNetwork))
        return neural_networks


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
async def write_neuro_type_to_DB(neuro_type: NeuroType) -> int:
    async with async_session() as session:
        session.add(neuro_type)
        await session.commit()
        await session.refresh(neuro_type)
        return neuro_type.id


async def write_network_to_DB(neural_network: NeuralNetwork) -> int:
    async with async_session() as session:
        session.add(neural_network)
        await session.commit()
        await session.refresh(neural_network)
        return neural_network.id
#===============================================================

#=============================================================== Оновлення інформації про нейронку
async def update_network_name(network_id: int, new_name: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(name=new_name)
            )
            
            await session.commit()


async def update_network_description(network_id: int, new_description: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(description=new_description)
            )
            
            await session.commit()


async def update_network_type(network_id: int, new_type_id: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(neuro_type=new_type_id)
            )
            
            await session.commit()


async def update_network_video_tutorial(network_id: int, new_video: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(neuro_video_tutorial=new_video)
            )
            
            await session.commit()


async def update_network_message_ref(network_id: int, new_message: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(neuro_message_ref=new_message)
            )
            
            await session.commit()


async def update_network_neuro_ref(network_id: int, new_ref: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(neuro_ref=new_ref)
            )
            
            await session.commit()


async def update_network_is_available(network_id: int, new_available: bool):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(NeuralNetwork)
                .where(NeuralNetwork.id == network_id)
                .values(is_available=new_available)
            )
            
            await session.commit()
#===============================================================




