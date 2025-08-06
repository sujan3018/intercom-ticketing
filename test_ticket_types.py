import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

# Get access token from environment
intercom_access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

if not intercom_access_token:
    raise ValueError("INTERCOM_ACCESS_TOKEN not found in environment variables")

def load_ticket_type_ids():
    """Load ticket type IDs from the previously saved file"""
    try:
        with open('ticket_type_ids.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ ticket_type_ids.json not found. Please run the ticket type creation script first.")
        return {}
    except Exception as e:
        print(f"❌ Error loading ticket type IDs: {str(e)}")
        return {}

def create_ticket(ticket_type_name, ticket_type_id, customer_email="test@example.com") -> int :
    """Create a new ticket"""
    url = "https://api.intercom.io/tickets"
    
    headers = {
        "Intercom-Version": "2.9",
        "accept": "application/json",
        "authorization": f"Bearer {intercom_access_token}",
        "content-type": "application/json"
    }
    
    # Sample ticket data for testing
    data = {
        "contacts": [
            {
                "email": customer_email
            }
        ],
        "ticket_attributes": {
            "_default_title_": f"Test {ticket_type_name}",
            "_default_description_": f"This is a test ticket for {ticket_type_name}"
        },
        "ticket_type_id": ticket_type_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            ticket_id = result['id']
            print(f"✅ Created ticket '{ticket_type_name}' with ID: {ticket_id}")
            return ticket_id
        else:
            print(f"❌ Failed to create ticket '{ticket_type_name}': {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating ticket '{ticket_type_name}': {str(e)}")
        return None


def main():
    print("🔍 Loading ticket type IDs...")
    ticket_type_ids = load_ticket_type_ids()
    
    if not ticket_type_ids:
        print("❌ No ticket type IDs found. Exiting.")
        return
    
    print(f"Found {len(ticket_type_ids)} ticket types:")
    for name, type_id in ticket_type_ids.items():
        print(f"  - {name}: {type_id}")
    print()
    
    print("🎫 Creating test tickets...")
    print("=" * 60)
    
    created_tickets = {}
    
    # Create a ticket for each ticket type
    for ticket_type_name, ticket_type_id in ticket_type_ids.items():
        print(f"📝 Creating ticket for: {ticket_type_name}")
        
        ticket_id = create_ticket(ticket_type_name, ticket_type_id)
        
        if ticket_id:
            created_tickets[ticket_type_name] = ticket_id
            
            # Wait a moment between requests to avoid rate limiting
            time.sleep(1)
            
            # TODO add a reply to the ticket, alex working on this
            # pass in the ticket id into the reply function TODO
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("📋 CREATED TICKETS SUMMARY:")
    print("=" * 60)
    
    for ticket_type, ticket_id in created_tickets.items():
        print(f"{ticket_type}: Ticket ID {ticket_id}")
    
    # Save created ticket IDs for reference
    try:
        with open('created_test_tickets.json', 'w') as f:
            json.dump(created_tickets, f, indent=2)
        print(f"\n💾 Created ticket IDs saved to 'created_test_tickets.json'")
    except Exception as e:
        print(f"❌ Failed to save created ticket IDs: {str(e)}")
    
    print(f"\n🎉 Successfully created {len(created_tickets)} test tickets with replies!")

if __name__ == "__main__":
    main()