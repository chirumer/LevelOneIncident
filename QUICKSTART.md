# Quick Start Guide

## 🚀 Get Started in 30 Seconds

### 1. Test the System
```bash
python test_system.py
```

This will verify everything is working correctly.

### 2. Run the Interactive System
```bash
python main.py
```

Choose option 2 for interactive mode, then try these queries:

## 📝 Example Queries to Try

### Count Queries
```
How many times was TSUNAMI mentioned?
Count security issues
```

### Meeting Queries
```
Show me all meetings related to TSUNAMI
How many meetings did teams have?
List meetings in October
```

### Issue Queries
```
What issues does the Frontend team have?
Show me all TSUNAMI related issues
Show high priority tickets
```

### Team-Specific Queries
```
What is the Backend team working on?
Tell me about the TSUNAMI Response Team
What is the Frontend team's status?
```

## 🎯 How It Works

1. **You ask a question** → The master agent analyzes it
2. **Master selects relevant agents** → Based on keywords and capabilities
3. **Slave agents respond** → Each with their team's information
4. **Master aggregates** → Combines results into one answer

## 📊 Understanding the Output

When you ask a question, you'll see:

1. **Agent Selection Process**: Which agents were chosen and why
2. **Query Progress**: As each agent is queried
3. **Final Answer**: Aggregated results from all relevant agents

## 🔧 Adding Your Own Team Data

1. Create a new `.txt` file in `team_info/` folder
2. Follow this format:
   ```
   Team Name: Your Team Name
   Team Lead: Lead Name
   Members: Member1, Member2, Member3

   === JIRA Integration Data ===
   [Your JIRA data]

   === Confluence Integration Data ===
   [Your Confluence data]

   === Slack Integration Data ===
   [Your Slack data]
   ```
3. Restart the system - your team will be automatically loaded!

## 💡 Pro Tips

- **Be specific**: "TSUNAMI meetings" is better than "meetings"
- **Use keywords**: The system recognizes team names, issue IDs, and topics
- **Try variations**: If you don't get what you want, rephrase your question

## 🐛 Troubleshooting

**No agents found?**
- Make sure `.txt` files are in the `team_info/` folder

**Agent not responding?**
- Check that your team file follows the correct format

**Wrong results?**
- Try being more specific in your query
- Use exact team names or issue IDs

---

**Ready to explore?** Run `python main.py` and start asking questions! 🎉
