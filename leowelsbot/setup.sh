#!/bin/bash

echo "🤖 Setting up Leo System Presentation Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if venv module is available
if ! python3 -c "import venv" &> /dev/null; then
    echo "❌ Python venv module is not available. Please install python3-venv."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📋 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Create assets directory
echo "📁 Creating assets directory..."
mkdir -p assets

# Create sample PDF placeholder if it doesn't exist
if [ ! -f "assets/leo_system_guide.pdf" ]; then
    echo "📄 Creating sample PDF placeholder..."
    python3 -c "from pdf_handler import create_sample_pdf; create_sample_pdf()"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your bot token!"
    echo "   1. Get a bot token from @BotFather on Telegram"
    echo "   2. Replace 'your_bot_token_here' with your actual token"
    echo ""
fi

echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your bot token"
echo "2. Replace assets/leo_system_guide_demo.txt with your actual PDF"
echo "3. Run the bot: source venv/bin/activate && python3 bot.py"
echo ""
echo "🚀 Your Leo System Bot is ready!"