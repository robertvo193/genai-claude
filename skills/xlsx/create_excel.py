import pandas as pd
import xlsxwriter
import sys

csv_file = sys.argv[1]
xlsx_file = csv_file.replace('.csv', '_formatted.xlsx')

# Read CSV and replace NaN with empty string
df = pd.read_csv(csv_file).fillna('')

# Reorder columns
columns_order = [
    'Lead Title', 'Lead ID', 'Lead Created', 'Lead Updated', 
    'Expected Close Date', 'Status', 'Seen', 'Value', 'Currency',
    'Source', 'Origin',
    'Owner ID', 'Owner Name', 'Owner Email',
    'Creator ID', 'Creator Name',
    'Person ID', 'Person Name', 'Person Email', 'Person Phone',
    'Organization ID', 'Organization Name', 'Organization Address',
    'Next Activity ID', 'Visible To', 'CC Email', 'Label IDs'
]

existing_columns = [c for c in columns_order if c in df.columns]
df_export = df[existing_columns].copy()
df_export = df_export.fillna('').replace(float('nan'), '').replace(pd.NaT, '')

wb = xlsxwriter.Workbook(xlsx_file, {'nan_inf_to_errors': True})
ws = wb.add_worksheet('Leads')

header_fmt = wb.add_format({
    'bold': True, 'bg_color': '#4472C4', 'font_color': 'FFFFFF',
    'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1
})

active_fmt = wb.add_format({'bg_color': '#E2EFDA', 'border': 1})
archived_fmt = wb.add_format({'bg_color': '#F4B084', 'border': 1})
cell_fmt = wb.add_format({'valign': 'top', 'border': 1})

# Write headers
for col, header in enumerate(existing_columns):
    ws.write(0, col, header, header_fmt)

# Set column widths
widths = {
    'Lead Title': 30, 'Lead ID': 40, 'Lead Created': 20, 'Lead Updated': 20,
    'Expected Close Date': 18, 'Status': 12, 'Seen': 10, 'Value': 12,
    'Currency': 10, 'Source': 15, 'Origin': 15, 'Owner ID': 12,
    'Owner Name': 18, 'Owner Email': 25, 'Creator ID': 12, 'Creator Name': 18,
    'Person ID': 12, 'Person Name': 20, 'Person Email': 25, 'Person Phone': 18,
    'Organization ID': 15, 'Organization Name': 30, 'Organization Address': 35,
    'Next Activity ID': 18, 'Visible To': 12, 'CC Email': 45, 'Label IDs': 15
}

for col, header in enumerate(existing_columns):
    ws.set_column(col, col, widths.get(header, 15))

# Write data
status_col_idx = existing_columns.index('Status') if 'Status' in existing_columns else -1

for row_idx, row_data in enumerate(df_export.itertuples(index=False), 1):
    for col_idx, value in enumerate(row_data):
        fmt = cell_fmt
        if col_idx == status_col_idx:
            if str(value) == 'Active':
                fmt = active_fmt
            elif str(value) == 'Archived':
                fmt = archived_fmt
        ws.write(row_idx, col_idx, str(value) if value != '' else '', fmt)

ws.freeze_panes(1, 0)

# Summary sheet
ws_summ = wb.add_worksheet('Summary')
title_fmt = wb.add_format({'bold': True, 'font_size': 14})
bold_fmt = wb.add_format({'bold': True})

ws_summ.write(0, 0, 'Pipedrive Leads Export Summary', title_fmt)
ws_summ.write(2, 0, 'Total Leads:', bold_fmt)
ws_summ.write(2, 1, len(df_export))
ws_summ.write(3, 0, 'Columns:', bold_fmt)
ws_summ.write(3, 1, len(existing_columns))

row = 6
ws_summ.write(row, 0, 'Status Breakdown', bold_fmt)
row += 1
ws_summ.write(row, 0, 'Status', bold_fmt)
ws_summ.write(row, 1, 'Count', bold_fmt)
row += 1

if 'Status' in df_export.columns:
    for status, count in df_export['Status'].value_counts().items():
        ws_summ.write(row, 0, str(status))
        ws_summ.write(row, 1, count)
        row += 1

row += 1
ws_summ.write(row, 0, 'Source Breakdown', bold_fmt)
row += 1
ws_summ.write(row, 0, 'Source', bold_fmt)
ws_summ.write(row, 1, 'Count', bold_fmt)
row += 1

if 'Source' in df_export.columns:
    for source, count in df_export['Source'].value_counts().items():
        ws_summ.write(row, 0, str(source))
        ws_summ.write(row, 1, count)
        row += 1

ws_summ.set_column(0, 0, 25)
ws_summ.set_column(1, 1, 15)

wb.close()
print(f'Created: {xlsx_file}')
