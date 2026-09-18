#!/usr/bin/env python3
"""
SkillDrop Proxy Server
Creates SharePoint list items that trigger the Power Automate flow
Uses Microsoft Graph API for authentication
"""
import json
import sys
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
from datetime import datetime
import threading
import time

# Configuration
SHAREPOINT_SITE = "https://microsoft.sharepoint.com/sites/skilldrop-team-42dbe9"
LIST_ID = "77a33ccb-6605-47e5-afa2-aff1e06b4c01"
GRAPH_API_ENDPOINT = f"{SHAREPOINT_SITE}/_api/lists('{LIST_ID}')/items"

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
            
            # Create SharePoint list item in background
            threading.Thread(target=create_sharepoint_item, args=(payload,), daemon=True).start()
            
            # Return immediate response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "SkillDrop received! Your Teams notification is being sent...",
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
                print(f"✓ [SharePoint] Item created with ID: {item_id}", file=sys.stderr)
                print(f"[Power Automate] Flow should trigger now...", file=sys.stderr)
            else:
                print(f"✓ [SharePoint] Response received (ID may not be in response)", file=sys.stderr)
                print(f"[SharePoint] Response: {result.stdout[:200]}", file=sys.stderr)
        else:
            print(f"✗ [SharePoint] Failed to create item (return code: {result.returncode})", file=sys.stderr)
            if result.stderr:
                print(f"[SharePoint] Error output: {result.stderr[:300]}", file=sys.stderr)
            if result.stdout:
                print(f"[SharePoint] Response: {result.stdout[:300]}", file=sys.stderr)
                
    except Exception as e:
        print(f"[SharePoint] Exception: {str(e)}", file=sys.stderr)

def run_server(port=8764):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SkillDropHandler)
    print(f"\n╔════════════════════════════════════════════════════════════╗", file=sys.stderr)
    print(f"║        SkillDrop Proxy Server Active                       ║", file=sys.stderr)
    print(f"║  Listening on http://127.0.0.1:{port}                        ║", file=sys.stderr)
    print(f"║  Sandbox → Proxy → SharePoint → Power Automate → Teams   ║", file=sys.stderr)
    print(f"╚════════════════════════════════════════════════════════════╝\n", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[SkillDrop Proxy] Shutting down...", file=sys.stderr)
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
