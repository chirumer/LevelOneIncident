"""
Web server for incident response visualization
Displays task graphs and assignment tables
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse
from incident_master_agent import IncidentMasterAgent


class IncidentResponseHandler(BaseHTTPRequestHandler):
    """HTTP request handler for incident response visualization."""
    
    # Class variable to store the master agent
    master_agent = None
    current_incident_data = None
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/api/incident':
            self.serve_incident_data()
        elif path == '/api/teams':
            self.serve_teams_data()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/create_incident':
            self.handle_create_incident()
        else:
            self.send_error(404, "Not Found")
    
    def serve_index(self):
        """Serve the main HTML page."""
        html = self.generate_index_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_incident_data(self):
        """Serve current incident data as JSON."""
        if self.current_incident_data is None:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No incident data"}).encode())
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.current_incident_data).encode())
    
    def serve_teams_data(self):
        """Serve teams information as JSON."""
        if self.master_agent is None:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Master agent not initialized"}).encode())
            return
        
        teams = [agent.get_team_info() for agent in self.master_agent.slave_agents]
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(teams).encode())
    
    def handle_create_incident(self):
        """Handle incident creation request."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        # Extract comprehensive incident report data
        title = data.get('title', '')
        description = data.get('description', '')
        severity = data.get('severity', 'medium')
        hours_to_deadline = data.get('hours_to_deadline', 24)
        affected_services = data.get('affected_services', '')
        impact = data.get('impact', '')
        reported_by = data.get('reported_by', 'Unknown')
        detection_method = data.get('detection_method', '')
        initial_actions = data.get('initial_actions', '')
        
        if not description:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Incident description required"}).encode())
            return
        
        # Build comprehensive incident description for agents
        full_description = f"{title}: {description}"
        if affected_services:
            full_description += f" | Affected Services: {affected_services}"
        if impact:
            full_description += f" | Customer Impact: {impact}"
        if severity:
            full_description += f" | Severity: {severity.upper()}"
        if initial_actions:
            full_description += f" | Initial Actions: {initial_actions}"
        
        # Calculate deadline
        deadline = datetime.now() + timedelta(hours=hours_to_deadline)
        
        # Handle incident with comprehensive description
        incident_data = self.master_agent.handle_incident(full_description, deadline)
        
        # Add incident report metadata
        incident_data['incident_report'] = {
            'title': title,
            'description': description,
            'severity': severity,
            'affected_services': affected_services,
            'impact': impact,
            'reported_by': reported_by,
            'detection_method': detection_method,
            'initial_actions': initial_actions,
            'reported_at': datetime.now().isoformat()
        }
        
        # Store in class variable so it persists across requests
        IncidentResponseHandler.current_incident_data = incident_data
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "data": incident_data}).encode())
    
    def _generate_internals_html(self):
        """Generate HTML explaining the internal coordination process."""
        if not self.current_incident_data:
            return ""
        
        assignments = self.current_incident_data.get('assignments', [])
        
        html = """
        <div style="background: #f9fafb; border-radius: 8px; padding: 20px; border: 2px solid #e5e7eb;">
            <h3 style="margin: 0 0 15px 0; color: #059669;">🤖 Multi-Agent Coordination Process</h3>
            
            <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid #3b82f6;">
                <h4 style="margin: 0 0 10px 0; color: #1e40af;">📡 Step 1: Incident Broadcast</h4>
                <p style="margin: 0; color: #4b5563; font-size: 14px;">
                    The <strong>Master Agent</strong> received your incident report and broadcast it to all team agents. 
                    Each team agent independently analyzed the incident based on their expertise and current workload.
                </p>
            </div>
            
            <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid #8b5cf6;">
                <h4 style="margin: 0 0 10px 0; color: #6d28d9;">🧠 Step 2: Team Agent Analysis</h4>
                <p style="margin: 0 0 10px 0; color: #4b5563; font-size: 14px;">
                    Each team agent has access to real-time data from multiple sources:
                </p>
                <ul style="margin: 0; padding-left: 20px; color: #4b5563; font-size: 14px;">
                    <li><strong>JIRA Integration:</strong> Current sprint tasks, team capacity, and ongoing work</li>
                    <li><strong>Confluence:</strong> Team documentation, runbooks, and procedures</li>
                    <li><strong>Slack Activity:</strong> Recent discussions, mentions, and team availability</li>
                    <li><strong>Team Expertise:</strong> Technical skills and domain knowledge</li>
                    <li><strong>Historical Data:</strong> Past incidents and resolution patterns</li>
                </ul>
            </div>
        """
        
        # Add team-specific analysis
        for assignment in assignments:
            team_name = assignment.get('team_name', 'Unknown Team')
            task_count = assignment.get('task_count', 0)
            
            html += f"""
            <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid #f59e0b;">
                <h4 style="margin: 0 0 10px 0; color: #d97706;">👥 {team_name}</h4>
                <p style="margin: 0 0 8px 0; color: #4b5563; font-size: 14px;">
                    <strong>Relevance Analysis:</strong> This team calculated their relevance score by matching incident keywords 
                    with their expertise areas and checking for similar past incidents.
                </p>
                <p style="margin: 0 0 8px 0; color: #4b5563; font-size: 14px;">
                    <strong>Task Generation:</strong> Based on relevance, the team agent proposed <strong>{task_count} tasks</strong> 
                    by analyzing:
                </p>
                <ul style="margin: 0; padding-left: 20px; color: #4b5563; font-size: 13px;">
                    <li>Current team capacity from JIRA</li>
                    <li>Relevant runbooks from Confluence</li>
                    <li>Team member availability from Slack</li>
                    <li>Historical incident response patterns</li>
                </ul>
            </div>
            """
        
        html += """
            <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid #ec4899;">
                <h4 style="margin: 0 0 10px 0; color: #be185d;">🔗 Step 3: Dependency Analysis</h4>
                <p style="margin: 0; color: #4b5563; font-size: 14px;">
                    The <strong>Master Agent</strong> analyzed all proposed tasks and automatically identified dependencies. 
                    Tasks were linked based on:
                </p>
                <ul style="margin: 5px 0 0 0; padding-left: 20px; color: #4b5563; font-size: 14px;">
                    <li>Technical dependencies (e.g., "diagnose issue" before "implement fix")</li>
                    <li>Resource dependencies (e.g., shared infrastructure)</li>
                    <li>Priority ordering (critical tasks first)</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid #10b981;">
                <h4 style="margin: 0 0 10px 0; color: #059669;">📊 Step 4: Visualization & Coordination</h4>
                <p style="margin: 0; color: #4b5563; font-size: 14px;">
                    The Master Agent generated the task dependency graph and prioritized assignments. 
                    The graph shows the optimal execution order, and tasks are assigned to teams based on 
                    expertise, capacity, and current workload.
                </p>
            </div>
            
            <div style="background: #fef3c7; padding: 15px; border-radius: 6px; border-left: 4px solid #f59e0b;">
                <h4 style="margin: 0 0 10px 0; color: #d97706;">💡 Key Insight</h4>
                <p style="margin: 0; color: #92400e; font-size: 14px;">
                    This entire coordination process happened in <strong>seconds</strong>. Each team agent independently 
                    analyzed the incident using their own context (JIRA, Confluence, Slack data), and the Master Agent 
                    synthesized their proposals into a coordinated response plan. No human intervention was needed!
                </p>
            </div>
        </div>
        """
        
        return html
    
    def _generate_teams_list_html(self):
        """Generate HTML list of teams involved in the incident response."""
        if not self.current_incident_data:
            return ""
        
        assignments = self.current_incident_data.get('assignments', [])
        if not assignments:
            return ""
        
        html = """
        <div style="margin-top: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; border-left: 4px solid #667eea;">
            <h4 style="margin: 0 0 10px 0; color: #333; font-size: 14px;">👥 Responding Teams:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """
        
        for assignment in assignments:
            team_name = assignment.get('team_name', 'Unknown Team')
            task_count = assignment.get('task_count', 0)
            html += f"""
                <div style="background: white; padding: 8px 12px; border-radius: 6px; border: 1px solid #e5e7eb; font-size: 13px;">
                    <strong>{team_name}</strong> <span style="color: #6b7280;">({task_count} tasks)</span>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def _generate_incident_overview_html(self):
        """Generate HTML for incident overview with comprehensive details."""
        if not self.current_incident_data:
            return ""
        
        report = self.current_incident_data.get('incident_report', {})
        
        # Severity badge color
        severity_colors = {
            'critical': '#dc2626',
            'high': '#ea580c',
            'medium': '#ca8a04',
            'low': '#16a34a'
        }
        severity = report.get('severity', 'medium')
        severity_color = severity_colors.get(severity, '#ca8a04')
        
        html = f"""
        <h3>{report.get('title', self.current_incident_data.get('incident', 'Incident'))}</h3>
        <div style="display: inline-block; background: {severity_color}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: 600; margin: 10px 0;">
            {severity.upper()} SEVERITY
        </div>
        <p style="margin-top: 15px;"><strong>Description:</strong> {report.get('description', 'N/A')}</p>
        """
        
        if report.get('affected_services'):
            html += f"<p><strong>Affected Services:</strong> {report.get('affected_services')}</p>"
        
        if report.get('impact'):
            html += f"<p><strong>Customer Impact:</strong> {report.get('impact')}</p>"
        
        if report.get('reported_by'):
            html += f"<p><strong>Reported By:</strong> {report.get('reported_by')}</p>"
        
        if report.get('detection_method'):
            html += f"<p><strong>Detection Method:</strong> {report.get('detection_method').replace('_', ' ').title()}</p>"
        
        if report.get('initial_actions'):
            html += f"<p><strong>Initial Actions:</strong> {report.get('initial_actions')}</p>"
        
        html += f"<p><strong>Deadline:</strong> {self.current_incident_data.get('deadline', '')}</p>"
        
        return html
    
    def generate_index_html(self):
        """Generate the main HTML page."""
        graph_html = ""
        assignments_html = ""
        
        if self.current_incident_data:
            graph_html = self.master_agent.generate_graph_html(
                self.current_incident_data["task_graph"]
            )
            assignments_html = self.master_agent.generate_assignments_html(
                self.current_incident_data["assignments"]
            )
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incident Response Coordination System</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 16px;
        }}
        
        .incident-form {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }}
        
        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            font-family: inherit;
        }}
        
        .form-group textarea {{
            resize: vertical;
            min-height: 100px;
        }}
        
        .form-group input:focus,
        .form-group textarea:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px 30px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
        }}
        
        .btn:active {{
            transform: translateY(0);
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .incident-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .incident-info h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .incident-info p {{
            color: #666;
            margin-bottom: 8px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .no-data {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 16px;
        }}
        
        .example-buttons {{
            display: flex;
            gap: 10px;
            margin: 15px 0 25px 0;
            flex-wrap: wrap;
        }}
        
        .example-btn {{
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .example-btn:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
        }}
        
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Incident Response Coordination System</h1>
            <p>Multi-agent task coordination and visualization platform</p>
        </div>
        
        <div class="incident-form" id="incidentFormContainer">
            <h2 style="margin-bottom: 20px;">📋 Incident Report</h2>
            <div style="background: #f0f9ff; border-left: 4px solid #667eea; padding: 15px; margin-bottom: 25px; border-radius: 6px;">
                <p style="margin: 0 0 12px 0; font-size: 14px; color: #1e40af; font-weight: 600;">
                    💡 Quick Examples
                </p>
                <p style="margin: 0 0 12px 0; font-size: 13px; color: #1e40af;">
                    Click any button to auto-fill the form with a sample incident:
                </p>
                <div class="example-buttons" style="margin: 0;">
                    <button type="button" class="example-btn" onclick="loadExample('rds')">💾 RDS Outage</button>
                    <button type="button" class="example-btn" onclick="loadExample('security')">🔒 Security Breach</button>
                    <button type="button" class="example-btn" onclick="loadExample('lambda')">⚡ Lambda Timeout</button>
                    <button type="button" class="example-btn" onclick="loadExample('s3')">📦 S3 Access Issue</button>
                    <button type="button" class="example-btn" onclick="loadExample('api')">🌐 API Slowdown</button>
                    <button type="button" class="example-btn" onclick="loadExample('disk')">💿 Disk Space Alert</button>
                    <button type="button" class="example-btn" onclick="loadExample('ssl')">🔐 SSL Certificate Expiry</button>
                    <button type="button" class="example-btn" onclick="loadExample('memory')">🧠 Memory Leak</button>
                </div>
            </div>
            <form id="incidentForm">
                <div class="form-group">
                    <label for="title">Incident Title *</label>
                    <input type="text" id="title" name="title" placeholder="Brief title (e.g., 'Production RDS Outage')" required>
                </div>
                
                <div class="form-group">
                    <label for="description">Detailed Description *</label>
                    <textarea id="description" name="description" placeholder="Describe what happened, when it started, and what's affected..." required></textarea>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="form-group">
                        <label for="severity">Severity *</label>
                        <select id="severity" name="severity" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 14px;" required>
                            <option value="">Select severity...</option>
                            <option value="critical">🔴 Critical - Complete service outage</option>
                            <option value="high">🟠 High - Major functionality impaired</option>
                            <option value="medium">🟡 Medium - Partial functionality affected</option>
                            <option value="low">🟢 Low - Minor issue</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="deadline">Hours to Deadline *</label>
                        <input type="number" id="deadline" name="deadline" value="24" min="1" max="168" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="affected_services">Affected AWS Services</label>
                    <input type="text" id="affected_services" name="affected_services" placeholder="e.g., RDS, EC2, Lambda, S3 (comma-separated)">
                </div>
                
                <div class="form-group">
                    <label for="impact">Customer Impact</label>
                    <textarea id="impact" name="impact" placeholder="Describe how customers are affected..." style="min-height: 60px;"></textarea>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="form-group">
                        <label for="reported_by">Reported By</label>
                        <input type="text" id="reported_by" name="reported_by" placeholder="Your name">
                    </div>
                    
                    <div class="form-group">
                        <label for="detection_method">Detection Method</label>
                        <select id="detection_method" name="detection_method" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 14px;">
                            <option value="">Select method...</option>
                            <option value="monitoring">CloudWatch Alarm</option>
                            <option value="customer">Customer Report</option>
                            <option value="internal">Internal Testing</option>
                            <option value="automated">Automated Detection</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="initial_actions">Initial Actions Taken (Optional)</label>
                    <textarea id="initial_actions" name="initial_actions" placeholder="Any immediate actions already taken..." style="min-height: 60px;"></textarea>
                </div>
                
                <button type="submit" class="btn">🚀 Coordinate Response</button>
            </form>
        </div>
        
        <div id="results" style="display: {'block' if self.current_incident_data else 'none'};">
            <div class="section">
                <div class="section-title">📊 Incident Overview</div>
                <div class="incident-info">
                    {self._generate_incident_overview_html() if self.current_incident_data else ''}
                </div>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{self.current_incident_data.get('total_tasks', 0) if self.current_incident_data else 0}</div>
                        <div class="stat-label">Total Tasks</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{self.current_incident_data.get('teams_involved', 0) if self.current_incident_data else 0}</div>
                        <div class="stat-label">Teams Involved</div>
                    </div>
                </div>
                {self._generate_teams_list_html() if self.current_incident_data else ''}
            </div>
            
            <div class="section">
                <div class="section-title">🕸️ Task Dependency Graph</div>
                {graph_html if graph_html else '<div class="no-data">No graph data available</div>'}
            </div>
            
            <div class="section">
                <div class="section-title">📋 Task Assignments</div>
                {assignments_html if assignments_html else '<div class="no-data">No assignments available</div>'}
            </div>
            
            <div class="section">
                <button onclick="toggleInternals()" class="btn" style="width: 100%; background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                    🔍 See Internals - How We Generated This Response
                </button>
                
                <div id="internals" style="display: none; margin-top: 20px;">
                    {self._generate_internals_html() if self.current_incident_data else ''}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('incidentForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            
            // Collect all form data
            const formData = {{
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                severity: document.getElementById('severity').value,
                hours_to_deadline: parseInt(document.getElementById('deadline').value),
                affected_services: document.getElementById('affected_services').value,
                impact: document.getElementById('impact').value,
                reported_by: document.getElementById('reported_by').value,
                detection_method: document.getElementById('detection_method').value,
                initial_actions: document.getElementById('initial_actions').value
            }};
            
            // Show loading state
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<div class=\"loading\"><div class=\"spinner\"></div><p>Coordinating response...</p></div>';
            
            try {{
                const response = await fetch('/api/create_incident', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(formData)
                }});
                
                const result = await response.json();
                
                if (result.success) {{
                    // Hide form and header, show only results
                    document.getElementById('incidentFormContainer').style.display = 'none';
                    document.querySelector('.header p').innerHTML = '<a href="/" style="color: #667eea; text-decoration: none;">← Report New Incident</a>';
                    
                    // Reload page to show results
                    window.location.reload();
                }} else {{
                    alert('Error: ' + (result.error || 'Unknown error'));
                }}
            }} catch (error) {{
                alert('Error creating incident: ' + error.message);
                resultsDiv.style.display = 'none';
            }}
        }});
        
        // Example incident scenarios
        function loadExample(type) {{
            const examples = {{
                'rds': {{
                    title: 'Production RDS Connection Pool Exhaustion',
                    description: 'PostgreSQL RDS instance (prod-db-01) experiencing connection pool exhaustion. Started at 14:30 UTC. Authentication service unable to establish database connections, causing cascading failures across API endpoints.',
                    severity: 'critical',
                    deadline: 4,
                    affected_services: 'RDS, EC2, Lambda, API Gateway',
                    impact: 'Complete service outage - users unable to login, all API requests failing with 500 errors. Approximately 50,000 active users affected.',
                    reported_by: 'CloudWatch Alarm',
                    detection_method: 'monitoring',
                    initial_actions: 'Verified RDS instance health, checked CloudWatch metrics showing 100% connection pool utilization, attempted connection pool restart (failed)'
                }},
                'security': {{
                    title: 'Suspicious IAM Activity Detected',
                    description: 'GuardDuty detected unusual IAM role assumption patterns from unknown IP addresses. Multiple failed authentication attempts followed by successful access to S3 buckets containing customer data.',
                    severity: 'critical',
                    deadline: 2,
                    affected_services: 'IAM, S3, CloudTrail, GuardDuty',
                    impact: 'Potential data breach - unauthorized access to customer data buckets. No confirmed data exfiltration yet but access logs show suspicious read operations.',
                    reported_by: 'Security Team',
                    detection_method: 'automated',
                    initial_actions: 'Revoked compromised IAM credentials, enabled MFA requirement, isolated affected S3 buckets, initiated CloudTrail log analysis'
                }},
                'lambda': {{
                    title: 'Lambda Function Timeout Spike',
                    description: 'Payment processing Lambda functions experiencing widespread timeouts (>90% failure rate). Functions timing out after 30 seconds when attempting to connect to external payment gateway API.',
                    severity: 'high',
                    deadline: 6,
                    affected_services: 'Lambda, API Gateway, DynamoDB, SQS',
                    impact: 'Payment processing completely down. Users unable to complete purchases. Estimated revenue loss: $5,000/hour. Queue backlog building up in SQS.',
                    reported_by: 'Customer Support',
                    detection_method: 'customer',
                    initial_actions: 'Checked Lambda CloudWatch logs, verified payment gateway API status (operational), increased Lambda timeout to 60s (no improvement), scaled up concurrent executions'
                }},
                's3': {{
                    title: 'S3 Bucket Access Denied Errors',
                    description: 'Production application unable to access S3 bucket (prod-assets-bucket) due to permission errors. Bucket policy was recently updated and appears to have incorrect IAM permissions.',
                    severity: 'medium',
                    deadline: 12,
                    affected_services: 'S3, CloudFront, EC2',
                    impact: 'Static assets (images, CSS, JS) not loading on website. Users seeing broken images and unstyled pages. Approximately 30% of page functionality affected.',
                    reported_by: 'DevOps Team',
                    detection_method: 'internal',
                    initial_actions: 'Reviewed recent S3 bucket policy changes, attempted to rollback policy (access denied), verified IAM role permissions, checked CloudTrail for policy modification events'
                }},
                'api': {{
                    title: 'API Response Time Degradation',
                    description: 'REST API endpoints showing increased response times. Average latency increased from 200ms to 3000ms over the past hour. Affecting all API Gateway endpoints.',
                    severity: 'high',
                    deadline: 8,
                    affected_services: 'API Gateway, Lambda, DynamoDB',
                    impact: 'Mobile app and web application experiencing slow performance. User complaints increasing. Approximately 25,000 active users affected.',
                    reported_by: 'Monitoring Team',
                    detection_method: 'monitoring',
                    initial_actions: 'Checked API Gateway metrics, reviewed Lambda execution times, verified DynamoDB throttling (none detected)'
                }},
                'disk': {{
                    title: 'EC2 Instance Disk Space Critical',
                    description: 'Production EC2 instance (i-0abc123def) disk usage at 95%. Application logs filling up /var/log partition. Risk of service disruption if disk fills completely.',
                    severity: 'medium',
                    deadline: 6,
                    affected_services: 'EC2',
                    impact: 'No immediate user impact, but application may crash if disk fills. Log rotation not functioning properly.',
                    reported_by: 'CloudWatch Alarm',
                    detection_method: 'monitoring',
                    initial_actions: 'Identified large log files, manually compressed old logs to free 10% space temporarily'
                }},
                'ssl': {{
                    title: 'SSL Certificate Expiring Soon',
                    description: 'SSL certificate for api.example.com expires in 5 days. Certificate renewal process needs to be initiated to avoid service disruption.',
                    severity: 'low',
                    deadline: 96,
                    affected_services: 'CloudFront, Route53, ACM',
                    impact: 'No current impact. If not renewed, users will see security warnings and API access will be blocked.',
                    reported_by: 'Security Team',
                    detection_method: 'automated',
                    initial_actions: 'Verified certificate details in ACM, checked DNS validation records'
                }},
                'memory': {{
                    title: 'Application Memory Leak Detected',
                    description: 'Node.js application showing gradual memory increase over 24 hours. Memory usage started at 512MB, now at 3.2GB and climbing. Application performance degrading.',
                    severity: 'high',
                    deadline: 12,
                    affected_services: 'EC2, ECS',
                    impact: 'Application becoming unresponsive. Response times increasing. Will require restart soon, causing brief downtime.',
                    reported_by: 'DevOps Team',
                    detection_method: 'monitoring',
                    initial_actions: 'Captured heap dump for analysis, reviewed recent code deployments, prepared restart procedure'
                }}
            }};
            
            const example = examples[type];
            if (example) {{
                document.getElementById('title').value = example.title;
                document.getElementById('description').value = example.description;
                document.getElementById('severity').value = example.severity;
                document.getElementById('deadline').value = example.deadline;
                document.getElementById('affected_services').value = example.affected_services;
                document.getElementById('impact').value = example.impact;
                document.getElementById('reported_by').value = example.reported_by;
                document.getElementById('detection_method').value = example.detection_method;
                document.getElementById('initial_actions').value = example.initial_actions;
                
                // Scroll to form
                document.getElementById('title').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}
        }}
        
        // Toggle internals section
        function toggleInternals() {{
            const internalsDiv = document.getElementById('internals');
            const button = event.target;
            
            if (internalsDiv.style.display === 'none') {{
                internalsDiv.style.display = 'block';
                button.textContent = '🔼 Hide Internals';
                internalsDiv.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }} else {{
                internalsDiv.style.display = 'none';
                button.textContent = '🔍 See Internals - How We Generated This Response';
            }}
        }}
        
        // On page load, hide form if results are shown
        window.addEventListener('DOMContentLoaded', function() {{
            const resultsDiv = document.getElementById('results');
            const formContainer = document.getElementById('incidentFormContainer');
            const headerSubtitle = document.querySelector('.header p');
            
            if (resultsDiv && resultsDiv.style.display === 'block') {{
                // Hide the form
                formContainer.style.display = 'none';
                
                // Change header subtitle to "Report New Incident" link
                headerSubtitle.innerHTML = '<a href="/" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 6px; display: inline-block; transition: all 0.2s;" onmouseover="this.style.background=\\'rgba(255,255,255,0.3)\\'" onmouseout="this.style.background=\\'rgba(255,255,255,0.2)\\'">← Report New Incident</a>';
                
                // Scroll to results
                resultsDiv.scrollIntoView({{ behavior: 'smooth' }});
            }}
        }});
    </script>
</body>
</html>
        """
        
        return html
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def start_server(team_info_directory: str, port: int = 8000):
    """
    Start the web server.
    
    Args:
        team_info_directory: Directory containing team information files
        port: Port to run the server on
    """
    print(f"\n{'='*80}")
    print("INCIDENT RESPONSE WEB SERVER")
    print(f"{'='*80}\n")
    
    # Initialize master agent
    print("Initializing master agent...")
    IncidentResponseHandler.master_agent = IncidentMasterAgent(team_info_directory)
    
    print(f"\n{'='*80}")
    print(f"Server starting on http://localhost:{port}")
    print(f"{'='*80}")
    print("\nOpen your browser and navigate to:")
    print(f"  → http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server\n")
    
    server = HTTPServer(('localhost', port), IncidentResponseHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()
        print("Server stopped.")


if __name__ == "__main__":
    import sys
    
    team_info_dir = os.path.join(os.path.dirname(__file__), 'team_info')
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    
    start_server(team_info_dir, port)
