import asyncio
import json
import os

import aiohttp
from aiotractive import Tractive

BATTERY_THRESHOLD = 50


async def send_telegram_message(bot_token: str, chat_id: str, message: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, json={"chat_id": chat_id, "text": message}
        ) as response:
            response.raise_for_status()


def build_low_battery_message(
    tracker_id: str, battery_level: int, tracker_names: dict
) -> str:
    name = tracker_names.get(tracker_id)
    if name:
        return f"{name}'s tracker has {battery_level}% battery 🪫"
    return f"Tracker {tracker_id} has {battery_level}% battery 🪫"


async def main(
    email: str,
    password: str,
    battery_threshold: int,
    telegram_bot_token: str,
    telegram_chat_id: str,
    tracker_names: dict,
):
    async with Tractive(email, password) as client:
        await client.authenticate()

        print("Authenticated. Getting trackers...")
        trackers = await client.trackers()

        for tracker in trackers:
            info = await tracker.hw_info()
            tracker_id = info.get("_id")
            if not tracker_id:
                continue
            battery_level = info.get("battery_level", 0)

            if battery_level < battery_threshold:
                message = build_low_battery_message(
                    tracker_id, battery_level, tracker_names
                )
                print(message)
                await send_telegram_message(
                    telegram_bot_token, telegram_chat_id, message
                )


if __name__ == "__main__":
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    if not email or not password:
        raise Exception("EMAIL and PASSWORD are required env vars")

    try:
        battery_threshold = int(os.getenv("BATTERY_THRESHOLD", BATTERY_THRESHOLD))
    except ValueError:
        raise Exception("BATTERY_THRESHOLD must be an integer")

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not telegram_bot_token or not telegram_chat_id:
        raise Exception("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required env vars")

    tracker_names = {}
    if raw_names := os.getenv("TRACKER_NAMES"):
        try:
            tracker_names = json.loads(raw_names)
        except json.JSONDecodeError:
            raise Exception("TRACKER_NAMES must be valid JSON")

    asyncio.run(
        main(
            email,
            password,
            battery_threshold,
            telegram_bot_token,
            telegram_chat_id,
            tracker_names,
        )
    )
