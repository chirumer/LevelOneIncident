"""
Demo script for the incident response system
Shows how the system works without running the web server
"""

import os
from datetime import datetime, timedelta
from incident_master_agent import IncidentMasterAgent


def run_demo():
    """Run a demonstration of the incident response system."""
    
    print("\n" + "="*80)
    print(" "*20 + "INCIDENT RESPONSE SYSTEM DEMO")
    print("="*80 + "\n")
    
    # Initialize master agent
    team_info_dir = os.path.join(os.path.dirname(__file__), 'team_info')
    print("Initializing Incident Response System...")
    print("-" * 80)
    
    master = IncidentMasterAgent(team_info_dir)
    
    print("-" * 80)
    
    # Demo scenarios
    scenarios = [
        {
            "description": "Production database outage - authentication service down",
            "hours": 12
        },
        {
            "description": "Security breach detected in user authentication module",
            "hours": 8
        },
        {
            "description": "Frontend application performance degradation affecting all users",
            "hours": 24
        }
    ]
    
    print("\n" + "="*80)
    print("DEMO SCENARIOS")
    print("="*80)
    print("\nWe'll simulate 3 different incident types to show how teams respond:\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['description']}")
        print(f"   Deadline: {scenario['hours']} hours\n")
    
    choice = input("Select scenario (1-3) or press Enter for scenario 1: ").strip()
    
    if choice == '2':
        scenario = scenarios[1]
    elif choice == '3':
        scenario = scenarios[2]
    else:
        scenario = scenarios[0]
    
    # Calculate deadline
    deadline = datetime.now() + timedelta(hours=scenario["hours"])
    
    # Handle incident
    print("\n" + "="*80)
    result = master.handle_incident(scenario["description"], deadline)
    print("="*80)
    
    # Display summary
    print("\n" + "="*80)
    print("INCIDENT RESPONSE SUMMARY")
    print("="*80)
    
    print(f"\nIncident: {result['incident']}")
    print(f"Deadline: {deadline.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTotal Tasks Proposed: {result['total_tasks']}")
    print(f"Teams Involved: {result['teams_involved']}")
    
    print("\n" + "-"*80)
    print("TASK ASSIGNMENTS BY TEAM (Sorted by Priority)")
    print("-"*80 + "\n")
    
    for assignment in result['assignments']:
        print(f"📋 {assignment['team_name']}")
        print(f"   Tasks: {assignment['task_count']} | "
              f"Est. Hours: {assignment['total_estimated_hours']} | "
              f"Avg Priority: {assignment['average_importance']}")
        print()
        
        for i, task in enumerate(assignment['tasks'], 1):
            importance = task['importance']
            priority_emoji = "🔴" if importance >= 8 else "🟡" if importance >= 5 else "🟢"
            
            print(f"   {i}. {priority_emoji} [{task['task_id']}] Priority: {importance}")
            print(f"      {task['description']}")
            print(f"      Assigned: {task['assigned_to']} | "
                  f"Est: {task['estimated_hours']}h | "
                  f"Due: {task['tentative_deadline'].strftime('%Y-%m-%d %H:%M')}")
            
            if task.get('dependencies'):
                print(f"      Dependencies: {', '.join(task['dependencies'])}")
            print()
    
    print("="*80)
    print("\nGRAPH STRUCTURE")
    print("="*80)
    
    graph = result['task_graph']
    print(f"\nNodes: {len(graph['nodes'])} (1 incident + {len(graph['nodes'])-1} tasks)")
    print(f"Edges: {len(graph['edges'])}")
    
    print("\nTask → Incident Connections (showing importance weights):")
    for edge in graph['edges']:
        if edge['to'] == 'INCIDENT' and edge.get('type') != 'dependency':
            task_node = next((n for n in graph['nodes'] if n['id'] == edge['from']), None)
            if task_node:
                print(f"  • {task_node['label'][:50]}... → Weight: {edge['weight']}")
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\nTo see the full visualization with interactive graph:")
    print("  1. Run: python web_server.py")
    print("  2. Open: http://localhost:8000")
    print("  3. Enter an incident description and deadline")
    print("  4. View the interactive task graph and assignment tables")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    run_demo()
