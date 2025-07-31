from fastapi import FastAPI, Request
import database
import bot
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.to_thread(bot.start_bot))

@app.post("/payment-callback")
async def payment_callback(request: Request):
    data = await request.json()
    if data.get("status") == "paid":
        user_id = int(data.get("order_id"))
        database.activate_subscription(user_id)
        return {"status": "ok"}
    return {"status": "ignored"}
