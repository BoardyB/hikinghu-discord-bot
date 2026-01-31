# Reddit to Discord Bot

This bot monitors a subreddit RSS feed and posts new submissions to a Discord channel as threads. It also automatically cleans up inactive threads after a configured period.

## Features

- 🔄 **Auto-posting**: Fetches new posts from r/hikingHungary every 30 minutes
- 🧵 **Thread creation**: Creates a Discord thread for each Reddit post
- 🗑️ **Auto-cleanup**: Removes threads with no replies after 14 days
- 💾 **State management**: Tracks posted links to avoid duplicates

## Setup

### 1. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this later)
5. Under "Privileged Gateway Intents", enable:
   - ✅ MESSAGE CONTENT INTENT
6. Go to OAuth2 → URL Generator
7. Select scopes:
   - `bot`
8. Select bot permissions:
   - `Manage Threads`
   - `Read Message History`
   - `View Channel`
   - `Send Messages in Threads`
9. Copy the generated URL and open it to invite the bot to your server

### 2. Discord Webhook Setup

1. In your Discord server, go to Server Settings → Integrations → Webhooks
2. Click "New Webhook"
3. Choose the channel where you want posts to appear
4. Copy the webhook URL

### 3. GitHub Secrets Setup

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL (for posting)
- `DISCORD_BOT_TOKEN`: Your Discord bot token (for cleanup)
- `DISCORD_CHANNEL_ID`: The ID of the Discord channel to monitor
  - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
  - Right-click the channel and select "Copy Channel ID"

### 4. Deploy

1. Push this code to your GitHub repository
2. The workflows will run automatically:
   - **Reddit to Discord**: Every 30 minutes
   - **Cleanup Inactive Threads**: Daily at 2 AM UTC

You can also trigger them manually from the Actions tab.

## Configuration

### Adjust Cleanup Period

Edit `.github/workflows/cleanup.yml` and change the `INACTIVE_DAYS` value:

```yaml
env:
  INACTIVE_DAYS: "14"  # Change this number
```

### Adjust Posting Frequency

Edit `.github/workflows/bot.yml` and change the cron schedule:

```yaml
on:
  schedule:
    - cron: "*/30 * * * *"  # Change this schedule
```

## File Structure

```
.
├── bot.py                      # Main bot script (posts to Discord)
├── cleanup_threads.py          # Thread cleanup script
├── posted.json                 # State file (auto-generated)
├── .github/
│   └── workflows/
│       ├── bot.yml            # Posting workflow
│       └── cleanup.yml        # Cleanup workflow
└── README.md                  # This file
```

## How It Works

### Posting Flow

1. GitHub Actions runs `bot.py` every 30 minutes
2. Script fetches the RSS feed from r/hikingHungary
3. Compares new posts against `posted.json`
4. Posts new threads via Discord webhook
5. Updates `posted.json` and commits to repository

### Cleanup Flow

1. GitHub Actions runs `cleanup_threads.py` daily
2. Script connects to Discord using the bot token
3. Iterates through all threads in the channel
4. For threads older than 14 days with no replies:
   - Deletes the thread
5. Logs summary of deletions

## Troubleshooting

### Bot can't delete threads

- Ensure the bot has "Manage Threads" permission
- Check that the bot role is above the thread creator's role in the server hierarchy

### Webhook posting fails

- Verify the webhook URL is correct
- Make sure the webhook hasn't been deleted from Discord

### posted.json conflicts

- The workflow commits changes automatically
- If you see merge conflicts, you can delete `posted.json` and let it regenerate

## License

MIT
