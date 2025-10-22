# Incident Response Coordination System

## 🚨 Overview

This system implements a **multi-agent incident response coordination platform** where teams autonomously propose tasks to resolve incidents, and a master agent creates prioritized assignments with visual task graphs.

## 🏗️ New Architecture

### How It Works

1. **User Reports Incident** → Describes the issue and sets a deadline
2. **Master Agent Coordinates** → Asks each team to propose tasks
3. **Teams Propose Tasks** → Each team suggests how they can help with importance weights
4. **Graph Creation** → Tasks form edges to the incident (weighted by importance)
5. **Assignment Prioritization** → Master creates sorted task assignments
6. **Visualization** → Interactive graph and tables displayed on web interface

### Architecture Diagram

```
User Reports Incident
        ↓
   Master Agent
        ↓
   ┌────┴────┬────────┬─────────┐
   ↓         ↓        ↓         ↓
Team A    Team B   Team C   Team D
   ↓         ↓        ↓         ↓
Tasks     Tasks    Tasks    Tasks
(weighted by importance)
   ↓         ↓        ↓         ↓
   └────┬────┴────────┴─────────┘
        ↓
  Task Graph (Visualization)
        +
  Assignment Table (Sorted by Priority)
        ↓
    Web Display
```

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

```bash
# Start the web server
python web_server.py

# Open browser to http://localhost:8000
# Enter incident details and see visualizations
```

### Option 2: Command Line Demo

```bash
# Run the demo script
python incident_demo.py

# Choose a scenario and see the coordination process
```

## 📊 Features

### 1. **Task Dependency Graph**
- Visual representation of all tasks
- Edges show task → incident relationships
- Edge weights represent task importance
- Dependency edges show task prerequisites
- Interactive zoom and pan

### 2. **Prioritized Assignment Tables**
- Tasks grouped by team
- Sorted by importance within each team
- Color-coded priority badges (HIGH/MEDIUM/LOW)
- Shows assignee, estimated hours, and deadlines
- Team statistics (total tasks, hours, avg priority)

### 3. **Intelligent Task Proposal**
- Teams analyze incident based on their expertise
- Propose relevant tasks automatically
- Assign importance weights (1-10 scale)
- Set tentative deadlines
- Identify task dependencies

## 🎯 Example Scenarios

### Scenario 1: Database Outage
```
Incident: "Production database outage - authentication service down"
Deadline: 12 hours

Response:
  • Backend Infrastructure Team (High Priority)
    - Check server health (Priority: 9)
    - Restart affected services (Priority: 10)
    - Scale up resources (Priority: 8)
  
  • TSUNAMI Response Team (Medium Priority)
    - Monitor security implications (Priority: 5)
  
  • Frontend Team (Low Priority)
    - Display user notification (Priority: 4)
```

### Scenario 2: Security Breach
```
Incident: "Security breach detected in user authentication module"
Deadline: 8 hours

Response:
  • TSUNAMI Response Team (Critical Priority)
    - Security audit (Priority: 10)
    - Review access logs (Priority: 9)
    - Implement patches (Priority: 11)
  
  • Backend Infrastructure Team (High Priority)
    - Infrastructure support (Priority: 8)
```

## 🖥️ Web Interface

### Main Page Features

1. **Incident Form**
   - Description text area
   - Hours to deadline input
   - Submit button to coordinate response

2. **Incident Overview**
   - Incident details
   - Deadline countdown
   - Total tasks and teams involved

3. **Task Dependency Graph**
   - Interactive vis.js network graph
   - Hierarchical layout (incident at top)
   - Color-coded by importance
   - Hover for details
   - Zoom and pan controls

4. **Task Assignment Tables**
   - Grouped by team
   - Sorted by priority
   - Color-coded badges
   - Team statistics
   - Responsive design

## 📁 File Structure

```
orgai/
├── incident_slave_agent.py       # Team agents that propose tasks
├── incident_master_agent.py      # Coordinates incident response
├── web_server.py                 # Web server with visualizations
├── incident_demo.py              # Command-line demo
├── INCIDENT_README.md            # This file
└── team_info/                    # Team data files
    ├── tsunami_response_team.txt
    ├── frontend_team.txt
    └── backend_infrastructure_team.txt
```

## 🔧 How Teams Propose Tasks

Each team agent:

1. **Analyzes Incident** → Calculates relevance to their expertise
2. **Generates Tasks** → Creates task list based on incident type
3. **Assigns Importance** → Weights tasks (1-10 scale)
4. **Sets Deadlines** → Proposes tentative completion times
5. **Identifies Dependencies** → Links tasks that depend on others

### Task Importance Scale

- **10+**: Critical - Must be done immediately
- **8-9**: High - Very important for resolution
- **5-7**: Medium - Helpful but not critical
- **1-4**: Low - Supporting tasks

## 📈 Graph Visualization

### Node Types

- **Incident Node** (Red/Pink)
  - Central node representing the incident
  - All tasks connect to this

- **Task Nodes** (Blue gradient)
  - Color intensity based on importance
  - Darker = higher priority

### Edge Types

- **Task → Incident** (Solid arrows)
  - Width based on importance weight
  - Label shows priority level

- **Task → Task** (Dashed green arrows)
  - Shows dependencies
  - Label: "depends on"

## 🎨 Assignment Table Features

### Team Header
- Gradient background
- Team name
- Statistics: task count, total hours, avg priority

### Task Rows
- Priority badge (color-coded)
- Task ID (monospace font)
- Description
- Assigned person
- Estimated hours
- Deadline timestamp

### Priority Colors
- 🔴 **HIGH** (8+): Red badge
- 🟡 **MEDIUM** (5-7): Orange badge
- 🟢 **LOW** (1-4): Green badge

## 💻 API Endpoints

### GET `/`
Returns the main HTML page with visualizations

### POST `/api/create_incident`
Create a new incident and get task assignments

**Request Body:**
```json
{
  "description": "Incident description",
  "hours_to_deadline": 24
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "incident": "...",
    "deadline": "2024-10-23T14:00:00",
    "task_graph": {...},
    "assignments": [...],
    "total_tasks": 15,
    "teams_involved": 3
  }
}
```

### GET `/api/teams`
Get information about all available teams

### GET `/api/incident`
Get current incident data

## 🔍 Example Output

### Console Output
```
================================================================================
INCIDENT RESPONSE COORDINATION
================================================================================
Incident: Production database outage - authentication service down
Deadline: 2024-10-23 02:00:00
================================================================================

Step 1: Collecting task proposals from teams...
  • Requesting tasks from TSUNAMI Response Team...
    → Proposed 1 tasks
  • Requesting tasks from Frontend Development Team...
    → Proposed 2 tasks
  • Requesting tasks from Backend Infrastructure Team...
    → Proposed 3 tasks

Total tasks proposed: 6

Step 2: Building task dependency graph...
  ✓ Graph created with 7 nodes and 9 edges

Step 3: Creating prioritized task assignments...
  ✓ Assignments created for 3 teams
```

### Web Display
- Beautiful gradient header
- Interactive graph with zoom/pan
- Styled assignment tables
- Responsive design
- Real-time updates

## 🚀 Running the System

### Start Web Server
```bash
python web_server.py

# Or specify custom port
python web_server.py 8080
```

### Run Demo
```bash
python incident_demo.py
```

### Test Scenarios
1. Database outage
2. Security breach
3. Performance degradation

## 🎯 Use Cases

- **Production Incidents**: Coordinate team response to outages
- **Security Events**: Organize security incident response
- **Performance Issues**: Coordinate optimization efforts
- **Deployment Problems**: Manage rollback and fixes
- **System Failures**: Orchestrate recovery tasks

## 🔐 Customization

### Add New Team
1. Create team file in `team_info/`
2. Restart server
3. Team automatically included in coordination

### Modify Task Generation
Edit methods in `incident_slave_agent.py`:
- `_generate_security_tasks()`
- `_generate_infrastructure_tasks()`
- `_generate_frontend_tasks()`
- `_generate_database_tasks()`

### Customize Visualization
Edit HTML generation in `incident_master_agent.py`:
- `generate_graph_html()` - Graph appearance
- `generate_assignments_html()` - Table styling

## 📊 Statistics

The system provides:
- Total tasks proposed
- Teams involved
- Total estimated hours
- Average priority per team
- Task distribution across teams

## 🎉 Key Benefits

1. **Automated Coordination** - No manual task assignment needed
2. **Visual Clarity** - See all tasks and dependencies at once
3. **Priority-Based** - Most important tasks highlighted
4. **Team Autonomy** - Teams decide how they can help
5. **Real-time Updates** - Instant visualization of response plan

---

**Ready to coordinate incident response?** Run `python web_server.py` and open http://localhost:8000! 🚀
