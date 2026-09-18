#!/usr/bin/env python3
"""
SkillDrop Proxy Server
For local demos, forwards SkillDrop payloads to a configured workflow endpoint.
"""
import json
import sys
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error

# Configuration
SHAREPOINT_SITE = "https://microsoft.sharepoint.com/sites/skilldrop-team-42dbe9"
LIST_ID = "77a33ccb-6605-47e5-afa2-aff1e06b4c01"
GRAPH_API_ENDPOINT = f"{SHAREPOINT_SITE}/_api/lists('{LIST_ID}')/items"
FLOW_ENDPOINT = os.environ.get("SKILLDROP_FLOW_URL")

class SkillDropHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            payload = json.loads(body)
            print(f"[SkillDrop] Received payload from {self.client_address[0]}", file=sys.stderr)
            print(f"[SkillDrop] Payload: {payload.get('PlaylistName')} → {payload.get('RecipientEmail')}", file=sys.stderr)
            
            success, message = send_skilldrop(payload)
            status_code = 200 if success else 503
            
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "success" if success else "error",
                "message": message,
                "playlistName": payload.get("PlaylistName"),
                "recipientEmail": payload.get("RecipientEmail")
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"[SkillDrop] Error: {str(e)}", file=sys.stderr)
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "status": "error",
                "message": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def send_skilldrop(payload):
    if FLOW_ENDPOINT:
        return send_to_flow(payload)
    return create_sharepoint_item(payload)

def send_to_flow(payload):
    try:
        print("[Power Automate] Sending payload to SKILLDROP_FLOW_URL...", file=sys.stderr)
        req = urllib.request.Request(
            FLOW_ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            body = response.read().decode('utf-8', errors='replace')
            print(f"[Power Automate] Response {response.status}: {body[:300]}", file=sys.stderr)
            if 200 <= response.status < 300:
                return True, "SkillDrop sent to the configured Power Automate workflow."
            return False, f"Power Automate returned HTTP {response.status}."
    except Exception as e:
        print(f"[Power Automate] Exception: {str(e)}", file=sys.stderr)
        return False, f"Power Automate handoff failed: {str(e)}"

def create_sharepoint_item(payload):
    """
    Create a SharePoint list item that will trigger the Power Automate flow
    Uses the existing user's SharePoint session via curl with cookies
    Ensures all fields have string values (not null/undefined) to prevent JSON errors
    """
    try:
        print(f"[SharePoint] Creating list item...", file=sys.stderr)
        
        # Build the list item payload with proper defaults
        # Note: SharePoint will ignore fields that don't exist as columns
        fields = {
            "Title": payload.get("Title") or "SkillDrop",
            "PlaylistName": payload.get("PlaylistName") or "",
            "RecipientEmail": payload.get("RecipientEmail") or "",
            "NuggetQuestion": payload.get("NuggetQuestion") or "",
            "ChoiceA": payload.get("ChoiceA") or "",
            "ChoiceB": payload.get("ChoiceB") or "",
            "ChoiceC": payload.get("ChoiceC") or "",
            "CorrectChoice": payload.get("CorrectChoice") or "",
            "Fact1Title": payload.get("Fact1Title") or "",
            "Fact1Value": payload.get("Fact1Value") or "",
            "Fact2Title": payload.get("Fact2Title") or "",
            "Fact2Value": payload.get("Fact2Value") or "",
            "Fact3Title": payload.get("Fact3Title") or "",
            "Fact3Value": payload.get("Fact3Value") or "",
            "Fact4Title": payload.get("Fact4Title") or "",
            "Fact4Value": payload.get("Fact4Value") or "",
            "ScenarioPrompt": payload.get("ScenarioPrompt") or ""
        }
        
        # Remove any None values to avoid JSON serialization issues
        fields = {k: v for k, v in fields.items() if v is not None}
        
        item_data = {"fields": fields}
        
        print(f"[SharePoint] Preparing to send {len(fields)} fields", file=sys.stderr)
        print(f"[SharePoint] Fields: {', '.join(fields.keys())}", file=sys.stderr)
        
        # Prepare the request
        req_data = json.dumps(item_data).encode('utf-8')
        req = urllib.request.Request(
            GRAPH_API_ENDPOINT,
            data=req_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            method='POST'
        )
        
        # Use curl instead for better auth handling with cookies
        curl_cmd = [
            'curl',
            '-s',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-H', 'Accept: application/json',
            '-d', json.dumps(item_data),
            GRAPH_API_ENDPOINT
        ]
        
        print(f"[SharePoint] Executing curl to: {GRAPH_API_ENDPOINT[:80]}...", file=sys.stderr)
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout:
            response_data = json.loads(result.stdout) if result.stdout else {}
            if 'd' in response_data and 'ID' in response_data['d']:
                item_id = response_data['d']['ID']
                print(f"[SharePoint] Item created with ID: {item_id}", file=sys.stderr)
                print(f"[Power Automate] Flow should trigger now...", file=sys.stderr)
                return True, f"SharePoint item created with ID {item_id}; Power Automate should trigger."
            else:
                print(f"[SharePoint] Response received without item ID", file=sys.stderr)
                print(f"[SharePoint] Response: {result.stdout[:200]}", file=sys.stderr)
                return False, "SharePoint responded, but no list item ID was returned."
        else:
            print(f"[SharePoint] Failed to create item (return code: {result.returncode})", file=sys.stderr)
            if result.stderr:
                print(f"[SharePoint] Error output: {result.stderr[:300]}", file=sys.stderr)
            if result.stdout:
                print(f"[SharePoint] Response: {result.stdout[:300]}", file=sys.stderr)
            return False, "SharePoint list handoff failed. Set SKILLDROP_FLOW_URL to a Power Automate HTTP trigger for reliable local demos."
                
    except Exception as e:
        print(f"[SharePoint] Exception: {str(e)}", file=sys.stderr)
        return False, f"SharePoint list handoff failed: {str(e)}"

def run_server(port=8764):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SkillDropHandler)
    print(f"\n╔════════════════════════════════════════════════════════════╗", file=sys.stderr)
    print(f"║        SkillDrop Proxy Server Active                       ║", file=sys.stderr)
    print(f"║  Listening on http://127.0.0.1:{port}                        ║", file=sys.stderr)
    if FLOW_ENDPOINT:
        print(f"║  Sandbox → Proxy → Power Automate HTTP trigger → Teams   ║", file=sys.stderr)
    else:
        print(f"║  No SKILLDROP_FLOW_URL set; SharePoint fallback enabled  ║", file=sys.stderr)
    print(f"╚════════════════════════════════════════════════════════════╝\n", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[SkillDrop Proxy] Shutting down...", file=sys.stderr)
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
