import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import (createregistredbotuser,imgword,imgwordcheck,updatecheckeduser,
                updateuserage,checkregistredbotuser,
                updatealloweduser,getbotuser,getcategorybyplname,checkallowuser)

from buttons import vote,categories,categoryplaces
from draw import drawimg
logging.basicConfig(level=logging.INFO)

API_TOKEN = "1974105410:AAEgB77ojFYxBhuvH_oz6y9qv7F2GOq7diw"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class PhoneNumber(StatesGroup):
    phone = State()

# start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = int(message.chat.id)
    await message.answer("Assalomu alaykum, eng yaxshi brendlarni aniqlash uchun tashkil etilgan 🏆 YOSHLAR TEXNOPARKI VOTE tanlovining ovoz berish botiga xush kelibsiz!")
    await message.answer_photo(open("start.jpg","rb"),caption="🏆 YOSHLAR TEXNOPARKI VOTE tanlovi orqali Eng yaxshi brendlarni aniqlang!\n\n📄 Tanlov natijalari vote.uz platformasida yoritib boriladi:\n👉 https://vote.uz")
    if checkregistredbotuser(user_id):
        add_brand = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_brand.row(types.KeyboardButton(text="➕ brend qo'shish"),types.KeyboardButton(text="natijalar 📈"))
        await message.answer("Agar o'z brendingizni qo'shmoqchi bo'lsangiz brend qo'shish tugmasini bosing",reply_markup=add_brand)
        await message.answer("Ovoz berishni boshlashingiz mumkun ovoz berish tugmasini bosing",reply_markup=vote())
    else:
        phone_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        phone_keyboard.add(types.KeyboardButton(text="raqamni tasdiqlash ☎️", request_contact=True))
        await message.answer("Raqamningizni tasdiqlang raqamni tasdqilash tugmasini bosning",reply_markup=phone_keyboard)
        await PhoneNumber.phone.set()

class ImgWord(StatesGroup):
    check = State()

@dp.message_handler(state=PhoneNumber.phone,content_types=types.ContentTypes.CONTACT)
async def registredbotuser(message: types.Message, state: FSMContext):
    phonenumber = message.contact.phone_number
    createregistredbotuser(phonenumber,message.chat.id,message.chat.username)
    await state.finish()
    await message.answer("Muvofaqiyatlik yuborildi ✅", reply_markup=types.ReplyKeyboardRemove())
    drawimg()
    imgword(message.chat.id,drawimg())
    await message.answer_photo(open("img/test.png","rb"),caption="rasmdagi so'zni yozing")
    await ImgWord.check.set()

class UserAge(StatesGroup):
    age = State()

@dp.message_handler(state=ImgWord.check)
async def checkimgword(message: types.Message, state: FSMContext):
    dbword = imgwordcheck(message.chat.id).lower()
    msgword = message.text.lower()
    if dbword == msgword:
        updatecheckeduser(message.chat.id)
        await message.answer("Tekshiruv ko'di tasdiqlandi ✅")
        await state.finish()
        await message.answer("Iltimos yoshingizni kiritin?\nhohlamasangiz 'no' so'zini yozing")
        await UserAge.age.set()
    else:
        drawimg()
        imgword(message.chat.id, drawimg())
        await message.answer_photo(open("img/test.png", "rb"), caption="👆 itimos ovoz berishni boshlash uchun rasmdagi so'zni to'g'ri yozing")

class Status(StatesGroup):
    status = State()

@dp.message_handler(state=UserAge.age)
async def agewrite(message: types.Message, state: FSMContext):
    userid = int(message.chat.id)
    if message.text.lower() != "no":
        if message.text.isdigit():
            msgage = int(message.text)
            if msgage <= 80 and msgage >= 12:
                updateuserage(userid,msgage)
                status_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton(text="roziman ✅")
                button2 = types.KeyboardButton(text="roziemasman ❌")
                status_keyboard.row(
                    button1,button2
                )
                await message.answer("Muvofaqiyatlik yuborildi ✅")
                await message.answer("Iltimos nizom bilan tanishib chiqing\nhttp://vote.uz/nizom\nagar nizomga rozi bo'lgan bo'lsangiz roziman tugmasini bosing\naks holda roziemasman tugmasini bosing",reply_markup=status_keyboard)
                await state.finish()
                await Status.status.set()
            else:
                await message.answer("Yoshingizn 12dan katta 80dan kichik bo'lishi kerag")
        else:
            await message.answer("Iltimos yoshingizni kiritin faqat son ko'rinishida")
    else:
        updateuserage(userid, 0)
        status_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="roziman ✅")
        button2 = types.KeyboardButton(text="roziemasman ❌")
        status_keyboard.row(
            button1, button2
                            )
        await message.answer("Yoshingizni mahfiy qoldi ✅")
        await message.answer("Iltimos nizom bilan tanishib chiqing\nhttp://vote.uz/nizom\nagar nizomga rozi bo'lgan bo'lsangiz roziman tugmasini bosing\naks holda roziemasman tugmasini bosing",reply_markup=status_keyboard)
        await state.finish()
        await Status.status.set()

@dp.message_handler(state=Status.status)
async def status(message: types.Message, state: FSMContext):
    msg = str(message.text.lower())
    if msg == "roziman ✅":
        updatealloweduser(message.chat.id)
        await state.finish()
        add_brand = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_brand.row(types.KeyboardButton(text="➕ brend qo'shish"),types.KeyboardButton(text="natijalar 📈"))
        await message.answer("Agar o'z brendingizni qo'shmoqchi bo'lsangiz brend qo'shish tugmasini bosing",reply_markup=add_brand)
        await message.answer("Ovoz berish uchun ovoz berish tugmasini bosing",reply_markup=vote())
    elif msg == "roziemasman ❌":
        await state.finish()
        add_brand = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_brand.row(types.KeyboardButton(text="➕ brend qo'shish"),types.KeyboardButton(text="natijalar 📈"))
        await message.answer("Agar o'z brendingizni qo'shmoqchi bo'lsangiz brend qo'shish tugmasini bosing",reply_markup=add_brand)
        await message.answer("Ovoz berish uchun ovoz berish tugmasini bosing", reply_markup=vote())
    else:
        await message.answer("Iltimos faqat tumalardn birini bosing")

class StatusAgain(StatesGroup):
    status = State()

class AllowUser(StatesGroup):
    allow = State()

@dp.message_handler()
async def other(message: types.Message):
    if checkregistredbotuser(message.chat.id):
        if message.text == "➕ brend qo'shish":
            if checkallowuser(message.chat.id):
                await message.answer("Iltimos siz bilan bog'lanish mumkun bo'lgan telefo'n raqam va brend nomini va brend haqida yozing",reply_markup=types.ReplyKeyboardRemove())
                await AllowUser.allow.set()
            else:
                status_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton(text="roziman ✅")
                button2 = types.KeyboardButton(text="roziemasman ❌")
                status_keyboard.row(
                    button1, button2
                )
                await message.answer("Iltimos brend qo'shish uchun nizom bilan tanishib chqing va rozi bo'ling agar rozi bo'lmasangiz brend qo'sha olmaysiz\nnizom http://vote.uz/nizom",reply_markup=status_keyboard)
                await StatusAgain.status.set()
        elif message.text == "natijalar 📈":
            await message.answer("Natijalar https://vote.uz saytida")
        else:
            add_brand = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            add_brand.row(types.KeyboardButton(text="➕ brend qo'shish"),types.KeyboardButton(text="natijalar 📈"))
            await message.answer("Agar o'z brendingizni qo'shmoqchi bo'lsangiz brend qo'shish tugmasini bosing",reply_markup=add_brand)
            await message.answer("Ovoz berishni boshlashingiz mumkun ovoz berish tugmasini bosing", reply_markup=vote())
    else:
        await message.answer("ro'yhatdan o'tmagansiz iltimos /start ni bosing")



@dp.message_handler(state=StatusAgain.status)
async def statusagain(message: types.Message, state: FSMContext):
    msg = str(message.text.lower())
    if msg == "roziman ✅":
        updatealloweduser(message.chat.id)
        await message.answer("Iltimos siz bilan bog'lanish mumkun bo'lgan telefo'n raqam va brend nomini va brend haqida yozing",reply_markup=types.ReplyKeyboardRemove())
        await AllowUser.allow.set()
        await state.finish()
    elif msg == "roziemasman ❌":
        add_brand = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_brand.add(types.KeyboardButton(text="➕ brend qo'shish"))
        await message.answer("Afsus nizomga rozi bo'lmasangiz brend qo'sha olmaysiz",reply_markup=add_brand)
        await message.answer("Ovoz berish uchun ovoz berish tugmasini bosing", reply_markup=vote())
        await state.finish()
    else:
        await message.answer("Iltimos faqat tumalardn birini bosing")

@dp.message_handler(state=AllowUser.allow)
async def addbrand(message: types.Message, state: FSMContext):
    if len(message.text) >= 30:
        # await Bot(token="1974105410:AAEgB77ojFYxBhuvH_oz6y9qv7F2GOq7diw").send_message(1144957860,f"Yangi brend:\n{message.text}")
        add_brand = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        add_brand.row(types.KeyboardButton(text="➕ brend qo'shish"), types.KeyboardButton(text="natijalar 📈"))
        await message.answer("Muvofaqiyatlik yuborildi siz bilan bo'glanishadi",reply_markup=add_brand)
        await state.finish()
    else:
        await message.answer("Iltimos malumotni to'lliq yozing 30ta harfdan yuqori bo'lishi kerag")

@dp.callback_query_handler(lambda c: c.data == 'vote')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Iltimos kategoriyalardan tanlang",reply_markup=categories())

@dp.callback_query_handler(lambda call:True)
async def process_callback_button(call: types.CallbackQuery):
    if call.data.startswith("forallcategory"):
        category_name = call.data[14:]
        placesbtns = categoryplaces(category_name)
        await bot.send_message(call.from_user.id,"Joy nomini tanlang va bosing",reply_markup=placesbtns)
    elif call.data.startswith("forplaces"):
        place_name = call.data[9:]
        if getbotuser(place_name,call.from_user.id,call.from_user.first_name):
            success_category =  getcategorybyplname(place_name)
            await bot.send_message(call.from_user.id,"Muvofaqiyatlik ovoz berdingiz ✅")
            # await bot.answer_callback_query(call.id,f"Eng yaxshi\n{success_category} lardan biriga\nmuvofaqiyatlik ovoz berdingiz ✅",show_alert=True)

        else:
            error_category = getcategorybyplname(place_name)
            await bot.send_message(call.from_user.id, f"❌ Siz oldin eng yaxshi {error_category} lardan biriga ovoz bergansiz iltimos boshqa kategoriya tanlab ovoz berin",reply_markup=categories())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)