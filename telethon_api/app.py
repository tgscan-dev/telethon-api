import os

from fastapi import FastAPI
from loguru import logger
from telethon.sync import TelegramClient

sessions_folder = "telethon_api/session"
api_id = 1024
api_hash = "b18441a1ff607e10a989891a5462e627"
clients = []

app = FastAPI()


@app.get("/get_chat_history_count/{username}")
async def get_chat_history_count(username: str, client_idx: int):
    try:
        client = clients[client_idx]
        count = (await client.get_messages(username, limit=0)).total

        return {"code": 0, "data": f"{count}"}
    except Exception as e:
        return {"code": -1, "data": f"{e}"}


async def main():
    for filename in os.listdir(sessions_folder):
        if filename.__contains__("journal"):
            continue
        if not filename.endswith(".session"):
            continue
        session_file = os.path.join(sessions_folder, filename)

        try:
            client = TelegramClient(session_file, api_id, api_hash)
            await client.start('9')
            clients.append(client)
            # print(await client.get_me())
            logger.info(session_file + " login success")
        except Exception as e:
            logger.error(f"{session_file} login fail: {e}")


@app.on_event("startup")
async def startup_event():
    await main()
    logger.info("start success")
