# 🚀 START HERE - Incident Response System

## What You Have

A **multi-agent incident response coordination system** that:
1. Takes an incident description and deadline
2. Asks each team to propose tasks
3. Creates a visual task dependency graph
4. Generates prioritized assignment tables
5. Displays everything in a beautiful web interface

## Quick Start (30 seconds)

### Step 1: Install Dependencies (First Time Only)

```bash
cd /Users/chiru/Desktop/orgai
./install.sh
```

Or manually:
```bash
pip3 install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (optional but recommended)
```

### Step 2: Run the System

**Option 1: Web Interface** ⭐ RECOMMENDED

```bash
python3 web_server.py
```

Then open your browser to: **http://localhost:8000**

**Option 2: Command Line Test**

```bash
python3 test_incident.py
```

You'll see detailed logging showing exactly what's happening!

## What Happens

### 1. You Report an Incident
Example: "Production database outage affecting authentication"

### 2. Master Agent Coordinates
Asks all teams: "How can you help?"

### 3. Teams Propose Tasks
- **Backend Team**: Check servers, restart services, scale resources
- **Security Team**: Audit security, review logs, apply patches  
- **Frontend Team**: Show user notifications, implement fallbacks

### 4. System Creates Visualizations

**Task Graph:**
```
         [INCIDENT]
            ↑ ↑ ↑
            │ │ │
   ┌────────┼─┼─┼────────┐
   │        │ │ │        │
[Task 1] [Task 2] [Task 3]
Weight:10 Weight:8 Weight:5
```

**Assignment Table:**
```
Backend Infrastructure Team
├─ 🔴 HIGH (10): Restart affected services
├─ 🔴 HIGH (9): Check server health
└─ 🟡 MEDIUM (8): Scale up resources
```

## Web Interface Features

### 📝 Incident Form
- Enter incident description
- Set hours to deadline
- Click "Coordinate Response"

### 📊 Visualizations

**1. Task Dependency Graph**
- Interactive network visualization
- Nodes = Tasks (colored by priority)
- Edges = Connections (weighted by importance)
- Zoom, pan, and click for details

**2. Assignment Tables**
- Grouped by team
- Sorted by priority
- Color-coded badges (HIGH/MEDIUM/LOW)
- Shows assignee, hours, deadlines

## Example Scenarios

### Scenario 1: Database Outage
```
Description: "Production database outage - authentication down"
Deadline: 12 hours

Result: 11 tasks across 3 teams
- Backend: 5 high-priority infrastructure tasks
- Security: 5 medium-priority security checks
- Frontend: 1 low-priority user notification
```

### Scenario 2: Security Breach
```
Description: "Security breach in authentication module"
Deadline: 8 hours

Result: 9 tasks across 2 teams
- Security: 6 critical security tasks
- Backend: 3 high-priority support tasks
```

### Scenario 3: Performance Issue
```
Description: "Frontend performance degradation affecting users"
Deadline: 24 hours

Result: 8 tasks across 3 teams
- Frontend: 4 high-priority UI tasks
- Backend: 3 medium-priority optimization tasks
- Infrastructure: 1 monitoring task
```

## File Structure

```
orgai/
├── 🌐 Web Interface
│   └── web_server.py              # Start this!
│
├── 🤖 Core System
│   ├── incident_master_agent.py   # Coordinates teams
│   └── incident_slave_agent.py    # Team agents
│
├── 📊 Data
│   └── team_info/                 # Team information
│       ├── tsunami_response_team.txt
│       ├── frontend_team.txt
│       └── backend_infrastructure_team.txt
│
├── 🧪 Testing
│   ├── test_incident.py           # Quick test
│   └── incident_demo.py           # Interactive demo
│
└── 📚 Documentation
    ├── START_HERE.md              # This file
    ├── INCIDENT_README.md         # Full documentation
    └── ...
```

## How to Use the Web Interface

### Step 1: Start Server
```bash
python3 web_server.py
```

You'll see:
```
================================================================================
INCIDENT RESPONSE WEB SERVER
================================================================================

Initializing master agent...
✓ Initialized incident agent for: Frontend Development Team
✓ Initialized incident agent for: TSUNAMI Response Team
✓ Initialized incident agent for: Backend Infrastructure Team

Total incident response agents: 3

================================================================================
Server starting on http://localhost:8000
================================================================================

Open your browser and navigate to:
  → http://localhost:8000
```

### Step 2: Open Browser
Navigate to **http://localhost:8000**

### Step 3: Report Incident
Fill in the form:
- **Incident Description**: "Production database outage"
- **Hours to Deadline**: 12
- Click **"🚀 Coordinate Response"**

### Step 4: View Results
See:
- 📊 Incident overview with statistics
- 🕸️ Interactive task dependency graph
- 📋 Prioritized assignment tables

## Understanding the Visualizations

### Task Graph

**Nodes:**
- 🔴 **Red/Pink** = Incident (center)
- 🔵 **Blue** = Tasks (darker = higher priority)

**Edges:**
- **Solid arrows** = Task helps resolve incident (width = importance)
- **Dashed green arrows** = Task dependencies

**Interactions:**
- Scroll to zoom
- Drag to pan
- Click nodes for details

### Assignment Tables

**Team Header:**
- Team name
- 📋 Task count
- ⏱️ Total estimated hours
- ⭐ Average priority

**Task Rows:**
- 🔴 **HIGH** (8-10): Critical tasks
- 🟡 **MEDIUM** (5-7): Important tasks
- 🟢 **LOW** (1-4): Supporting tasks

## Customization

### Add Your Own Teams

1. Create a new file in `team_info/`:
```bash
touch team_info/your_team.txt
```

2. Add team information:
```
Team Name: Your Team Name
Team Lead: Lead Name
Members: Member1, Member2, Member3

=== JIRA Integration Data ===
[Your team's work]

=== Confluence Integration Data ===
[Your team's documentation]

=== Slack Integration Data ===
[Your team's communication]
```

3. Restart the server - team is automatically included!

### Test Different Incidents

Try these:
- "API rate limiting causing 429 errors"
- "Memory leak in production servers"
- "DDoS attack on authentication endpoints"
- "Data corruption in user profiles table"
- "SSL certificate expiration in 2 hours"

## Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
python3 web_server.py 8080
```

### No tasks generated
- Check that team_info files exist
- Verify team files have content
- Try more specific incident descriptions

### Graph not showing
- Refresh the page
- Check browser console for errors
- Ensure vis.js library loaded (requires internet)

## Next Steps

1. ✅ **Test the system** - Run `python3 web_server.py`
2. ✅ **Try different incidents** - See how teams respond
3. ✅ **Add your teams** - Create real team data files
4. ✅ **Customize tasks** - Edit task generation logic
5. ✅ **Deploy** - Use in real incident response

## Key Files to Read

1. **INCIDENT_README.md** - Complete documentation
2. **incident_master_agent.py** - See how coordination works
3. **incident_slave_agent.py** - See how teams propose tasks
4. **web_server.py** - See how visualizations are generated

## Architecture Summary

```
User Input (Incident + Deadline)
         ↓
   Master Agent
         ↓
    Asks Teams: "How can you help?"
         ↓
   ┌─────┴─────┬─────────┐
   ↓           ↓         ↓
Team A      Team B    Team C
   ↓           ↓         ↓
Tasks       Tasks     Tasks
(weighted by importance)
   ↓           ↓         ↓
   └─────┬─────┴─────────┘
         ↓
   Task Graph Created
   (Tasks → Incident edges)
         ↓
   Assignments Sorted
   (By priority)
         ↓
   Web Visualization
   (Graph + Tables)
```

## Success Metrics

After running, you should see:
- ✅ 3 teams initialized
- ✅ 8-15 tasks proposed (depends on incident)
- ✅ Interactive graph with nodes and edges
- ✅ Sorted assignment tables
- ✅ Beautiful web interface

## Questions?

- Read **INCIDENT_README.md** for full documentation
- Check code comments in Python files
- Run `python3 test_incident.py` to verify system works

---

**Ready to coordinate incident response?**

```bash
python3 web_server.py
```

Then open **http://localhost:8000** and report your first incident! 🚀
