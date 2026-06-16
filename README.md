# 🤖 Bot de Análisis de Apuestas Deportivas

Bot de Telegram que usa IA (Claude) para analizar partidos y dar predicciones detalladas.

---

## 📋 Requisitos

- Python 3.10+
- Cuenta de Telegram
- API Key de Anthropic (https://console.anthropic.com)

---

## 🚀 Instalación paso a paso

### 1. Crear el bot en Telegram

1. Abre Telegram y busca **@BotFather**
2. Escribe `/newbot`
3. Ponle un nombre (ej: `Analizador de Apuestas`)
4. Ponle un username (ej: `mi_apuestas_bot`)
5. BotFather te dará un **token** — guárdalo

### 2. Obtener tu API Key de Anthropic

1. Ve a https://console.anthropic.com
2. Crea una cuenta o inicia sesión
3. Ve a **API Keys** → **Create Key**
4. Copia la key

### 3. Configurar el proyecto

```bash
# Clonar / descargar los archivos
cd telegram-bet-bot

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env y pon tus tokens
```

### 4. Ejecutar el bot

```bash
# Opción A: con variables de entorno en el sistema
export TELEGRAM_TOKEN="tu_token_aqui"
export ANTHROPIC_API_KEY="tu_api_key_aqui"
python bot.py

# Opción B: con dotenv (instala python-dotenv primero)
pip install python-dotenv
# Añade al inicio de bot.py: from dotenv import load_dotenv; load_dotenv()
python bot.py
```

---

## 💬 Comandos del bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Mensaje de bienvenida |
| `/predecir Real Madrid vs Barcelona` | Analiza un partido |
| `/ayuda` | Ver instrucciones |
| Texto libre | También funciona sin comandos |

---

## 📊 Ejemplo de análisis

```
⚽ ANÁLISIS: Real Madrid vs Barcelona

📊 PREDICCIÓN PRINCIPAL
• Resultado más probable: Victoria local
• Confianza: 58%

📈 PROBABILIDADES ESTIMADAS
• Victoria local: 55%
• Empate: 25%
• Victoria visitante: 20%

🎯 APUESTAS RECOMENDADAS
• Bet principal: Real Madrid o empate (doble oportunidad) → Cuota mínima: 1.35
• Bet secundaria: Ambos equipos marcan → Cuota mínima: 1.75

🧠 RAZONAMIENTO
El Real Madrid llega en excelente forma con 4 victorias consecutivas...

⚠️ AVISO DE RIESGO
Nivel de riesgo: MEDIO
Stake recomendado: 2% del bankroll
```

---

## ☁️ Despliegue en servidor (opcional)

Para que el bot esté activo 24/7, puedes desplegarlo en:
- **Railway** (gratis) → https://railway.app
- **Render** (gratis) → https://render.com
- **VPS** (DigitalOcean, Contabo, etc.)

---

⚠️ *Este bot es solo para fines informativos. Apuesta siempre de forma responsable.*
