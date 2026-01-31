# Quick Setup Checklist

Follow these steps to get your bot running:

## Prerequisites
- [ ] GitHub repository created
- [ ] Discord server where you're an admin

## Discord Setup

### 1. Create Discord Bot
- [ ] Go to https://discord.com/developers/applications
- [ ] Click "New Application"
- [ ] Navigate to "Bot" → "Add Bot"
- [ ] Copy the bot token (save it securely)
- [ ] Enable "MESSAGE CONTENT INTENT" under Privileged Gateway Intents

### 2. Create Discord Webhook
- [ ] In Discord: Server Settings → Integrations → Webhooks
- [ ] Click "New Webhook"
- [ ] Select target channel
- [ ] Copy webhook URL (save it securely)

### 3. Get Channel ID
- [ ] Enable Developer Mode: User Settings → Advanced → Developer Mode
- [ ] Right-click your target channel
- [ ] Click "Copy Channel ID" (save it)

### 4. Invite Bot to Server
- [ ] In Developer Portal: OAuth2 → URL Generator
- [ ] Select scopes: `bot`
- [ ] Select permissions:
  - Manage Threads
  - Read Message History
  - View Channel
  - Send Messages in Threads
- [ ] Open the generated URL
- [ ] Select your server and authorize

## GitHub Setup

### 5. Add Repository Secrets
Go to: Repository Settings → Secrets and variables → Actions → New repository secret

Add these three secrets:
- [ ] `DISCORD_WEBHOOK_URL` = (your webhook URL)
- [ ] `DISCORD_BOT_TOKEN` = (your bot token)
- [ ] `DISCORD_CHANNEL_ID` = (your channel ID)

### 6. Push Code
- [ ] Clone/fork this repository
- [ ] Push to your GitHub account

### 7. Verify Workflows
- [ ] Go to Actions tab in your repository
- [ ] You should see two workflows:
  - "Reddit to Discord" (runs every 30 min)
  - "Cleanup Inactive Threads" (runs daily)
- [ ] Manually trigger "Reddit to Discord" to test

## Testing

### 8. Test Posting
- [ ] Go to Actions → "Reddit to Discord" → "Run workflow"
- [ ] Check your Discord channel for new threads

### 9. Test Cleanup (Optional)
- [ ] Create a test thread manually in the channel
- [ ] Go to Actions → "Cleanup Inactive Threads" → "Run workflow"
- [ ] Note: It won't delete recent threads (must be 14+ days old with no replies)
