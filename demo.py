"""
Quick demonstration of the multi-agent system capabilities
"""

import os
from master_agent import MasterAgent


def run_demo():
    """Run a quick demo showing the system's capabilities."""
    
    print("\n" + "="*80)
    print(" "*25 + "SYSTEM DEMONSTRATION")
    print("="*80 + "\n")
    
    # Initialize
    team_info_dir = os.path.join(os.path.dirname(__file__), 'team_info')
    master = MasterAgent(team_info_dir)
    
    print("\n" + "="*80)
    
    # Demo queries
    demos = [
        {
            "title": "EXAMPLE 1: Counting Mentions",
            "query": "How many times was TSUNAMI mentioned?",
            "description": "This demonstrates how the master agent selects only relevant agents"
        },
        {
            "title": "EXAMPLE 2: Finding Meetings",
            "query": "Show me all meetings related to TSUNAMI",
            "description": "This shows how the system aggregates meeting information"
        },
        {
            "title": "EXAMPLE 3: Team-Specific Query",
            "query": "What issues does the Frontend team have?",
            "description": "This demonstrates intelligent agent selection for specific teams"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{'#'*80}")
        print(f"{demo['title']}")
        print(f"{'#'*80}")
        print(f"\n{demo['description']}\n")
        
        response = master.ask(demo['query'], verbose=True)
        print(response)
        
        if i < len(demos):
            print("\n" + "-"*80)
            input("Press Enter to continue to next example...")
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE!")
    print("="*80)
    print("\nKey Takeaways:")
    print("  1. Master agent intelligently selects which slave agents to query")
    print("  2. Each slave agent only knows about its specific team")
    print("  3. Results are aggregated and formatted for easy understanding")
    print("  4. The system scales easily - just add more team files!")
    print("\nTry it yourself: python main.py")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_demo()
