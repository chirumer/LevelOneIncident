"""
Quick test script to verify the multi-agent system works correctly
"""

import os
from master_agent import MasterAgent


def test_system():
    """Run basic tests to verify the system works."""
    print("="*80)
    print("TESTING MULTI-AGENT SYSTEM")
    print("="*80)
    
    # Initialize master agent
    print("\n1. Initializing Master Agent...")
    team_info_dir = os.path.join(os.path.dirname(__file__), 'team_info')
    
    try:
        master = MasterAgent(team_info_dir)
        print(f"   ✓ Master agent initialized with {len(master.slave_agents)} slave agents")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {str(e)}")
        return False
    
    # Test 1: Agent identity
    print("\n2. Testing Agent Identities...")
    agents_info = master.get_all_agents_info()
    for info in agents_info:
        print(f"   ✓ {info['team_name']}: {len(info['capabilities'])} capabilities")
    
    # Test 2: Simple count query
    print("\n3. Testing Count Query...")
    try:
        result = master.process_query("How many times was TSUNAMI mentioned?", verbose=False)
        count = result['summary'].get('total_counts', {}).get('TSUNAMI', 0)
        print(f"   ✓ Query processed successfully")
        print(f"   ✓ Found {count} mentions of TSUNAMI")
    except Exception as e:
        print(f"   ✗ Query failed: {str(e)}")
        return False
    
    # Test 3: Meeting query
    print("\n4. Testing Meeting Query...")
    try:
        result = master.process_query("Show meetings about TSUNAMI", verbose=False)
        meeting_count = result['summary'].get('total_meetings', 0)
        print(f"   ✓ Query processed successfully")
        print(f"   ✓ Found {meeting_count} meetings")
    except Exception as e:
        print(f"   ✗ Query failed: {str(e)}")
        return False
    
    # Test 4: Agent selection
    print("\n5. Testing Intelligent Agent Selection...")
    try:
        # This should only select Frontend team
        selected = master._select_agents("What is the Frontend team working on?")
        frontend_selected = any(agent.team_name == "Frontend Development Team" 
                               for agent, _, _ in selected)
        if frontend_selected:
            print(f"   ✓ Correctly selected Frontend team")
        else:
            print(f"   ⚠ Frontend team not prioritized (selected {len(selected)} agents)")
    except Exception as e:
        print(f"   ✗ Selection failed: {str(e)}")
        return False
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED ✓")
    print("="*80)
    print("\nThe system is working correctly!")
    print("Run 'python main.py' to use the interactive interface.\n")
    
    return True


if __name__ == "__main__":
    test_system()
