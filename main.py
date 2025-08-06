# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import requests

load_dotenv()


intercom_access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

if not intercom_access_token:
    print(f"❌ Error: INTERCOM_ACCESS_TOKEN not found in environment variables")
    print("Please create a .env file with: INTERCOM_ACCESS_TOKEN=your_token")
    exit(1)

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
ticket_type_id = "2752399"  # Replace with your actual ticket type ID

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
            "email": "alex@theburntapp.com"  # Replace with actual test email
        }
    ],
    "ticket_attributes": {
        "Priority": "P1"
    },
    "ticket_type_id": "2752399"  # Replace with your actual ticket type ID
}

ticket_response = requests.post(ticket_url, headers=ticket_headers, json=ticket_data)
print("Ticket Creation - Status Code:", ticket_response.status_code)
print("Ticket Creation - Response:", ticket_response.text)

# Extract ticket ID and contact ID from the response
ticket_id = None
contact_id = "8989"
if ticket_response.status_code == 200:
    import json
    ticket_data_response = json.loads(ticket_response.text)
    ticket_id = ticket_data_response.get("id")
    
  

print("\n" + "="*60)
print("USER-SUPPORT COMMUNICATION")
print("="*60)

def get_current_admin():
    """Get the current admin's information from the API"""
    admin_url = "https://api.intercom.io/me"
    admin_headers = {
        "Intercom-Version": "2.9",
        "Authorization": f"Bearer {intercom_access_token}"
    }
    
    response = requests.get(admin_url, headers=admin_headers)
    if response.status_code == 200:
        admin_data = json.loads(response.text)
        admin_id = admin_data.get("id")
        admin_name = admin_data.get("name", "Unknown")
        admin_email = admin_data.get("email", "Unknown")
        
        print(f"📋 Current Admin Info:")
        print(f"   ID: {admin_id}")
        print(f"   Name: {admin_name}")
        print(f"   Email: {admin_email}")
        
        return admin_id
    else:
        print(f"❌ Failed to get admin info: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def add_support_reply(ticket_id, admin_id, message):
    """Add a support staff reply to a ticket (visible to user)"""
    reply_url = f"https://api.intercom.io/tickets/{ticket_id}/reply"
    
    reply_payload = {
        "message_type": "note",  # Visible to user
        "type": "admin",
        "admin_id": admin_id,
        "body": message
    }
    
    reply_headers = {
        "Content-Type": "application/json",
        "Intercom-Version": "2.9",
        "Authorization": f"Bearer {intercom_access_token}"
    }
    
    response = requests.post(reply_url, json=reply_payload, headers=reply_headers)
    return response

def add_user_reply(ticket_id, contact_id, message):
    """Add a user reply to a ticket"""
    reply_url = f"https://api.intercom.io/conversations/{ticket_id}/reply"
    
    reply_payload = {
        "type": "user",
        "user_id": contact_id,
        "body": message,
        "message_type": "comment"
    } 
    
    reply_headers = {
        "Content-Type": "application/json",
        "Intercom-Version": "2.9",
        "Authorization": f"Bearer {intercom_access_token}"
    }
    
    response = requests.post(reply_url, json=reply_payload, headers=reply_headers)
    return response

def get_ticket_conversation(ticket_id):
    """Retrieve the conversation for a ticket"""
    ticket_url = f"https://api.intercom.io/tickets/{ticket_id}"
    ticket_headers = {
        "Intercom-Version": "2.9",
        "Authorization": f"Bearer {intercom_access_token}"
    } 
    
    response = requests.get(ticket_url, headers=ticket_headers)
    return response

def create_or_update_user(user_email):
    """Create or update a user in Intercom"""
    user_url = "https://api.intercom.io/contacts"
    user_headers = {
        "Content-Type": "application/json",
        "Intercom-Version": "2.9",
        "Authorization": f"Bearer {intercom_access_token}"
    }
    
    user_payload = {
        "role": "user",
        "email": user_email
    }
    
    response = requests.post(user_url, json=user_payload, headers=user_headers)
    return response

def create_user_conversation(user_email, initial_message):
    """Create a new conversation started by a user"""
    conversation_url = "https://api.intercom.io/conversations"
    conversation_headers = {
        "Content-Type": "application/json",
        "Intercom-Version": "2.9", 
        "Authorization": f"Bearer {intercom_access_token}"
    }
    
    conversation_payload = {
        "from": {
            "type": "user",
            "email": user_email
        },
        "body": initial_message
    }
    
    response = requests.post(conversation_url, json=conversation_payload, headers=conversation_headers)
    return response

def display_conversation(conversation_data):
    """Display the conversation"""
    print(f"\n📋 Conversation #{conversation_data.get('id')}")
    print(f"   Status: {conversation_data.get('state', 'N/A')}")
    
    # Display contacts
    contacts = conversation_data.get('contacts', {}).get('contacts', [])
    if contacts:
        print(f"   👤 User: {contacts[0].get('email', 'N/A')}")
    
    # Display conversation parts
    conversation_parts = conversation_data.get('conversation_parts', {}).get('conversation_parts', [])
    if conversation_parts:
        print(f"\n💬 Conversation:")
        print("-" * 40)
        
        for part in conversation_parts:
            author = part.get('author', {})
            author_type = author.get('type', 'unknown')
            author_name = author.get('name', 'Unknown')
            body = part.get('body', 'No content')
            
            # Show who sent the message
            if author_type == "user":
                print(f"👤 User ({author_name}): {body}")
            else:
                print(f"👨‍💼 Support ({author_name}): {body}")
            print()

def workflow_standalone_conversation(admin_id):
    """Workflow 1: User starts a standalone conversation"""
    print("\n🔸 WORKFLOW 1: Standalone Conversation")
    
    # Create/ensure user exists
    print("\n➡️  Creating user...")
    user_email = "user_email"
    user_response = create_or_update_user(user_email)
    if user_response.status_code in [200, 201]:
        print(f"   ✅ User created/updated: {user_email}")
    else:
        print(f"   ⚠️  User creation response: {user_response.status_code}")
    
    # User creates conversation
    print("\n➡️  User starting conversation...")
    conversation_response = create_user_conversation(
        user_email,
        "Hi, I need help with my account. I can't access my dashboard."
    )
    
    if conversation_response.status_code == 200:
        conversation_data = json.loads(conversation_response.text)
        conversation_id = conversation_data.get("id")
        print(f"   ✅ Conversation created: {conversation_id}")
        
        # Support replies
        print("\n➡️  Support staff replying...")
        support_reply_url = f"https://api.intercom.io/conversations/{conversation_id}/reply"
        support_reply_payload = {
            "type": "admin",
            "admin_id": admin_id,
            "message_type": "comment",
            "body": "Hello! I'm here to help with your dashboard access issue. Can you tell me what error message you're seeing?"
        }
        support_reply_headers = {
            "Content-Type": "application/json",
            "Intercom-Version": "2.9",
            "Authorization": f"Bearer {intercom_access_token}"
        }
        
        support_response = requests.post(support_reply_url, json=support_reply_payload, headers=support_reply_headers)
        if support_response.status_code == 200:
            print("   ✅ Support reply sent successfully")
        else:
            print(f"   ❌ Support reply failed: {support_response.status_code}")
            print(f"   Error: {support_response.text}")
        
        # Display conversation
        print("\n➡️  Retrieving conversation...")
        get_conversation_url = f"https://api.intercom.io/conversations/{conversation_id}"
        get_conversation_headers = {
            "Intercom-Version": "2.9",
            "Authorization": f"Bearer {intercom_access_token}"
        }
        
        get_response = requests.get(get_conversation_url, headers=get_conversation_headers)
        if get_response.status_code == 200:
            full_conversation_data = json.loads(get_response.text)
            display_conversation(full_conversation_data)
        else:
            print(f"   ❌ Failed to retrieve conversation: {get_response.status_code}")
    else:
        print(f"   ❌ Conversation creation failed: {conversation_response.status_code}")
        print(f"   Error: {conversation_response.text}")

def workflow_ticket_to_conversation(admin_id, ticket_id):
    """Workflow 2: Start with ticket, then create conversation"""
    print("\n🔸 WORKFLOW 2: Ticket-Based Conversation")
    
    if ticket_id:
        # Use the ticket as basis for conversation
        print(f"\n➡️  Using existing ticket: {ticket_id}")
        
        # Add admin reply to ticket (which might create conversation)
        print("\n➡️  Support staff replying to ticket...")
        support_response = add_support_reply(
            ticket_id,
            admin_id,
            "Thank you for creating this ticket. I've reviewed your priority issue and I'm here to help resolve it."
        )
        
        if support_response.status_code == 200:
            print("   ✅ Support reply sent to ticket")
            
            # Try to get the conversation associated with the ticket
            print("\n➡️  Retrieving ticket conversation...")
            conversation_response = get_ticket_conversation(ticket_id)
            if conversation_response.status_code == 200:
                ticket_data = json.loads(conversation_response.text)
                print(f"   📋 Ticket #{ticket_data.get('id')}")
                
                # Display any conversation parts
                conversation_parts = ticket_data.get('conversation_parts', {}).get('conversation_parts', [])
                if conversation_parts:
                    print(f"   💬 Found {len(conversation_parts)} conversation parts")
                    display_conversation(ticket_data)
                else:
                    print("   📝 No conversation parts found - this is a ticket-only interaction")
            else:
                print(f"   ❌ Failed to retrieve ticket: {conversation_response.status_code}")
        else:
            print(f"   ❌ Support reply failed: {support_response.status_code}")
            print(f"   Error: {support_response.text}")
    else:
        print("   ❌ No ticket ID available")

# Communication workflow selector
print("\n🔸 Getting Admin Information...")
admin_id = get_current_admin()

if admin_id:
    print("\n" + "="*60)
    print("COMMUNICATION WORKFLOWS")
    print("="*60)
    
    print("\nSelect workflow:")
    print("1. Standalone Conversation (user starts chat)")
    print("2. Ticket-based Conversation (ticket → replies)")
    print("3. Both workflows")
    
    # For demo, run both workflows
    choice = "3"  # You can change this to "1" or "2" to run specific workflows
    
    if choice in ["1", "3"]:
        workflow_standalone_conversation(admin_id)
    
    if choice in ["2", "3"]:
        workflow_ticket_to_conversation(admin_id, ticket_id)
        
else:
    print("   ❌ Could not get admin ID - communication demo skipped")

print("\n" + "="*60)
print("COMMUNICATION SETUP COMPLETE")
print("="*60)
print("✅ Basic communication features implemented:")
print("   • Users can reply to tickets")  
print("   • Support staff can respond to users")
print("   • View full conversation history")
print("   • Auto-retrieve admin ID from API")
print("\n💡 No additional setup required - uses your access token to get admin info!")