import telebot, json, threading
from flask import Flask
from pathlib import Path
TOKEN = "8874296813:AAE4YZuZN5ag8o1pyh7MyXFRcMmQhsNHDI8"
bot = telebot.TeleBot(TOKEN)
app = Flask('')
@app.route('/')
def home(): return "Aziziyah Bot Shagal"
threading.Thread(target=lambda: app.run(host='0.0.0.0',port=8080)).start()
ORDERS_FILE = Path("orders.json")
LOCK = threading.Lock()
MENU = {"classic":{"name":"برگر كلاسيك","price":7500},"cheese":{"name":"برگر بالجبن","price":8500},"zinger":{"name":"زنجر","price":8000}}
def save_order(order):
    with LOCK:
        data=[]
        if ORDERS_FILE.exists():
            try: data=json.loads(ORDERS_FILE.read_text(encoding='utf-8'))
            except: data=[]
        data.append(order)
        ORDERS_FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
@bot.message_handler(commands=['start'])
def start(m):
    kb=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for v in MENU.values(): kb.add(v['name'])
    bot.send_message(m.chat.id,"أهلا بمطعم العزيزية 🍔\nاختار من المنيو:",reply_markup=kb)
@bot.message_handler(func=lambda m:True)
def handle(m):
    for item in MENU.values():
        if item['name'] in m.text:
            save_order({"user":m.from_user.id,"item":item['name'],"price":item['price']})
            bot.reply_to(m,f"✅ تم طلبك: {item['name']} - {item['price']} دينار")
            return
    bot.reply_to(m,"دز اسم البرگر من المنيو")
print("البوت اشتغل...")
bot.infinity_polling()
