#!/bin/bash

# Quick script to start the incident response web server

echo "=================================="
echo "Starting Incident Response Server"
echo "=================================="
echo ""

cd "$(dirname "$0")"

python3 web_server.py

echo ""
echo "Server stopped."
