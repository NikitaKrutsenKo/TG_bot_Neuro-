from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext

from bot_logic.database.models import async_session, NeuroType, NeuralNetwork
from bot_logic.admin_keyboards import choose_neuro_types_keyboard
import bot_logic.admin_states as admin_states 
import bot_logic.database.requests as rq

import re



admin_router = Router()


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        telegram_id = message.from_user.id
        async with async_session() as session:
            user = await rq.get_user(telegram_id=telegram_id)
            if user:
                session.add(user)
                await session.refresh(user)
                return user.is_bot_admin
        return False


@admin_router.message(Command('start_admin'), AdminFilter())
async def help_admin(message: Message):
    await message.reply(
    'Адмін-панель до ваших послуг, ' + message.from_user.full_name + '\n' +
    '/add_new_neuro - додати нову нейронку, (під час створення не намагайтесь ввести інші команди, вони вимкнені)\n')


#=============================================================== Процес створення нової нейронки
@admin_router.message(Command('add_new_neuro'), AdminFilter())
async def start_add_new_neuro(message: Message, state: FSMContext):
    await state.set_state(admin_states.CreateNewNeuro.name)
    await message.answer('Введіть ім\'я нової нейронки: ' )
    

@admin_router.message(admin_states.CreateNewNeuro.name)
async def neuro_name_added(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(admin_states.CreateNewNeuro.description)
    await message.answer('Ім\'я ввели, тепер коротенько опишіть нейронку (не більше 300 символів)')


@admin_router.message(admin_states.CreateNewNeuro.description)
async def neuro_description_added(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(admin_states.CreateNewNeuro.neuro_type)
    await message.answer('Опис прописали, тепер треба обрати її тип. Введіть новий, або оберіть старий', 
    reply_markup = await choose_neuro_types_keyboard())


@admin_router.callback_query(F.data.startswith('choose_neuro_type_'), admin_states.CreateNewNeuro.neuro_type)
async def neuro_type_create_or_choose(callback : CallbackQuery, state: FSMContext):
    neyro_type_id = re.search(r'\d+', callback.data)
    callback.answer(None)
    if not neyro_type_id:
        await state.set_state(admin_states.CreateNewNeuro.new_neuro_type)
        await callback.message.answer('Створимо новий тип. Введіть його назву')
    else:
        neyro_type_value = await rq.get_neuro_type_by_id(int(neyro_type_id.group()))
        await state.update_data(neuro_type = neyro_type_value.id)
        await state.set_state(admin_states.CreateNewNeuro.nuero_video_tutorial)
        await callback.message.answer('Введіть посилання на відос з ютубу якщо таке є, якщо нема то відправте просто крапку -> .')


@admin_router.message(admin_states.CreateNewNeuro.new_neuro_type)
async def neuro_type_create(message: Message, state: FSMContext):
    async with async_session() as session:
        new_type = NeuroType(name = message.text)
        session.add(new_type)
        await session.commit()
        await session.refresh(new_type)  # Оновлюємо об'єкт для отримання згенерованого ID
        new_type_id = new_type.id
        await state.update_data(neuro_type = new_type_id)
        

    await state.set_state(admin_states.CreateNewNeuro.neuro_video_tutorial)
    await message.answer('Введіть посилання на відос з ютубу якщо таке є, якщо нема то відправте просто крапку -> .')


@admin_router.message(admin_states.CreateNewNeuro.neuro_video_tutorial)
async def neuro_video_added(message: Message, state: FSMContext):
    vid_ref = message.text.strip()
    if vid_ref != '.':
        await state.update_data(neuro_video_tutorial = message.text)
    else:
        await state.update_data(neuro_video_tutorial = None)
    await state.set_state(admin_states.CreateNewNeuro.neuro_message_ref)    
    await message.answer('Тепер надайте посилання на повідомлення з детільним поясненням роботи з нейронкою' +
    'якщо такого нема, то напишіть просто крапку -> .')


@admin_router.message(admin_states.CreateNewNeuro.neuro_message_ref)
async def neuro_message_ref_added(message: Message, state: FSMContext):
    message_ref = message.text.strip()
    if message_ref != '.':
        await state.update_data(neuro_message_ref = message.text)
    else:
        await state.update_data(neuro_message_ref = None)
    await state.set_state(admin_states.CreateNewNeuro.neuro_ref)
    await message.answer('Тепер киньте посилання на саму нейронку, щоб її можна було знайти в інеті')


@admin_router.message(admin_states.CreateNewNeuro.neuro_ref)
async def neuro_ref_added(message: Message, state: FSMContext):
    await state.update_data(neuro_ref = message.text)
    await state.set_state(admin_states.CreateNewNeuro.is_available)
    await message.answer('Останній штрих, напишіть \'так\', якщо ви хочете, щоб нейронку бачили всі користувачі бота'+ 
    'або напишіть \'ні\' якщо хочете, щоб вона поки нікому не попадалась')


@admin_router.message(admin_states.CreateNewNeuro.is_available)
async def neuro_is_available_added(message: Message, state: FSMContext):
    message_answer = message.text.strip().lower()
    if message_answer == 'так':
        await state.update_data(is_available = True)
    elif message_answer == 'ні':
        await state.update_data(is_available = False)
    await create_neuro_with_user_info(state=state)
    await state.clear()
    await message.answer('Нова нейронка записана')
    

async def create_neuro_with_user_info(state: FSMContext):
    async with async_session() as session:
        data = await state.get_data()
        t = data["neuro_type"]
        new_neuro = NeuralNetwork(
        name=data["name"],
        description=data["description"],
        neuro_type=data["neuro_type"],
        neuro_video_tutorial=data["neuro_video_tutorial"],
        neuro_message_ref=data["neuro_message_ref"],
        neuro_ref = data["neuro_ref"],
        is_available=data["is_available"])
        session.add(new_neuro)
        await session.commit()

#===============================================================