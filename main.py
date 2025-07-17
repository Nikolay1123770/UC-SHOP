import threading
import asyncio
import uvicorn
from freekassa_server import app
from bot import main as bot_main

def run_flask():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_bot():
    asyncio.run(bot_main())

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_bot()
