from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import datetime

app = Flask(__name__)

# Rutinas físicas
rutinas = {
    "Monday": "Piernas & glúteos 🍑",
    "Tuesday": "Pecho & tríceps 💪",
    "Wednesday": "Espalda & bíceps 🏋️",
    "Thursday": "Core (abdomen) 🔥",
    "Friday": "Full body dinámico ⚡",
    "Saturday": "Piernas & core 🚴",
    "Sunday": "Movilidad & recuperación 🧘"
}

# Hobbies nocturnos
hobbies = {
    "Monday": "🎸 Guitarra",
    "Tuesday": "🎮 Gaming",
    "Wednesday": "🐍 Clase de Python en Platzi",
    "Thursday": "🎸 Guitarra",
    "Friday": "🎮 Gaming",
    "Saturday": "🚴 Ciclismo",
    "Sunday": "🎸 Guitarra o 🚴 Ciclismo"
}

# Frases motivadoras
frases_motivadoras = [
    "You’ve got this, Juan! 💥",
    "Let’s crush today’s workout! 🔥",
    "Every rep counts. Keep going! 💪",
    "Discipline beats motivation. You’re doing great! 🙌",
    "Kyara would be proud 🐶. Let’s move!"
]

# Días de práctica de guitarra
dias_guitarra = ["Monday", "Thursday", "Sunday"]

# Canciones por día
canciones_guitarra = {
    "Monday": "🎸 *La Flaca* – Jarabe de Palo (Am – G – F – E)",
    "Thursday": "🎸 *Persiana Americana* – Soda Stereo (Em – C – G – D)",
    "Sunday": "🎸 *De Música Ligera* (acústica) – Soda Stereo (A – D – E)"
}

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    today = datetime.datetime.now().strftime("%A")
    resp = MessagingResponse()
    msg = resp.message()

    if "menu" in incoming_msg:
        msg.body(
            "📋 *Menú de opciones*\n"
            "1️⃣ *rutina* – Ver tu entrenamiento y hobby\n"
            "2️⃣ *motivación* – Recibir una frase inspiradora\n"
            "3️⃣ *guitarra* – Ver tu canción de práctica (solo en días asignados)\n"
            "4️⃣ *sí rutina* / *no rutina* – Registrar tu ejercicio\n"
            "5️⃣ *sí guitarra* / *no guitarra* – Registrar tu práctica musical\n"
            "6️⃣ *kyara* – Saludo especial para tu compañera peluda 🐶"
        )

    elif "rutina" in incoming_msg:
        rutina_hoy = rutinas.get(today, "¡Día libre! 🎉")
        hobby_hoy = hobbies.get(today, "Descanso creativo 🌙")
        motivacion = frases_motivadoras[datetime.datetime.now().day % len(frases_motivadoras)]
        msg.body(
            f"🏋️ Rutina de hoy: {rutina_hoy}\n"
            f"🌙 Hobby nocturno: {hobby_hoy}\n"
            f"💬 Motivación: {motivacion}\n\n"
            "¿Ya hiciste el ejercicio? Responde *sí rutina* o *no rutina*."
        )

    elif "motivación" in incoming_msg:
        frase = frases_motivadoras[datetime.datetime.now().day % len(frases_motivadoras)]
        msg.body(f"💬 {frase}")

    elif "sí rutina" in incoming_msg:
        with open("registro_rutina.txt", "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d')} ✅ Rutina completada\n")
        msg.body("¡Excelente, Juan! Rutina marcada como completada ✅")

    elif "no rutina" in incoming_msg:
        with open("registro_rutina.txt", "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d')} ❌ Rutina no realizada\n")
        msg.body("No pasa nada, Juan. Mañana es otra oportunidad 💪")

    elif "guitarra" in incoming_msg:
        if today in dias_guitarra:
            cancion_hoy = canciones_guitarra.get(today)
            msg.body(
                f"🎸 Hoy es {today}.\nTu canción de práctica es:\n{cancion_hoy}\n\n¿Ya la tocaste?\nResponde *sí guitarra* o *no guitarra*."
            )
        else:
            msg.body("🎸 Hoy no tienes práctica de guitarra según tu calendario. Puedes repasar o descansar 🎶")

    elif "sí guitarra" in incoming_msg:
        with open("registro_guitarra.txt", "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d')} ✅ Canción practicada\n")
        msg.body("¡Excelente, Juan! 🎶 Canción marcada como practicada ✅")

    elif "no guitarra" in incoming_msg:
        with open("registro_guitarra.txt", "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d')} ❌ Canción no practicada\n")
        msg.body("No pasa nada, Juan. Mañana hay otra oportunidad para rockear 🎸")

    elif "kyara" in incoming_msg:
        msg.body("🐾 ¡Hola Kyara! Espero que hayas tenido una buena caminata hoy. Tu energía alegra la casa 💚")

    else:
        msg.body("¡Hola Juan! Escribe *menu* para ver las opciones disponibles 📋")

    return str(resp)

if __name__ == "__main__":
    app.run()

