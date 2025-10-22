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
        
        <div class="incident-form">
            <h2 style="margin-bottom: 20px;">📋 Incident Report</h2>
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
            </div>
            
            <div class="section">
                <div class="section-title">🕸️ Task Dependency Graph</div>
                {graph_html if graph_html else '<div class="no-data">No graph data available</div>'}
            </div>
            
            <div class="section">
                <div class="section-title">📋 Task Assignments</div>
                {assignments_html if assignments_html else '<div class="no-data">No assignments available</div>'}
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
