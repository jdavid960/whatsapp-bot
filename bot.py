from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import os

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    today = datetime.datetime.now().strftime("%A").lower()

    # Rutina física por día (mañana)
    rutina_mañana = {
        "monday": "🏋️ Piernas: Sentadillas, zancadas, wall sit, elevación de talones",
        "tuesday": "🏋️ Pecho: Flexiones, flexiones inclinadas, apertura con bandas",
        "wednesday": "🏋️ Espalda: Superman, remo con mochila, plancha con elevación de brazo",
        "thursday": "🏋️ Brazos: Fondos en silla, curls con botellas, extensiones de tríceps",
        "friday": "🏋️ Core: Crunches, planchas, elevación de piernas, bicicleta",
        "saturday": "🚴 Ciclismo suave: 20 min de pedaleo o caminata activa",
        "sunday": "🧘 Estiramiento + movilidad: respiración guiada y movilidad articular"
    }

    # Rutina de hobbies por día (noche)
    rutina_noche = {
        "monday": "🎸 Guitarra técnica (La Flaca)",
        "tuesday": "🐍 Clase de Python + 🎸 Guitarra libre",
        "wednesday": "🎮 Gaming (PlayStation)",
        "thursday": "🐍 Clase de Python",
        "friday": "🎮 Gaming libre + relajación",
        "saturday": "🚴 Ciclismo nocturno + 🎸 Guitarra (Soda Stereo)",
        "sunday": "🧘 Reflexión + 🚴 Ciclismo suave"
    }

    # Canciones de guitarra por nivel
    canciones_guitarra = {
        "fácil": {
            "nombre": "Lamento Boliviano – Enanitos Verdes",
            "link": "https://www.youtube.com/watch?v=pz_IQgV6XLs",
            "descripcion": "Acordes sencillos y ritmo estable. Ideal para empezar."
        },
        "intermedio": [
            {
                "nombre": "La Flaca – Jarabe de Palo",
                "link": "https://www.youtube.com/watch?v=bflRZEZPdQg",
                "descripcion": "Acompañamiento vocal y rasgueo fluido."
            },
            {
                "nombre": "Maldito Duende – Héroes del Silencio",
                "link": "https://www.youtube.com/watch?v=UM3oAdBCYlE",
                "descripcion": "Rasgueos intensos y progresión de acordes."
            },
            {
                "nombre": "Mariposa Tecknicolor – Fito Páez",
                "link": "https://www.youtube.com/watch?v=mfomemgURwo",
                "descripcion": "Melodía colorida y ritmo fluido."
            }
        ],
        "avanzado": {
            "nombre": "De Música Ligera – Soda Stereo",
            "link": "https://www.youtube.com/watch?v=TRciSsMYuZ0",
            "descripcion": "Tutorial completo con acordes, punteos y ritmo funky."
        }
    }

    # Comandos
    if "rutina mañana" in incoming_msg:
        msg.body("🌅 Rutina de la mañana (4:00 am – 4:20 am):\n" + "\n".join(
            [f"{day.capitalize()}: {actividad}" for day, actividad in rutina_mañana.items()]
        ))
    elif "rutina noche" in incoming_msg:
        msg.body("🌙 Rutina de la noche (8:45 pm – 10:00 pm):\n" + "\n".join(
            [f"{day.capitalize()}: {actividad}" for day, actividad in rutina_noche.items()]
        ))
    elif "guitarra fácil" in incoming_msg:
        c = canciones_guitarra["fácil"]
        msg.body(f"🎸 Nivel fácil:\n{c['nombre']}\n{c['descripcion']}\n🔗 {c['link']}")
    elif "guitarra intermedio" in incoming_msg:
        intermedias = "\n\n".join([
            f"{c['nombre']}\n{c['descripcion']}\n🔗 {c['link']}"
            for c in canciones_guitarra["intermedio"]
        ])
        msg.body(f"🎸 Nivel intermedio:\n{intermedias}")
    elif "guitarra avanzado" in incoming_msg:
        c = canciones_guitarra["avanzado"]
        msg.body(f"🎸 Nivel avanzado:\n{c['nombre']}\n{c['descripcion']}\n🔗 {c['link']}")
    elif "auto mañana" in incoming_msg:
        actividad = rutina_mañana.get(today, "Descanso activo")
        msg.body(f"🌅 Buenos días, Juan\nHoy toca: {actividad}\n💬 Frase: “Hoy no se trata de intensidad, sino de constancia.”")
    elif "auto noche" in incoming_msg:
        actividad = rutina_noche.get(today, "Descanso emocional")
        tutorial = ""
        if "guitarra" in actividad.lower():
            tutorial = "🎸 Tutorial: https://www.youtube.com/watch?v=bflRZEZPdQg"
        msg.body(f"🌙 Hora de tu rutina nocturna, Juan\nHoy toca: {actividad}\n{tutorial}\n💬 Frase: “Code and strum!”")
    else:
        msg.body("Hola Juan 👋 Escribe:\n- 'rutina mañana' para tu entrenamiento\n- 'rutina noche' para tus hobbies\n- 'guitarra fácil/intermedio/avanzado' para practicar 🎸")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


