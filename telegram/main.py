import asyncio
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

url = "https://api.panferov.site/v1/sentiment"

bot = Bot(token='6894388039:AAGqnXt7UpsG48xH81-I9oum_WxX8K0t3uA')
dp = Dispatcher()


@dp.message(Command('start'))
async def start(msg: types.Message):
    await msg.answer('Отправь мне текст, а я определю его характер')


@dp.message()
async def get_message(msg: types.Message, bot: Bot):
    await msg.answer('Запрос принят, ожидайте выполнения...')
    headers = {'Content-type': 'application/json'}
    data = {'messages': [f'{msg.text}']}
    response = requests.post(url, json=data, headers=headers).json()
    d = {'positive': 'Позитивное сообщение', 'neutral': 'Нейтральное сообщение', 'negative': 'Негативное сообщение',
         'speech': 'Управление коммуникацией', 'skip': 'Тональность сообщения не определена'}
    mx = [0, 0]
    for i in response[0]["functional_sentiment"]:
        if response[0]["functional_sentiment"][i] > mx[1]:
            mx = [i, response[0]["functional_sentiment"][i]]
    if response:
        await bot.edit_message_text(f'Был обнаружен:\n{response[0]["detected_language"]}\n\n'
                                    f'Функциональный анализ:\n{d[mx[0]]}\n\n'
                                    f'Эмоциональный анализ:\n{response[0]["emotional_sentiment"]}',
                                    message_id=msg.message_id + 1,
                                    chat_id=msg.from_user.id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
