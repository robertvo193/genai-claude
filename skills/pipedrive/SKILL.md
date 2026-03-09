---
name: pipedrive
description: Direct CRUD operations for Pipedrive CRM objects including leads, deals, persons, organizations, activities, notes, and products
argument-hint: "<command> [options]"
---

# Pipedrive

Direct CRUD operations for Pipedrive CRM objects using REST API.

## Commands

### Setup

**setup**
Show setup status and instructions for configuring the skill.
```bash
/pipedrive setup
```

**set-token**
Set your Pipedrive API token.
```bash
/pipedrive set-token YOUR_API_TOKEN_HERE
```

### Leads

**list-leads**
List all leads with optional filters and sorting.
```bash
/pipedrive list-leads [--status <status>] [--label <label>] [--person-id <id>] [--org-id <id>] [--sort-by <field>] [--sort-order <asc|desc>] [--limit <n>]
```

**get-lead**
Get specific lead by ID.
```bash
/pipedrive get-lead --id <lead_id>
```

**create-lead**
Create new lead.
```bash
/pipedrive create-lead --title <title> [--person-id <id>] [--org-id <id>] [--value <value>] [--currency <currency>] [--expected-close-date <date>] [--probability <0-100>] [--label <label>]
```

**update-lead**
Update existing lead.
```bash
/pipedrive update-lead --id <lead_id> [--title <title>] [--person-id <id>] [--org-id <id>] [--value <value>] [--currency <currency>] [--expected-close-date <date>] [--probability <0-100>] [--label <label>] [--status <status>]
```

**delete-lead**
Delete lead.
```bash
/pipedrive delete-lead --id <lead_id>
```

### Deals

**list-deals**
List all deals with optional filters.
```bash
/pipedrive list-deals [--status <status>] [--stage-id <id>] [--user-id <id>] [--limit <n>]
```

**get-deal**
Get specific deal by ID.
```bash
/pipedrive get-deal --id <deal_id>
```

**create-deal**
Create new deal.
```bash
/pipedrive create-deal --title <title> [--value <value>] [--currency <currency>] [--person-id <id>] [--org-id <id>] [--stage-id <id>] [--probability <0-100>]
```

**update-deal**
Update existing deal.
```bash
/pipedrive update-deal --id <deal_id> [--title <title>] [--value <value>] [--currency <currency>] [--stage-id <id>] [--status <status>] [--probability <0-100>]
```

**delete-deal**
Delete deal.
```bash
/pipedrive delete-deal --id <deal_id>
```

### Persons

**list-persons**
List all persons with optional filters.
```bash
/pipedrive list-persons [--name <name>] [--email <email>] [--org-id <id>] [--limit <n>]
```

**get-person**
Get specific person by ID.
```bash
/pipedrive get-person --id <person_id>
```

**create-person**
Create new person.
```bash
/pipedrive create-person --name <name> [--email <email>] [--phone <phone>] [--org-id <id>] [--title <title>]
```

**update-person**
Update existing person.
```bash
/pipedrive update-person --id <person_id> [--name <name>] [--email <email>] [--phone <phone>] [--org-id <id>] [--title <title>]
```

**delete-person**
Delete person.
```bash
/pipedrive delete-person --id <person_id>
```

### Organizations

**list-organizations**
List all organizations with optional filters.
```bash
/pipedrive list-organizations [--name <name>] [--limit <n>]
```

**get-organization**
Get specific organization by ID.
```bash
/pipedrive get-organization --id <org_id>
```

**create-organization**
Create new organization.
```bash
/pipedrive create-organization --name <name> [--website <url>] [--industry <industry>] [--address <address>]
```

**update-organization**
Update existing organization.
```bash
/pipedrive update-organization --id <org_id> [--name <name>] [--website <url>] [--industry <industry>] [--address <address>]
```

**delete-organization**
Delete organization.
```bash
/pipedrive delete-organization --id <org_id>
```

### Activities

**list-activities**
List all activities with optional filters.
```bash
/pipedrive list-activities [--type <type>] [--deal-id <id>] [--person-id <id>] [--limit <n>]
```

**get-activity**
Get specific activity by ID.
```bash
/pipedrive get-activity --id <activity_id>
```

**create-activity**
Create new activity.
```bash
/pipedrive create-activity --subject <subject> --type <type> [--deal-id <id>] [--person-id <id>] [--note <note>] [--due-date <date>]
```

**update-activity**
Update existing activity.
```bash
/pipedrive update-activity --id <activity_id> [--subject <subject>] [--type <type>] [--status <status>] [--note <note>]
```

**delete-activity**
Delete activity.
```bash
/pipedrive delete-activity --id <activity_id>
```

### Notes

**list-notes**
List all notes with optional filters.
```bash
/pipedrive list-notes [--deal-id <id>] [--person-id <id>] [--org-id <id>] [--limit <n>]
```

**get-note**
Get specific note by ID.
```bash
/pipedrive get-note --id <note_id>
```

**create-note**
Create new note.
```bash
/pipedrive create-note --content <content> [--deal-id <id>] [--person-id <id>] [--org-id <id>]
```

**delete-note**
Delete note.
```bash
/pipedrive delete-note --id <note_id>
```

### Products

**list-products**
List all products with optional filters.
```bash
/pipedrive list-products [--name <name>] [--code <code>] [--limit <n>]
```

**get-product**
Get specific product by ID.
```bash
/pipedrive get-product --id <product_id>
```

**create-product**
Create new product.
```bash
/pipedrive create-product --name <name> [--code <code>] [--price <price>] [--currency <currency>]
```

**update-product**
Update existing product.
```bash
/pipedrive update-product --id <product_id> [--name <name>] [--code <code>] [--price <price>] [--currency <currency>]
```

**delete-product**
Delete product.
```bash
/pipedrive delete-product --id <product_id>
```

## Configuration

The skill uses the following configuration (from environment variables or files):

- **PIPEDRIVE_API_TOKEN**: Your Pipedrive API token (required)
- **PIPEDRIVE_COMPANY_URL**: Your Pipedrive company URL (e.g., https://yourcompany.pipedrive.com) (required)

Or create these files in `.claude/skills/pipedrive/`:
- `token`: Contains your API token
- `company_url`: Contains your company URL
