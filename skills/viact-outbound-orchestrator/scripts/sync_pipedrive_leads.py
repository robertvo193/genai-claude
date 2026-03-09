#!/usr/bin/env python3
"""
Sync Pipedrive Leads to Google Sheet
Fetches latest leads from Pipedrive and updates the orchestrator sheet.
"""

import subprocess
import sys
import os


def sync_pipedrive_leads(limit: int = 10) -> dict:
    """
    Sync Pipedrive leads to the orchestrator Google Sheet.

    Fetches the N newest leads from Pipedrive and returns lead data.

    Args:
        limit: Number of leads to fetch (default: 10)

    Returns:
        Dictionary with leads data
    """
    # Get the path to pipedrive skill
    pipedrive_skill_dir = os.path.expanduser("~/.claude/skills/pipedrive")
    if not os.path.exists(pipedrive_skill_dir):
        # Try project-relative path
        pipedrive_skill_dir = os.path.join(os.path.dirname(__file__), "..", "pipedrive")
        if not os.path.exists(pipedrive_skill_dir):
            print(f"❌ Pipedrive skill not found at expected locations")
            return {"error": "Pipedrive skill not found"}

    pipedrive_script = os.path.join(pipedrive_skill_dir, "scripts", "pipedrive.py")

    if not os.path.exists(pipedrive_script):
        print(f"❌ Pipedrive script not found at {pipedrive_script}")
        return {"error": "Pipedrive script not found"}

    # Call pipedrive to list leads (sorted by most recent)
    cmd = [
        "python3",
        pipedrive_script,
        "list-leads",
        "--sort-by", "update_time",
        "--sort-order", "desc",
        "--limit", str(limit)
    ]

    print(f"🔍 Syncing leads from Pipedrive (top {limit})...")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=os.getcwd()
        )

        if result.returncode != 0:
            print(f"❌ Error fetching leads: {result.stderr}")
            return {"error": str(result.stderr)}

        # Parse the JSON output
        import json
        output = result.stdout.strip()

        # Find the JSON array in the output
        start_idx = output.find("[")
        if start_idx == -1:
            print(f"❌ Could not parse Pipedrive output")
            return {"error": "Could not parse output"}

        end_idx = output.rfind("]")
        if end_idx == -1:
            print(f"❌ Could not parse Pipedrive output")
            return {"error": "Could not parse output"}

        json_str = output[start_idx + 1:end_idx]
        leads = json.loads(json_str)

        if not isinstance(leads, list):
            print(f"❌ Expected list of leads, got: {type(leads)}")
            return {"error": "Expected list of leads"}

        print(f"✅ Fetched {len(leads)} leads from Pipedrive")

        # Transform to lead data structure for orchestrator
        lead_data = {
            "leads": [],
            "metadata": {
                "total_fetched": len(leads),
                "limit": limit,
                "source": "pipedrive"
            }
        }

        for lead in leads:
            # Map Pipedrive lead fields to orchestrator fields
            lead_info = {
                "lead_id": str(lead.get("id", "")),
                "lead_name": lead.get("title", ""),
                "person_id": str(lead.get("person_id", "")) if lead.get("person_id") else "",
                "org_id": str(lead.get("organization_id", "")) if lead.get("organization_id") else "",
                "add_time": lead.get("add_time", ""),
                "update_time": lead.get("update_time", ""),
                "value": str(lead.get("value", 0)) if lead.get("value") else "",
                "currency": lead.get("currency", ""),
                "expected_close_date": lead.get("expected_close_date", ""),
                "owner_id": str(lead.get("owner_id", "")) if lead.get("owner_id") else "",
                "source": "pipedrive",
            }

            lead_data["leads"].append(lead_info)

        return lead_data

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Sync Pipedrive Leads to Google Sheet')
    parser.add_argument('--limit', type=int, default=10, help='Number of leads to fetch (default: 10)')

    args = parser.parse_args()

    result = sync_pipedrive_leads(limit=args.limit)

    if "error" in result:
        print(f"❌ Failed to sync leads")
        sys.exit(1)

    # Output summary
    metadata = result.get("metadata", {})
    leads = result.get("leads", [])

    print("=" * 50)
    print(f"📊 Total Leads Fetched: {metadata.get('total_fetched', 0)}")
    print(f"📤 Limit Requested: {metadata.get('limit', 0)}")
    print(f"📋 Leads Returned: {len(leads)}")
    print("=" * 50)

    # Print summary for each lead
    for i, lead in enumerate(leads, 1):
        print(f"\n   {i}. {lead.get('lead_name', 'N/A')}")

    return result


if __name__ == '__main__':
    main()
