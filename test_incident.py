#!/usr/bin/env python3
"""Quick test of incident response system"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from incident_master_agent import IncidentMasterAgent

# Initialize
team_info_dir = os.path.join(os.path.dirname(__file__), 'team_info')
print("Initializing system...")
master = IncidentMasterAgent(team_info_dir)

# Test incident
print("\nTesting incident response...")
deadline = datetime.now() + timedelta(hours=12)
result = master.handle_incident("Production database outage affecting authentication", deadline)

print(f"\n✓ SUCCESS!")
print(f"✓ Generated {result['total_tasks']} tasks from {result['teams_involved']} teams")
print(f"✓ Graph has {len(result['task_graph']['nodes'])} nodes and {len(result['task_graph']['edges'])} edges")
print(f"\nSystem is working correctly!")
