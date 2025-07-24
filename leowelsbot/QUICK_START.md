# 🚀 Quick Start Guide - Leo System Bot

## ⚡ Fast Deployment (2 minutes)

### 1. Get Bot Token
```bash
# 1. Open Telegram and message @BotFather
# 2. Send /newbot
# 3. Choose bot name and username
# 4. Copy the token (looks like: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
```

### 2. Configure Bot
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your token
nano .env
# Replace: BOT_TOKEN=your_bot_token_here
# With:    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### 3. Run Bot
```bash
# Option A: Use setup script (recommended)
./setup.sh

# Option B: Manual setup
source venv/bin/activate
python3 bot.py
```

## 📱 Bot Features

### 🟦 Main Menu
- **Start Command**: `/start` - Shows main presentation
- **Interactive Buttons**: Navigate through all sections
- **Direct Contact**: Links to @leowels

### 🟦 PDF Distribution
- **Protected Content**: Cannot be forwarded
- **Automatic Logging**: Tracks who downloads
- **Fallback Handling**: Error messages with contact info

### 🟦 Sales Funnel
1. **Attraction**: Start message hooks users
2. **Information**: Leo System explanation
3. **Options**: Bot service or mentorship
4. **Action**: Direct contact with Leo

## 🔧 Customization

### Change Messages
Edit `config.py` → `Messages` class:
```python
START_MESSAGE = "Your custom welcome message..."
LEO_SYSTEM_INFO = "Your system description..."
```

### Change Username
Edit `.env` file:
```bash
LEO_USERNAME=your_new_username
```

### Add Real PDF
Replace `assets/leo_system_guide_demo.txt` with:
- `assets/leo_system_guide.pdf` (actual PDF file)

## 🐛 Common Issues

### Bot Not Responding
```bash
# Check token is correct
grep BOT_TOKEN .env

# Check bot is running
ps aux | grep python

# Check logs for errors
python3 bot.py
```

### PDF Not Sending
```bash
# Check file exists
ls -la assets/leo_system_guide.pdf

# Check file permissions
chmod 644 assets/leo_system_guide.pdf
```

### Dependencies Issues
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

## 📊 Monitoring

### View Logs
```bash
# Real-time logs
python3 bot.py

# Save logs to file
python3 bot.py > bot.log 2>&1
```

### Check Bot Status
```bash
# Telegram API check
curl -X GET "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

## 🚀 Production Deployment

### Option 1: Screen Session
```bash
screen -S leobot
source venv/bin/activate
python3 bot.py
# Press Ctrl+A, then D to detach
```

### Option 2: Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/leobot.service

# Enable and start
sudo systemctl enable leobot
sudo systemctl start leobot
```

### Option 3: Docker
```bash
# Build image
docker build -t leobot .

# Run container
docker run -d --name leobot --env-file .env leobot
```

## 📈 Success Metrics

Track these KPIs:
- **User Engagement**: Start command usage
- **PDF Downloads**: Conversion rate
- **Contact Rate**: Direct messages to Leo
- **Retention**: Return users

## 🔒 Security Tips

1. **Keep token secret**: Never commit .env to git
2. **Regular updates**: Update dependencies monthly
3. **Monitor logs**: Watch for suspicious activity
4. **Backup data**: Save user analytics

## 📞 Support

Issues? Contact [@leowels](https://t.me/leowels)

---

**Ready to scale your Telegram business? Start now!** 🚀