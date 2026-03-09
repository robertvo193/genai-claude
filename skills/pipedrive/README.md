# Pipedrive Skill

Direct CRUD operations for Pipedrive CRM objects.

## Features

- **Deals**: Create, Read, Update, Delete, List
- **Persons**: Create, Read, Update, Delete, List
- **Organizations**: Create, Read, Update, Delete, List
- **Activities**: Create, Read, Update, Delete, List
- **Notes**: Create, Read, Delete, List
- **Products**: Create, Read, Update, Delete, List

## Setup

1. Get your Pipedrive API token:
   - Log in to Pipedrive
   - Go to Settings → Personal preferences → API
   - Copy your API token

2. Set up authentication:
   ```bash
   # Option 1: Environment variable
   export PIPEDRIVE_API_TOKEN="your_token_here"
   export PIPEDRIVE_COMPANY_URL="https://yourcompany.pipedrive.com"

   # Option 2: Create token file (recommended)
   echo "your_token_here" > .claude/skills/pipedrive/token
   echo "https://yourcompany.pipedrive.com" > .claude/skills/pipedrive/company_url
   ```

3. Install dependencies:
   ```bash
   cd .claude/skills/pipedrive
   pip install -r requirements.txt
   ```

## Usage Examples

```bash
# List all deals
/pipedrive list-deals

# Get a specific deal
/pipedrive get-deal --id 123

# Create a new deal
/pipedrive create-deal --title "New Deal" --value 10000 --currency USD

# Update a deal
/pipedrive update-deal --id 123 --title "Updated Title"

# Delete a deal
/pipedrive delete-deal --id 123

# List all persons
/pipedrive list-persons

# Create a person
/pipedrive create-person --name "John Doe" --email john@example.com

# List all organizations
/pipedrive list-organizations

# Create an organization
/pipedrive create-organization --name "Acme Corp" --website "https://acme.com"

# List activities
/pipedrive list-activities

# Create an activity
/pipedrive create-activity --subject "Follow up" --type call --deal-id 123
```

## Commands

### Deals
- `list-deals` - List all deals with optional filters
- `get-deal` - Get specific deal by ID
- `create-deal` - Create new deal
- `update-deal` - Update existing deal
- `delete-deal` - Delete deal

### Persons
- `list-persons` - List all persons
- `get-person` - Get specific person by ID
- `create-person` - Create new person
- `update-person` - Update existing person
- `delete-person` - Delete person

### Organizations
- `list-organizations` - List all organizations
- `get-organization` - Get specific organization by ID
- `create-organization` - Create new organization
- `update-organization` - Update existing organization
- `delete-organization` - Delete organization

### Activities
- `list-activities` - List all activities
- `get-activity` - Get specific activity by ID
- `create-activity` - Create new activity
- `update-activity` - Update existing activity
- `delete-activity` - Delete activity

### Notes
- `list-notes` - List all notes
- `get-note` - Get specific note by ID
- `create-note` - Create new note
- `delete-note` - Delete note

### Products
- `list-products` - List all products
- `get-product` - Get specific product by ID
- `create-product` - Create new product
- `update-product` - Update existing product
- `delete-product` - Delete product
