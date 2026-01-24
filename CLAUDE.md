# Last War Butler Toolkit - Development Guide

## Project Overview
A Python toolkit for Last War alliance management featuring:
- Discord bot for coordination and notifications
- Data tracker/analytics for player stats and war results
- Streamlit web dashboard for visualization
- Automation scripts for repetitive tasks

## Directory Structure
- `src/bot/` - Discord bot (discord.py)
- `src/data/` - Data models, tracking, and storage (SQLAlchemy)
- `src/dashboard/` - Streamlit web dashboard
- `src/scripts/` - Automation scripts
- `tests/` - pytest test suite
- `data/` - Local data storage (gitignored)

## Commands
```bash
uv sync                              # Install dependencies
uv run python -m src.bot.main        # Run Discord bot
uv run streamlit run src/dashboard/app.py  # Run dashboard
uv run pytest                        # Run tests
uv run ruff check .                  # Lint code
uv run ruff format .                 # Format code
```

## Tech Stack
- Python 3.11+
- discord.py 2.0+ for bot
- Streamlit for dashboard
- SQLAlchemy + SQLite for data storage
- pandas for data manipulation
- pytest for testing
- ruff for linting/formatting

## Code Style
- Use type hints for all function signatures
- Follow PEP 8 with 100 char line limit
- Use async/await for Discord bot handlers
- Prefer context managers for database sessions

## Environment Variables
See `.env.example` for required configuration:
- `DISCORD_BOT_TOKEN` - Discord bot token (required for bot)
- `DISCORD_GUILD_ID` - Target Discord server ID
- `DATABASE_URL` - Database connection string (defaults to SQLite)

## Data Models
Located in `src/data/models.py`:
- `Player` - Player info and stats
- `Alliance` - Alliance info
- `WarResult` - War result tracking

## Adding Features
1. **New bot command**: Add to `src/bot/cogs/` as a Cog
2. **New data model**: Add to `src/data/models.py`
3. **New dashboard page**: Add to `src/dashboard/pages/`
4. **New automation**: Add to `src/scripts/`
