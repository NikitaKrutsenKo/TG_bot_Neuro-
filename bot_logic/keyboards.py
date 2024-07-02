from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_features_keyboard = ReplyKeyboardMarkup(keyboard=
        [[KeyboardButton(text='Навігатор')]],        
    resize_keyboard=True, 
    input_field_placeholder='Оберіть задачу'
)

neuro_type_keyboard = ReplyKeyboardMarkup(keyboard=
        [[KeyboardButton(text='Відео')]],        
    resize_keyboard=True, 
    input_field_placeholder='Оберіть тип нейронки'
)

main_features_list = {
    'Навігатор': neuro_type_keyboard
}

neuro_type_list = {
    'Відео': 'Відповідь є [тут](https://t.me/c/2156359075/2/3)',
}