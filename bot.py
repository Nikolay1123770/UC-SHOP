import asyncio
import hashlib
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "7617774533:AAGkOJwFblUBZjEkBDx8nIpvFwQ2EZkzS2U"
MERCHANT_ID = "63882"
SECRET_1 = "}kv}fs0X2EnD,vu"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Пример товара
packs = {
    "100uc": {"price": 100, "uc": 100},
    "500uc": {"price": 450, "uc": 500},
}

def get_freekassa_url(user_id: int, amount: int, order_id: str):
    sign_str = f"{MERCHANT_ID}:{amount}:{SECRET_1}:{order_id}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return f"https://pay.freekassa.ru/?m={MERCHANT_ID}&oa={amount}&o={order_id}&s={sign}&us_user={user_id}"

@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = InlineKeyboardBuilder()
    for key, pack in packs.items():
        kb.button(
            text=f"Купить {pack['uc']} UC за {pack['price']} руб.",
            callback_data=f"buy:{key}"
        )
    kb.adjust(1)
    await message.answer("Выберите пакет UC для покупки:", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("buy:"))
async def handle_purchase(call: CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    pack_key = call.data.removeprefix("buy:")
    pack = packs.get(pack_key)
    if not pack:
        await call.message.answer("Пакет не найден.")
        return
    order_id = f"{user_id}_{pack['uc']}_{int(time.time())}"
    pay_url = get_freekassa_url(user_id, pack["price"], order_id)
    text = (f"Оплата пакета {pack['uc']} UC
"
            f"Сумма: {pack['price']} руб.

"
            f"Перейдите по ссылке для оплаты:
{pay_url}")
    await call.message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
