#!/usr/bin/env node
/**
 * Pipedrive Export Skill
 *
 * Export Pipedrive deals with email threads to Excel and Google Sheets.
 *
 * Usage: PIPEDRIVE_API_TOKEN=xxx node --import tsx export.ts [options]
 *
 * Options:
 *   --days <n>       Days to look back (default: 90)
 *   --deal-id <id>   Export specific deal only
 *   --format <type>  excel, sheets, both (default: both)
 *   --output <path>  Output directory (default: ./query-results)
 *   --mcp-server <path>  Path to pipedrive-mcp-server (default: auto-detect)
 */

import { spawn } from 'child_process';
import { writeFileSync, mkdirSync, existsSync, readFileSync as fsReadFileSync } from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import * as XLSX from 'xlsx';

const __filename = fileURLToPath(import.meta.url);
const SKILL_DIR = path.dirname(__filename);

// Types for MCP communication
interface MCPRequest {
  jsonrpc: '2.0';
  id: number;
  method: string;
  params?: any;
}

interface MCPResponse {
  jsonrpc: '2.0';
  id: number;
  result?: any;
  error?: any;
}

interface Deal {
  id: number;
  title: string;
  value?: number;
  currency?: string;
  status?: string;
  stage_id?: number;
  add_time?: string;
  update_time?: string;
  expected_close_date?: string;
  person_id?: number;
  org_id?: number;
  user_id?: number;
  [key: string]: any;
}

interface MailMessage {
  id: number;
  subject: string;
  snippet?: string;
  from?: Array<{ name: string; email_address?: string; email?: string }>;
  to?: Array<{ name: string; email_address?: string; email?: string }>;
  cc?: Array<{ name: string; email_address?: string; email?: string }>;
  message_time?: string;
  sent_flag?: boolean;
  mail_thread_id?: number;
  has_body_flag?: boolean;
  body_url?: string;
}

interface ExportConfig {
  days: number;
  dealId: number | null;
  format: 'excel' | 'sheets' | 'both';
  outputDir: string;
  mcpServerPath: string;
  gdriveConfigPath: string;
}

// Parse CLI arguments
function parseArgs(): ExportConfig {
  const args = process.argv.slice(2);
  const config: Partial<ExportConfig> = {
    days: 90,
    dealId: null,
    format: 'both',
    outputDir: './query-results',
    gdriveConfigPath: path.join(process.env.HOME || '', '.gdrivelm'),
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    switch (arg) {
      case '--days':
        config.days = parseInt(next, 10) || 90;
        i++;
        break;
      case '--deal-id':
        config.dealId = parseInt(next, 10) || null;
        i++;
        break;
      case '--format':
        if (next === 'excel' || next === 'sheets' || next === 'both') {
          config.format = next;
        }
        i++;
        break;
      case '--output':
        config.outputDir = next;
        i++;
        break;
      case '--mcp-server':
        config.mcpServerPath = next;
        i++;
        break;
    }
  }

  // Auto-detect MCP server path if not provided
  if (!config.mcpServerPath) {
    const candidates = [
      path.join(process.env.HOME || '', 'projects/pipedrive-mcp-server'),
      path.join(SKILL_DIR, '../../pipedrive-mcp-server'),
    ];
    for (const candidate of candidates) {
      if (existsSync(path.join(candidate, 'src/index.ts'))) {
        config.mcpServerPath = candidate;
        break;
      }
    }
  }

  if (!config.mcpServerPath || !existsSync(path.join(config.mcpServerPath, 'src/index.ts'))) {
    throw new Error('Pipedrive MCP server not found. Use --mcp-server <path> or ensure it exists in ~/projects/pipedrive-mcp-server');
  }

  // Resolve output dir relative to CWD
  if (config.outputDir && !path.isAbsolute(config.outputDir)) {
    config.outputDir = path.resolve(process.cwd(), config.outputDir);
  }

  return config as ExportConfig;
}

// Calculate date threshold
function calculateDateThreshold(daysOffset: number): Date {
  const threshold = new Date();
  threshold.setDate(threshold.getDate() - daysOffset);
  return threshold;
}

// MCP Client class
class MCPClient {
  private proc: any;
  private requestId = 0;
  private pendingRequests = new Map<number, {
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }>();
  private mcpServerPath: string;

  constructor(mcpServerPath: string) {
    this.mcpServerPath = mcpServerPath;
  }

  async start() {
    let apiToken = process.env.PIPEDRIVE_API_TOKEN;

    // Fallback: read from token file
    if (!apiToken) {
      try {
        const { readFileSync } = await import('fs');
        const tokenPath = path.join(process.env.HOME || '', '.pipedrive-token');
        if (existsSync(tokenPath)) {
          apiToken = readFileSync(tokenPath, 'utf-8').trim();
        }
      } catch (e) {
        // Ignore
      }
    }

    if (!apiToken) {
      throw new Error('PIPEDRIVE_API_TOKEN environment variable or ~/.pipedrive-token file is required');
    }

    // Spawn MCP server process
    this.proc = spawn('node', ['--import', 'tsx', 'src/index.ts'], {
      cwd: this.mcpServerPath,
      env: { ...process.env, PIPEDRIVE_API_TOKEN: apiToken },
      stdio: ['pipe', 'pipe', 'inherit']
    });

    // Handle stdout (JSON-RPC responses)
    let buffer = '';
    this.proc.stdout.on('data', (data: Buffer) => {
      buffer += data.toString();
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const response: MCPResponse = JSON.parse(line);
          this.handleResponse(response);
        } catch (e) {
          // Skip non-JSON lines
        }
      }
    });

    this.proc.on('error', (err: Error) => {
      console.error('Process error:', err);
    });

    this.proc.on('exit', (code: number) => {
      console.log(`Process exited with code ${code}`);
    });

    await this.sleep(1000);
  }

  private handleResponse(response: MCPResponse) {
    const pending = this.pendingRequests.get(response.id);
    if (pending) {
      this.pendingRequests.delete(response.id);
      if (response.error) {
        pending.reject(new Error(response.error.message || 'Unknown error'));
      } else {
        pending.resolve(response.result);
      }
    }
  }

  async callTool(toolName: string, args: any = {}): Promise<any> {
    const request: MCPRequest = {
      jsonrpc: '2.0',
      id: ++this.requestId,
      method: 'tools/call',
      params: { name: toolName, arguments: args }
    };

    return new Promise((resolve, reject) => {
      this.pendingRequests.set(request.id, { resolve, reject });
      this.proc.stdin.write(JSON.stringify(request) + '\n');

      setTimeout(() => {
        if (this.pendingRequests.has(request.id)) {
          this.pendingRequests.delete(request.id);
          reject(new Error(`Timeout calling tool ${toolName}`));
        }
      }, 60000);
    });
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  stop() {
    if (this.proc) {
      this.proc.kill();
    }
  }
}

// Helper functions
function parseDate(dateStr: string | undefined): Date | null {
  if (!dateStr) return null;
  return new Date(dateStr);
}

function matchesDateFilter(deal: Deal, threshold: Date): boolean {
  const createdDate = parseDate(deal.add_time);
  const updatedDate = parseDate(deal.update_time);

  if (createdDate && createdDate >= threshold) return true;
  if (updatedDate && updatedDate >= threshold) return true;

  return false;
}

function sanitizeSheetName(name: string): string {
  return name
    .replace(/[\\/:*?\[\]]/g, '')
    .substring(0, 31)
    .trim() || 'Sheet';
}

// Fetch functions
async function fetchAllDeals(client: MCPClient): Promise<Deal[]> {
  const allDeals: Deal[] = [];
  let start = 0;
  const limit = 100;

  console.log('📊 Fetching all deals...');

  while (true) {
    const result = await client.callTool('get-deals', { start, limit });
    const content = result.content?.[0];
    if (!content) break;

    const deals = JSON.parse(content.text);
    if (!deals || deals.length === 0) break;

    allDeals.push(...deals);
    console.log(`   Fetched ${deals.length} deals (total: ${allDeals.length})`);

    if (deals.length < limit) break;
    start += limit;

    await new Promise(r => setTimeout(r, 100));
  }

  return allDeals;
}

async function fetchAllMailMessages(client: MCPClient, dealId: number): Promise<MailMessage[]> {
  const allMessages: MailMessage[] = [];
  let start = 0;
  const limit = 100;

  while (true) {
    const result = await client.callTool('get-deal-mail-messages', { dealId, start, limit });
    const content = result.content?.[0];
    if (!content || result.isError) break;

    const data = JSON.parse(content.text);
    const messages = data.messages || [];
    if (messages.length === 0) break;

    allMessages.push(...messages);

    if (messages.length < limit) break;
    start += limit;

    await new Promise(r => setTimeout(r, 100));
  }

  return allMessages;
}

// Strip HTML tags and convert to plain text
function stripHtml(html: string): string {
  if (!html) return '';

  // Remove style and script tags first (including their content)
  let text = html
    .replace(/<style[^>]*>.*?<\/style>/gis, '')
    .replace(/<script[^>]*>.*?<\/script>/gis, '')
    // Remove meta, link tags
    .replace(/<(meta|link)[^>]+>/gi, '')
    // Replace block elements with newlines
    .replace(/<div[^>]*>/gi, '\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<p[^>]*>/gi, '\n')
    .replace(/<\/p>/gi, '\n')
    .replace(/<li[^>]*>/gi, '\n• ')
    .replace(/<\/li>/gi, '\n')
    .replace(/<tr[^>]*>/gi, '\n')
    .replace(/<\/tr>/gi, '\n')
    .replace(/<\/td>/gi, ' | ')
    .replace(/<\/th>/gi, ' | ')
    // Remove head and body tags
    .replace(/<\/?(head|body|html)[^>]*>/gi, '');

  // Remove all remaining HTML tags
  text = text.replace(/<[^>]+>/g, '');

  // Remove CSS class names patterns like div.pipe-mailbody-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx p.pd-MsoNormal
  // These are leftover text from HTML email structure
  text = text
    .replace(/div\.pipe-mailbody-[a-f0-9\-]+(?:\s+p\.pd-[a-zA-Z0-9\-]+)*/g, '')
    .replace(/div\.pipe-mailbody-[a-f0-9\-]+/g, '')
    .replace(/p\.pd-[a-zA-Z0-9\-]+/g, '')
    .replace(/li\.pd-[a-zA-Z0-9\-]+/g, '')
    // Remove other common CSS class patterns in email
    .replace(/\{[^\}]*\}/g, '')  // Remove {...} CSS blocks
    .replace(/[a-zA-Z0-9\-]+\s*\{/g, '')  // Remove CSS rule starts
    // Clean up common email artifacts
    .replace(/margin:\s*[0-9a-z]+(?:px|in|cm|em|%);?/gi, '')
    .replace(/font-size:\s*[0-9a-z]+(?:px|pt|em|%);?/gi, '')
    .replace(/font-family:\s*[^;]+;?/gi, '');

  // Decode HTML entities
  // Node.js fallback - basic entity decoding
  text = text
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&#x60;/g, '`')
    .replace(/&#x3D;/g, '=')
    .replace(/&#[0-9]+;/g, '')  // Remove any other numeric entities
    .replace(/&#x[0-9a-f]+;/gi, '');  // Remove hex entities

  // Clean up whitespace
  text = text
    .replace(/\n{3,}/g, '\n\n')  // Max 2 consecutive newlines
    .replace(/[ \t]+/g, ' ')     // Collapse spaces
    .replace(/ \n/g, '\n')        // Remove trailing spaces
    .replace(/\n +\n/g, '\n\n')   // Clean spaces between newlines
    .trim();

  return text;
}

async function fetchEmailBody(client: MCPClient, messageId: number, bodyUrl?: string): Promise<string> {
  const result = await client.callTool('get-mail-message-body', { messageId, bodyUrl });
  const content = result.content?.[0];
  if (!content || result.isError) return '';

  const data = JSON.parse(content.text);
  const bodyContent = data.body_content || '';
  // Strip HTML and return plain text
  return stripHtml(bodyContent);
}

// Generate timestamp
function getTimestamp(): string {
  const now = new Date();
  const datePart = now.toISOString().split('T')[0];  // YYYY-MM-DD
  const timePart = now.toTimeString().split(' ')[0].replace(/:/g, '-');  // HH-MM-SS
  return `${datePart}-${timePart}`;
}

// Format email address
function formatEmailAddr(addrList: Array<{ name?: string; email?: string; email_address?: string }> | undefined): string {
  if (!addrList || addrList.length === 0) return 'N/A';
  return addrList
    .map(addr => {
      const name = addr.name || '';
      const email = addr.email || addr.email_address || '';
      if (name && email) return `${name} <${email}>`;
      if (email) return email;
      return name || 'N/A';
    })
    .join('; ');
}

// Generate Deals Info Excel
function generateDealsInfoExcel(
  dealsWithData: Array<{ deal: Deal; messages: Array<MailMessage & { body?: string }> }>,
  outputDir: string,
  timestamp: string
): string {
  const workbook = XLSX.utils.book_new();

  // Per-deal sheets with deal info
  for (const item of dealsWithData) {
    const deal = item.deal;
    const sheetName = sanitizeSheetName(`${deal.id}-${deal.title}`);

    const dealInfo = [
      // Deal Overview Section
      ['DEAL OVERVIEW', '', ''],
      ['', '', ''],
      ['Field', 'Value', ''],
      ['', '', ''],
      ['Deal ID', deal.id, ''],
      ['Deal Name', deal.title || '', ''],
      ['Status', deal.status || 'N/A', ''],
      ['Value', `${deal.value || 0} ${deal.currency || ''}`, ''],
      ['Currency', deal.currency || 'N/A', ''],
      ['Stage ID', deal.stage_id || 'N/A', ''],
      ['Created', deal.add_time || 'N/A', ''],
      ['Updated', deal.update_time || 'N/A', ''],
      ['Expected Close Date', deal.expected_close_date || 'N/A', ''],
      ['Person ID', deal.person_id || 'N/A', ''],
      ['Organization ID', deal.org_id || 'N/A', ''],
      ['User ID', deal.user_id || 'N/A', ''],
      ['', '', ''],
      ['', '', ''],
      // Email Summary Section
      ['EMAIL SUMMARY', '', ''],
      ['', '', ''],
      ['Total Emails', item.messages.length, ''],
    ];

    const sheet = XLSX.utils.aoa_to_sheet(dealInfo);
    sheet['!cols'] = [
      { wch: 25 },
      { wch: 50 },
      { wch: 15 }
    ];

    XLSX.utils.book_append_sheet(workbook, sheet, sheetName);
  }

  mkdirSync(outputDir, { recursive: true });
  const outputPath = path.join(outputDir, `deals_info_${timestamp}.xlsx`);
  XLSX.writeFile(workbook, outputPath);

  return outputPath;
}

// Generate Mail Thread Excel
function generateMailThreadExcel(
  dealsWithData: Array<{ deal: Deal; messages: Array<MailMessage & { body?: string }> }>,
  outputDir: string,
  timestamp: string
): string {
  const workbook = XLSX.utils.book_new();

  // Per-deal sheets with email threads
  for (const item of dealsWithData) {
    const deal = item.deal;
    const sheetName = sanitizeSheetName(`${deal.id}-${deal.title}`);

    const emailData = [
      ['EMAIL THREADS', '', '', '', '', '', ''],
      ['', '', '', '', '', '', ''],
      ['Deal ID', deal.id, '', '', '', '', ''],
      ['Deal Name', deal.title || '', '', '', '', '', ''],
      ['', '', '', '', '', '', ''],
      ['', '', '', '', '', '', ''],
      // Email headers
      ['#', 'Direction', 'Date', 'From', 'To', 'Subject', 'Body'],
    ];

    for (let i = 0; i < item.messages.length; i++) {
      const msg = item.messages[i];
      const direction = msg.sent_flag === 1 ? 'Outgoing' : 'Incoming';
      const from = formatEmailAddr(msg.from);
      const to = formatEmailAddr(msg.to);
      const body = msg.body || '(No body content)';

      // Full content, no truncation
      emailData.push([
        i + 1,
        direction,
        msg.message_time || 'N/A',
        from,
        to,
        msg.subject || '(No subject)',
        body
      ]);
    }

    const sheet = XLSX.utils.aoa_to_sheet(emailData);
    sheet['!cols'] = [
      { wch: 5 },     // #
      { wch: 12 },    // Direction
      { wch: 18 },    // Date
      { wch: 35 },    // From
      { wch: 35 },    // To
      { wch: 40 },    // Subject
      { wch: 80 }     // Body
    ];

    XLSX.utils.book_append_sheet(workbook, sheet, sheetName);
  }

  mkdirSync(outputDir, { recursive: true });
  const outputPath = path.join(outputDir, `mail_thread_${timestamp}.xlsx`);
  XLSX.writeFile(workbook, outputPath);

  return outputPath;
}

// Generate both Excel files
function generateExcel(
  dealsWithData: Array<{ deal: Deal; messages: Array<MailMessage & { body?: string }> }>,
  outputDir: string
): { dealsInfoPath: string; mailThreadPath: string; timestamp: string } {
  const timestamp = getTimestamp();

  const dealsInfoPath = generateDealsInfoExcel(dealsWithData, outputDir, timestamp);
  const mailThreadPath = generateMailThreadExcel(dealsWithData, outputDir, timestamp);

  return { dealsInfoPath, mailThreadPath, timestamp };
}

// Upload to Google Sheets
async function uploadToGoogleSheets(
  localFilePath: string,
  fileName: string,
  gdriveConfigPath: string,
  outputDir: string
): Promise<{ url: string; fileId: string } | null> {
  if (!existsSync(gdriveConfigPath)) {
    console.log('⚠️  Google Drive config not found - skipping upload');
    return null;
  }

  console.log('📤 Uploading to Google Drive...');

  // First, read the Excel file to get workbook data
  const workbook = XLSX.read(fsReadFileSync(localFilePath), { type: 'buffer' });
  const sheetNames = workbook.SheetNames;
  const sheetsData: Record<string, string[][]> = {};

  for (const sheetName of sheetNames) {
    const sheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' }) as string[][];
    sheetsData[sheetName] = data;
  }

  // Convert to base64 to pass to Python
  const sheetsJson = JSON.stringify(sheetsData);
  const base64Data = Buffer.from(sheetsJson).toString('base64');

  const uploadScript = `
import os
import sys
import json
import base64
import httplib2
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gdrive_path = "${gdriveConfigPath}"
os.chdir(gdrive_path)

gauth = GoogleAuth(settings_file=os.path.join(gdrive_path, "settings.yaml"))
gauth.LoadCredentialsFile(os.path.join(gdrive_path, "token.json"))
if gauth.credentials is None:
    print("ERROR: No credentials found", file=sys.stderr)
    sys.exit(1)
elif gauth.access_token_expired:
    gauth.Refresh()
    gauth.SaveCredentialsFile(os.path.join(gdrive_path, "token.json"))

drive = GoogleDrive(gauth)

# Create the spreadsheet file first
title = "${fileName.replace(/"/g, '\\"').replace('.xlsx', '')}"
file_metadata = {
    'title': title,
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

file = drive.CreateFile(file_metadata)
file.Upload()

# Decode sheets data
sheets_data_json = base64.b64decode("${base64Data}").decode('utf-8')
sheets_data = json.loads(sheets_data_json)

# Use HTTP to update sheets
spreadsheet_id = file['id']
gauth.Authorize()
http = gauth.http

for sheet_name, rows in sheets_data.items():
    if not rows:
        continue

    # Calculate column letter for range
    max_cols = max(len(row) for row in rows) if rows else 1
    if max_cols > 26:
        end_col = 'Z'
    else:
        end_col = chr(65 + max_cols - 1) if max_cols > 0 else 'A'

    row_count = len(rows)
    range_notation = f"'{{sheet_name}}'!A1:{{end_col}}{{row_count}}"

    # Prepare values as 2D array
    values = [[str(cell) if cell is not None else '' for cell in row] for row in rows]

    # Build batch_update request
    batch_update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{{spreadsheet_id}}/values:batchUpdate"
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
                "range": range_notation,
                "values": values
            }
        ]
    }

    resp, content = http.request(
        batch_update_url,
        "POST",
        body=json.dumps(body),
        headers={"Content-Type": "application/json"}
    )

    if resp.status not in [200, 201]:
        print(f"WARNING: Failed to update sheet {{sheet_name}}: {{content.decode()}}", file=sys.stderr)

# Set sharing permissions
permission = file.InsertPermission({
    'type': 'anyone',
    'role': 'writer',
    'value': 'anyone with link',
    'withLink': True
})

print(f"FILE_ID:{file['id']}")
print(f"URL:https://docs.google.com/spreadsheets/d/{file['id']}/edit")
`;

  const tempScriptPath = path.join(outputDir, 'gdrive_upload.py');
  writeFileSync(tempScriptPath, uploadScript);

  const { execSync } = await import('child_process');

  try {
    const output = execSync(`python3 "${tempScriptPath}"`, { encoding: 'utf-8', stdio: 'pipe' });

    let fileId = '';
    let url = '';

    for (const line of output.split('\n')) {
      if (line.startsWith('FILE_ID:')) fileId = line.replace('FILE_ID:', '').trim();
      else if (line.startsWith('URL:')) url = line.replace('URL:', '').trim();
    }

    if (url && fileId) {
      console.log(`✅ Uploaded to Google Sheets`);
      console.log(`   File ID: ${fileId}`);
      console.log(`   URL: ${url}`);
      return { url, fileId };
    } else {
      console.log('⚠️  Upload completed but could not extract URL');
      return null;
    }
  } catch (error: any) {
    console.log(`⚠️  Google Drive upload failed: ${error.message}`);
    return null;
  } finally {
    try {
      const { unlinkSync } = await import('fs');
      unlinkSync(tempScriptPath);
    } catch {}
  }
}

// Main execution
async function main() {
  const config = parseArgs();
  const dateThreshold = calculateDateThreshold(config.days);
  const dateThresholdStr = dateThreshold.toISOString().split('T')[0];

  console.log('==========================================');
  console.log('Pipedrive Export');
  console.log('==========================================');
  console.log(`📅 Date filter: deals created or active since ${dateThresholdStr}`);
  if (config.dealId) {
    console.log(`🎯 Single deal mode: ID ${config.dealId}`);
  }
  console.log(`📁 Output: ${config.outputDir}`);
  console.log(`📤 Format: ${config.format}`);
  console.log('');

  const client = new MCPClient(config.mcpServerPath);

  try {
    console.log('🚀 Starting MCP client...');
    await client.start();

    console.log('📋 Fetching deals...');
    const allDeals = await fetchAllDeals(client);
    console.log(`✅ Total deals fetched: ${allDeals.length}`);

    // Filter deals
    let filteredDeals: Deal[];
    if (config.dealId) {
      filteredDeals = allDeals.filter(d => d.id === config.dealId);
      console.log(`✅ Found deal: ${filteredDeals.length}`);
    } else {
      filteredDeals = allDeals.filter(d => matchesDateFilter(d, dateThreshold));
      console.log(`✅ Deals within date range: ${filteredDeals.length}`);
    }

    if (filteredDeals.length === 0) {
      console.log('⚠️  No deals found.');
      return;
    }

    const dealsWithData: Array<{
      deal: Deal;
      messages: Array<MailMessage & { body?: string }>;
    }> = [];

    // Process deals
    for (let i = 0; i < filteredDeals.length; i++) {
      const deal = filteredDeals[i];
      console.log(`\n📧 [${i + 1}/${filteredDeals.length}] Processing: ${deal.title} (ID: ${deal.id})`);

      const messages = await fetchAllMailMessages(client, deal.id);
      console.log(`   Found ${messages.length} email messages`);

      const messagesWithBodies: Array<MailMessage & { body?: string }> = [];

      for (let j = 0; j < messages.length; j++) {
        const msg = messages[j];
        console.log(`   Fetching body ${j + 1}/${messages.length}...`);
        const body = await fetchEmailBody(client, msg.id, msg.body_url);
        messagesWithBodies.push({ ...msg, body });
      }

      dealsWithData.push({ deal, messages: messagesWithBodies });
      await new Promise(r => setTimeout(r, 200));
    }

    // Generate outputs
    console.log('\n📊 Generating outputs...');

    const excelResult = generateExcel(dealsWithData, config.outputDir);
    console.log(`✅ Deals Info: ${excelResult.dealsInfoPath}`);
    console.log(`✅ Mail Thread: ${excelResult.mailThreadPath}`);

    // JSON backup - use same timestamp
    const jsonPath = path.join(config.outputDir, `pipedrive-deals-${excelResult.timestamp}.json`);
    writeFileSync(jsonPath, JSON.stringify(dealsWithData, null, 2));
    console.log(`✅ JSON: ${jsonPath}`);

    // Google Sheets - upload both files
    let gdriveResults: Array<{ url: string; fileId: string; name: string }> = [];
    if (config.format === 'sheets' || config.format === 'both') {
      // Upload deals_info
      const dealsInfoUpload = await uploadToGoogleSheets(
        excelResult.dealsInfoPath,
        path.basename(excelResult.dealsInfoPath),
        config.gdriveConfigPath,
        config.outputDir
      );
      if (dealsInfoUpload) {
        gdriveResults.push({ ...dealsInfoUpload, name: 'Deals Info' });
      }

      // Upload mail_thread
      const mailThreadUpload = await uploadToGoogleSheets(
        excelResult.mailThreadPath,
        path.basename(excelResult.mailThreadPath),
        config.gdriveConfigPath,
        config.outputDir
      );
      if (mailThreadUpload) {
        gdriveResults.push({ ...mailThreadUpload, name: 'Mail Thread' });
      }
    }

    // Summary
    console.log('\n==========================================');
    console.log('📄 Summary');
    console.log('==========================================');
    console.log(`   Deals processed: ${dealsWithData.length}`);
    console.log(`   Emails fetched: ${dealsWithData.reduce((sum, d) => sum + d.messages.length, 0)}`);
    console.log(`   Excel files: 2 (deals_info + mail_thread)`);
    console.log(`   Sheets per file: ${dealsWithData.length} (one per deal)`);
    if (gdriveResults.length > 0) {
      console.log(`\n🔗 Google Sheets:`);
      for (const result of gdriveResults) {
        console.log(`   ${result.name}: ${result.url}`);
      }
    }

  } catch (error) {
    console.error('❌ Error:', error);
    throw error;
  } finally {
    client.stop();
  }
}

main().catch(console.error);
