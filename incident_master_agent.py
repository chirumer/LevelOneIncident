"""
Incident Response Master Agent
Coordinates teams to respond to incidents, creates task assignments and visualizations
"""

import os
import json
from typing import List, Dict, Any, Tuple
from datetime import datetime
from incident_slave_agent import IncidentSlaveAgent


class IncidentMasterAgent:
    """
    Master agent that coordinates incident response across multiple teams.
    Creates task graphs and prioritized assignments.
    """
    
    def __init__(self, team_info_directory: str):
        """
        Initialize the incident master agent.
        
        Args:
            team_info_directory: Directory containing team information files
        """
        self.team_info_directory = team_info_directory
        self.slave_agents: List[IncidentSlaveAgent] = []
        self._initialize_slave_agents()
    
    def _initialize_slave_agents(self):
        """Create a slave agent for each team info file."""
        if not os.path.exists(self.team_info_directory):
            raise FileNotFoundError(f"Team info directory not found: {self.team_info_directory}")
        
        for filename in os.listdir(self.team_info_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.team_info_directory, filename)
                try:
                    agent = IncidentSlaveAgent(file_path)
                    self.slave_agents.append(agent)
                    print(f"✓ Initialized incident agent for: {agent.team_name}")
                except Exception as e:
                    print(f"✗ Failed to initialize agent for {filename}: {str(e)}")
        
        print(f"\nTotal incident response agents: {len(self.slave_agents)}")
    
    def handle_incident(self, incident_description: str, deadline: datetime) -> Dict[str, Any]:
        """
        Handle an incident by coordinating all teams.
        
        Args:
            incident_description: Description of the incident
            deadline: Deadline to resolve the incident
            
        Returns:
            Dictionary containing task graph and assignments
        """
        print(f"\n{'='*80}")
        print(f"INCIDENT RESPONSE COORDINATION")
        print(f"{'='*80}")
        print(f"Incident: {incident_description}")
        print(f"Deadline: {deadline.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Step 1: Collect task proposals from all teams
        print("Step 1: Collecting task proposals from teams...")
        all_tasks = []
        team_tasks = {}
        
        for agent in self.slave_agents:
            print(f"  • Requesting tasks from {agent.team_name}...")
            tasks = agent.propose_tasks(incident_description, deadline)
            team_tasks[agent.team_name] = tasks
            all_tasks.extend(tasks)
            print(f"    → Proposed {len(tasks)} tasks")
        
        print(f"\nTotal tasks proposed: {len(all_tasks)}\n")
        
        # Step 2: Create task graph
        print("Step 2: Building task dependency graph...")
        task_graph = self._build_task_graph(all_tasks, incident_description)
        print(f"  ✓ Graph created with {len(task_graph['nodes'])} nodes and {len(task_graph['edges'])} edges\n")
        
        # Step 3: Create prioritized assignments
        print("Step 3: Creating prioritized task assignments...")
        assignments = self._create_assignments(all_tasks, team_tasks)
        print(f"  ✓ Assignments created for {len(assignments)} teams\n")
        
        return {
            "incident": incident_description,
            "deadline": deadline.isoformat(),
            "task_graph": task_graph,
            "assignments": assignments,
            "total_tasks": len(all_tasks),
            "teams_involved": len(team_tasks)
        }
    
    def _build_task_graph(self, all_tasks: List[Dict[str, Any]], 
                         incident_description: str) -> Dict[str, Any]:
        """
        Build a graph representation of tasks and their relationships.
        
        Returns:
            Dictionary with nodes and edges for visualization
        """
        nodes = []
        edges = []
        
        # Add incident as central node
        nodes.append({
            "id": "INCIDENT",
            "label": incident_description[:50] + "..." if len(incident_description) > 50 else incident_description,
            "type": "incident",
            "importance": 10
        })
        
        # Add task nodes
        for task in all_tasks:
            nodes.append({
                "id": task["task_id"],
                "label": task["description"][:40] + "..." if len(task["description"]) > 40 else task["description"],
                "type": "task",
                "importance": task["importance"],
                "team": task.get("assigned_to", "Unassigned"),
                "deadline": task["tentative_deadline"].isoformat()
            })
            
            # Create edge from task to incident (task helps resolve incident)
            edges.append({
                "from": task["task_id"],
                "to": "INCIDENT",
                "weight": task["importance"],
                "label": f"Priority: {task['importance']}"
            })
            
            # Create edges for dependencies
            for dep in task.get("dependencies", []):
                edges.append({
                    "from": dep,
                    "to": task["task_id"],
                    "weight": 5,
                    "label": "depends on",
                    "type": "dependency"
                })
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def _create_assignments(self, all_tasks: List[Dict[str, Any]], 
                           team_tasks: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Create prioritized task assignments grouped by team.
        
        Returns:
            List of team assignments with sorted tasks
        """
        assignments = []
        
        for team_name, tasks in team_tasks.items():
            if not tasks:
                continue
            
            # Sort tasks by importance (descending)
            sorted_tasks = sorted(tasks, key=lambda x: x["importance"], reverse=True)
            
            # Convert datetime objects to strings for JSON serialization
            json_safe_tasks = []
            for task in sorted_tasks:
                task_copy = task.copy()
                if isinstance(task_copy.get("tentative_deadline"), datetime):
                    task_copy["tentative_deadline"] = task_copy["tentative_deadline"].isoformat()
                json_safe_tasks.append(task_copy)
            
            # Calculate team metrics
            total_hours = sum(task["estimated_hours"] for task in tasks)
            avg_importance = sum(task["importance"] for task in tasks) / len(tasks)
            
            assignments.append({
                "team_name": team_name,
                "task_count": len(tasks),
                "total_estimated_hours": total_hours,
                "average_importance": round(avg_importance, 2),
                "tasks": json_safe_tasks
            })
        
        # Sort teams by average importance (most critical teams first)
        assignments.sort(key=lambda x: x["average_importance"], reverse=True)
        
        return assignments
    
    def generate_graph_html(self, task_graph: Dict[str, Any]) -> str:
        """
        Generate HTML for graph visualization using vis.js.
        
        Args:
            task_graph: Task graph data
            
        Returns:
            HTML string
        """
        nodes_json = json.dumps(task_graph["nodes"])
        edges_json = json.dumps(task_graph["edges"])
        
        html = f"""
        <div id="graph-container" style="width: 100%; height: 600px; border: 1px solid #ddd; border-radius: 8px;"></div>
        
        <script type="text/javascript">
            var nodes = new vis.DataSet({nodes_json});
            var edges = new vis.DataSet({edges_json});
            
            var container = document.getElementById('graph-container');
            var data = {{
                nodes: nodes,
                edges: edges
            }};
            
            var options = {{
                nodes: {{
                    shape: 'box',
                    margin: 10,
                    widthConstraint: {{
                        maximum: 200
                    }},
                    font: {{
                        size: 14
                    }},
                    color: {{
                        border: '#2B7CE9',
                        background: '#D2E5FF',
                        highlight: {{
                            border: '#2B7CE9',
                            background: '#FFC107'
                        }}
                    }}
                }},
                edges: {{
                    arrows: {{
                        to: {{
                            enabled: true,
                            scaleFactor: 0.5
                        }}
                    }},
                    smooth: {{
                        type: 'cubicBezier',
                        forceDirection: 'vertical'
                    }},
                    color: {{
                        color: '#848484',
                        highlight: '#FFC107'
                    }},
                    font: {{
                        size: 11,
                        align: 'middle'
                    }}
                }},
                layout: {{
                    hierarchical: {{
                        direction: 'UD',
                        sortMethod: 'directed',
                        nodeSpacing: 150,
                        levelSeparation: 200
                    }}
                }},
                physics: {{
                    enabled: false
                }}
            }};
            
            // Customize node appearance based on type
            nodes.forEach(function(node) {{
                if (node.type === 'incident') {{
                    node.color = {{
                        border: '#D32F2F',
                        background: '#FFCDD2'
                    }};
                    node.font = {{size: 16, bold: true}};
                    node.shape = 'ellipse';
                }} else {{
                    var importance = node.importance || 1;
                    var intensity = Math.min(255, 150 + importance * 10);
                    node.color = {{
                        border: '#2B7CE9',
                        background: 'rgb(' + (255 - importance * 10) + ', ' + (255 - importance * 5) + ', 255)'
                    }};
                }}
            }});
            
            // Customize edge appearance based on weight
            edges.forEach(function(edge) {{
                if (edge.type === 'dependency') {{
                    edge.color = {{color: '#4CAF50'}};
                    edge.dashes = true;
                }} else {{
                    var weight = edge.weight || 1;
                    edge.width = Math.max(1, weight / 2);
                }}
            }});
            
            var network = new vis.Network(container, data, options);
        </script>
        """
        
        return html
    
    def generate_assignments_html(self, assignments: List[Dict[str, Any]]) -> str:
        """
        Generate HTML for task assignments table.
        
        Args:
            assignments: Task assignments data
            
        Returns:
            HTML string
        """
        html = """
        <div class="assignments-container">
            <style>
                .assignments-container {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }
                .team-section {
                    margin-bottom: 30px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    overflow: hidden;
                }
                .team-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                }
                .team-name {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .team-stats {
                    display: flex;
                    gap: 30px;
                    font-size: 14px;
                    opacity: 0.9;
                }
                .stat-item {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }
                .tasks-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .tasks-table th {
                    background: #f5f5f5;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #ddd;
                }
                .tasks-table td {
                    padding: 12px;
                    border-bottom: 1px solid #eee;
                }
                .tasks-table tr:hover {
                    background: #f9f9f9;
                }
                .priority-badge {
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
                .priority-high {
                    background: #ffebee;
                    color: #c62828;
                }
                .priority-medium {
                    background: #fff3e0;
                    color: #e65100;
                }
                .priority-low {
                    background: #e8f5e9;
                    color: #2e7d32;
                }
                .task-id {
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    color: #666;
                }
            </style>
        """
        
        for assignment in assignments:
            team_name = assignment["team_name"]
            task_count = assignment["task_count"]
            total_hours = assignment["total_estimated_hours"]
            avg_importance = assignment["average_importance"]
            
            html += f"""
            <div class="team-section">
                <div class="team-header">
                    <div class="team-name">{team_name}</div>
                    <div class="team-stats">
                        <div class="stat-item">
                            <span>📋</span>
                            <span>{task_count} tasks</span>
                        </div>
                        <div class="stat-item">
                            <span>⏱️</span>
                            <span>{total_hours} hours estimated</span>
                        </div>
                        <div class="stat-item">
                            <span>⭐</span>
                            <span>Avg Priority: {avg_importance}</span>
                        </div>
                    </div>
                </div>
                <table class="tasks-table">
                    <thead>
                        <tr>
                            <th>Priority</th>
                            <th>Task ID</th>
                            <th>Description</th>
                            <th>Assigned To</th>
                            <th>Est. Hours</th>
                            <th>Deadline</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for task in assignment["tasks"]:
                importance = task["importance"]
                if importance >= 8:
                    priority_class = "priority-high"
                    priority_label = "HIGH"
                elif importance >= 5:
                    priority_class = "priority-medium"
                    priority_label = "MEDIUM"
                else:
                    priority_class = "priority-low"
                    priority_label = "LOW"
                
                # Handle both datetime objects and ISO strings
                deadline = task["tentative_deadline"]
                if isinstance(deadline, datetime):
                    deadline_str = deadline.strftime("%Y-%m-%d %H:%M")
                else:
                    # Already a string (ISO format), just format it nicely
                    deadline_str = deadline[:16].replace('T', ' ')
                
                html += f"""
                        <tr>
                            <td><span class="priority-badge {priority_class}">{priority_label} ({importance})</span></td>
                            <td class="task-id">{task["task_id"]}</td>
                            <td>{task["description"]}</td>
                            <td>{task["assigned_to"]}</td>
                            <td>{task["estimated_hours"]}h</td>
                            <td>{deadline_str}</td>
                        </tr>
                """
            
            html += """
                    </tbody>
                </table>
            </div>
            """
        
        html += "</div>"
        return html
    
    def __repr__(self):
        return f"IncidentMasterAgent(teams={len(self.slave_agents)})"
