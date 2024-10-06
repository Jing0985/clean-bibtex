# About: clean and process bibtex files
# Author: hjx
# Time: 2024-04-15

# %%
# pip install bibtexparser --pre
# please note the version may change as time goes by
# cf. https://github.com/sciunto-org/python-bibtexparser?tab=readme-ov-file

import bibtexparser 
from collections import Counter


# %%
# cf. https://bibtexparser.readthedocs.io/en/main/quickstart.html#step-1-parsing-with-defaults
# replace the file name with your own file name

library = bibtexparser.parse_file("miko_mendeley_raw.bib")

# %%
# check errors
# drop duplicates

distinct_keys = set()
distinct_entries = []

for entry in library.entries:
    key = entry["ID"]
    if key not in distinct_keys:
        distinct_keys.add(key)
        distinct_entries.append(entry)

# get the key of the failed blocks

if len(library.failed_blocks) > 0:
    failed_blocks = library.failed_blocks
    if failed_blocks:
        print("Failed to parse the following blocks:")
        for block in failed_blocks:
            # Access the ID (entry key) of the failed block
            failed_entry_id = block.key
            print("Failed block ID:", failed_entry_id)
    else:
        print("All blocks parsed successfully.")
else:
    print("No failed blocks found.")

# %%
#distinct_entries_bib = [dict(t) for t in {tuple(d.items()) for d in distinct_entries}]
# create a new bib file with distinct entries

with open('miko_mendeley_distinct.bib', 'w') as bibfile:
    for entry in distinct_entries:
        bibfile.write('@' + entry.entry_type + '{' + entry.key + ',\n')
        for key, value in entry.items():
            if key not in ['ENTRYTYPE', 'ID']:
                bibfile.write('    ' + key + ' = {' + value + '},\n')
        bibfile.write('}\n\n')


# %%
# parse the distinct bib file
distinct_bib = bibtexparser.parse_file("miko_mendeley_distinct.bib")

# check entry_type 

def print_entry_type_num(entry):
    '''
    print the number of each entry type of a bibtex
    '''
    print('total number of entries:', len(entry.entries))

    entry_types = []
    for entry in entry.entries:
        entry_types.append(entry.entry_type)

    counts = Counter(entry_types)
    for key, value in counts.items():
        print(key, value)

        #return key, value

print_entry_type_num(distinct_bib)

# %%
# write the change to the bib file "working.bib"

with open('working.bib', 'w') as bibfile:
    for entry in distinct_bib.entries:
        bibfile.write('@' + entry.entry_type + '{' + entry.key + ',\n')
        for key, value in entry.items():
            if key not in ['ENTRYTYPE', 'ID']:
                bibfile.write('    ' + key + ' = {' + value + '},\n')
        bibfile.write('}\n\n')

# %%
# load finnal cleaned bib file

distinct_bib_final = bibtexparser.parse_file("working.bib")
print_entry_type_num(distinct_bib_final)

# %%
# change entries and write to the existing bib file

# essential fields based on Email from MiKo and APA7 style
essential_fields_article = ['author', 'year', 'title', 'journal', 'volume', 'issue', 'pages', 'doi']
essential_fields_book = ['author', 'year', 'title', 'edition', 'volume', 'publisher', 'doi', 'url']
essential_fields_inbook_inproceedings = ['author', 'year', 'title', 'editor', 'journal', 'edition', 'volume', 'pages', 'publisher', 'doi', 'url']
essential_fields_misc = ['author', 'year', 'title', 'journal', 'month', 'day', 'url', 'urldate']

# check if the essential fields are in the first entry
def add_essential_fields(entry, essential_fields):
    '''
    add the essential fields to the entry
    '''
    for field in essential_fields:
        if field not in entry:
            if field == 'urldate':
                entry[field] = '2024-06-05'
            else:
                entry[field] = ''
        else:
            print(field, 'in the entry')

for entry in distinct_bib.entries:

    if entry['ENTRYTYPE'] == 'article':
        add_essential_fields(entry, essential_fields_article)

    elif entry['ENTRYTYPE'] == 'book':
       add_essential_fields(entry, essential_fields_book)

    elif entry['ENTRYTYPE'] == 'inbook' or entry['ENTRYTYPE'] == 'inproceedings':
       add_essential_fields(entry, essential_fields_inbook_inproceedings)
    
    elif entry['ENTRYTYPE'] == 'misc':
         add_essential_fields(entry, essential_fields_misc)
   
    else:
        print(entry['ENTRYTYPE'])



# %%
# load the working bib file
working_dev_bib = bibtexparser.parse_file("working.bib")
print_entry_type_num(working_dev_bib)

# %%
print(bibtexparser.__version__)
# %%
