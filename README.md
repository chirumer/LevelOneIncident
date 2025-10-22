# Multi-Agent Team Information System

A sophisticated master-slave agent architecture for querying team information collected from various integrations (JIRA, Confluence, Slack, etc.).

## 🎯 Overview

This system implements an intelligent multi-agent architecture where:

- **Slave Agents**: Each represents knowledge about a specific team. They only know about their team's information and nothing else.
- **Master Agent**: Intelligently selects which slave agents to query based on the user's question, aggregates results, and provides comprehensive answers.

## 🏗️ Architecture

```
User Query
    ↓
Master Agent (Intelligent Selection)
    ↓
Selected Slave Agents (Parallel Queries)
    ↓
Aggregated Response
```

### Key Features

1. **Intelligent Agent Selection**: The master agent analyzes queries and selects only relevant slave agents
2. **Self-Identifying Agents**: Each slave agent identifies its capabilities so the master knows who to ask
3. **Capability-Based Routing**: Agents are selected based on topics, team names, and data sources
4. **Aggregated Results**: Multiple agent responses are intelligently combined into coherent answers

## 📁 Project Structure

```
orgai/
├── team_info/                          # Team information files
│   ├── tsunami_response_team.txt       # TSUNAMI team data
│   ├── frontend_team.txt               # Frontend team data
│   └── backend_infrastructure_team.txt # Backend team data
├── slave_agent.py                      # Slave agent implementation
├── master_agent.py                     # Master agent implementation
├── main.py                             # Main interface
├── requirements.txt                    # Dependencies (none required!)
└── README.md                           # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- No external dependencies required!

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd orgai
   ```

### Running the System

Run the main interface:

```bash
python main.py
```

You'll be presented with two options:
1. **Run example queries**: See pre-configured examples demonstrating the system
2. **Interactive mode**: Ask your own questions

## 💡 Example Queries

The system can handle various types of queries:

### Count Queries
```
"How many times was TSUNAMI mentioned?"
"Count occurrences of security issues"
```

### Meeting Queries
```
"Show me all meetings related to TSUNAMI"
"How many meetings did teams have about security?"
"List all meetings in October"
```

### Issue/Ticket Queries
```
"What issues does the Frontend team have?"
"Show me all TSUNAMI related issues"
"List high priority tickets"
```

### General Queries
```
"What is the Backend team working on?"
"Tell me about infrastructure changes"
```

## 🧠 How It Works

### Slave Agent

Each slave agent:
1. **Loads team information** from a text file
2. **Identifies capabilities** (topics, projects, data sources)
3. **Answers queries** about its specific team
4. **Returns structured results** to the master agent

Key methods:
- `get_identity()`: Returns agent capabilities for selection
- `answer_query()`: Processes queries and returns relevant information

### Master Agent

The master agent:
1. **Analyzes user queries** to extract keywords and intent
2. **Scores all agents** based on relevance to the query
3. **Selects appropriate agents** (may query 1, some, or all agents)
4. **Aggregates results** from multiple agents
5. **Formats responses** into human-readable answers

Key methods:
- `_select_agents()`: Intelligent agent selection algorithm
- `process_query()`: Coordinates the query process
- `ask()`: Main interface for asking questions

## 📊 Team Information Format

Team information files should follow this structure:

```
Team Name: [Team Name]
Team Lead: [Lead Name]
Members: [Member1], [Member2], ...

=== JIRA Integration Data ===
[JIRA issues and tickets]

=== Confluence Integration Data ===
[Documentation and meeting notes]

=== Slack Integration Data ===
[Communication metrics and discussions]
```

## 🔧 Customization

### Adding New Teams

1. Create a new `.txt` file in the `team_info/` directory
2. Follow the team information format
3. Restart the system - the new agent will be automatically initialized

### Extending Query Types

To add new query types:

1. **In `slave_agent.py`**: Add new methods to handle specific query patterns
2. **In `master_agent.py`**: Update `_aggregate_results()` to handle new result types

### Custom Capabilities

Modify `_identify_capabilities()` in `slave_agent.py` to extract additional metadata from team files.

## 🎨 Example Output

```
================================================================================
MASTER AGENT: Processing query
================================================================================
Query: How many times was TSUNAMI mentioned?

Agent Selection Process:
  • Analyzed 3 available agents
  • Selected 2 relevant agents

Selected Agents (by relevance):
  1. TSUNAMI Response Team (score: 20)
     Matching capabilities: topic:TSUNAMI
  2. Backend Infrastructure Team (score: 10)
     Matching capabilities: topic:TSUNAMI

Querying: TSUNAMI Response Team...
  ✓ Response received

Querying: Backend Infrastructure Team...
  ✓ Response received

================================================================================
MASTER AGENT: Final Answer
================================================================================

Count Results:
  • 'TSUNAMI' mentioned 55 times across all teams

Teams with mentions: 2

================================================================================
```

## 🤝 Contributing

To extend this system:

1. Add more sophisticated NLP for query understanding
2. Implement caching for frequently asked questions
3. Add support for more data source formats (JSON, CSV, databases)
4. Create a web interface
5. Add machine learning for better agent selection

## 📝 License

This project is open source and available for educational and commercial use.

## 🙋 Support

For questions or issues, please refer to the code comments or create an issue in the repository.

---

**Built with Python 3 and no external dependencies!** 🐍
