"""
Configuration management for the incident response system
Loads environment variables and provides configuration access
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loaded configuration from {env_path}")
else:
    print(f"⚠ No .env file found at {env_path}")
    print(f"  Create one by copying .env.example and adding your API key")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
GEMINI_MAX_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', '2048'))

# Server Configuration
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
DEBUG_MODE = os.getenv('DEBUG_MODE', 'true').lower() == 'true'

# Validation
def validate_config():
    """Validate that required configuration is present."""
    issues = []
    
    if not GEMINI_API_KEY:
        issues.append("GEMINI_API_KEY is not set")
    
    if issues:
        print("\n" + "="*80)
        print("⚠ CONFIGURATION ISSUES")
        print("="*80)
        for issue in issues:
            print(f"  • {issue}")
        print("\nTo fix:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Gemini API key to .env")
        print("  3. Get API key from: https://makersuite.google.com/app/apikey")
        print("="*80 + "\n")
        return False
    
    return True

def is_gemini_enabled():
    """Check if Gemini API is configured and available."""
    return bool(GEMINI_API_KEY)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("CONFIGURATION STATUS")
    print("="*80)
    print(f"Gemini API Key: {'✓ Set' if GEMINI_API_KEY else '✗ Not set'}")
    print(f"Gemini Model: {GEMINI_MODEL}")
    print(f"Server Port: {SERVER_PORT}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print("="*80 + "\n")
    
    if validate_config():
        print("✓ Configuration is valid!")
    else:
        print("✗ Configuration has issues (see above)")
