import os
import logging
import anthropic
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Configuración ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres un analista experto en apuestas deportivas con más de 15 años de experiencia.
Tu trabajo es analizar partidos de fútbol y otros deportes y proporcionar predicciones detalladas.

Cuando el usuario te indique un partido, debes responder SIEMPRE en este formato exacto:

⚽ **ANÁLISIS: [Equipo Local] vs [Equipo Visitante]**

📊 **PREDICCIÓN PRINCIPAL**
• Resultado más probable: [resultado]
• Confianza: [porcentaje]%

📈 **PROBABILIDADES ESTIMADAS**
• Victoria local: [X]%
• Empate: [X]%
• Victoria visitante: [X]%

🎯 **APUESTAS RECOMENDADAS**
• Bet principal: [descripción] → Cuota mínima recomendada: [X.XX]
• Bet secundaria: [descripción] → Cuota mínima recomendada: [X.XX]

🧠 **RAZONAMIENTO**
[3-4 frases explicando el análisis basado en forma reciente, historial h2h, lesiones conocidas, contexto del partido]

⚠️ **AVISO DE RIESGO**
Nivel de riesgo: [BAJO / MEDIO / ALTO]
Stake recomendado: [1-5]% del bankroll

---
⚠️ *Esto es solo análisis informativo. Apuesta siempre con responsabilidad.*

Si el usuario no menciona un partido concreto, pídele que especifique los dos equipos.
Si no reconoces el partido o los equipos, indícalo honestamente pero intenta igualmente dar un análisis general.
Responde siempre en español."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Bot de Análisis de Apuestas Deportivas*\n\n"
        "Bienvenido. Puedo analizar partidos y darte predicciones con IA.\n\n"
        "📌 *Comandos:*\n"
        "• /predecir [partido] — Analiza un partido\n"
        "• /ayuda — Ver instrucciones\n\n"
        "💬 O simplemente escríbeme el partido directamente:\n"
        "_Ej: Real Madrid vs Barcelona_\n"
        "_Ej: Análisis Manchester City vs PSG_",
        parse_mode="Markdown",
    )


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *¿Cómo usar el bot?*\n\n"
        "1️⃣ Escribe el nombre de los dos equipos\n"
        "   _Ejemplo: Bayern Munich vs Arsenal_\n\n"
        "2️⃣ O usa el comando:\n"
        "   `/predecir Liverpool vs Chelsea`\n\n"
        "3️⃣ Recibirás un análisis completo con:\n"
        "   • Predicción del resultado\n"
        "   • Probabilidades detalladas\n"
        "   • Apuestas recomendadas\n"
        "   • Razonamiento del analista IA\n"
        "   • Nivel de riesgo y stake sugerido\n\n"
        "⚠️ *Recuerda:* Este bot es solo orientativo. Apuesta siempre de forma responsable.",
        parse_mode="Markdown",
    )


async def predecir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        partido = " ".join(context.args)
    else:
        await update.message.reply_text(
            "❌ Indica el partido. Ejemplo:\n`/predecir Real Madrid vs Barcelona`",
            parse_mode="Markdown",
        )
        return
    await analizar_partido(update, partido)


async def mensaje_libre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    await analizar_partido(update, texto)


async def analizar_partido(update: Update, partido: str):
    msg = await update.message.reply_text("🔍 Analizando partido... un momento ⏳")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Analiza este partido y dame tu predicción completa: {partido}",
                }
            ],
        )

        prediccion = response.content[0].text

        await msg.delete()
        await update.message.reply_text(prediccion, parse_mode="Markdown")

    except anthropic.APIError as e:
        logger.error(f"Error Anthropic API: {e}")
        await msg.edit_text("❌ Error al conectar con la IA. Inténtalo de nuevo.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        await msg.edit_text("❌ Algo salió mal. Inténtalo de nuevo en unos segundos.")


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("Falta TELEGRAM_TOKEN en las variables de entorno")
    if not ANTHROPIC_API_KEY:
        raise ValueError("Falta ANTHROPIC_API_KEY en las variables de entorno")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("predecir", predecir))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_libre))

    logger.info("Bot iniciado correctamente ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
