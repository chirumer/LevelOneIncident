# Setup Guide - Incident Response System with Gemini AI

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd /Users/chiru/Desktop/orgai
pip install -r requirements.txt
```

This installs:
- `requests` - For Gemini API calls
- `python-dotenv` - For environment variable management

### Step 2: Get Gemini API Key

1. Go to **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key

### Step 3: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

In `.env`, replace `your_api_key_here` with your actual API key:

```bash
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
SERVER_PORT=8000
DEBUG_MODE=true
```

### Step 4: Verify Configuration

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

### Step 5: Test the System

```bash
python3 test_incident.py
```

You should see detailed logging output showing:
- Team initialization
- Task generation
- Gemini API enhancement (if configured)
- Final task assignments

### Step 6: Start Web Server

```bash
python3 web_server.py
```

Open **http://localhost:8000** in your browser.

## 📊 What You'll See

### With Gemini API Enabled

```
================================================================================
GEMINI API INTEGRATION
================================================================================
✓ Gemini API enabled
  Model: gemini-pro
  Temperature: 0.7
================================================================================

[Backend_Infrastructure_Team] PROPOSING TASKS
================================================================================
  Incident: Production database outage affecting authentication...
  Deadline: 2024-10-23 14:52:55
  Team Expertise: backend, infrastructure, database

  [Analysis] Calculating relevance to incident...
    • Expertise 'backend' matches: +10 points
    • Expertise 'infrastructure' matches: +10 points
    • Expertise 'database' matches: +10 points
    • Outage/down + infrastructure/backend: +15 points
  [Analysis] Relevance score: 45

  [Generation] Generating expert tasks based on relevance...
  [Generation] Generated 3 base task(s)

  [Enhancement] Checking for AI enhancement...

────────────────────────────────────────────────────────────────────────────────
[Gemini] Enhancing tasks for Backend Infrastructure Team
────────────────────────────────────────────────────────────────────────────────
  Incident: Production database outage affecting authentication...
  Team Expertise: backend, infrastructure, database
  Base Tasks: 3
  [Gemini] Sending request to API...
  [Gemini] API Status: 200
  [Gemini] Response length: 456 characters
  [Gemini] Parsing response...
  [Gemini] Parsed 2 tasks from response
    • Task 1: Implement database connection pooling to prevent fu... (Priority: 8)
    • Task 2: Set up automated database health monitoring with al... (Priority: 7)
  ✓ Generated 2 additional tasks via Gemini

  [Result] Final task count: 5
    1. [rule-based] Check server health and resource utilization (Priority: 9)
    2. [rule-based] Restart affected services and verify connectivity (Priority: 10)
    3. [rule-based] Scale up resources if needed (Priority: 8)
    4. [gemini] Implement database connection pooling to prevent fu... (Priority: 8)
    5. [gemini] Set up automated database health monitoring with al... (Priority: 7)
================================================================================
```

### Without Gemini API

```
================================================================================
GEMINI API INTEGRATION
================================================================================
✗ Gemini API disabled (no API key)
  Using rule-based task generation
================================================================================

[Backend_Infrastructure_Team] PROPOSING TASKS
================================================================================
  [Enhancement] Checking for AI enhancement...
  [Gemini] Skipping enhancement (API not configured)

  [Result] Final task count: 3
    1. [rule-based] Check server health and resource utilization (Priority: 9)
    2. [rule-based] Restart affected services and verify connectivity (Priority: 10)
    3. [rule-based] Scale up resources if needed (Priority: 8)
================================================================================
```

## 🔍 Understanding the Logging

### Agent Initialization
```
────────────────────────────────────────────────────────────────────────────────
[SlaveAgent] Initializing agent from: team_info/backend_infrastructure_team.txt
────────────────────────────────────────────────────────────────────────────────
  [Loading] Reading team file...
  [Loading] File size: 1847 characters
  [Loading] Extracting team information...
  [Loading] Found team name: Backend Infrastructure Team
  [Loading] Found team lead: Robert Zhang
  [Loading] Found 5 members
  [Expertise] Analyzing team expertise...
  [Expertise] Identified: backend
  [Expertise] Identified: infrastructure
  [Expertise] Identified: database
  ✓ Team: Backend Infrastructure Team
  ✓ Lead: Robert Zhang
  ✓ Members: 5
  ✓ Expertise: backend, infrastructure, database
────────────────────────────────────────────────────────────────────────────────
```

### Task Proposal Process
```
[Backend_Infrastructure_Team] PROPOSING TASKS
  Incident: Production database outage...
  Deadline: 2024-10-23 14:52:55
  Team Expertise: backend, infrastructure, database

  [Analysis] Calculating relevance to incident...
    • Expertise 'backend' matches: +10 points
    • Expertise 'infrastructure' matches: +10 points
    • Outage/down + infrastructure/backend: +15 points
  [Analysis] Relevance score: 35

  [Generation] Generating expert tasks based on relevance...
  [Generation] Generated 3 base task(s)

  [Enhancement] Checking for AI enhancement...
  [Gemini] Enhancing tasks...
  ✓ Generated 2 additional tasks via Gemini

  [Result] Final task count: 5
```

### Gemini API Interaction
```
[Gemini] Enhancing tasks for Backend Infrastructure Team
  Incident: Production database outage...
  Team Expertise: backend, infrastructure, database
  Base Tasks: 3
  [Gemini] Sending request to API...
  [Gemini] API Status: 200
  [Gemini] Response length: 456 characters
  [Gemini] Parsing response...
  [Gemini] Parsed 2 tasks from response
    • Task 1: Implement database connection pooling... (Priority: 8)
    • Task 2: Set up automated monitoring... (Priority: 7)
  ✓ Generated 2 additional tasks via Gemini
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Your Gemini API key |
| `GEMINI_MODEL` | `gemini-pro` | Gemini model to use |
| `GEMINI_TEMPERATURE` | `0.7` | Creativity (0.0-1.0) |
| `GEMINI_MAX_TOKENS` | `2048` | Max response length |
| `SERVER_PORT` | `8000` | Web server port |
| `DEBUG_MODE` | `true` | Enable debug logging |

### Adjusting AI Behavior

**More Creative (Higher Temperature)**:
```bash
GEMINI_TEMPERATURE=0.9
```

**More Deterministic (Lower Temperature)**:
```bash
GEMINI_TEMPERATURE=0.3
```

**Longer Responses**:
```bash
GEMINI_MAX_TOKENS=4096
```

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY is not set"

**Solution**:
1. Make sure `.env` file exists in the project root
2. Check that the API key is correctly set in `.env`
3. Verify no extra spaces around the `=` sign

```bash
# Correct
GEMINI_API_KEY=AIzaSyC...

# Wrong
GEMINI_API_KEY = AIzaSyC...
```

### Issue: "Gemini API error: 400"

**Solution**: Invalid API key or request format
1. Verify your API key is correct
2. Check that you have API access enabled
3. Try regenerating the API key

### Issue: "Gemini API error: 429"

**Solution**: Rate limit exceeded
1. Wait a few minutes before trying again
2. Consider reducing the number of requests
3. Check your API quota at https://makersuite.google.com

### Issue: "Request timeout after 30 seconds"

**Solution**: Network or API slowness
1. Check your internet connection
2. Try again in a few moments
3. System will fall back to rule-based generation

### Issue: No additional tasks from Gemini

**Solution**: This is normal if:
- Base tasks already cover everything
- Gemini determines no additional tasks needed
- The response was empty `[]`

## 📈 Performance Tips

### Faster Response Times

1. **Disable Gemini for testing**:
   ```bash
   # Remove or comment out API key in .env
   # GEMINI_API_KEY=
   ```

2. **Reduce token limit**:
   ```bash
   GEMINI_MAX_TOKENS=1024
   ```

3. **Use caching** (future enhancement):
   - Cache Gemini responses for similar incidents
   - Implement request deduplication

### Better Task Quality

1. **Adjust temperature**:
   - Lower (0.3-0.5): More focused, deterministic
   - Higher (0.7-0.9): More creative, diverse

2. **Provide better team data**:
   - Add more detailed expertise in team files
   - Include past incident responses
   - Document team capabilities

## 🔐 Security Best Practices

### API Key Security

✅ **DO**:
- Store API key in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys periodically

❌ **DON'T**:
- Commit `.env` to version control
- Share API keys in code or documentation
- Use the same key across environments
- Hardcode keys in source files

### Production Deployment

```bash
# Use environment variables
export GEMINI_API_KEY="your-key-here"

# Or use a secrets manager
# - AWS Secrets Manager
# - Google Secret Manager
# - HashiCorp Vault
```

## 📊 Monitoring API Usage

### Check API Calls

The system logs every Gemini API call:
```
[Gemini] Sending request to API...
[Gemini] API Status: 200
```

### Track Costs

1. Visit https://makersuite.google.com
2. Check your API usage dashboard
3. Monitor quota and billing

### Optimize Usage

- Gemini is only called when enabled
- Falls back to rule-based if API fails
- Each incident triggers 1 API call per team
- Typical: 3 teams = 3 API calls per incident

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Get API key
3. ✅ Configure `.env`
4. ✅ Test the system
5. ✅ Start web server
6. 🚀 Report your first incident!

## 📚 Additional Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **API Key Management**: https://makersuite.google.com/app/apikey
- **Rate Limits**: https://ai.google.dev/pricing
- **System Documentation**: See `INCIDENT_README.md`

---

**Need help?** Check the logs - they tell you exactly what's happening! 🔍
