import os
from dotenv import load_dotenv
import requests

load_dotenv()


intercom_access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

headers = {
    "Intercom-Version": "2.9",
    "accept": "application/json",
    "authorization": f"Bearer {intercom_access_token}"
}

print("="*60)
print("GETTING ALL TICKET TYPES AND THEIR ATTRIBUTES")
print("="*60)

url = "https://api.intercom.io/ticket_types"
response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)

if response.status_code == 200:
    import json
    ticket_types_data = json.loads(response.text)
    
    print("\n📋 TICKET TYPES SUMMARY:")
    print("-" * 40)
    
    for ticket_type in ticket_types_data.get("data", []):
        print(f"🎫 Ticket Type: {ticket_type['name']}")
        print(f"   ID: {ticket_type['id']}")
        print(f"   Icon: {ticket_type['icon']}")
        print(f"   Internal: {ticket_type['is_internal']}")
        print(f"   Created: {ticket_type['created_at']}")
        
        # Show attributes for this ticket type
        attributes = ticket_type.get("ticket_type_attributes", {}).get("data", [])
        print(f"   📝 Attributes ({len(attributes)}):")
        
        for attr in attributes:
            attr_type = attr['data_type']
            required = "✅ Required" if attr['required_to_create'] else "⚪ Optional"
            default = "🔧 Default" if attr.get('default', False) else "👤 Custom"
            
            print(f"      - {attr['name']} ({attr_type}) [{required}] [{default}]")
            
            # Show list options if it's a list type
            if attr_type == "list" and "input_options" in attr:
                list_options = attr["input_options"].get("list_options", [])
                if list_options:
                    options = [opt['label'] for opt in list_options]
                    print(f"        Options: {', '.join(options)}")
        
        print("-" * 40)
else:
    print("Failed to fetch ticket types:", response.text)




print("\n" + "="*60)
print("CREATING NEW TICKET TYPES")
print("="*60)

# Define the ticket types you want to create
ticket_types_to_create = [
    {
        "name": "Quantity Issue",
        "icon": "📊",
        "is_internal": False,
        "description": "Issues related to product quantities, inventory, or stock"
    },
    {
        "name": "Logging Issue", 
        "icon": "📝",
        "is_internal": True,
        "description": "Technical issues related to system logging and monitoring"
    },
    {
        "name": "Other",
        "icon": "❓",
        "is_internal": False,
        "description": "General issues that don't fit other categories"
    }
]

created_ticket_types = []

for ticket_type_data in ticket_types_to_create:
    print(f"\n➡️  Creating '{ticket_type_data['name']}' ticket type...")
    
    create_ticket_type_url = "https://api.intercom.io/ticket_types"
    create_ticket_type_headers = {
        "Intercom-Version": "2.9",
        "accept": "application/json",
        "authorization": f"Bearer {intercom_access_token}",
        "content-type": "application/json"
    }
    
    create_response = requests.post(create_ticket_type_url, headers=create_ticket_type_headers, json=ticket_type_data)
    
    if create_response.status_code == 200:
        response_data = json.loads(create_response.text)
        ticket_type_id = response_data.get("id")
        created_ticket_types.append({
            "name": ticket_type_data['name'],
            "id": ticket_type_id
        })
        print(f"   ✅ Successfully created '{ticket_type_data['name']}' (ID: {ticket_type_id})")
    else:
        print(f"   ❌ Failed to create '{ticket_type_data['name']}': {create_response.status_code}")
        print(f"   Error: {create_response.text}")

print(f"\n📋 Successfully created {len(created_ticket_types)} ticket types:")
for created_type in created_ticket_types:
    print(f"   - {created_type['name']} (ID: {created_type['id']})")

print("\n" + "="*60)
print("CREATING DIFFERENT TYPES OF ATTRIBUTES")
print("="*60)

# Get the ticket type ID (using the first one from the response)
ticket_type_id = "REPLACE_WITH_TICKET_TYPE_ID"  # Replace with your actual ticket type ID

# Example 1: List Attribute (Priority)
print("\n🔸 Creating LIST attribute (Priority)...")
priority_attr_data = {
    "required_to_create": True,
    "required_to_create_for_contacts": False,
    "visible_on_create": True,
    "visible_to_contacts": False,
    "name": "Priority",
    "data_type": "list",
    "list_items": "P1, P2, P3"
}

# Example 2: Text Attribute (Description)
print("🔸 Creating TEXT attribute (Issue Description)...")
description_attr_data = {
    "required_to_create": False,
    "required_to_create_for_contacts": False,
    "visible_on_create": True,
    "visible_to_contacts": True,
    "name": "Issue Description",
    "data_type": "string"
}

# Example 3: Number Attribute (Urgency Score)
print("🔸 Creating NUMBER attribute (Urgency Score)...")
urgency_attr_data = {
    "required_to_create": False,
    "required_to_create_for_contacts": False,
    "visible_on_create": True,
    "visible_to_contacts": False,
    "name": "Urgency Score",
    "data_type": "integer"
}

# Example 4: Date Attribute (Due Date)
print("🔸 Creating DATE attribute (Due Date)...")
date_attr_data = {
    "required_to_create": False,
    "required_to_create_for_contacts": False,
    "visible_on_create": True,
    "visible_to_contacts": True,
    "name": "Due Date",
    "data_type": "date"
}

# Create all attributes
attributes_to_create = [
    ("Priority", priority_attr_data),
    ("Issue Description", description_attr_data),
    ("Urgency Score", urgency_attr_data),
    ("Due Date", date_attr_data)
]

for attr_name, attr_data in attributes_to_create:
    print(f"\n➡️  Creating '{attr_name}' attribute...")
    
    attr_url = f"https://api.intercom.io/ticket_types/{ticket_type_id}/attributes"
    attr_headers = {
        "Intercom-Version": "2.9",
        "accept": "application/json",
        "authorization": f"Bearer {intercom_access_token}",
        "content-type": "application/json"
    }
    
    attr_response = requests.post(attr_url, headers=attr_headers, json=attr_data)
    
    if attr_response.status_code == 200:
        print(f"   ✅ Successfully created '{attr_name}'")
    else:
        print(f"   ❌ Failed to create '{attr_name}': {attr_response.status_code}")
        print(f"   Error: {attr_response.text}")

print("\n" + "="*50)

print("\n" + "="*50)
print("Creating a Test Ticket")
print("="*50)

# Create a test ticket
ticket_url = "https://api.intercom.io/tickets"
ticket_headers = {
    "Intercom-Version": "2.9",
    "accept": "application/json",
    "authorization": f"Bearer {intercom_access_token}",
    "content-type": "application/json"
}
ticket_data = {
    "contacts": [
        {
            "email": "test@example.com"  # Replace with actual test email
        }
    ],
    "ticket_attributes": {
        "Priority": "P1"
    },
    "ticket_type_id": "ticket"  # Replace with your actual ticket type ID
}

ticket_response = requests.post(ticket_url, headers=ticket_headers, json=ticket_data)
print("Ticket Creation - Status Code:", ticket_response.status_code)
print("Ticket Creation - Response:", ticket_response.text)

# Extract ticket ID from the response
ticket_id = None
if ticket_response.status_code == 200:
    import json
    ticket_data_response = json.loads(ticket_response.text)
    ticket_id = ticket_data_response.get("id")
    print(f"Created ticket with ID: {ticket_id}")

print("\n" + "="*50)
print("Adding Reply to Ticket")
print("="*50)

if ticket_id:
    reply_url = f"https://api.intercom.io/tickets/{ticket_id}/reply"
    
    reply_payload = {
        "message_type": "note",  # Changed from "comment" to "note" 
        "type": "admin",
        "admin_id": os.getenv("INTERCOM_ADMIN_ID"),  # Your admin ID from environment
        "body": "hello world - burnt people"
    }
    
    reply_headers = {
        "Content-Type": "application/json",
        "Intercom-Version": "2.9",  # Using consistent version
        "Authorization": f"Bearer {intercom_access_token}"  # Using your actual token
    }
    
    reply_response = requests.post(reply_url, json=reply_payload, headers=reply_headers)
    print("Reply Creation - Status Code:", reply_response.status_code)
    print("Reply Creation - Response:", reply_response.text)
else:
    print("Could not create reply - no ticket ID available")