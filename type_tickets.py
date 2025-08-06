import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Ticket types to create
ticket_types = [
    "Quantity Issue",
    "Address Issue", 
    "LLM Failure",
    "Other",
    "PO Missing",
    "Logged Wrong",
    "Wrong Delivery Date",
]

# Get access token from environment
intercom_access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

if not intercom_access_token:
    raise ValueError("INTERCOM_ACCESS_TOKEN not found in environment variables")

def get_existing_ticket_types():
    """Get all existing ticket types in the workspace"""
    url = "https://api.intercom.io/ticket_types"
    headers = {
        "Intercom-Version": "2.9",
        "accept": "application/json",
        "authorization": f"Bearer {intercom_access_token}",
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            existing_types = {ticket_type['name']: ticket_type['id'] for ticket_type in data.get('ticket_types', [])}
            return existing_types
        else:
            print(f"❌ Failed to fetch existing ticket types: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        print(f"❌ Error fetching existing ticket types: {str(e)}")
        return {}

def create_ticket_type(ticket_type_name):
    """Create a single ticket type"""
    url = "https://api.intercom.io/ticket_types"
    headers = {
        "Intercom-Version": "2.9",
        "accept": "application/json",
        "authorization": f"Bearer {intercom_access_token}",
        "content-type": "application/json"
    }

    # Define icons and categories for each type
    type_config = {
        "Quantity Issue": {"icon": "📦", "category": "Customer", "description": "Issues with order quantities"},
        "Address Issue": {"icon": "🏠", "category": "Customer", "description": "Delivery address problems"},
        "LLM Failure": {"icon": "🤖", "category": "Back-office", "description": "AI system issues"},
        "Other": {"icon": "❓", "category": "Customer", "description": "General support issues"},
        "PO Missing": {"icon": "📋", "category": "Customer", "description": "Missing purchase order"},
        "Logged Wrong": {"icon": "❌", "category": "Back-office", "description": "Incorrectly logged information"},
        "Wrong Delivery Date": {"icon": "📅", "category": "Customer", "description": "Incorrect delivery date issues"}
    }

    config = type_config.get(ticket_type_name, {"icon": "🎫", "category": "Customer", "description": "Support ticket"})
    
    data = {
        "name": ticket_type_name,
        "description": config["description"],
        "icon": config["icon"],
        "category": config["category"]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Created '{ticket_type_name}' with ID: {result['id']}")
            return result['id']
        else:
            print(f"❌ Failed to create '{ticket_type_name}': {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating '{ticket_type_name}': {str(e)}")
        return None

def main():
    print("🔍 Checking existing ticket types...")
    existing_types = get_existing_ticket_types()
    
    if existing_types:
        print(f"Found {len(existing_types)} existing ticket types:")
        for name, type_id in existing_types.items():
            print(f"  - {name}: {type_id}")
        print()

    # Store all ticket type IDs (existing + new)
    all_ticket_type_ids = existing_types.copy()
    
    print("🚀 Creating missing ticket types...")
    print("=" * 60)
    
    for ticket_type in ticket_types:
        if ticket_type in existing_types:
            print(f"⏭️  Skipping '{ticket_type}' (already exists with ID: {existing_types[ticket_type]})")
        else:
            print(f"📝 Creating ticket type: {ticket_type}")
            ticket_id = create_ticket_type(ticket_type)
            if ticket_id:
                all_ticket_type_ids[ticket_type] = ticket_id
        
        print("-" * 40)

    print("\n" + "=" * 60)
    print("📋 FINAL TICKET TYPE IDs:")
    print("=" * 60)
    
    for name, type_id in all_ticket_type_ids.items():
        print(f"{name}: {type_id}")

    # Save to file for later use
    try:
        with open('ticket_type_ids.json', 'w') as f:
            json.dump(all_ticket_type_ids, f, indent=2)
        print(f"\n💾 IDs saved to 'ticket_type_ids.json'")
    except Exception as e:
        print(f"❌ Failed to save IDs to file: {str(e)}")

    return all_ticket_type_ids

if __name__ == "__main__":
    ticket_type_ids = main()