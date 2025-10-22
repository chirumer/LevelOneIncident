# Usage Examples

This document shows real examples of how the system works with actual output.

## Example 1: Counting Mentions

### Query
```
"How many times was TSUNAMI mentioned?"
```

### What Happens

**Step 1: Master Agent Analyzes Query**
```
Keywords extracted: ['TSUNAMI', 'times', 'count']
Query type: COUNT
```

**Step 2: Agent Selection**
```
Scoring agents...
  • TSUNAMI Response Team: 20 points (has topic:TSUNAMI)
  • Backend Infrastructure Team: 10 points (mentions TSUNAMI)
  • Frontend Development Team: 0 points (no TSUNAMI content)

Selected: 2 agents
```

**Step 3: Querying Selected Agents**
```
Querying: TSUNAMI Response Team...
  Result: 15 mentions

Querying: Backend Infrastructure Team...
  Result: 8 mentions
```

**Step 4: Aggregation**
```
Total: 15 + 8 = 23 mentions
Teams with mentions: 2
```

### Output
```
================================================================================
MASTER AGENT: Final Answer
================================================================================

Count Results:
  • 'TSUNAMI' mentioned 23 times across all teams

Teams with mentions: 2

================================================================================
```

---

## Example 2: Finding Meetings

### Query
```
"Show me all meetings related to TSUNAMI"
```

### What Happens

**Step 1: Agent Selection**
```
Selected agents (by relevance):
  1. TSUNAMI Response Team (score: 20)
     Matching capabilities: topic:TSUNAMI, has:meetings
  2. Backend Infrastructure Team (score: 10)
     Matching capabilities: topic:TSUNAMI, has:meetings
```

**Step 2: Each Agent Searches Its Meetings**

TSUNAMI Response Team finds:
```
- 2024-10-02: Emergency meeting to address TSUNAMI-101 vulnerability
- 2024-10-09: Weekly standup - TSUNAMI progress review
- 2024-10-16: TSUNAMI security audit planning
```

Backend Infrastructure Team finds:
```
- 2024-10-04: TSUNAMI infrastructure requirements discussion
```

**Step 3: Aggregation**
```
Total meetings: 4
Sorted by date (newest first)
```

### Output
```
================================================================================
MASTER AGENT: Final Answer
================================================================================

Total Meetings Found: 4

• 2024-10-16 - TSUNAMI Response Team
  TSUNAMI security audit planning

• 2024-10-09 - TSUNAMI Response Team
  Weekly standup - TSUNAMI progress review

• 2024-10-04 - Backend Infrastructure Team
  TSUNAMI infrastructure requirements discussion

• 2024-10-02 - TSUNAMI Response Team
  Emergency meeting to address TSUNAMI-101 vulnerability

================================================================================
```

---

## Example 3: Team-Specific Query

### Query
```
"What issues does the Frontend team have?"
```

### What Happens

**Step 1: Agent Selection**
```
Keyword: "Frontend"
Team name match: Frontend Development Team

Selected agents:
  1. Frontend Development Team (score: 20)
     Matching capabilities: team:Frontend Development Team
```

**Step 2: Query Single Agent**
```
Querying: Frontend Development Team...
  Found 3 issues:
    - FRONT-201: Redesign user dashboard
    - FRONT-202: Mobile responsiveness issues
    - FRONT-203: Implement dark mode
```

### Output
```
================================================================================
MASTER AGENT: Final Answer
================================================================================

Total Issues Found: 3

• FRONT-201 - Frontend Development Team
  Redesign user dashboard (Priority: High, Status: In Progress)

• FRONT-202 - Frontend Development Team
  Mobile responsiveness issues on checkout page (Priority: Critical)

• FRONT-203 - Frontend Development Team
  Implement dark mode (Priority: Low, Status: Backlog)

================================================================================
```

---

## Example 4: Cross-Team Query

### Query
```
"How many meetings did teams have in October?"
```

### What Happens

**Step 1: Agent Selection**
```
General query with "meetings" keyword
All agents have meetings capability

Selected agents: All 3 teams
```

**Step 2: Each Agent Counts Its Meetings**
```
TSUNAMI Response Team: 3 meetings
Frontend Development Team: 3 meetings
Backend Infrastructure Team: 3 meetings
```

**Step 3: Aggregation**
```
Total: 3 + 3 + 3 = 9 meetings
```

### Output
```
================================================================================
MASTER AGENT: Final Answer
================================================================================

Total Meetings Found: 9

• 2024-10-21 - Backend Infrastructure Team
  Weekly infrastructure review

• 2024-10-20 - Frontend Development Team
  Design review session

• 2024-10-18 - Backend Infrastructure Team
  Database migration planning

... (showing all 9 meetings)

================================================================================
```

---

## Example 5: Complex Query

### Query
```
"Show me all high priority TSUNAMI issues"
```

### What Happens

**Step 1: Agent Selection**
```
Keywords: ['TSUNAMI', 'high', 'priority', 'issues']

Selected agents:
  1. TSUNAMI Response Team (score: 30)
     Matching: topic:TSUNAMI, source:jira
  2. Backend Infrastructure Team (score: 10)
     Matching: topic:TSUNAMI
```

**Step 2: Filter by Priority**
```
TSUNAMI Response Team:
  - TSUNAMI-101: Critical vulnerability (Priority: High)
  - TSUNAMI-103: API rate limiting (Priority: High)

Backend Infrastructure Team:
  - INFRA-303: TSUNAMI integration support (Priority: High, Completed)
```

### Output
```
================================================================================
MASTER AGENT: Final Answer
================================================================================

Total Issues Found: 3

• TSUNAMI-101 - TSUNAMI Response Team
  Critical vulnerability in authentication module (Priority: High)

• TSUNAMI-103 - TSUNAMI Response Team
  API rate limiting implementation (Priority: High)

• INFRA-303 - Backend Infrastructure Team
  TSUNAMI integration support (Priority: High, Status: Completed)

================================================================================
```

---

## Example 6: General Information Query

### Query
```
"Tell me about the Backend Infrastructure Team"
```

### What Happens

**Step 1: Agent Selection**
```
Team name match: "Backend Infrastructure Team"

Selected agents:
  1. Backend Infrastructure Team (score: 20)
```

**Step 2: General Search**
```
Agent returns relevant sections:
  - Team information
  - Active issues
  - Recent meetings
  - Key metrics
```

### Output
```
================================================================================
MASTER AGENT: Final Answer
================================================================================

Results by Team:

• Backend Infrastructure Team
  Relevance score: 20

  Team Lead: Robert Zhang
  Members: 5 people
  
  Active Issues: 4
  - Database migration (High priority)
  - Auto-scaling implementation (Medium)
  - Redis cache optimization (Medium)
  
  Recent Activity:
  - 98 commits (last 30 days)
  - 99.97% uptime
  - Average incident response: 15 minutes

================================================================================
```

---

## Interactive Mode Examples

### Session Transcript

```
Your question: How many times was TSUNAMI mentioned?

[Master agent processes query...]

Count Results:
  • 'TSUNAMI' mentioned 23 times across all teams
Teams with mentions: 2

Your question: Which teams are working on TSUNAMI?

[Master agent processes query...]

Teams Working on TSUNAMI:
  1. TSUNAMI Response Team (Primary)
     - 3 active issues
     - 3 meetings in October
  
  2. Backend Infrastructure Team (Support)
     - 1 completed issue (infrastructure support)
     - 1 meeting with TSUNAMI team

Your question: What's the status of TSUNAMI-101?

[Master agent processes query...]

Issue: TSUNAMI-101
Team: TSUNAMI Response Team
Title: Critical vulnerability in authentication module
Status: In Progress
Priority: High
Assigned to: Mike Johnson
Last Updated: 2024-10-15
Comments: 3 security patches applied, testing in progress

Your question: exit

Goodbye!
```

---

## Tips for Better Results

### ✅ Good Queries
```
"How many times was TSUNAMI mentioned?"          # Specific term
"Show meetings about security"                   # Clear topic
"What is the Frontend team working on?"          # Specific team
"List all high priority issues"                  # Clear criteria
```

### ❌ Less Effective Queries
```
"Tell me everything"                             # Too broad
"What's happening?"                              # No context
"Show me stuff"                                  # Vague
```

### 💡 Pro Tips

1. **Use specific terms**: Team names, issue IDs, topics
2. **Be clear about what you want**: count, list, show, find
3. **Include context**: time periods, priorities, statuses
4. **Try variations**: If you don't get what you want, rephrase

---

## Query Patterns

### Counting
```
"How many times was X mentioned?"
"Count occurrences of Y"
"How many meetings about Z?"
```

### Finding
```
"Show me all X"
"Find Y related to Z"
"List all A that match B"
```

### Team-Specific
```
"What is [team name] working on?"
"Show [team name]'s issues"
"Tell me about [team name]"
```

### Time-Based
```
"Meetings in October"
"Issues opened this month"
"Recent activity"
```

### Priority/Status
```
"High priority issues"
"Completed tasks"
"In progress work"
```

---

**Try these examples yourself by running `python main.py`!** 🚀
