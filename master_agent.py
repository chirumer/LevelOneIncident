"""
Master Agent - Intelligently coordinates slave agents to answer user queries
The master agent selects which slave agents to query based on their capabilities
"""

import os
import re
from typing import List, Dict, Any, Tuple
from slave_agent import SlaveAgent


class MasterAgent:
    """
    Master agent that coordinates multiple slave agents.
    It intelligently selects which agents to query based on the user's question.
    """
    
    def __init__(self, team_info_directory: str):
        """
        Initialize the master agent with all available slave agents.
        
        Args:
            team_info_directory: Directory containing team information files
        """
        self.team_info_directory = team_info_directory
        self.slave_agents: List[SlaveAgent] = []
        self._initialize_slave_agents()
    
    def _initialize_slave_agents(self):
        """Create a slave agent for each team info file."""
        if not os.path.exists(self.team_info_directory):
            raise FileNotFoundError(f"Team info directory not found: {self.team_info_directory}")
        
        # Find all text files in the directory
        for filename in os.listdir(self.team_info_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.team_info_directory, filename)
                try:
                    agent = SlaveAgent(file_path)
                    self.slave_agents.append(agent)
                    print(f"✓ Initialized slave agent for: {agent.team_name}")
                except Exception as e:
                    print(f"✗ Failed to initialize agent for {filename}: {str(e)}")
        
        print(f"\nTotal slave agents initialized: {len(self.slave_agents)}")
    
    def get_all_agents_info(self) -> List[Dict[str, Any]]:
        """Get identity information from all slave agents."""
        return [agent.get_identity() for agent in self.slave_agents]
    
    def _extract_query_keywords(self, query: str) -> List[str]:
        """
        Extract important keywords from the user's query.
        
        Args:
            query: User's question
            
        Returns:
            List of keywords
        """
        keywords = []
        
        # Extract capitalized words (likely project/issue names)
        capitalized = re.findall(r'\b([A-Z][A-Z]+)\b', query)
        keywords.extend(capitalized)
        
        # Extract issue IDs (e.g., TSUNAMI-101)
        issue_ids = re.findall(r'\b([A-Z]+-\d+)\b', query)
        keywords.extend(issue_ids)
        
        # Extract important terms
        important_terms = [
            'meeting', 'issue', 'ticket', 'jira', 'confluence', 'slack',
            'frontend', 'backend', 'infrastructure', 'security', 'team'
        ]
        
        query_lower = query.lower()
        for term in important_terms:
            if term in query_lower:
                keywords.append(term)
        
        return list(set(keywords))
    
    def _score_agent_relevance(self, agent: SlaveAgent, query: str, keywords: List[str]) -> Tuple[int, List[str]]:
        """
        Score how relevant an agent is to the query.
        
        Args:
            agent: The slave agent to score
            query: User's question
            keywords: Extracted keywords from the query
            
        Returns:
            Tuple of (relevance_score, matching_capabilities)
        """
        score = 0
        matching_capabilities = []
        
        identity = agent.get_identity()
        capabilities = identity['capabilities']
        
        # Check if keywords match capabilities
        for keyword in keywords:
            keyword_upper = keyword.upper()
            keyword_lower = keyword.lower()
            
            for capability in capabilities:
                if keyword_upper in capability.upper() or keyword_lower in capability.lower():
                    score += 10
                    matching_capabilities.append(capability)
        
        # Check if team name is mentioned in query
        team_name = identity['team_name'].lower()
        if team_name in query.lower():
            score += 20
            matching_capabilities.append(f"team:{identity['team_name']}")
        
        # If query is very general, include all agents with lower score
        general_terms = ['all', 'every', 'total', 'overall']
        if any(term in query.lower() for term in general_terms):
            score += 1
        
        return score, matching_capabilities
    
    def _select_agents(self, query: str) -> List[Tuple[SlaveAgent, int, List[str]]]:
        """
        Intelligently select which slave agents should be queried.
        
        Args:
            query: User's question
            
        Returns:
            List of tuples (agent, relevance_score, matching_capabilities)
        """
        keywords = self._extract_query_keywords(query)
        
        # Score all agents
        scored_agents = []
        for agent in self.slave_agents:
            score, matching = self._score_agent_relevance(agent, query, keywords)
            if score > 0:
                scored_agents.append((agent, score, matching))
        
        # Sort by relevance score (highest first)
        scored_agents.sort(key=lambda x: x[1], reverse=True)
        
        # If no agents scored, query all agents (general query)
        if not scored_agents:
            scored_agents = [(agent, 1, []) for agent in self.slave_agents]
        
        return scored_agents
    
    def process_query(self, query: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Process a user query by selecting and querying appropriate slave agents.
        
        Args:
            query: User's question
            verbose: Whether to print detailed selection process
            
        Returns:
            Dictionary containing the aggregated results
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"MASTER AGENT: Processing query")
            print(f"{'='*80}")
            print(f"Query: {query}\n")
        
        # Select relevant agents
        selected_agents = self._select_agents(query)
        
        if verbose:
            print(f"Agent Selection Process:")
            print(f"  • Analyzed {len(self.slave_agents)} available agents")
            print(f"  • Selected {len(selected_agents)} relevant agents\n")
            
            print("Selected Agents (by relevance):")
            for i, (agent, score, matching) in enumerate(selected_agents, 1):
                print(f"  {i}. {agent.team_name} (score: {score})")
                if matching:
                    print(f"     Matching capabilities: {', '.join(matching)}")
            print()
        
        # Query selected agents
        results = []
        for agent, score, matching in selected_agents:
            if verbose:
                print(f"Querying: {agent.team_name}...")
            
            answer = agent.answer_query(query)
            answer['relevance_score'] = score
            answer['matching_capabilities'] = matching
            results.append(answer)
            
            if verbose:
                print(f"  ✓ Response received\n")
        
        # Aggregate results
        aggregated = self._aggregate_results(query, results)
        
        return aggregated
    
    def _aggregate_results(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results from multiple slave agents into a coherent answer.
        
        Args:
            query: Original user query
            results: List of results from slave agents
            
        Returns:
            Aggregated results
        """
        aggregated = {
            "query": query,
            "agents_queried": len(results),
            "individual_results": results,
            "summary": {}
        }
        
        # Aggregate based on query type
        if results and results[0].get('query_type') == 'count':
            # Aggregate counts
            total_counts = {}
            for result in results:
                for term, count in result.get('results', {}).items():
                    if term not in total_counts:
                        total_counts[term] = 0
                    total_counts[term] += count
            
            aggregated['summary'] = {
                "type": "count",
                "total_counts": total_counts,
                "teams_with_mentions": sum(1 for r in results if r.get('total_mentions', 0) > 0)
            }
        
        elif results and results[0].get('query_type') == 'meetings':
            # Aggregate meetings
            total_meetings = sum(r.get('meeting_count', 0) for r in results)
            all_meetings = []
            for result in results:
                for meeting in result.get('meetings', []):
                    meeting['team'] = result['team_name']
                    all_meetings.append(meeting)
            
            # Sort by date
            all_meetings.sort(key=lambda x: x['date'], reverse=True)
            
            aggregated['summary'] = {
                "type": "meetings",
                "total_meetings": total_meetings,
                "all_meetings": all_meetings
            }
        
        elif results and results[0].get('query_type') == 'issues':
            # Aggregate issues
            total_issues = sum(r.get('issue_count', 0) for r in results)
            all_issues = []
            for result in results:
                for issue in result.get('issues', []):
                    issue['team'] = result['team_name']
                    all_issues.append(issue)
            
            # Sort by relevance
            all_issues.sort(key=lambda x: x['relevance'], reverse=True)
            
            aggregated['summary'] = {
                "type": "issues",
                "total_issues": total_issues,
                "all_issues": all_issues
            }
        
        else:
            # General aggregation
            aggregated['summary'] = {
                "type": "general",
                "results_by_team": {r['team_name']: r for r in results}
            }
        
        return aggregated
    
    def format_response(self, aggregated_results: Dict[str, Any]) -> str:
        """
        Format the aggregated results into a human-readable response.
        
        Args:
            aggregated_results: Aggregated results from process_query
            
        Returns:
            Formatted string response
        """
        output = []
        output.append("\n" + "="*80)
        output.append("MASTER AGENT: Final Answer")
        output.append("="*80 + "\n")
        
        summary = aggregated_results.get('summary', {})
        summary_type = summary.get('type')
        
        if summary_type == 'count':
            output.append("Count Results:")
            total_counts = summary.get('total_counts', {})
            for term, count in total_counts.items():
                output.append(f"  • '{term}' mentioned {count} times across all teams")
            output.append(f"\nTeams with mentions: {summary.get('teams_with_mentions', 0)}")
        
        elif summary_type == 'meetings':
            total = summary.get('total_meetings', 0)
            output.append(f"Total Meetings Found: {total}\n")
            
            meetings = summary.get('all_meetings', [])
            for meeting in meetings:
                output.append(f"• {meeting['date']} - {meeting['team']}")
                # Extract first line of meeting info
                first_line = meeting['info'].split('\n')[0]
                output.append(f"  {first_line}")
        
        elif summary_type == 'issues':
            total = summary.get('total_issues', 0)
            output.append(f"Total Issues Found: {total}\n")
            
            issues = summary.get('all_issues', [])
            for issue in issues[:10]:  # Show top 10
                output.append(f"• {issue['issue_id']} - {issue['team']}")
                # Extract first line of issue info
                first_line = issue['info'].split('\n')[0]
                output.append(f"  {first_line}")
        
        else:
            output.append("Results by Team:\n")
            for result in aggregated_results.get('individual_results', []):
                output.append(f"• {result['team_name']}")
                output.append(f"  Relevance score: {result.get('relevance_score', 0)}")
        
        output.append("\n" + "="*80)
        
        return "\n".join(output)
    
    def ask(self, query: str, verbose: bool = True) -> str:
        """
        Main method to ask a question and get a formatted response.
        
        Args:
            query: User's question
            verbose: Whether to show detailed process
            
        Returns:
            Formatted response string
        """
        results = self.process_query(query, verbose=verbose)
        return self.format_response(results)
    
    def __repr__(self):
        return f"MasterAgent(slave_agents={len(self.slave_agents)})"
