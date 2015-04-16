#!/usr/bin/env python
# encoding: utf-8

import re, argparse, os, sys
import xlrd
import getpass
import datetime
from collections import Counter
begin_msg = r'''\begin_inset Note Note
status open
\begin_layout Plain Layout
'''
end_msg = r'''
\end_layout
\end_inset
'''
begin_stats_msg = r'''\begin_layout Standard
\begin_inset Note Note
status open
'''
end_stats_msg = r'''\end_inset
\end_layout
'''
flex_update = r'\begin_inset Flex .update citations'
flex_arg = r'\begin_inset Flex .[argument]'
citation_begin = r'\begin_inset CommandInset citation'
begin_layout = r'\begin_layout'
end_layout = r'\end_layout'
begin_inset = r'\begin_inset'
end_inset = r'\end_inset'
end_body = r'\end_body'
backslash = r'\backslash'
re_lyxcmds = re.compile(r'\\\w+ \w+')


def main(infl, outfl, opts, guff):
    '''Update the bibliography citations keys based on excel file provided'''
    def inset_contents():
        '''Get contents of inset minus formatting.'''
        contents = ''
        layouts, insets = 0, 1
        for line in infl:
            outfl.write(line)
            if line == '\n':
                continue
            elif begin_layout in line:
                # exclude first occurrence of \begin_layout
                layouts += 1
                if layouts > 1:
                    contents += line
            elif begin_inset in line:
                insets += 1
                contents += line
            elif end_layout in line:
            # exclude last occurrence of \end_layout
                if layouts > 1:
                    contents += line
                layouts -= 1
            elif end_inset in line:
                insets -= 1
                if insets == 0:
                    return contents
                else:
                    contents += line
            elif re_lyxcmds.match(line):
                continue
            else:
                if layouts > 0:
                    contents += line

    def write_stats_note():
        outfl.write(begin_stats_msg)
        outfl.write(begin_layout + ' Plain Layout\n')
        outfl.write('This note is auto-generated with script "update citations" under user "%s" on %s. \n'
            'Below are old keys and # of times it has been replaced:\n' % (
                getpass.getuser(), datetime.datetime.utcnow()
            )
        )
        outfl.write(end_layout + '\n')
        for key in count_updated_keys:
            outfl.write(begin_layout + ' Plain Layout\n')
            outfl.write('%s - %s' % (key, count_updated_keys[key]) + '\n')
            outfl.write(end_layout + '\n')
        outfl.write(end_stats_msg)

    def citation_inset_update():
        outfl.write(infl.next())
        key_line = infl.next()
        m = re.match(r'key "(.*)"', key_line)
        keys = [key.strip() for key in m.group(1).split(',')]
        updated_keys = [
            key if key not in citation_keys else citation_keys[key]
            for key in keys
        ]
        count_updated_keys.update([key for key in keys if key in citation_keys])
        new_key_line = 'key "%s"' % ','.join(updated_keys)
        outfl.write(new_key_line)

    def read_citation_keys(excel_file):
        if not os.path.exists(excel_file.strip()):
            errors.append("Excel file '%s' can't be opened" % excel_file)
            return {}
        book = xlrd.open_workbook(excel_file)
        sheet = book.sheets()[0]
        old_keys = sheet.col_values(0)[1:]
        new_keys = sheet.col_values(1)[1:]
        if len(old_keys) != len(new_keys):
            errors.append('Number of cells in two first columns of file % are not equal' % excel_file)
            return {}
        d = {old_key.strip(): new_key.strip() for (old_key, new_key) in
             zip(old_keys, new_keys)}
        return d

    def write_msg(msg):
        '''Write a yellow note error message'''
        outfl.write(begin_msg)
        outfl.write(msg)
        outfl.write(end_msg)

    outfl.write(guff)
    guff = ''
    parser = argparse.ArgumentParser(description='Update citations')

    parser.add_argument(
        '-s', '--suppress', action='store_true',
        default=False, help='Suppress replacement messages'
    )
    args = parser.parse_args(opts)
    errors = []
    citation_keys = {}
    count_updated_keys = Counter()
    waiting_for_argument = False
    for line in infl:
        # flex_update found, need to wait for argument
        if flex_update in line:
            waiting_for_argument = True
            outfl.write(line)
            # skip contents of flex_update
            inset_contents()
        # empty line
        elif len(line.strip()) == 0:
            continue
        # found argument with name of excel file
        elif (flex_arg in line) and waiting_for_argument:
            outfl.write(line)
            excel_file = inset_contents()
            citation_keys.update(read_citation_keys(excel_file.strip()))
            while errors:
                write_msg(errors.pop())
            waiting_for_argument = False
        # no argument after flex_update
        elif waiting_for_argument:
            write_msg("Please provide excel file as an argument (use .[Argument] inset).")
            outfl.write(line)
            waiting_for_argument = False
        # citation found
        elif citation_begin in line:
            outfl.write(line)
            citation_inset_update()
        # end_of_file
        elif end_body in line:
            break
        else:
            outfl.write(line)
    print count_updated_keys
    if len(count_updated_keys) > 0 and not args.suppress:
        write_stats_note()
    outfl.write(line)
    outfl.write(infl.next())
