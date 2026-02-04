# Last War Butler Toolkit - Development Guide

## Project Overview
A Python toolkit for Last War alliance management featuring:
- Discord bot for coordination and notifications
- Duel VS tracking system with tier assignments and analytics
- Kill count tracking and history
- Streamlit web dashboard for visualization and player card exports
- Automation scripts for repetitive tasks

## Directory Structure
- `src/bot/` - Discord bot (discord.py); cogs dir exists but is currently empty
- `src/data/` - Data models, tracking, and storage (SQLAlchemy)
  - `models.py` - All SQLAlchemy models
  - `storage.py` - Database connection, migrations, and session management
  - `tracker.py` - General data collection and tracking
  - `duel_tracker.py` - Duel VS tracking, tier assignment, and reporting
- `src/dashboard/` - Streamlit web dashboard (single `app.py` with embedded pages)
  - `exports/` - Player card image generation (PNG/GIF)
- `src/scripts/` - Automation and example scripts
- `tests/` - pytest test suite
- `data/` - Local data storage (gitignored)
- `.streamlit/config.toml` - Streamlit theme configuration

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
- plotly for charts
- easyocr for OCR functionality
- pillow for image processing (player card exports)
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
- `STREAMLIT_SERVER_PORT` - Dashboard port (defaults to 8501)

## Data Models
Located in `src/data/models.py`:
- `Player` - Player info and stats
- `Alliance` - Alliance info
- `WarResult` - War result tracking
- `DuelCycle` - 4-week duel cycle
- `DuelWeek` - Duel VS week tracking
- `DuelWeeklyStats` - Player stats for a duel week
- `DuelDay` - Single day within a duel week
- `DuelDailyStats` - Player stats for a specific day
- `DuelCycleStats` - Player stats aggregated over a 4-week cycle
- `KillImport` - Batch imports of kill counts
- `KillHistory` - Historical kill count tracking
- `Setting` - Application settings stored in database

## Dashboard Pages
All pages live in `src/dashboard/app.py` via session-state routing:
- Overview, Player Summary, Players, Import Members, Update Kills,
  Duel VS Report, War Results, Analytics, Settings

## Adding Features
1. **New bot command**: Add to `src/bot/cogs/` as a Cog
2. **New data model**: Add to `src/data/models.py`
3. **New dashboard page**: Add page function to `src/dashboard/app.py` and register in nav
4. **New automation**: Add to `src/scripts/`
