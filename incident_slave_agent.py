"""
Incident Response Slave Agent
Each team agent proposes tasks to help resolve an incident
"""

import re
from typing import Dict, List, Any
from datetime import datetime, timedelta
from gemini_integration import get_gemini_enhancer


class IncidentSlaveAgent:
    """
    A slave agent that represents a team and can propose tasks to resolve incidents.
    """
    
    def __init__(self, team_file_path: str):
        """
        Initialize the incident response agent with team information.
        
        Args:
            team_file_path: Path to the text file containing team information
        """
        print(f"\n{'─'*80}")
        print(f"[SlaveAgent] Initializing agent from: {team_file_path}")
        print(f"{'─'*80}")
        
        self.team_file_path = team_file_path
        self.team_name = ""
        self.team_lead = ""
        self.members = []
        self.content = ""
        self.expertise = []
        
        self._load_team_info()
        self._identify_expertise()
        
        print(f"  ✓ Team: {self.team_name}")
        print(f"  ✓ Lead: {self.team_lead}")
        print(f"  ✓ Members: {len(self.members)}")
        print(f"  ✓ Expertise: {', '.join(self.expertise)}")
        print(f"{'─'*80}")
    
    def _load_team_info(self):
        """Load and parse team information from the file."""
        print(f"  [Loading] Reading team file...")
        try:
            with open(self.team_file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            print(f"  [Loading] File size: {len(self.content)} characters")
            
            # Extract team name
            print(f"  [Loading] Extracting team information...")
            team_name_match = re.search(r'Team Name:\s*(.+)', self.content)
            if team_name_match:
                self.team_name = team_name_match.group(1).strip()
                print(f"  [Loading] Found team name: {self.team_name}")
            
            # Extract team lead
            team_lead_match = re.search(r'Team Lead:\s*(.+)', self.content)
            if team_lead_match:
                self.team_lead = team_lead_match.group(1).strip()
                print(f"  [Loading] Found team lead: {self.team_lead}")
            
            # Extract members
            members_match = re.search(r'Members:\s*(.+)', self.content)
            if members_match:
                members_str = members_match.group(1).strip()
                self.members = [m.strip() for m in members_str.split(',')]
                print(f"  [Loading] Found {len(self.members)} members")
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Team info file not found: {self.team_file_path}")
        except Exception as e:
            raise Exception(f"Error loading team info: {str(e)}")
    
    def _identify_expertise(self):
        """Identify team's areas of expertise based on content."""
        print(f"  [Expertise] Analyzing team expertise...")
        self.expertise = []
        content_lower = self.content.lower()
        
        # Identify expertise areas
        expertise_keywords = {
            'security': ['security', 'vulnerability', 'authentication', 'encryption'],
            'frontend': ['frontend', 'ui', 'ux', 'dashboard', 'mobile', 'responsive'],
            'backend': ['backend', 'api', 'database', 'server', 'infrastructure'],
            'infrastructure': ['infrastructure', 'deployment', 'scaling', 'monitoring', 'uptime'],
            'database': ['database', 'migration', 'sql', 'cache', 'redis'],
            'performance': ['performance', 'optimization', 'scaling', 'rate limiting'],
            'monitoring': ['monitoring', 'alerts', 'logging', 'metrics']
        }
        
        for area, keywords in expertise_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                self.expertise.append(area)
                print(f"  [Expertise] Identified: {area}")
    
    def get_team_info(self) -> Dict[str, Any]:
        """Return team information."""
        return {
            "team_name": self.team_name,
            "team_lead": self.team_lead,
            "member_count": len(self.members),
            "expertise": self.expertise
        }
    
    def propose_tasks(self, incident_description: str, deadline: datetime) -> List[Dict[str, Any]]:
        """
        Propose tasks that this team can do to help resolve the incident.
        
        Args:
            incident_description: Description of the incident
            deadline: Deadline to resolve the incident
            
        Returns:
            List of proposed tasks with importance weights
        """
        print(f"\n{'='*80}")
        print(f"[{self.team_name}] PROPOSING TASKS")
        print(f"{'='*80}")
        print(f"  Incident: {incident_description[:70]}...")
        print(f"  Deadline: {deadline.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Team Expertise: {', '.join(self.expertise)}")
        
        tasks = []
        incident_lower = incident_description.lower()
        
        # Analyze incident relevance to team's expertise
        print(f"\n  [Analysis] Calculating relevance to incident...")
        relevance_score = self._calculate_relevance(incident_description)
        print(f"  [Analysis] Relevance score: {relevance_score}")
        
        if relevance_score == 0:
            # Team has no relevant expertise, propose minimal support
            print(f"  [Decision] Low relevance - proposing minimal support task")
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_SUPPORT_01",
                "description": f"Monitor {self.team_name} systems for any related issues",
                "importance": 1,  # Low importance
                "estimated_hours": 2,
                "tentative_deadline": deadline - timedelta(hours=4),
                "assigned_to": self.team_lead,
                "dependencies": []
            })
            print(f"  [Result] Proposed {len(tasks)} task(s)")
            print(f"{'='*80}\n")
            return tasks
        
        # Generate tasks based on team expertise and incident type
        print(f"  [Generation] Generating expert tasks based on relevance...")
        tasks = self._generate_expert_tasks(incident_description, deadline, relevance_score)
        print(f"  [Generation] Generated {len(tasks)} base task(s)")
        
        # Enhance with Gemini AI if available
        print(f"  [Enhancement] Checking for AI enhancement...")
        gemini = get_gemini_enhancer()
        if gemini.enabled:
            tasks = gemini.enhance_task_proposals(
                self.team_name, 
                self.expertise, 
                incident_description, 
                tasks
            )
        
        # Set deadlines for any tasks that don't have them
        for i, task in enumerate(tasks):
            if task.get('tentative_deadline') is None:
                hours_before = max(2, (len(tasks) - i) * 2)
                task['tentative_deadline'] = deadline - timedelta(hours=hours_before)
            if task.get('assigned_to') == 'TBD':
                task['assigned_to'] = self.team_lead if not self.members else self.members[i % len(self.members)]
        
        print(f"\n  [Result] Final task count: {len(tasks)}")
        for i, task in enumerate(tasks, 1):
            source = task.get('source', 'rule-based')
            print(f"    {i}. [{source}] {task['description'][:60]}... (Priority: {task['importance']})")
        print(f"{'='*80}\n")
        
        return tasks
    
    def _calculate_relevance(self, incident_description: str) -> int:
        """Calculate how relevant this incident is to the team's expertise."""
        incident_lower = incident_description.lower()
        score = 0
        
        # Check if team name is mentioned
        if self.team_name.lower() in incident_lower:
            score += 20
            print(f"    • Team name mentioned: +20 points")
        
        # Check expertise match
        for expertise in self.expertise:
            if expertise in incident_lower:
                score += 10
                print(f"    • Expertise '{expertise}' matches: +10 points")
        
        # Check for specific keywords in team content
        if 'outage' in incident_lower or 'down' in incident_lower:
            if 'infrastructure' in self.expertise or 'backend' in self.expertise:
                score += 15
                print(f"    • Outage/down + infrastructure/backend: +15 points")
        
        if 'security' in incident_lower or 'breach' in incident_lower:
            if 'security' in self.expertise:
                score += 20
                print(f"    • Security incident + security expertise: +20 points")
        
        if 'performance' in incident_lower or 'slow' in incident_lower:
            if 'performance' in self.expertise or 'database' in self.expertise:
                score += 15
                print(f"    • Performance issue + relevant expertise: +15 points")
        
        return score
    
    def _generate_expert_tasks(self, incident_description: str, deadline: datetime, 
                               relevance_score: int) -> List[Dict[str, Any]]:
        """Generate tasks based on team's expertise."""
        tasks = []
        incident_lower = incident_description.lower()
        
        # Determine task importance based on relevance
        base_importance = min(10, max(1, relevance_score // 5))
        
        # Generate tasks based on team type
        if 'security' in self.expertise:
            tasks.extend(self._generate_security_tasks(incident_description, deadline, base_importance))
        
        if 'infrastructure' in self.expertise or 'backend' in self.expertise:
            tasks.extend(self._generate_infrastructure_tasks(incident_description, deadline, base_importance))
        
        if 'frontend' in self.expertise:
            tasks.extend(self._generate_frontend_tasks(incident_description, deadline, base_importance))
        
        if 'database' in self.expertise:
            tasks.extend(self._generate_database_tasks(incident_description, deadline, base_importance))
        
        # If no specific tasks generated, create general support tasks
        if not tasks:
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_INVESTIGATE_01",
                "description": f"Investigate incident impact on {self.team_name} systems",
                "importance": base_importance,
                "estimated_hours": 3,
                "tentative_deadline": deadline - timedelta(hours=6),
                "assigned_to": self.team_lead,
                "dependencies": []
            })
        
        return tasks
    
    def _generate_security_tasks(self, incident: str, deadline: datetime, 
                                 base_importance: int) -> List[Dict[str, Any]]:
        """Generate security-related tasks."""
        tasks = []
        incident_lower = incident.lower()
        
        if 'security' in incident_lower or 'breach' in incident_lower or 'vulnerability' in incident_lower:
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_SEC_01",
                "description": "Conduct immediate security audit of affected systems",
                "importance": base_importance + 3,
                "estimated_hours": 4,
                "tentative_deadline": deadline - timedelta(hours=8),
                "assigned_to": self.members[0] if self.members else self.team_lead,
                "dependencies": []
            })
            
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_SEC_02",
                "description": "Review access logs for suspicious activity",
                "importance": base_importance + 2,
                "estimated_hours": 3,
                "tentative_deadline": deadline - timedelta(hours=6),
                "assigned_to": self.members[1] if len(self.members) > 1 else self.team_lead,
                "dependencies": [f"{self.team_name.replace(' ', '_')}_SEC_01"]
            })
            
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_SEC_03",
                "description": "Implement security patches and hotfixes",
                "importance": base_importance + 4,
                "estimated_hours": 6,
                "tentative_deadline": deadline - timedelta(hours=2),
                "assigned_to": self.team_lead,
                "dependencies": [f"{self.team_name.replace(' ', '_')}_SEC_01"]
            })
        
        return tasks
    
    def _generate_infrastructure_tasks(self, incident: str, deadline: datetime,
                                       base_importance: int) -> List[Dict[str, Any]]:
        """Generate infrastructure-related tasks."""
        tasks = []
        incident_lower = incident.lower()
        
        if 'outage' in incident_lower or 'down' in incident_lower or 'unavailable' in incident_lower:
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_INFRA_01",
                "description": "Check server health and resource utilization",
                "importance": base_importance + 4,
                "estimated_hours": 2,
                "tentative_deadline": deadline - timedelta(hours=10),
                "assigned_to": self.members[0] if self.members else self.team_lead,
                "dependencies": []
            })
            
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_INFRA_02",
                "description": "Restart affected services and verify connectivity",
                "importance": base_importance + 5,
                "estimated_hours": 3,
                "tentative_deadline": deadline - timedelta(hours=6),
                "assigned_to": self.team_lead,
                "dependencies": [f"{self.team_name.replace(' ', '_')}_INFRA_01"]
            })
            
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_INFRA_03",
                "description": "Scale up resources if needed",
                "importance": base_importance + 3,
                "estimated_hours": 4,
                "tentative_deadline": deadline - timedelta(hours=4),
                "assigned_to": self.members[1] if len(self.members) > 1 else self.team_lead,
                "dependencies": [f"{self.team_name.replace(' ', '_')}_INFRA_01"]
            })
        
        return tasks
    
    def _generate_frontend_tasks(self, incident: str, deadline: datetime,
                                 base_importance: int) -> List[Dict[str, Any]]:
        """Generate frontend-related tasks."""
        tasks = []
        incident_lower = incident.lower()
        
        if 'ui' in incident_lower or 'frontend' in incident_lower or 'user' in incident_lower:
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_FRONT_01",
                "description": "Display user-facing incident notification",
                "importance": base_importance + 2,
                "estimated_hours": 2,
                "tentative_deadline": deadline - timedelta(hours=8),
                "assigned_to": self.members[0] if self.members else self.team_lead,
                "dependencies": []
            })
            
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_FRONT_02",
                "description": "Implement graceful degradation for affected features",
                "importance": base_importance + 3,
                "estimated_hours": 5,
                "tentative_deadline": deadline - timedelta(hours=4),
                "assigned_to": self.team_lead,
                "dependencies": []
            })
        
        return tasks
    
    def _generate_database_tasks(self, incident: str, deadline: datetime,
                                 base_importance: int) -> List[Dict[str, Any]]:
        """Generate database-related tasks."""
        tasks = []
        incident_lower = incident.lower()
        
        if 'database' in incident_lower or 'data' in incident_lower or 'slow' in incident_lower:
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_DB_01",
                "description": "Analyze database query performance",
                "importance": base_importance + 3,
                "estimated_hours": 3,
                "tentative_deadline": deadline - timedelta(hours=8),
                "assigned_to": self.members[0] if self.members else self.team_lead,
                "dependencies": []
            })
            
            tasks.append({
                "task_id": f"{self.team_name.replace(' ', '_')}_DB_02",
                "description": "Optimize slow queries and add indexes",
                "importance": base_importance + 4,
                "estimated_hours": 5,
                "tentative_deadline": deadline - timedelta(hours=3),
                "assigned_to": self.team_lead,
                "dependencies": [f"{self.team_name.replace(' ', '_')}_DB_01"]
            })
        
        return tasks
    
    def __repr__(self):
        return f"IncidentSlaveAgent(team='{self.team_name}', expertise={self.expertise})"
