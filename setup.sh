#!/bin/bash
# Quick start script for Delphi Backend

set -e

echo "🚀 Delphi Backend Setup"
echo "======================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your configuration:"
    echo "   - DATABASE_URL"
    echo "   - SECRET_KEY (generate with: openssl rand -hex 32)"
    echo "   - GEMINI_API_KEY (optional, for AI features)"
    echo ""
    read -p "Press enter when you've configured .env..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run database migrations: ./run_migrations.sh"
echo "2. Start the server: cd app && python main.py"
echo "3. Visit API docs: http://localhost:8000/docs"
