# 🔑 API Key Setup - Simple Guide

## Where to Put Your Gemini API Key

### Step-by-Step Instructions

#### 1. Get Your API Key

Visit: **https://makersuite.google.com/app/apikey**

- Sign in with your Google account
- Click **"Create API Key"**
- Copy the key (starts with `AIzaSy...`)

#### 2. Create .env File

```bash
cd /Users/chiru/Desktop/orgai
cp .env.example .env
```

#### 3. Edit .env File

```bash
nano .env
```

Or use any text editor:
```bash
open -e .env
```

#### 4. Add Your API Key

Replace `your_api_key_here` with your actual key:

**Before**:
```bash
GEMINI_API_KEY=your_api_key_here
```

**After**:
```bash
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuv
```

#### 5. Save and Exit

- In nano: Press `Ctrl+X`, then `Y`, then `Enter`
- In TextEdit: Press `Cmd+S`

#### 6. Verify It Works

```bash
python3 config.py
```

You should see:
```
================================================================================
CONFIGURATION STATUS
================================================================================
Gemini API Key: ✓ Set
Gemini Model: gemini-pro
Server Port: 8000
Debug Mode: True
================================================================================

✓ Configuration is valid!
```

## 📁 File Location

```
/Users/chiru/Desktop/orgai/
├── .env.example          ← Template (DO NOT edit)
├── .env                  ← Your file (ADD KEY HERE)
└── config.py             ← Reads the .env file
```

## 🔐 Security

### ✅ DO

- Keep `.env` file local
- Add `.env` to `.gitignore` (already done)
- Never commit `.env` to git
- Rotate keys periodically

### ❌ DON'T

- Share `.env` file
- Commit to version control
- Hardcode key in source files
- Email or message the key

## 🎯 Complete .env File Example

```bash
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuv

# Optional Settings (defaults shown)
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048

# Server Configuration
SERVER_PORT=8000
DEBUG_MODE=true
```

## 🧪 Test It

```bash
# Test configuration
python3 config.py

# Test full system
python3 test_incident.py

# Start web server
python3 web_server.py
```

## 🐛 Troubleshooting

### Problem: "GEMINI_API_KEY is not set"

**Check**:
1. Does `.env` file exist?
   ```bash
   ls -la .env
   ```

2. Is the key in the file?
   ```bash
   cat .env | grep GEMINI_API_KEY
   ```

3. No spaces around `=`?
   ```bash
   # Correct
   GEMINI_API_KEY=AIzaSy...
   
   # Wrong
   GEMINI_API_KEY = AIzaSy...
   ```

### Problem: "API Status: 401"

**Solution**: Invalid API key
- Verify key is correct
- Try regenerating at https://makersuite.google.com/app/apikey
- Check for extra spaces or newlines

### Problem: "API Status: 429"

**Solution**: Rate limit exceeded
- Wait a few minutes
- Check your quota
- System will fall back to rule-based generation

## 📊 With vs Without API Key

### Without API Key

```
[Gemini] Skipping enhancement (API not configured)

Tasks: 3 (all rule-based)
```

### With API Key

```
[Gemini] Enhancing tasks...
[Gemini] API Status: 200
✓ Generated 2 additional tasks via Gemini

Tasks: 5 (3 rule-based + 2 AI-enhanced)
```

## 💰 Cost

- **Free Tier**: 60 requests per minute
- **Cost**: ~$0.001 per incident
- **1000 incidents**: ~$1-2

Very affordable!

## 🎉 Quick Reference

| Step | Command |
|------|---------|
| 1. Copy template | `cp .env.example .env` |
| 2. Edit file | `nano .env` |
| 3. Add key | `GEMINI_API_KEY=your_key` |
| 4. Save | `Ctrl+X`, `Y`, `Enter` |
| 5. Verify | `python3 config.py` |
| 6. Test | `python3 test_incident.py` |

## 📚 More Information

- **Setup Guide**: See `SETUP_GUIDE.md`
- **Gemini Integration**: See `GEMINI_INTEGRATION.md`
- **Full Documentation**: See `INCIDENT_README.md`

---

**That's it! Your API key is now configured.** 🎉

The system will automatically use Gemini to enhance task generation! 🤖
