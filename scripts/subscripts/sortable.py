# Sort the rows of a table according to values in specified
# columns. Part of the pLyX system; not an independent script.
#
# sortable.py
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
import re, argparse
from operator import itemgetter

def main(infl, outfl, opts, guff):
    '''Sort table rows according to the values in specified columns'''
    
    # no change to LyX header material required
    outfl.write(guff)
    guff = ''
    
    # parse options; this is unnecessarily complicated but it allows
    # for additions to the option list
    parser = argparse.ArgumentParser(description = 'Sort notes?', version = '1.0')

    parser.add_argument('-n', '--notes', dest='n', action ='store_true', \
                    default = False, help="Makes LyX's (e.g. yellow) notes sortable")
    sort_notes = parser.parse_args(opts).n

    flex_sortable = r'\begin_inset Flex .sort table'
    row_start = r'<row'
    cell_start = r'<cell'
    cell_end = r'</cell>'
    row_end = r'</row>'
    table_end = r'</lyxtabular>'
    re_lyxcmds = re.compile(r'(\\\w+)|(status (open|collapsed))')
    begin_inset = r'\begin_inset'
    end_inset = r'\end_inset'
    begin_text = r'\begin_inset Text'
    bottom = r'bottom'
    botline = r'bottomline="true" '
    topline = r'topline="true" '

    # table_status
    # -1 = read & write lines unaltered; 0 = no marker yet; 1 = get sort spec;
    # 2 = find next row; 3 = this row; 4 = this cell; 5 = ERT|Note inset
    table_status = 0
    current_row = ''
    rows = []
    
    for line in infl:
        if table_status == 0:   #no marker yet
            outfl.write(line)
            if flex_sortable in line:
                table_status += 1
                sort_spec = ''
                insets = 1
        
        elif table_status == 1: #get sort spec
            outfl.write(line)
            if begin_inset in line:
                insets += 1
            elif end_inset in line:
                columns = re.findall(r'\d+',sort_spec)
                colsorts = re.findall(r'[-+AZaz]',sort_spec)
                numsorts =  len(columns)
                qeys = ['' for i in range(numsorts)]
                updn = [False for i in range(numsorts)]
                # reverse order since primary sort is last one done
                cols = [int(columns[numsorts-i-1]) for i in range(numsorts)]
                sort_type = [colsorts[numsorts-i-1] for i in range(numsorts)]
                insets -= 1
                table_status += 1   
            elif re_lyxcmds.search(line):
                continue
            else:
                sort_spec += line.strip()
            
        elif table_status == 2: # find next row
            if row_start == line[:4]:
                current_row = line
                colnum = 0
                table_status += 1
            # end of table
            elif table_end in line:
                for i in range(numsorts):
                    rows.sort(key=itemgetter(i), reverse = updn[i])
                numrows = len(rows)
                r = 0
                for item in rows:
                    r += 1
                    if r == numrows:
                        # restore the bottom hrule
                        item[numsorts] = item[numsorts].replace(topline, topline + botline)
                    outfl.write(item[numsorts])
                outfl.write(line)
                table_status = 0
                current_row = ''
                rows = []
            else:
                outfl.write(line)
            
        elif table_status == 3: # this row
            if cell_start == line[:5]:
                colnum += 1
                if bottom in line:
                    line = line.replace(botline, '') # del bottom hrule
                current_row += line
                if colnum in cols:
                    table_status += 1
                    qey = ''
            elif row_end == line[:6]:
                current_row += line
                table_status -= 1
                rows.append(qeys + [current_row])
            else:
                current_row += line

        elif table_status == 4:  # this cell
            current_row += line
            if cell_end == line[:7]:
                c = -1
                for i in range(cols.count(colnum)):
                    # in case same col. sorted more than once
                    c = cols.index(colnum, c + 1)
                    if sort_type[c] in 'az':
                        qeys[c] = qey.lower()
                    elif  sort_type[c] in 'AZ':
                        qeys[c]= qey
                    elif sort_type[c] in '+-':
                        qeys[c]= float(qey)
                    if  sort_type[c] in 'zZ-':
                        updn[c] = True # reverse order
                table_status -= 1
            elif begin_inset in line:
                if 'Text' in line:
                    continue
                elif sort_notes and 'Note Note' in line:
                    continue
                else:
                    table_status += 1
                    insets = 1
            elif re_lyxcmds.match(line):
                continue
            else:
                qey += line.strip()
                
        elif table_status == 5: # ert inset
            current_row += line
            if begin_inset in line:
                insets += 1
            elif end_inset in line:
                insets -= 1
                if insets == 0:
                    table_status -= 1

        else:
            outfl.write(line)
            
    return 1
