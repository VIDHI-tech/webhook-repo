from flask import Blueprint, request, jsonify
from datetime import datetime

# Create the webhook Blueprint
webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

def format_timestamp(timestamp):
    # Format the timestamp as "1st April 2021 - 9:30 PM UTC"
    return timestamp.strftime("%d %B %Y - %I:%M %p UTC")

def format_webhook_data(event_type, data):
    timestamp = format_timestamp(data['timestamp'])
    
    if event_type == "PUSH":
        return f"{data['author']} pushed to {data['to_branch']} on {timestamp}"
    
    elif event_type == "PR_OPENED":
        return f"{data['author']} submitted a pull request from {data['from_branch']} to {data['to_branch']} on {timestamp}"
    
    elif event_type == "MERGE":
        return f"{data['author']} merged branch {data['from_branch']} to {data['to_branch']} on {timestamp}"
    
    return "Unknown event type"

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    
    event_type = "UNKNOWN"
    event_data = {}

    print(data)

    # Handle push event
    if 'ref' in data and 'commits' in data:
        event_type = "PUSH"
        event_data = {
            "author": data['pusher']['name'],
            "to_branch": data['ref'].split('/')[-1],
            "timestamp": datetime.utcnow()  # Use UTC time
        }
    
    # Handle pull request event
    elif 'pull_request' in data:
        event_type = ""
        print(data['action'])

        event_data = {
            "author": data['pull_request']['user']['login'],
            "from_branch": data['pull_request']['head']['ref'],
            "to_branch": data['pull_request']['base']['ref'],
            "timestamp": datetime.utcnow()  # Use UTC time
        }

        if data['action'] == 'opened':
            event_type = "PR_OPENED"
        elif data['action'] == 'closed' and 'merged_by' in data['pull_request']:
            event_type = "MERGE"
        

 
    # Format the event data
    formatted_message = format_webhook_data(event_type, event_data)
    print(formatted_message)
    
    # Insert event into MongoDB
    webhook.collection.insert_one({"event_type": event_type, "message": formatted_message, **event_data})
    
    return jsonify({"message": formatted_message}), 200
