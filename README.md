# Tractive Alerts

A small async script that checks the battery level of your [Tractive](https://tractive.com) GPS pet trackers and sends a
Telegram notification when any tracker drops below a configurable threshold.

## Prerequisites

- Python >= 3.13
- A Tractive account (email + password)
- A Telegram bot token and chat ID (see [Creating a new bot](https://core.telegram.org/bots#creating-a-new-bot))

## Installation

```sh
uv sync
```

## Configuration

All configuration is via environment variables.

| Variable             | Required | Default | Description                                                                |
| -------------------- | -------- | ------- | -------------------------------------------------------------------------- |
| `EMAIL`              | yes      | -       | Tractive account email.                                                    |
| `PASSWORD`           | yes      | -       | Tractive account password.                                                 |
| `TELEGRAM_BOT_TOKEN` | yes      | -       | Token for the Telegram bot that sends notifications.                       |
| `TELEGRAM_CHAT_ID`   | yes      | -       | Telegram chat/channel ID to post messages to.                              |
| `BATTERY_THRESHOLD`  | no       | `50`    | Percentage below which a low-battery notification is sent. Must be an int. |
| `TRACKER_NAMES`      | no       | -       | JSON object mapping tracker IDs to pet names (see below).                  |

### Personalizing notifications

`TRACKER_NAMES` is a JSON object mapping a tracker's `_id` to a pet's name. When a tracker with a low battery is found,
its ID is looked up in this map:

- **Match found:** `<PetName>'s tracker has <level>% battery 🪫`
- **No match:** `Tracker <id> has <level>% battery 🪫` (fallback)

```sh
export TRACKER_NAMES='{"abc123":"Fido","def456":"Rex"}'
```

## Usage

```sh
export EMAIL="you@example.com"
export PASSWORD="your-password"
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF"
export TELEGRAM_CHAT_ID="987654321"
export BATTERY_THRESHOLD=40
export TRACKER_NAMES='{"abc123":"Fido"}'

uv run main.py
```

For each tracker whose `battery_level` is below `BATTERY_THRESHOLD`, a message is printed to stdout and posted to the
configured Telegram chat.
