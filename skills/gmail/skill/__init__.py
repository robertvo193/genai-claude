"""
Gmail Skill
Send and receive emails via Gmail API with OAuth2 authentication.
"""

SKILL_INFO = {
    "name": "gmail",
    "description": "Send and receive emails via Gmail API with OAuth2 authentication",
    "version": "1.0.0",
    "author": "Claude Skills",
    "main_function": "authenticate",
}

from .gmail_client import (
    authenticate,
    send_email,
    has_recent_reply,
    find_thread_id,
    get_thread_messages,
    search_messages,
    get_message
)

__all__ = [
    'authenticate',
    'send_email',
    'has_recent_reply',
    'find_thread_id',
    'get_thread_messages',
    'search_messages',
    'get_message'
]
