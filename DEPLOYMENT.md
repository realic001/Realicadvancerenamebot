# 🚀 Deployment Guide for Telegram Auto Renamer Bot

This guide covers deploying your Telegram Auto Renamer Bot to various cloud platforms.

## Prerequisites

1. **Telegram Bot Token**: Get from [@BotFather](https://t.me/BotFather)
2. **Python 3.11+**: Required for all deployments
3. **Dependencies**: All listed in pyproject.toml

## Environment Variables

Set these environment variables for your deployment:

```bash
# Required
BOT_TOKEN="your_telegram_bot_token_here"

# Optional Customization
START_PHOTO="https://your-domain.com/welcome-image.jpg"
CUSTOM_WELCOME_MSG="Welcome to your Auto Renamer Bot!"

# Server Configuration
WEB_SERVER="true"          # Set to "false" for local development
PORT="8080"                # Server port (platform dependent)
WEBHOOK_URL="https://your-app-domain.com"  # Your app's public URL

# Admin Configuration (comma-separated user IDs)
ADMIN_IDS="123456789,987654321"
```

## Platform-Specific Deployments

### 1. Railway (Recommended)

Railway offers simple deployment with automatic builds.

**Steps:**
1. Fork this repository to your GitHub
2. Connect Railway to your GitHub account
3. Create new project from your repository
4. Set environment variables in Railway dashboard:
   - `BOT_TOKEN`: Your bot token
   - `WEB_SERVER`: `true`
   - `PORT`: `$PORT` (Railway sets this automatically)
   - `WEBHOOK_URL`: Your Railway app URL

**railway.json** (create in root):
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### 2. Heroku

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-bot-name`
4. Set buildpack: `heroku buildpacks:set heroku/python`
5. Set environment variables:
   ```bash
   heroku config:set BOT_TOKEN="your_token_here"
   heroku config:set WEB_SERVER="true"
   heroku config:set WEBHOOK_URL="https://your-bot-name.herokuapp.com"
   ```
6. Deploy: `git push heroku main`

**Procfile** (create in root):
```
web: python main.py
```

### 3. Render

**Steps:**
1. Connect your GitHub repository to Render
2. Create new "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variables in Render dashboard

**render.yaml** (optional):
```yaml
services:
  - type: web
    name: telegram-auto-renamer-bot
    env: python
    buildCommand: pip install -e .
    startCommand: python main.py
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: WEB_SERVER
        value: "true"
```

### 4. DigitalOcean App Platform

**Steps:**
1. Create new app from GitHub repository
2. Configure build settings:
   - Build command: `pip install -e .`
   - Run command: `python main.py`
3. Set environment variables in app settings
4. Deploy

### 5. VPS (Ubuntu/Debian)

For self-hosted deployments on your own server.

**Installation:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-pip python3.11-venv -y

# Clone repository
git clone https://github.com/yourusername/telegram-auto-renamer-bot.git
cd telegram-auto-renamer-bot

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Create environment file
nano .env
```

**.env file:**
```bash
BOT_TOKEN=your_token_here
WEB_SERVER=true
PORT=8080
WEBHOOK_URL=https://your-domain.com
```

**Systemd Service** (`/etc/systemd/system/autorenamer-bot.service`):
```ini
[Unit]
Description=Telegram Auto Renamer Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram-auto-renamer-bot
Environment=PATH=/home/ubuntu/telegram-auto-renamer-bot/venv/bin
EnvironmentFile=/home/ubuntu/telegram-auto-renamer-bot/.env
ExecStart=/home/ubuntu/telegram-auto-renamer-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable autorenamer-bot
sudo systemctl start autorenamer-bot
sudo systemctl status autorenamer-bot
```

### 6. Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install -e .

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  autorenamer-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - WEB_SERVER=true
      - PORT=8080
      - WEBHOOK_URL=${WEBHOOK_URL}
    ports:
      - "8080:8080"
    restart: unless-stopped
    volumes:
      - ./data:/app/data
```

**Run with Docker:**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

## Webhook Setup

The bot automatically sets up webhooks when `WEB_SERVER=true`. The webhook URL should be:
```
https://your-domain.com/webhook
```

### SSL Certificate

Most platforms provide SSL automatically. For VPS deployments, use Let's Encrypt:

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logs

### Health Check Endpoint

The bot provides a health check at `/health`:
```bash
curl https://your-domain.com/health
# Response: {"status": "ok", "bot": "running"}
```

### Log Management

**View logs on Railway:**
```bash
railway logs
```

**View logs on Heroku:**
```bash
heroku logs --tail
```

**View logs on VPS:**
```bash
sudo journalctl -u autorenamer-bot -f
```

## Database Storage

The bot uses SQLite for data storage. Database files are created automatically in the `data/` directory:

- `data/users.db` - User settings and preferences
- `data/global.db` - Global statistics and leaderboards

For production deployments, ensure persistent storage:

**Railway**: Storage is persistent by default
**Heroku**: Use add-ons for persistent storage
**VPS**: Mount data directory to persistent disk

## Performance Optimization

### Memory Usage
- Default: ~50-100MB per instance
- With file processing: ~200-500MB peak
- Large file handling: Up to 1GB temporary usage

### Scaling
- Single instance handles 1000+ concurrent users
- Use load balancer for multiple instances
- Database is lightweight (SQLite sufficient for most use cases)

## Troubleshooting

### Common Issues

**Bot not responding:**
1. Check BOT_TOKEN is correct
2. Verify webhook URL is accessible
3. Check logs for errors

**File processing fails:**
1. Ensure sufficient disk space
2. Check file size limits
3. Verify dependencies installed

**Database errors:**
1. Check file permissions
2. Ensure data directory exists
3. Verify SQLite installation

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL="DEBUG"
python main.py
```

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to git
2. **Bot Token**: Keep private and rotate if compromised
3. **Admin IDs**: Verify admin user IDs are correct
4. **HTTPS**: Always use SSL/TLS in production
5. **File Limits**: Implement reasonable file size limits
6. **Rate Limiting**: Built-in Telegram rate limiting

## Support

For deployment issues:
1. Check the logs first
2. Verify environment variables
3. Test webhook connectivity
4. Contact support with specific error messages

---

Your Telegram Auto Renamer Bot is now ready for production deployment!