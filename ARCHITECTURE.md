# System Architecture

## 🏛️ Overview

This system implements a **Master-Slave Agent Architecture** for intelligent information retrieval across multiple teams.

## 🔄 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER QUERY                          │
│              "How many times was TSUNAMI mentioned?"        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      MASTER AGENT                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  1. Query Analysis                                    │  │
│  │     • Extract keywords (TSUNAMI)                      │  │
│  │     • Identify query type (count)                     │  │
│  │     • Determine intent                                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  2. Agent Selection (Intelligent Routing)             │  │
│  │     • Score all agents for relevance                  │  │
│  │     • Match capabilities to query                     │  │
│  │     • Select top N agents                             │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│SLAVE AGENT 1│  │SLAVE AGENT 2│  │SLAVE AGENT 3│
│             │  │             │  │             │
│  TSUNAMI    │  │  Frontend   │  │  Backend    │
│  Response   │  │  Team       │  │  Infra      │
│  Team       │  │             │  │  Team       │
│             │  │             │  │             │
│ Score: 20   │  │ Score: 0    │  │ Score: 10   │
│ SELECTED ✓  │  │ SKIPPED ✗   │  │ SELECTED ✓  │
└──────┬──────┘  └─────────────┘  └──────┬──────┘
       │                                  │
       │  Query: "count TSUNAMI"          │
       │                                  │
       ▼                                  ▼
┌─────────────┐                    ┌─────────────┐
│  Response:  │                    │  Response:  │
│  Count: 15  │                    │  Count: 8   │
└──────┬──────┘                    └──────┬──────┘
       │                                  │
       └───────────────┬──────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      MASTER AGENT                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  3. Result Aggregation                                │  │
│  │     • Combine responses                               │  │
│  │     • Calculate totals (15 + 8 = 23)                  │  │
│  │     • Format output                                   │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      FINAL ANSWER                           │
│  "TSUNAMI mentioned 23 times across 2 teams"                │
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Components

### 1. Slave Agent (`slave_agent.py`)

**Purpose**: Represents knowledge about a single team

**Key Responsibilities**:
- Load and parse team information from text files
- Identify capabilities (what information it can provide)
- Answer queries about its specific team only
- Return structured results

**Key Methods**:
```python
get_identity()      # Returns capabilities for agent selection
answer_query()      # Processes queries about the team
_count_occurrences() # Counts term mentions
_find_meetings()    # Extracts meeting information
_find_issues()      # Extracts issue/ticket information
```

**Capabilities System**:
Each agent identifies what it knows:
- `team:TSUNAMI Response Team` - Team identity
- `topic:TSUNAMI` - Specific topics/projects
- `source:jira` - Data sources available
- `has:meetings` - Types of information available

### 2. Master Agent (`master_agent.py`)

**Purpose**: Coordinate slave agents to answer user queries

**Key Responsibilities**:
- Analyze user queries to extract intent and keywords
- Score and select relevant slave agents
- Coordinate parallel queries to selected agents
- Aggregate and format results

**Key Methods**:
```python
ask()                    # Main interface for queries
process_query()          # Orchestrates the query process
_select_agents()         # Intelligent agent selection
_score_agent_relevance() # Scores agents for relevance
_aggregate_results()     # Combines multiple responses
```

**Selection Algorithm**:
1. Extract keywords from query (TSUNAMI, team names, etc.)
2. Score each agent based on:
   - Keyword matches in capabilities (+10 points)
   - Team name mentioned in query (+20 points)
   - General query terms (+1 point)
3. Sort agents by score (highest first)
4. Select agents with score > 0

### 3. Main Interface (`main.py`)

**Purpose**: User-facing interface

**Features**:
- Interactive mode for custom queries
- Example queries demonstration
- Agent information display
- User-friendly output formatting

## 🔍 Query Processing Flow

### Step 1: Query Analysis
```python
Query: "How many times was TSUNAMI mentioned?"
↓
Keywords extracted: ['TSUNAMI', 'times', 'count']
Query type: COUNT
```

### Step 2: Agent Selection
```python
For each agent:
    score = 0
    if 'TSUNAMI' in agent.capabilities:
        score += 10
    if agent.team_name in query:
        score += 20
    
Selected agents: [
    (TSUNAMI Response Team, score=20),
    (Backend Infrastructure Team, score=10)
]
```

### Step 3: Parallel Querying
```python
results = []
for agent in selected_agents:
    result = agent.answer_query(query)
    results.append(result)
```

### Step 4: Aggregation
```python
total_count = sum(result['count'] for result in results)
teams_with_mentions = len([r for r in results if r['count'] > 0])

return {
    "total_count": total_count,
    "teams_with_mentions": teams_with_mentions,
    "details": results
}
```

## 📊 Data Flow

```
team_info/
├── tsunami_response_team.txt
│   └── Loaded by → SlaveAgent("TSUNAMI Response Team")
│                    └── Capabilities: [team:TSUNAMI, topic:TSUNAMI, ...]
│
├── frontend_team.txt
│   └── Loaded by → SlaveAgent("Frontend Development Team")
│                    └── Capabilities: [team:Frontend, topic:FRONT, ...]
│
└── backend_infrastructure_team.txt
    └── Loaded by → SlaveAgent("Backend Infrastructure Team")
                     └── Capabilities: [team:Backend, topic:INFRA, ...]

All agents registered with → MasterAgent
                              └── Routes queries to relevant agents
```

## 🎯 Design Principles

### 1. **Separation of Concerns**
- Slave agents only know about their team
- Master agent only handles coordination
- No cross-contamination of knowledge

### 2. **Intelligent Routing**
- Don't query all agents for every question
- Use capabilities to select relevant agents
- Minimize unnecessary computation

### 3. **Scalability**
- Easy to add new teams (just add a file)
- Agents are independent and can be parallelized
- No hardcoded team references

### 4. **Extensibility**
- New query types can be added easily
- Capability system allows for complex routing
- Aggregation logic is modular

## 🔧 Extension Points

### Adding New Query Types

**In `slave_agent.py`**:
```python
def _find_new_type(self, query: str) -> Dict[str, Any]:
    # Custom logic for new query type
    return {"query_type": "new_type", ...}
```

**In `master_agent.py`**:
```python
def _aggregate_results(self, query: str, results: List[Dict]) -> Dict:
    if results[0].get('query_type') == 'new_type':
        # Custom aggregation logic
        pass
```

### Adding New Capabilities

**In `slave_agent.py`**:
```python
def _identify_capabilities(self):
    # Add custom capability detection
    if 'custom_pattern' in self.content:
        self.capabilities.append("has:custom_feature")
```

### Custom Scoring

**In `master_agent.py`**:
```python
def _score_agent_relevance(self, agent, query, keywords):
    score = 0
    # Add custom scoring logic
    if 'special_condition' in query:
        score += 50
    return score, matching
```

## 🚀 Performance Considerations

### Current Implementation
- **Sequential querying**: Agents queried one after another
- **In-memory processing**: All data loaded into memory
- **No caching**: Each query processes from scratch

### Potential Optimizations
1. **Parallel querying**: Use threading/asyncio for concurrent agent queries
2. **Caching**: Cache frequently asked questions
3. **Indexing**: Pre-index team information for faster searches
4. **Lazy loading**: Load team data only when needed

## 🔐 Security Considerations

- All data is local (no external API calls)
- No authentication required (add if needed)
- File system access is restricted to `team_info/` directory
- No code execution from team data files

## 📈 Future Enhancements

1. **Natural Language Processing**: Better query understanding
2. **Machine Learning**: Learn from query patterns
3. **Web Interface**: REST API and web UI
4. **Database Integration**: Support for SQL/NoSQL databases
5. **Real-time Updates**: Watch for file changes
6. **Multi-language Support**: Support for non-English queries

---

**This architecture provides a solid foundation for intelligent, scalable team information retrieval!** 🎉
