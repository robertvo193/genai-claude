#!/usr/bin/env python3
"""
Pipedrive CRUD Operations
Direct API access to Pipedrive CRM objects.

Usage: python3 pipedrive.py <command> [options]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests


class PipedriveClient:
    """Pipedrive REST API client"""

    def __init__(self, api_token: str, company_url: str):
        self.api_token = api_token
        self.company_url = company_url.rstrip('/')
        self.base_url = f"{self.company_url}/api/v1"
        self.session = requests.Session()
        self.session.params = {'api_token': self.api_token}

    def _request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Any:
        """Make API request"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=data)
            elif method == 'PUT':
                response = self.session.put(url, json=data)
            elif method == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unknown method: {method}")

            response.raise_for_status()
            result = response.json()

            if 'success' in result and not result['success']:
                error = result.get('error', 'Unknown error')
                raise Exception(f"Pipedrive API error: {error}")

            return result.get('data')

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    # ============= DEALS =============

    def list_deals(self, status: Optional[str] = None, stage_id: Optional[int] = None,
                   user_id: Optional[int] = None, limit: Optional[int] = None) -> List[Dict]:
        """List deals"""
        params = {}
        if status:
            params['status'] = status
        if stage_id:
            params['stage_id'] = stage_id
        if user_id:
            params['user_id'] = user_id
        if limit:
            params['limit'] = limit

        return self._request('GET', 'deals', params=params)

    def get_deal(self, deal_id: int) -> Dict:
        """Get specific deal"""
        return self._request('GET', f'deals/{deal_id}')

    def create_deal(self, title: str, value: Optional[float] = None,
                    currency: Optional[str] = None, person_id: Optional[int] = None,
                    org_id: Optional[int] = None, stage_id: Optional[int] = None,
                    probability: Optional[int] = None) -> Dict:
        """Create new deal"""
        data = {'title': title}
        if value is not None:
            data['value'] = value
        if currency:
            data['currency'] = currency
        if person_id:
            data['person_id'] = person_id
        if org_id:
            data['org_id'] = org_id
        if stage_id:
            data['stage_id'] = stage_id
        if probability is not None:
            data['probability'] = probability

        return self._request('POST', 'deals', data=data)

    def update_deal(self, deal_id: int, title: Optional[str] = None,
                    value: Optional[float] = None, currency: Optional[str] = None,
                    stage_id: Optional[int] = None, status: Optional[str] = None,
                    probability: Optional[int] = None) -> Dict:
        """Update deal"""
        data = {}
        if title:
            data['title'] = title
        if value is not None:
            data['value'] = value
        if currency:
            data['currency'] = currency
        if stage_id:
            data['stage_id'] = stage_id
        if status:
            data['status'] = status
        if probability is not None:
            data['probability'] = probability

        return self._request('PUT', f'deals/{deal_id}', data=data)

    def delete_deal(self, deal_id: int) -> Dict:
        """Delete deal"""
        return self._request('DELETE', f'deals/{deal_id}')



    # ============= LEADS =============

    def list_leads(self, status: Optional[str] = None, label: Optional[str] = None,
                  person_id: Optional[int] = None, org_id: Optional[int] = None,
                  sort_by: Optional[str] = None, sort_order: Optional[str] = None,
                  limit: Optional[int] = None) -> List[Dict]:
        """List leads"""
        params = {}
        if status:
            params['status'] = status
        if label:
            params['label'] = label
        if person_id:
            params['person_id'] = person_id
        if org_id:
            params['org_id'] = org_id
        if sort_by:
            params['sort'] = sort_by
        if sort_order:
            params['sort_order'] = sort_order
        if limit:
            params['limit'] = limit

        return self._request('GET', 'leads', params=params)

    def get_lead(self, lead_id: int) -> Dict:
        """Get specific lead"""
        return self._request('GET', f'leads/{lead_id}')

    def create_lead(self, title: str, person_id: Optional[int] = None,
                   org_id: Optional[int] = None, value: Optional[float] = None,
                   currency: Optional[str] = None, expected_close_date: Optional[str] = None,
                   probability: Optional[int] = None, label: Optional[str] = None) -> Dict:
        """Create new lead"""
        data = {'title': title}
        if person_id:
            data['person_id'] = person_id
        if org_id:
            data['org_id'] = org_id
        if value is not None:
            data['value'] = value
        if currency:
            data['currency'] = currency
        if expected_close_date:
            data['expected_close_date'] = expected_close_date
        if probability is not None:
            data['probability'] = probability
        if label:
            data['label'] = label

        return self._request('POST', 'leads', data=data)

    def update_lead(self, lead_id: int, title: Optional[str] = None,
                   person_id: Optional[int] = None, org_id: Optional[int] = None,
                   value: Optional[float] = None, currency: Optional[str] = None,
                   expected_close_date: Optional[str] = None, probability: Optional[int] = None,
                   label: Optional[str] = None, status: Optional[str] = None) -> Dict:
        """Update lead"""
        data = {}
        if title:
            data['title'] = title
        if person_id:
            data['person_id'] = person_id
        if org_id:
            data['org_id'] = org_id
        if value is not None:
            data['value'] = value
        if currency:
            data['currency'] = currency
        if expected_close_date:
            data['expected_close_date'] = expected_close_date
        if probability is not None:
            data['probability'] = probability
        if label:
            data['label'] = label
        if status:
            data['status'] = status

        return self._request('PUT', f'leads/{lead_id}', data=data)

    def delete_lead(self, lead_id: int) -> Dict:
        """Delete lead"""
        return self._request('DELETE', f'leads/{lead_id}')

    # ============= PRODUCTS =============

    def list_products(self, name: Optional[str] = None, code: Optional[str] = None,
                     limit: Optional[int] = None) -> List[Dict]:
        """List products"""
        params = {}
        if name:
            params['term'] = name
        if code:
            params['term'] = code
        if limit:
            params['limit'] = limit

        return self._request('GET', 'products', params=params)

    def get_product(self, product_id: int) -> Dict:
        """Get specific product"""
        return self._request('GET', f'products/{product_id}')

    def create_product(self, name: str, code: Optional[str] = None,
                     price: Optional[float] = None, currency: Optional[str] = None) -> Dict:
        """Create new product"""
        data = {'name': name}
        if code:
            data['code'] = code
        if price is not None:
            data['prices'] = [{'price': price, 'currency': currency or 'USD'}]
        if currency and price is None:
            data['prices'] = [{'price': 0, 'currency': currency}]

        return self._request('POST', 'products', data=data)

    def update_product(self, product_id: int, name: Optional[str] = None,
                      code: Optional[str] = None, price: Optional[float] = None,
                      currency: Optional[str] = None) -> Dict:
        """Update product"""
        data = {}
        if name:
            data['name'] = name
        if code:
            data['code'] = code
        if price is not None:
            data['prices'] = [{'price': price, 'currency': currency or 'USD'}]

        return self._request('PUT', f'products/{product_id}', data=data)

    def delete_product(self, product_id: int) -> Dict:
        """Delete product"""
        return self._request('DELETE', f'products/{product_id}')


def get_credentials() -> tuple:
    """Get API credentials from environment or files"""
    # Try environment variables first
    api_token = os.environ.get('PIPEDRIVE_API_TOKEN')
    company_url = os.environ.get('PIPEDRIVE_COMPANY_URL')

    # Fallback to files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)

    if not api_token:
        token_path = os.path.join(skill_dir, 'token')
        if os.path.exists(token_path):
            with open(token_path, 'r') as f:
                api_token = f.read().strip()

    if not company_url:
        url_path = os.path.join(skill_dir, 'company_url')
        if os.path.exists(url_path):
            with open(url_path, 'r') as f:
                company_url = f.read().strip()

    if not api_token or not company_url:
        print("❌ Error: Pipedrive credentials not found")
        print("\nPlease set up authentication:")
        print("  Option 1: Environment variables")
        print("    export PIPEDRIVE_API_TOKEN='your_token'")
        print("    export PIPEDRIVE_COMPANY_URL='https://yourcompany.pipedrive.com'")
        print("\n  Option 2: Token files")
        print(f"    echo 'your_token' > {skill_dir}/token")
        print(f"    echo 'https://yourcompany.pipedrive.com' > {skill_dir}/company_url")
        sys.exit(1)

    return api_token, company_url


def print_json(data: Any, pretty: bool = True):
    """Print data as JSON"""
    if pretty:
        print(json.dumps(data, indent=2, default=str))
    else:
        print(json.dumps(data, default=str))


def main():
    parser = argparse.ArgumentParser(description='Pipedrive CRUD Operations')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # ============= DEALS =============
    deal_parser = subparsers.add_parser('list-deals', help='List all deals')
    deal_parser.add_argument('--status', help='Filter by status (open, won, lost)')
    deal_parser.add_argument('--stage-id', type=int, help='Filter by stage ID')
    deal_parser.add_argument('--user-id', type=int, help='Filter by user ID')
    deal_parser.add_argument('--limit', type=int, help='Limit number of results')

    get_deal_parser = subparsers.add_parser('get-deal', help='Get specific deal')
    get_deal_parser.add_argument('--id', type=int, required=True, help='Deal ID')

    create_deal_parser = subparsers.add_parser('create-deal', help='Create new deal')
    create_deal_parser.add_argument('--title', required=True, help='Deal title')
    create_deal_parser.add_argument('--value', type=float, help='Deal value')
    create_deal_parser.add_argument('--currency', help='Currency code (e.g., USD)')
    create_deal_parser.add_argument('--person-id', type=int, help='Person ID')
    create_deal_parser.add_argument('--org-id', type=int, help='Organization ID')
    create_deal_parser.add_argument('--stage-id', type=int, help='Stage ID')
    create_deal_parser.add_argument('--probability', type=int, help='Probability (0-100)')

    update_deal_parser = subparsers.add_parser('update-deal', help='Update deal')
    update_deal_parser.add_argument('--id', type=int, required=True, help='Deal ID')
    update_deal_parser.add_argument('--title', help='Deal title')
    update_deal_parser.add_argument('--value', type=float, help='Deal value')
    update_deal_parser.add_argument('--currency', help='Currency code')
    update_deal_parser.add_argument('--stage-id', type=int, help='Stage ID')
    update_deal_parser.add_argument('--status', help='Status (open, won, lost)')
    update_deal_parser.add_argument('--probability', type=int, help='Probability (0-100)')

    delete_deal_parser = subparsers.add_parser('delete-deal', help='Delete deal')
    delete_deal_parser.add_argument('--id', type=int, required=True, help='Deal ID')

    # ============= LEADS =============
    lead_parser = subparsers.add_parser('list-leads', help='List all leads')
    lead_parser.add_argument('--status', help='Filter by status')
    lead_parser.add_argument('--label', help='Filter by label')
    lead_parser.add_argument('--person-id', type=int, help='Filter by person ID')
    lead_parser.add_argument('--org-id', type=int, help='Filter by organization ID')
    lead_parser.add_argument('--limit', type=int, help='Limit number of results')
    lead_parser.add_argument('--sort-by', help='Sort by field (add_time, update_time, etc.)')
    lead_parser.add_argument('--sort-order', choices=['asc', 'desc'], default='desc', help='Sort order (asc or desc, default: desc)')
    get_lead_parser = subparsers.add_parser('get-lead', help='Get specific lead')
    get_lead_parser.add_argument('--id', type=int, required=True, help='Lead ID')

    create_lead_parser = subparsers.add_parser('create-lead', help='Create new lead')
    create_lead_parser.add_argument('--title', required=True, help='Lead title')
    create_lead_parser.add_argument('--person-id', type=int, help='Person ID')
    create_lead_parser.add_argument('--org-id', type=int, help='Organization ID')
    create_lead_parser.add_argument('--value', type=float, help='Lead value')
    create_lead_parser.add_argument('--currency', help='Currency code (e.g., USD)')
    create_lead_parser.add_argument('--expected-close-date', help='Expected close date (YYYY-MM-DD)')
    create_lead_parser.add_argument('--probability', type=int, help='Probability (0-100)')
    create_lead_parser.add_argument('--label', help='Lead label')

    update_lead_parser = subparsers.add_parser('update-lead', help='Update lead')
    update_lead_parser.add_argument('--id', type=int, required=True, help='Lead ID')
    update_lead_parser.add_argument('--title', help='Lead title')
    update_lead_parser.add_argument('--person-id', type=int, help='Person ID')
    update_lead_parser.add_argument('--org-id', type=int, help='Organization ID')
    update_lead_parser.add_argument('--value', type=float, help='Lead value')
    update_lead_parser.add_argument('--currency', help='Currency code')
    update_lead_parser.add_argument('--expected-close-date', help='Expected close date')
    update_lead_parser.add_argument('--probability', type=int, help='Probability (0-100)')
    update_lead_parser.add_argument('--label', help='Lead label')
    update_lead_parser.add_argument('--status', help='Status')

    delete_lead_parser = subparsers.add_parser('delete-lead', help='Delete lead')
    delete_lead_parser.add_argument('--id', type=int, required=True, help='Lead ID')

    # ============= PERSONS =============
    person_parser = subparsers.add_parser('list-persons', help='List all persons')
    person_parser.add_argument('--name', help='Filter by name')
    person_parser.add_argument('--email', help='Filter by email')
    person_parser.add_argument('--org-id', type=int, help='Filter by organization ID')
    person_parser.add_argument('--limit', type=int, help='Limit number of results')

    get_person_parser = subparsers.add_parser('get-person', help='Get specific person')
    get_person_parser.add_argument('--id', type=int, required=True, help='Person ID')

    create_person_parser = subparsers.add_parser('create-person', help='Create new person')
    create_person_parser.add_argument('--name', required=True, help='Person name')
    create_person_parser.add_argument('--email', help='Email address')
    create_person_parser.add_argument('--phone', help='Phone number')
    create_person_parser.add_argument('--org-id', type=int, help='Organization ID')
    create_person_parser.add_argument('--title', help='Job title')

    update_person_parser = subparsers.add_parser('update-person', help='Update person')
    update_person_parser.add_argument('--id', type=int, required=True, help='Person ID')
    update_person_parser.add_argument('--name', help='Person name')
    update_person_parser.add_argument('--email', help='Email address')
    update_person_parser.add_argument('--phone', help='Phone number')
    update_person_parser.add_argument('--org-id', type=int, help='Organization ID')
    update_person_parser.add_argument('--title', help='Job title')

    delete_person_parser = subparsers.add_parser('delete-person', help='Delete person')
    delete_person_parser.add_argument('--id', type=int, required=True, help='Person ID')

    # ============= ORGANIZATIONS =============
    org_parser = subparsers.add_parser('list-organizations', help='List all organizations')
    org_parser.add_argument('--name', help='Filter by name')
    org_parser.add_argument('--limit', type=int, help='Limit number of results')

    get_org_parser = subparsers.add_parser('get-organization', help='Get specific organization')
    get_org_parser.add_argument('--id', type=int, required=True, help='Organization ID')

    create_org_parser = subparsers.add_parser('create-organization', help='Create new organization')
    create_org_parser.add_argument('--name', required=True, help='Organization name')
    create_org_parser.add_argument('--website', help='Website URL')
    create_org_parser.add_argument('--industry', help='Industry')
    create_org_parser.add_argument('--address', help='Address')

    update_org_parser = subparsers.add_parser('update-organization', help='Update organization')
    update_org_parser.add_argument('--id', type=int, required=True, help='Organization ID')
    update_org_parser.add_argument('--name', help='Organization name')
    update_org_parser.add_argument('--website', help='Website URL')
    update_org_parser.add_argument('--industry', help='Industry')
    update_org_parser.add_argument('--address', help='Address')

    delete_org_parser = subparsers.add_parser('delete-organization', help='Delete organization')
    delete_org_parser.add_argument('--id', type=int, required=True, help='Organization ID')

    # ============= ACTIVITIES =============
    activity_parser = subparsers.add_parser('list-activities', help='List all activities')
    activity_parser.add_argument('--type', help='Filter by activity type')
    activity_parser.add_argument('--deal-id', type=int, help='Filter by deal ID')
    activity_parser.add_argument('--person-id', type=int, help='Filter by person ID')
    activity_parser.add_argument('--limit', type=int, help='Limit number of results')

    get_activity_parser = subparsers.add_parser('get-activity', help='Get specific activity')
    get_activity_parser.add_argument('--id', type=int, required=True, help='Activity ID')

    create_activity_parser = subparsers.add_parser('create-activity', help='Create new activity')
    create_activity_parser.add_argument('--subject', required=True, help='Activity subject')
    create_activity_parser.add_argument('--type', required=True, help='Activity type (call, meeting, task, etc.)')
    create_activity_parser.add_argument('--deal-id', type=int, help='Deal ID')
    create_activity_parser.add_argument('--person-id', type=int, help='Person ID')
    create_activity_parser.add_argument('--note', help='Activity note')
    create_activity_parser.add_argument('--due-date', help='Due date (YYYY-MM-DD)')

    update_activity_parser = subparsers.add_parser('update-activity', help='Update activity')
    update_activity_parser.add_argument('--id', type=int, required=True, help='Activity ID')
    update_activity_parser.add_argument('--subject', help='Activity subject')
    update_activity_parser.add_argument('--type', help='Activity type')
    update_activity_parser.add_argument('--status', help='Status (done, planned, etc.)')
    update_activity_parser.add_argument('--note', help='Activity note')

    delete_activity_parser = subparsers.add_parser('delete-activity', help='Delete activity')
    delete_activity_parser.add_argument('--id', type=int, required=True, help='Activity ID')

    # ============= NOTES =============
    note_parser = subparsers.add_parser('list-notes', help='List all notes')
    note_parser.add_argument('--deal-id', type=int, help='Filter by deal ID')
    note_parser.add_argument('--person-id', type=int, help='Filter by person ID')
    note_parser.add_argument('--org-id', type=int, help='Filter by organization ID')
    note_parser.add_argument('--limit', type=int, help='Limit number of results')

    get_note_parser = subparsers.add_parser('get-note', help='Get specific note')
    get_note_parser.add_argument('--id', type=int, required=True, help='Note ID')

    create_note_parser = subparsers.add_parser('create-note', help='Create new note')
    create_note_parser.add_argument('--content', required=True, help='Note content')
    create_note_parser.add_argument('--deal-id', type=int, help='Deal ID')
    create_note_parser.add_argument('--person-id', type=int, help='Person ID')
    create_note_parser.add_argument('--org-id', type=int, help='Organization ID')

    delete_note_parser = subparsers.add_parser('delete-note', help='Delete note')
    delete_note_parser.add_argument('--id', type=int, required=True, help='Note ID')

    # ============= PRODUCTS =============
    product_parser = subparsers.add_parser('list-products', help='List all products')
    product_parser.add_argument('--name', help='Filter by name')
    product_parser.add_argument('--code', help='Filter by code')
    product_parser.add_argument('--limit', type=int, help='Limit number of results')

    get_product_parser = subparsers.add_parser('get-product', help='Get specific product')
    get_product_parser.add_argument('--id', type=int, required=True, help='Product ID')

    create_product_parser = subparsers.add_parser('create-product', help='Create new product')
    create_product_parser.add_argument('--name', required=True, help='Product name')
    create_product_parser.add_argument('--code', help='Product code')
    create_product_parser.add_argument('--price', type=float, help='Product price')
    create_product_parser.add_argument('--currency', help='Currency code (e.g., USD)')

    update_product_parser = subparsers.add_parser('update-product', help='Update product')
    update_product_parser.add_argument('--id', type=int, required=True, help='Product ID')
    update_product_parser.add_argument('--name', help='Product name')
    update_product_parser.add_argument('--code', help='Product code')
    update_product_parser.add_argument('--price', type=float, help='Product price')
    update_product_parser.add_argument('--currency', help='Currency code')

    delete_product_parser = subparsers.add_parser('delete-product', help='Delete product')
    delete_product_parser.add_argument('--id', type=int, required=True, help='Product ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Get credentials
    api_token, company_url = get_credentials()
    client = PipedriveClient(api_token, company_url)

    try:
        # ============= DEALS =============
        if args.command == 'list-deals':
            result = client.list_deals(
                status=args.status,
                stage_id=args.stage_id,
                user_id=args.user_id,
                limit=args.limit
            )
            print(f"✅ Found {len(result)} deals")
            print_json(result)

        elif args.command == 'get-deal':
            result = client.get_deal(args.id)
            print("✅ Deal retrieved successfully")
            print_json(result)

        elif args.command == 'create-deal':
            result = client.create_deal(
                title=args.title,
                value=args.value,
                currency=args.currency,
                person_id=args.person_id,
                org_id=args.org_id,
                stage_id=args.stage_id,
                probability=args.probability
            )
            print(f"✅ Deal created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'update-deal':
            result = client.update_deal(
                deal_id=args.id,
                title=args.title,
                value=args.value,
                currency=args.currency,
                stage_id=args.stage_id,
                status=args.status,
                probability=args.probability
            )
            print(f"✅ Deal updated successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-deal':
            result = client.delete_deal(args.id)
            print(f"✅ Deal deleted successfully (ID: {result['id']})")


        # ============= LEADS =============
        elif args.command == 'list-leads':
            result = client.list_leads(
                status=args.status,
                label=args.label,
                person_id=args.person_id,
                org_id=args.org_id,
                sort_by=getattr(args, 'sort_by', None),
                sort_order=getattr(args, 'sort_order', None),
                limit=args.limit
            )
            print(f"✅ Found {len(result)} leads")
            print_json(result)

        elif args.command == 'get-lead':
            result = client.get_lead(args.id)
            print("✅ Lead retrieved successfully")
            print_json(result)

        elif args.command == 'create-lead':
            result = client.create_lead(
                title=args.title,
                person_id=args.person_id,
                org_id=args.org_id,
                value=args.value,
                currency=args.currency,
                expected_close_date=args.expected_close_date,
                probability=args.probability,
                label=args.label
            )
            print(f"✅ Lead created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'update-lead':
            result = client.update_lead(
                lead_id=args.id,
                title=args.title,
                person_id=args.person_id,
                org_id=args.org_id,
                value=args.value,
                currency=args.currency,
                expected_close_date=args.expected_close_date,
                probability=args.probability,
                label=args.label,
                status=args.status
            )
            print(f"✅ Lead updated successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-lead':
            result = client.delete_lead(args.id)
            print(f"✅ Lead deleted successfully (ID: {result['id']})")

        # ============= PERSONS =============
        elif args.command == 'list-persons':
            result = client.list_persons(
                name=args.name,
                email=args.email,
                org_id=args.org_id,
                limit=args.limit
            )
            print(f"✅ Found {len(result)} persons")
            print_json(result)

        elif args.command == 'get-person':
            result = client.get_person(args.id)
            print("✅ Person retrieved successfully")
            print_json(result)

        elif args.command == 'create-person':
            result = client.create_person(
                name=args.name,
                email=args.email,
                phone=args.phone,
                org_id=args.org_id,
                title=args.title
            )
            print(f"✅ Person created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'update-person':
            result = client.update_person(
                person_id=args.id,
                name=args.name,
                email=args.email,
                phone=args.phone,
                org_id=args.org_id,
                title=args.title
            )
            print(f"✅ Person updated successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-person':
            result = client.delete_person(args.id)
            print(f"✅ Person deleted successfully (ID: {result['id']})")

        # ============= ORGANIZATIONS =============
        elif args.command == 'list-organizations':
            result = client.list_organizations(
                name=args.name,
                limit=args.limit
            )
            print(f"✅ Found {len(result)} organizations")
            print_json(result)

        elif args.command == 'get-organization':
            result = client.get_organization(args.id)
            print("✅ Organization retrieved successfully")
            print_json(result)

        elif args.command == 'create-organization':
            result = client.create_organization(
                name=args.name,
                website=args.website,
                industry=args.industry,
                address=args.address
            )
            print(f"✅ Organization created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'update-organization':
            result = client.update_organization(
                org_id=args.id,
                name=args.name,
                website=args.website,
                industry=args.industry,
                address=args.address
            )
            print(f"✅ Organization updated successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-organization':
            result = client.delete_organization(args.id)
            print(f"✅ Organization deleted successfully (ID: {result['id']})")

        # ============= ACTIVITIES =============
        elif args.command == 'list-activities':
            result = client.list_activities(
                activity_type=args.type,
                deal_id=args.deal_id,
                person_id=args.person_id,
                limit=args.limit
            )
            print(f"✅ Found {len(result)} activities")
            print_json(result)

        elif args.command == 'get-activity':
            result = client.get_activity(args.id)
            print("✅ Activity retrieved successfully")
            print_json(result)

        elif args.command == 'create-activity':
            result = client.create_activity(
                subject=args.subject,
                activity_type=args.type,
                deal_id=args.deal_id,
                person_id=args.person_id,
                note=args.note,
                due_date=args.due_date
            )
            print(f"✅ Activity created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'update-activity':
            result = client.update_activity(
                activity_id=args.id,
                subject=args.subject,
                activity_type=args.type,
                status=args.status,
                note=args.note
            )
            print(f"✅ Activity updated successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-activity':
            result = client.delete_activity(args.id)
            print(f"✅ Activity deleted successfully (ID: {result['id']})")

        # ============= NOTES =============
        elif args.command == 'list-notes':
            result = client.list_notes(
                deal_id=args.deal_id,
                person_id=args.person_id,
                org_id=args.org_id,
                limit=args.limit
            )
            print(f"✅ Found {len(result)} notes")
            print_json(result)

        elif args.command == 'get-note':
            result = client.get_note(args.id)
            print("✅ Note retrieved successfully")
            print_json(result)

        elif args.command == 'create-note':
            result = client.create_note(
                content=args.content,
                deal_id=args.deal_id,
                person_id=args.person_id,
                org_id=args.org_id
            )
            print(f"✅ Note created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-note':
            result = client.delete_note(args.id)
            print(f"✅ Note deleted successfully (ID: {result['id']})")

        # ============= PRODUCTS =============
        elif args.command == 'list-products':
            result = client.list_products(
                name=args.name,
                code=args.code,
                limit=args.limit
            )
            print(f"✅ Found {len(result)} products")
            print_json(result)

        elif args.command == 'get-product':
            result = client.get_product(args.id)
            print("✅ Product retrieved successfully")
            print_json(result)

        elif args.command == 'create-product':
            result = client.create_product(
                name=args.name,
                code=args.code,
                price=args.price,
                currency=args.currency
            )
            print(f"✅ Product created successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'update-product':
            result = client.update_product(
                product_id=args.id,
                name=args.name,
                code=args.code,
                price=args.price,
                currency=args.currency
            )
            print(f"✅ Product updated successfully (ID: {result['id']})")
            print_json(result)

        elif args.command == 'delete-product':
            result = client.delete_product(args.id)
            print(f"✅ Product deleted successfully (ID: {result['id']})")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
