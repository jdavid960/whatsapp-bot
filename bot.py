from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "menu" in incoming_msg:
        msg.body("📋 Menú del bot:\n1. 🎸 Rutina de guitarra\n2. 🏋️ Ejercicio\n3. 🧠 Inglés")
    elif "1" in incoming_msg:
        msg.body("🎸 Hoy toca: 'La Flaca' de Jarabe de Palo. ¡A darle!")
    elif "2" in incoming_msg:
        msg.body("🏋️ 20 minutos de cuerpo completo. ¡Vamos, Juan!")
    elif "3" in incoming_msg:
        msg.body("🧠 Frase del día: 'Keep going, you're doing great!'")
    else:
        msg.body("Hola Juan 👋 Escribe 'menu' para ver opciones.")

    return str(resp)

if __name__ == "__main__":
    app.run()
