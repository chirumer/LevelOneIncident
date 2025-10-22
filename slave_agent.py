"""
Slave Agent - Represents knowledge about a specific team
Each slave agent only knows about its team's information and can answer queries about it
"""

import re
from typing import Dict, Any, List


class SlaveAgent:
    """
    A slave agent that has knowledge about a specific team.
    It can identify itself and answer questions about its team's information.
    """
    
    def __init__(self, team_file_path: str):
        """
        Initialize the slave agent with team information from a file.
        
        Args:
            team_file_path: Path to the text file containing team information
        """
        self.team_file_path = team_file_path
        self.team_name = ""
        self.team_lead = ""
        self.members = []
        self.content = ""
        self.capabilities = []
        
        self._load_team_info()
        self._identify_capabilities()
    
    def _load_team_info(self):
        """Load and parse team information from the file."""
        try:
            with open(self.team_file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            # Extract team name
            team_name_match = re.search(r'Team Name:\s*(.+)', self.content)
            if team_name_match:
                self.team_name = team_name_match.group(1).strip()
            
            # Extract team lead
            team_lead_match = re.search(r'Team Lead:\s*(.+)', self.content)
            if team_lead_match:
                self.team_lead = team_lead_match.group(1).strip()
            
            # Extract members
            members_match = re.search(r'Members:\s*(.+)', self.content)
            if members_match:
                members_str = members_match.group(1).strip()
                self.members = [m.strip() for m in members_str.split(',')]
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Team info file not found: {self.team_file_path}")
        except Exception as e:
            raise Exception(f"Error loading team info: {str(e)}")
    
    def _identify_capabilities(self):
        """
        Identify what information this agent can provide based on its content.
        This helps the master agent decide which slave agents to query.
        """
        self.capabilities = []
        
        # Identify key topics and keywords
        content_lower = self.content.lower()
        
        # Add team name as primary capability
        if self.team_name:
            self.capabilities.append(f"team:{self.team_name}")
        
        # Identify specific projects/issues mentioned
        issue_patterns = [
            r'([A-Z]+-\d+)',  # JIRA-style issue IDs
            r'(TSUNAMI)',
            r'(frontend|backend|infrastructure|security)',
        ]
        
        for pattern in issue_patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE)
            for match in matches:
                capability = f"topic:{match.upper()}"
                if capability not in self.capabilities:
                    self.capabilities.append(capability)
        
        # Identify data sources
        if 'jira' in content_lower:
            self.capabilities.append("source:jira")
        if 'confluence' in content_lower:
            self.capabilities.append("source:confluence")
        if 'slack' in content_lower:
            self.capabilities.append("source:slack")
        
        # Identify meeting information
        if 'meeting' in content_lower:
            self.capabilities.append("has:meetings")
    
    def get_identity(self) -> Dict[str, Any]:
        """
        Return the agent's identity and capabilities.
        This is used by the master agent to decide which agents to query.
        
        Returns:
            Dictionary containing agent identity and capabilities
        """
        return {
            "team_name": self.team_name,
            "team_lead": self.team_lead,
            "member_count": len(self.members),
            "capabilities": self.capabilities,
            "file_path": self.team_file_path
        }
    
    def answer_query(self, query: str) -> Dict[str, Any]:
        """
        Answer a specific query about the team's information.
        
        Args:
            query: The question to answer
            
        Returns:
            Dictionary containing the answer and relevant information
        """
        query_lower = query.lower()
        
        # Count occurrences of specific terms
        if "how many times" in query_lower or "count" in query_lower:
            return self._count_occurrences(query)
        
        # Find meetings related to a topic
        if "meeting" in query_lower:
            return self._find_meetings(query)
        
        # Find issues/tickets
        if "issue" in query_lower or "ticket" in query_lower or "jira" in query_lower:
            return self._find_issues(query)
        
        # General search
        return self._general_search(query)
    
    def _count_occurrences(self, query: str) -> Dict[str, Any]:
        """Count how many times a term appears in the team's information."""
        # Extract the term to count
        terms_to_count = []
        
        # Look for specific patterns
        patterns = [
            r'how many times.*?(\w+)',
            r'count.*?(\w+)',
            r'occurrences of (\w+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            if matches:
                terms_to_count.extend(matches)
        
        # Also extract capitalized words (likely issue names)
        capitalized = re.findall(r'\b([A-Z][A-Z]+)\b', query)
        terms_to_count.extend(capitalized)
        
        results = {}
        for term in set(terms_to_count):
            count = len(re.findall(r'\b' + re.escape(term) + r'\b', self.content, re.IGNORECASE))
            results[term] = count
        
        return {
            "team_name": self.team_name,
            "query_type": "count",
            "results": results,
            "total_mentions": sum(results.values())
        }
    
    def _find_meetings(self, query: str) -> Dict[str, Any]:
        """Find meetings related to the query."""
        meetings = []
        
        # Extract meeting sections
        meeting_pattern = r'- (\d{4}-\d{2}-\d{2}):\s*(.+?)(?=\n  - |\n\n|\Z)'
        matches = re.findall(meeting_pattern, self.content, re.DOTALL)
        
        for date, meeting_info in matches:
            # Check if query terms are in the meeting info
            query_terms = re.findall(r'\b\w+\b', query.lower())
            meeting_lower = meeting_info.lower()
            
            relevance_score = sum(1 for term in query_terms if term in meeting_lower)
            
            if relevance_score > 0 or "all" in query.lower():
                meetings.append({
                    "date": date,
                    "info": meeting_info.strip(),
                    "relevance": relevance_score
                })
        
        return {
            "team_name": self.team_name,
            "query_type": "meetings",
            "meetings": meetings,
            "meeting_count": len(meetings)
        }
    
    def _find_issues(self, query: str) -> Dict[str, Any]:
        """Find issues/tickets related to the query."""
        issues = []
        
        # Extract issue sections
        issue_pattern = r'- ([A-Z]+-\d+):\s*(.+?)(?=\n  - |\n\n- [A-Z]+-|\n\n===|\Z)'
        matches = re.findall(issue_pattern, self.content, re.DOTALL)
        
        for issue_id, issue_info in matches:
            # Check if query terms are in the issue info
            query_terms = re.findall(r'\b\w+\b', query.lower())
            issue_lower = issue_info.lower()
            
            relevance_score = sum(1 for term in query_terms if term in issue_lower)
            
            if relevance_score > 0 or "all" in query.lower():
                issues.append({
                    "issue_id": issue_id,
                    "info": issue_info.strip(),
                    "relevance": relevance_score
                })
        
        return {
            "team_name": self.team_name,
            "query_type": "issues",
            "issues": issues,
            "issue_count": len(issues)
        }
    
    def _general_search(self, query: str) -> Dict[str, Any]:
        """Perform a general search in the team's information."""
        query_terms = re.findall(r'\b\w+\b', query.lower())
        
        # Find relevant sections
        relevant_sections = []
        sections = self.content.split('\n\n')
        
        for section in sections:
            section_lower = section.lower()
            relevance_score = sum(1 for term in query_terms if term in section_lower)
            
            if relevance_score > 0:
                relevant_sections.append({
                    "content": section.strip(),
                    "relevance": relevance_score
                })
        
        # Sort by relevance
        relevant_sections.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "team_name": self.team_name,
            "query_type": "general",
            "relevant_sections": relevant_sections[:5],  # Top 5 most relevant
            "total_matches": len(relevant_sections)
        }
    
    def __repr__(self):
        return f"SlaveAgent(team='{self.team_name}', capabilities={len(self.capabilities)})"
