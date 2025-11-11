import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "8294189105:AAHNetFIEPE5E4i3WV5wFd4QZbbhn3VGJGU"   # 🔑 Бу ерга ўз токенингизни қўйинг

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- Ma'lumotlar bazasi ---
conn = sqlite3.connect("lostfound.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    date TEXT,
    info TEXT
)""")
conn.commit()

# --- Start komandasi ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "👋 Assalomu alaykum!\n"
        "Bu <b>TOSHKENT METRO Lost & Found</b> bot.\n\n"
        "🔎 Qidirish uchun: <code>/search so'z</code>\n"
        
    )

# --- Qidirish ---
@dp.message_handler(commands=['search'])
async def search_item(message: types.Message):
    text = message.text.replace("/search", "").strip()
    if text == "":
        await message.answer("❗ Iltimos, qidirilayotgan buyumni yozing.\nMisol: /search telefon")
        return
    cursor.execute("SELECT id, name, location, date, info FROM items WHERE name LIKE ?", ('%' + text + '%',))
    results = cursor.fetchall()
    if results:
        msg = "🔎 Topilgan buyumlar:\n\n"
        for r in results:
            msg += f"🆔 <b>{r[0]}</b>\n📌 {r[1]} — {r[2]} ({r[3]})\nℹ️ {r[4]}\n\n"
        await message.answer(msg)
    else:
        await message.answer("❌ Hech narsa topilmadi.")

# --- Yangi buyum qo'shish ---
@dp.message_handler(commands=['add'])
async def add_item(message: types.Message):
    try:
        parts = message.text.split(" ", 3)   # 4 қисмга бўламиз
        if len(parts) < 4:
            await message.answer("❗ Format noto‘g‘ri.\nNamuna: /add Telefon Chilonzor 25.08.2025 qora_qop")
            return

        _, name, location, rest = parts
        date, info = rest.split(" ", 1)   # қолганини сана ва маълумотга ажратамиз

        cursor.execute("INSERT INTO items (name, location, date, info) VALUES (?, ?, ?, ?)",
                       (name, location, date, info))
        conn.commit()
        await message.answer("✅ Buyum qo'shildi.")
    except Exception as e:
        await message.answer("❗ Format noto‘g‘ri.\nNamuna: /add Telefon Chilonzor 25.08.2025 qora_qop")

# --- O'chirish ---
@dp.message_handler(commands=['delete'])
async def delete_item(message: types.Message):
    try:
        item_id = int(message.text.split()[1])
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        await message.answer(f"✅ ID {item_id} бўйича ёзув ўчирилди!")
    except Exception as e:
        await message.answer("❌ Ўчиришда хатолик! Тўғри ID киритинг.")

# --- Ma'lumotni tahrirlash ---
@dp.message_handler(commands=['edit'])
async def edit_item(message: types.Message):
    try:
        _, item_id, new_info = message.text.split(" ", 2)
        item_id = int(item_id)
        cursor.execute("UPDATE items SET info = ? WHERE id = ?", (new_info, item_id))
        conn.commit()
        await message.answer(f"✅ ID {item_id} маълумоти '{new_info}'га ўзгартирилди!")
    except Exception as e:
        await message.answer("❌ Янгилашда хатолик! Формат: /edit ID yangi_ma'lumot")

# --- Botni ishga tushirish ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
