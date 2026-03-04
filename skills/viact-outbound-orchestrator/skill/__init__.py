"""
viAct Outbound Orchestrator
Coordinates Google Sheets and Gmail for automated BD outreach.
"""

SKILL_INFO = {
    "name": "viact-outbound-orchestrator",
    "description": "Coordinates Google Sheets and Gmail for automated BD outreach with Human-in-the-Loop approval workflow",
    "version": "1.0.0",
    "author": "Claude Skills",
    "main_functions": ["send_pending_emails", "check_client_replies"],
}

from .orchestrator import (
    send_pending_emails,
    check_client_replies,
    get_status,
    load_config,
    column_letter_to_index,
    extract_column_value,
    extract_lead_data,
    is_approved,
    should_skip,
    update_row_status,
)

__all__ = [
    'send_pending_emails',
    'check_client_replies',
    'get_status',
    'load_config',
    'column_letter_to_index',
    'extract_column_value',
    'extract_lead_data',
    'is_approved',
    'should_skip',
    'update_row_status',
]
