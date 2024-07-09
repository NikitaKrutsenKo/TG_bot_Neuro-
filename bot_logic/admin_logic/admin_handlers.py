from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext

from bot_logic.database.models import async_session, NeuroType, NeuralNetwork
import bot_logic.admin_logic.admin_keyboards as admin_keyboards
import bot_logic.admin_logic.admin_states as admin_states 
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


async def show_admin_commands() -> str:
    result = []
    for key, value in admin_keyboards.admin_commands_list.items():
        if value is not None:
            result.append(f"{key} : {value}\n")
    text = "\n".join(result)
    return text


@admin_router.message(Command('start_admin'), AdminFilter())
async def start_admin(message: Message):
    await message.reply(
    'Адмін-панель до ваших послуг, ' + message.from_user.full_name + '\n' +
    await show_admin_commands(), reply_markup= await admin_keyboards.create_admin_feature_keyboard())


@admin_router.message(lambda message: message.text in admin_keyboards.admin_features_list, AdminFilter())
async def show_admin_keyboard(message :Message):
    feature = admin_keyboards.admin_features_list.get(message.text, None)
    await message.answer('Оберіть пункт з клавіатури ', reply_markup= await feature())


@admin_router.message(F.text == 'На головну', AdminFilter())
async def return_to_main_page(message : Message):
    await message.reply(
    'Повертаємось на головну клавіатуру', reply_markup= await admin_keyboards.create_admin_feature_keyboard())


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
    reply_markup = await admin_keyboards.choose_neuro_types_keyboard())


@admin_router.callback_query(F.data.startswith('choose_neuro_type_'), admin_states.CreateNewNeuro.neuro_type)
async def neuro_type_create_or_choose(callback : CallbackQuery, state: FSMContext):
    try:
        neyro_type_id = re.search(r'\d+', callback.data)
        await callback.answer(None)
        if not neyro_type_id:
            await state.set_state(admin_states.CreateNewNeuro.new_neuro_type)
            await callback.message.answer('Створимо новий тип. Введіть його назву')
        else:
            await state.update_data(neuro_type = int(neyro_type_id.group()))
            await state.set_state(admin_states.CreateNewNeuro.neuro_video_tutorial)
            await callback.message.answer('Введіть посилання на відос з ютубу якщо таке є, якщо нема то відправте просто крапку -> .')
    except Exception as e:
        await state.clear()
        await callback.message.answer(text=f'Сталася помилка {e}')


@admin_router.message(admin_states.CreateNewNeuro.new_neuro_type)
async def neuro_type_create(message: Message, state: FSMContext):
    new_type = NeuroType(name = message.text)        
    new_type_id = await rq.write_neuro_type_to_DB(new_type)
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
    else:
        await state.update_data(is_available = False)
    await create_neuro_with_user_info(state=state, message=message)
    await state.clear()
    await message.answer('Нова нейронка записана')
    

async def create_neuro_with_user_info(state: FSMContext, message: Message):
    try:
        data = await state.get_data()
        new_neuro = NeuralNetwork(
        name=data["name"],
        description=data["description"],
        neuro_type=data["neuro_type"],
        neuro_video_tutorial=data["neuro_video_tutorial"],
        neuro_message_ref=data["neuro_message_ref"],
        neuro_ref = data["neuro_ref"],
        is_available=data["is_available"])
        await rq.write_neuro_to_DB(new_neuro)
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')

#===============================================================

#=============================================================== Процес оновлення нейронки
@admin_router.message(Command('edit_neuro'), AdminFilter())
async def choose_neuro_to_edit(message : Message):
    await message.answer('Оберіть зі списку нейронку, яку хочете змінити', 
    reply_markup = await admin_keyboards.update_neuro_networks_keyboard())


@admin_router.callback_query(F.data.startswith("start_update_neuro_"))
async def start_network_update(callback : CallbackQuery, state : FSMContext):
    try:
        await callback.answer(None)
        update_network_id = int(re.search(r'\d+', callback.data).group())
        update_network = await rq.get_neuro_by_id(update_network_id)
        await state.set_state(admin_states.UpdateNeuro.update_start)
        await state.update_data(network_id = update_network_id)
        await callback.message.answer('Виберіть поле, яке хочете змінити', 
        reply_markup=await admin_keyboards.all_network_info(update_network))
    except Exception as e:
        await state.clear()
        await callback.message.answer(text=f'Сталася помилка {e}')

#=========================== Оновлення імені
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_name'))
async def get_new_neuro_name(callback : CallbackQuery, state : FSMContext):
    await state.set_state(admin_states.UpdateNeuro.new_name)
    await callback.answer(None)
    await callback.message.answer('Введіть нове ім\'я для нейронки')


@admin_router.message(admin_states.UpdateNeuro.new_name)
async def set_new_neuro_name(message : Message, state : FSMContext):  
    try:  
        data = await state.get_data()
        network_id = data["network_id"]
        if await rq.check_neuro_exist(network_id):
            await rq.update_neuro_name(network_id, message.text)            
            await message.answer("Назву змінено")
        else :
            await message.answer('Схоже, ця нейронка була видалена кимось')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#=========================== Оновлення опису
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_description'))
async def get_new_neuro_description(callback : CallbackQuery, state : FSMContext):
    await state.set_state(admin_states.UpdateNeuro.new_description)
    await callback.answer(None)
    await callback.message.answer('Введіть новий опис нейронки (до 300 символів)')


@admin_router.message(admin_states.UpdateNeuro.new_description)
async def set_new_neuro_description(message : Message, state : FSMContext):   
    try: 
        data = await state.get_data()
        network_id = data["network_id"]
        if await rq.check_neuro_exist(network_id):
            await rq.update_neuro_description(network_id, message.text)
            await message.answer("Опис змінено")
        else:
            await message.answer('Схоже, ця нейронка була видалена кимось')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#=========================== Оновлення типу нейронки
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_type'))
async def update_neuro_type_start(callback : CallbackQuery, state: FSMContext):
    await state.set_state(admin_states.UpdateNeuro.update_neuro_type)
    await callback.answer(None)
    await callback.message.answer('Оберіть новий тип зі списку', reply_markup = await admin_keyboards.choose_neuro_types_keyboard())


@admin_router.callback_query(admin_states.UpdateNeuro.update_neuro_type, F.data.startswith('choose_neuro_type_'))
async def update_neuro_type(callback : CallbackQuery, state: FSMContext):
    try:
        neuro_type_id = re.search(r'\d+', callback.data)
        await callback.answer(None)
        if not neuro_type_id:
            await state.set_state(admin_states.UpdateNeuro.new_update_neuro_type)
            await callback.message.answer('Створимо новий тип. Введіть його назву')
        else:
            data = await state.get_data()
            network_id = data["network_id"]
            if await rq.check_neuro_exist(network_id) and await rq.check_neuro_type_exist(neuro_type_id):
                await rq.update_neuro_type(network_id, int(neuro_type_id.group()))
                await callback.message.answer('Тип успішно оновлено')
            else:
                await callback.message.answer('Схоже, ця нейронка, або тип, були видалені кимось')
            await state.clear()
    except Exception as e:
        await state.clear()
        await callback.message.answer(text=f'Сталася помилка {e}')


@admin_router.message(admin_states.UpdateNeuro.new_update_neuro_type)
async def update_neuro_type_create(message: Message, state: FSMContext):
    try:
        new_type = NeuroType(name = message.text)            
        data = await state.get_data()
        network_id = data["network_id"]

        if await rq.check_neuro_exist(network_id):
            new_type_id = await rq.write_neuro_type_to_DB(new_type)
            await rq.update_neuro_type(network_id, new_type_id)
            await state.clear()
            await message.answer('Тип успішно створено і оновлено')            
        else:
            await message.answer('Схоже нейронка, якій ви хочете оновити тип, була видалена раніше')
        await state.clear()

    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#=========================== Оновлення відео-тутору
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_video'))
async def get_new_neuro_video_tutorial(callback : CallbackQuery, state : FSMContext):
    await state.set_state(admin_states.UpdateNeuro.update_neuro_video_tutorial)
    await callback.answer(None)
    await callback.message.answer('Киньте посилання на новий відео-тутор')


@admin_router.message(admin_states.UpdateNeuro.update_neuro_video_tutorial)
async def set_new_neuro_video_tutorial(message : Message, state : FSMContext):  
    try:  
        data = await state.get_data()
        network_id = data["network_id"]
        if await rq.check_neuro_exist(network_id):
            await rq.update_neuro_video_tutorial(network_id, message.text)
            await message.answer("Відео-тутор оновлено")
        else:
            await message.answer('Схоже, ця нейронка була видалена кимось')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#=========================== Оновлення посилання на повідомлення
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_message'))
async def get_new_neuro_message_ref(callback : CallbackQuery, state : FSMContext):
    await state.set_state(admin_states.UpdateNeuro.update_neuro_message_ref)
    await callback.answer(None)
    await callback.message.answer('Киньте посилання на нове повідомлення з деталями про нейронку')


@admin_router.message(admin_states.UpdateNeuro.update_neuro_message_ref)
async def set_new_neuro_message_ref(message : Message, state : FSMContext):  
    try:  
        data = await state.get_data()
        network_id = data["network_id"]
        if await rq.check_neuro_exist(network_id):
            await rq.update_neuro_message_ref(network_id, message.text)            
            await message.answer("Повідомлення оновлено")
        else:
            await message.answer('Схоже, ця нейронка була видалена кимось')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#=========================== Оновлення посилання на нейронку
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_ref'))
async def get_new_neuro_ref(callback : CallbackQuery, state : FSMContext):
    await state.set_state(admin_states.UpdateNeuro.update_neuro_ref)
    await callback.answer(None)
    await callback.message.answer('Киньте нове посилання на нейронку')


@admin_router.message(admin_states.UpdateNeuro.update_neuro_ref)
async def set_new_neuro_ref(message : Message, state : FSMContext): 
    try:   
        data = await state.get_data()
        network_id = data["network_id"]
        if await rq.check_neuro_exist(network_id):
            await rq.update_neuro_ref(network_id, message.text)
            await message.answer("Посилання на нейронку оновлено")
        else:
            await message.answer('Схоже, ця нейронка була видалена кимось')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#=========================== Оновлення доступності
@admin_router.callback_query(admin_states.UpdateNeuro.update_start, F.data.startswith('update_neuro_available'))
async def get_new_neuro_available(callback : CallbackQuery, state : FSMContext):
    await state.set_state(admin_states.UpdateNeuro.update_is_available)
    await callback.answer(None)
    await callback.message.answer('Напишіть \'так\', щоб  дозволити перегляд, або \'ні\', щоб заборонити')


@admin_router.message(admin_states.UpdateNeuro.update_is_available)
async def set_new_neuro_available(message: Message, state: FSMContext):
    try:
        message_answer = message.text.strip().lower()
        is_available = False
        if message_answer == 'так':
            is_available = True
        elif message_answer == 'ні':
            is_available = False

        data = await state.get_data()
        network_id = data["network_id"]
        if await rq.check_neuro_exist(network_id):
            await rq.update_neuro_is_available(network_id, is_available)
            await message.answer('Доступ до читання оновлено')
        else:
            await message.answer('Схоже, ця нейронка була видалена кимось')
        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
#===========================

#===============================================================

#=============================================================== Видалення типу нейронки

@admin_router.message(Command('delete_neuro_type'), AdminFilter())
async def get_neuro_type_for_delete(message : Message):
    await message.answer('Оберіть тип нейронки, який хочете видалити', reply_markup= await admin_keyboards.delete_neuro_type_keyboard())


@admin_router.callback_query(F.data.startswith('delete_neuro_type_'))
async def confirm_neuro_type_delete(callback : CallbackQuery, state : FSMContext):
    try:
        await callback.answer(None)
        neuro_type_id = int(re.search(r'\d+', callback.data).group())
        if await rq.check_neuro_type_exist(neuro_type_id):
            await state.update_data(delete_neuro_type = neuro_type_id)
            await state.set_state(admin_states.DelteNeuroType.confirm_neuro_type_delete)
            await callback.message.answer('Напишіть \'так\', щоб підтвердити видалення, або \'ні\', щоб скасувати')
            await callback.message.answer('Схоже, цей тип вже було видалено раніше')
        else:
            await callback.message.answer('Схоже, цей тип вже було видалено раніше')
    except Exception as e:
        await state.clear()
        await callback.message.answer(text=f'Сталася помилка {e}')


@admin_router.message(admin_states.DelteNeuroType.confirm_neuro_type_delete)
async def delete_neuro_type(message : Message, state :FSMContext):
    try:
        message_answer = message.text.strip().lower()
        if message_answer == 'так':
            data = await state.get_data()
            if await rq.check_neuro_type_exist(data["delete_neuro_type"]):
                await rq.delete_neuro_type(data["delete_neuro_type"])
                await message.answer('Тип видалено')
            else:
                await message.answer('Схоже, цей тип вже видалили раніше')
        else:
            await message.answer('Видалення типу скасовано')

        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
    

#===============================================================

#=============================================================== Видалення нейронки

@admin_router.message(Command('delete_neuro'), AdminFilter())
async def get_neuro_type_for_delete(message : Message):
    await message.answer('Оберіть нейронку, яку хочете видалити', reply_markup= await admin_keyboards.delete_neuro_networks_keyboard())


@admin_router.callback_query(F.data.startswith('delete_neuro_network_'))
async def confirm_neuro_type_delete(callback : CallbackQuery, state : FSMContext):
    neuro_id = int(re.search(r'\d+', callback.data).group())
    await callback.answer(None)
    await state.update_data(delete_neuro = neuro_id)
    await state.set_state(admin_states.DeleteNeuro.confirm_neuro_delete)
    await callback.message.answer('Напишіть \'так\', щоб підтвердити видалення, або \'ні\', щоб скасувати')


@admin_router.message(admin_states.DeleteNeuro.confirm_neuro_delete)
async def delete_neuro_type(message : Message, state :FSMContext):
    try:
        message_answer = message.text.strip().lower()
        if message_answer == 'так':
            data = await state.get_data()
            if await rq.check_neuro_exist(data["delete_neuro"]):
                await rq.delete_neuro(data["delete_neuro"])
                await message.answer('Нейронку видалено')
            else:
                await message.answer('Схоже, цю нейронку вже видалили раніше')
        else:
            await message.answer('Видалення нейронки скасовано')

        await state.clear()
    except Exception as e:
        await state.clear()
        await message.answer(text=f'Сталася помилка {e}')
    

#===============================================================