#!/usr/bin/env python3
from collections import defaultdict
import re



def create_activity_link(link):
    '''
    Entry format is:
    day, name, link
    '''
    out = link[0]
    out += ': ' + create_link(link[1:])

    return out


def create_lecture_link(links):
    '''
    Entry format is:
    text, video link (optional), slides link (optional), files link (optional)

    Any entries beyond those are treated as name/address pairs
    (i.e., they will be written out in README as [name](address))
    '''
    order = ('video', 'slides', 'files')

    out = links[0]
    for i in range(len(order)):
        if len(links) > i + 1 and len(links[i + 1]) > 0:
            out += ' ' + create_link((order[i], links[i + 1]))

    for i in range(len(order) + 1, len(links), 2):
        name = links[i]
        addr = links[i + 1]
        out += ' ' + create_link((name, addr))

    return out


def create_link(link):
    '''
    Entry format is:
    text, link (optional), additional text (optional)
    '''
    if len(link) > 1 and len(link[1]) > 0:
        out = '[%s](%s)' % link[:2]
    else:
        out = str(link[0])

    if len(link) > 2:
        out += ' -- %s' % ', '.join(link[2:])

    return out


def create_comma_list(parts):
    return ','.join(parts)


def gen_week_number(week):
    start = '|  '
    end = '  '
    if len(week) < 2:
        week = '0' + str(week)

    return start + week + end


def gen_zero_padded_date(date_str):
    date_parts = date_str.split('/')
    for i in range(len(date_parts)):
        if len(date_parts[i]) == 1:
            date_parts[i] = '0' + str(date_parts[i])
    return '/'.join(date_parts)


def gen_date_range(week_dates):
    start = '|  '
    end = '  | '
    zero_padded_dates = map(gen_zero_padded_date, week_dates[0])

    return start + ' - '.join(zero_padded_dates) + end


def gen_headings(data):
    headings = list(data['Headings'].keys())
    first_line = '| ' + ' | '.join(headings) + ' |\n'
    second_line = re.sub('[a-zA-Z0-9]', '-', first_line)
    return first_line + second_line


def gen_activities_from_data(data, week, category, sep=' <br> '):
    return gen_from_data(data, week, category, sep, processor=create_activity_link)


def gen_lectures_from_data(data, week, category, sep=' <br> '):
    return gen_from_data(data, week, category, sep, processor=create_lecture_link)


def gen_strings_from_data(data, week, category, sep=' <br> '):
    return gen_from_data(data, week, category, sep, processor=create_comma_list)


def gen_from_data(data, week, category, sep, processor):
    week = str(week)
    all_links = data[category][week]
    out = []
    for link in all_links:
        out.append(processor(link))
    return sep.join(out)


heading_symbol = '>'
comment_symbol = '#'
data_file_name = '.readme-data.txt'
delimiter = ','
base_fname = '.base-readme.md'
output_fname = 'README.md'

'''
Read data into single dictionary of dictionaries of tuples:
{'Activities': {'0': (activities, ...), '1': (...), ...},
 'Topics': {'0': ...}
 ...
}
'''
current_heading = None
data = defaultdict(lambda : defaultdict(list))
with open(data_file_name, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith(heading_symbol):
            current_heading = line[1:].strip()
        elif line.startswith(comment_symbol):
            pass
        elif len(line) != 0:
            split_line = [s.strip() for s in line.split(delimiter)]
            week = split_line[0]
            data[current_heading][week].append(tuple(split_line[1:]))

'''
Build html/markdown from csv by
* going week by week
* within a given week, creating each column separately and then joining them

Each column (topics, activities, etc.) is generally a list of things,
but the items in the list are formatted differently.
Write a function to process an individual "thing" (usually create_*) for a
particular column,
then use the generic gen_from_data to generate the whole column for the week.
'''
schedule = gen_headings(data)
for week in data['Weeks'].keys():
    dates = gen_date_range(data['Weeks'][week])
    topics = gen_lectures_from_data(data, week, 'Topics')
    activities = gen_activities_from_data(data, week, 'Activities')
    todos = gen_strings_from_data(data, week, 'Activities')

    schedule += gen_week_number(week) + \
                dates + \
                ' | '.join([topics, activities, todos]) + \
                ' |\n'

with open(base_fname, 'r') as f:
    base = f.read()

with open(output_fname, 'w') as f:
    f.write(base + schedule)
