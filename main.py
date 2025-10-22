"""
Main interface for the Multi-Agent Team Information System
Demonstrates how to use the master-slave agent architecture
"""

import os
from master_agent import MasterAgent


def print_header():
    """Print a nice header for the application."""
    print("\n" + "="*80)
    print(" "*20 + "MULTI-AGENT TEAM INFORMATION SYSTEM")
    print("="*80)
    print("\nThis system uses a master-slave agent architecture:")
    print("  • Each SLAVE AGENT knows about one specific team")
    print("  • The MASTER AGENT intelligently selects which agents to query")
    print("="*80 + "\n")


def print_agent_info(master: MasterAgent):
    """Print information about all available agents."""
    print("Available Team Agents:")
    print("-" * 80)
    
    agents_info = master.get_all_agents_info()
    for i, info in enumerate(agents_info, 1):
        print(f"\n{i}. Team: {info['team_name']}")
        print(f"   Lead: {info['team_lead']}")
        print(f"   Members: {info['member_count']}")
        print(f"   Capabilities: {len(info['capabilities'])}")
        print(f"   Key topics: {', '.join([c.split(':')[1] for c in info['capabilities'] if c.startswith('topic:')])}")
    
    print("\n" + "-" * 80)


def run_example_queries(master: MasterAgent):
    """Run example queries to demonstrate the system."""
    
    example_queries = [
        "How many times was TSUNAMI mentioned?",
        "Show me all meetings related to TSUNAMI",
        "What issues does the Frontend team have?",
        "How many meetings did teams have about TSUNAMI?",
        "Show me all TSUNAMI related issues"
    ]
    
    print("\n" + "="*80)
    print("RUNNING EXAMPLE QUERIES")
    print("="*80)
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n\n{'#'*80}")
        print(f"EXAMPLE {i}/{len(example_queries)}")
        print(f"{'#'*80}")
        
        response = master.ask(query, verbose=True)
        print(response)
        
        input("\nPress Enter to continue to next example...")


def interactive_mode(master: MasterAgent):
    """Run in interactive mode where user can ask questions."""
    print("\n" + "="*80)
    print("INTERACTIVE MODE")
    print("="*80)
    print("\nYou can now ask questions about the teams.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            query = input("Your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            response = master.ask(query, verbose=True)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


def main():
    """Main function to run the application."""
    print_header()
    
    # Initialize the master agent
    team_info_dir = os.path.join(os.path.dirname(__file__), 'team_info')
    
    print("Initializing Master Agent...")
    print("-" * 80)
    
    try:
        master = MasterAgent(team_info_dir)
    except Exception as e:
        print(f"\nError initializing master agent: {str(e)}")
        return
    
    print("-" * 80)
    
    # Show available agents
    print_agent_info(master)
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("  1. Run example queries (demonstrates the system)")
    print("  2. Interactive mode (ask your own questions)")
    print("  3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            run_example_queries(master)
            break
        elif choice == '2':
            interactive_mode(master)
            break
        elif choice == '3':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
