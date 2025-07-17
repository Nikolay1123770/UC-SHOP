from flask import Flask, request
import hashlib

app = Flask(__name__)

MERCHANT_ID = "63882"
SECRET_2 = "m)OkN.hH/ZJ^eS2"

@app.route("/freekassa/callback", methods=["POST"])
def callback():
    data = request.form
    sign_str = f"{data['MERCHANT_ID']}:{data['AMOUNT']}:{SECRET_2}:{data['intid']}"
    expected_sign = hashlib.md5(sign_str.encode()).hexdigest()

    if data.get("SIGN") != expected_sign:
        return "Invalid SIGN", 400

    print("✅ Оплата подтверждена:", data)
    # Здесь можно отправить сообщение в Telegram-бот о подтверждении оплаты
    return "YES", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
