import csv
import sys
import os
import argparse

from csvmoney import classification

out_keys = ['Transaction Date', 'Amount', 'Description', 'Account', 'Category', 'Notes']

def make_schoolsfirst_dict(row, identify):
    '''
    convert SchoolsFirst row
    '''
    category = identify(row['Description'])
    values = [row['Transaction Date'],
              row['Amount'],
              row['Description'],
              'SchoolsFirst',
              category,
              '']                         # notes
    return dict(zip(out_keys, values))

def make_sapphire_dict(row, identify):
    '''
    convert Chase Sapphire row
    '''
    description = ' '.join([row['Category'],row['Description']])
    category = identify(description)
    values = [row['Transaction Date'],
              row['Amount'],
              description,
              'Chase Sapphire',
              category,
              '']                         # notes
    return dict(zip(out_keys, values))

# dictionary of account names and conversion function
row_parser = {'schoolsfirst':make_schoolsfirst_dict,
              'sapphire':make_sapphire_dict}

# dictionary of CSV header. TODO: move this else where (maybe in a db)
csv_headers = {}
csv_headers['bofa'] = ['Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount']
csv_headers['citi'] = ['Status', 'Date', 'Description', 'Debit', 'Credit', 'Member Name']
csv_headers['discover'] = ['Trans. Date', 'Post Date', 'Description', 'Amount', 'Category']
csv_headers['amzn'] = ['Transaction Date', 'Post Date', 'Description', 'Category', 'Type', 'Amount']
csv_headers['sapphire'] = ['Transaction Date', 'Post Date', 'Description', 'Category', 'Type', 'Amount', 'Memo']
csv_headers['schoolsfirst'] = ['Transaction Date', 'Check#', 'Category', 'Amount', 'Description', 'Check Description', 'Balance', 'Available Balance', 'Effective Date', 'Penalty', 'Previous Available Balance', 'Fee']

def import_statement(account, input_path, output_path):
    classifier = classification()
    with open(input_path, 'r') as fin_csv, open(output_path, 'w') as fout_csv:
        # DictReader uses first line in file for column headings by default
        orig_data = csv.DictReader(fin_csv) 
        updated_data = csv.DictWriter(fout_csv, fieldnames=out_keys)
        
        # continue if CSV headers match
        assert csv_headers[account] == orig_data.fieldnames

        # read in all data
        # check for duplicates and mark them as needed
        # is dup if date, amount, and description are repeated
        for row in orig_data:
            updated_row = row_parser[account](row, classifier.identify)
            updated_data.writerow(updated_row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--institution',
            help = 'institution generated csv statement')
    parser.add_argument('-c', '--input_path',
            help = 'path to institution generated csv file')
    parser.add_argument('-o', '--out',
            help = 'output csv')
    parser.add_argument('-t', '--test', action='store_true',
            help = 'parse file without updating database')
    args = parser.parse_args()

    institution = args.institution
    input_path = os.path.expanduser(args.input_path)
    out = os.path.expanduser(args.out)
    import_statement(institution, input_path)
