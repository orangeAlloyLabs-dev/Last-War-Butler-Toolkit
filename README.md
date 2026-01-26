# Last War Butler Toolkit

A Python-based toolkit for Last War alliance management, including a Discord bot, data analytics, and a web dashboard. An Orange Alloy Labs production

## Features

- **Discord Bot**: Coordination and notifications for your alliance
- **Data Tracker**: Track player stats and war results
- **Dashboard**: Streamlit web interface for visualization
- **Automation**: Scripts for repetitive alliance management tasks

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Quick Start

### 1. Clone and Setup

```bash
cd Last-War-Butler-Toolkit
```

### 2. Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e ".[dev]"
```

### 3. Configure Environment

Copy the example environment file and fill in your values:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `DISCORD_BOT_TOKEN`: Your Discord bot token
- `DISCORD_GUILD_ID`: Your Discord server ID

### 4. Initialize Database

The database will be automatically created on first run. Default location: `data/lastwar.db`

## Usage

### Run Discord Bot
```bash
uv run python -m src.bot.main
```

### Run Dashboard
```bash
uv run streamlit run src/dashboard/app.py
```

The dashboard will be available at http://localhost:8501

### Run Tests
```bash
uv run pytest
```

### Lint and Format Code
```bash
uv run ruff check .
uv run ruff format .
```

## Project Structure

```
Last-War-Butler-Toolkit/
├── src/
│   ├── bot/          # Discord bot
│   ├── data/         # Data models and storage
│   ├── dashboard/    # Streamlit dashboard
│   └── scripts/      # Automation scripts
├── tests/            # Test suite
├── data/             # Local data storage (gitignored)
├── pyproject.toml    # Project configuration
└── .env.example      # Environment template
```

## Creating a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the token to your `.env` file
5. Enable "Message Content Intent" under Privileged Gateway Intents
6. Generate an invite URL under OAuth2 > URL Generator:
   - Scopes: `bot`, `applications.commands`
   - Permissions: `Send Messages`, `Read Message History`, etc.
7. Invite the bot to your server

## License

MIT
