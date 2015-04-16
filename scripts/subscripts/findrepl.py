# Find & replace elements of the LyX source.
# Part of the pLyX.py system.
#
# findrepl.py
#
# Andrew Parsloe (aparsloe@clear.net.nz) 15 January 2014
#

import argparse, re, sys

re_squash = re.compile(r'\n\n+')
re_backslash = re.compile(r'\n?\\backslash\n')
re_lyxcmds = re.compile(r'\\\w+')

flex_fr = r'\begin_inset Flex .find-&-repl'
flex_arg = r'\begin_inset Flex .[argument]'
begin_layout = r'\begin_layout'
end_layout = r'\end_layout'
begin_std = r'\begin_layout Standard'
begin_inset = r'\begin_inset'
end_inset = r'\end_inset'
begin_inline = r'\begin_inset Formula $'
begin_formula = r'\begin_inset Formula'
begins = r'\begin'
end_body = r'\end_body'
end_document = r'\end_document'
ends = r'\end'
backslash = r'\backslash'

begin_msg = r'''\begin_inset Note Note
status open
\begin_layout Plain Layout
'''
end_msg = r'''
\end_layout
\end_inset
'''

lyxcmds = [r'\\begin_', r'\\end_', r'\\emph ', r'\\family ', r'\\series ',
           r'\\shape ', r'\\size ', r'\\noun ', r'\\color ', r'\\lang ',
           r'\\labelwidthstring', r'\\align ', r'\\noindent ', r'\\strikeout ',
           r'\\bar under', r'\\uuline ', r'\\uwave ', r'\\no_bar',
           r'\\no_emph', r'\\no_noun', r'\\no_strikeout', r'\\no_uuline',
           r'\\no_uuline', r'\\no_uwave']
lyxcmdd = [r'\\\\begin_', r'\\\\end_', r'\\\\emph ', r'\\\\family ',
           r'\\\\series ', r'\\\\shape ', r'\\\\size ', r'\\\\noun ',
           r'\\\\color ', r'\\\\lang ', r'\\\\labelwidthstring', r'\\\\align ',
           r'\\\\noindent ', r'\\\\strikeout ', r'\\\\bar under',
           r'\\\\uuline ', r'\\\\uwave ', r'\\\\no_bar', r'\\\\no_emph',
           r'\\\\no_noun', r'\\\\no_strikeout', r'\\\\no_uuline',
           r'\\\\no_uuline', r'\\\\no_uwave']

######################################################
def main(infl, outfl, options, guff):

    def strip_outers(stuff):
        '''Strip enclosing layout statements.'''
        stuff = stuff.partition('\n')[2]
        stuff = stuff.rpartition(end_layout)[0]
        return stuff
        
    def inset_contents():
        '''Get contents of inset minus LyX paragraphing.'''
        
        contents = lines = ''
        layouts, insets = 0, 1
        status = True
        newpara = False

        for line in infl:
            lines += line
            if line == '\n':
                continue
            elif status:
                if begin_layout in line:
                    status = False
                    layouts = 1
            elif begin_layout in line:
                # exclude LyX paragraphing of contents
                layouts += 1
                if layouts > 1:
                    contents += line + '\n'
                else:
                    newpara = True
            elif begin_inset in line:
                insets += 1
                contents += line
            elif backslash in line:
                if newpara:
                    contents += '\n' + line
                else:
                    contents += line
            elif end_layout in line:
                newpara = False
                # exclude LyX paragraphing of contents
                if layouts > 1:
                    contents += line
                layouts -= 1
            elif end_inset in line:
                newpara = False
                insets -= 1
                if insets == 0:
                    return contents, lines
                else:
                    contents += line
            else:
                newpara = False
                contents += line
                    
    def math_contents(formline):
        '''Get contents of math inset.'''
        
        contents = lastlines = ''
        beginnings = 1
        firstlines = formline
        
        for line in infl:
            if line == '\n':
                continue
            elif (begins in line) or (r'\[' in line):
                beginnings += 1
                if beginnings > 2:
                    contents += line
                else:
                    firstlines += line
            elif (ends in line) or ('\]' in line):
                beginnings -= 1
                if beginnings > 2:
                    contents += line
                else:
                    lastlines += line
                    if beginnings == 0:
                        return contents, firstlines, lastlines
            else:
                contents += line
                
    def write_msg(msg):
        '''Write a yellow note error message'''
        outfl.write(begin_msg)
        outfl.write(msg)
        outfl.write(end_msg)

    def write_last_count(flines, count, suppress):
        if not suppress:
            temp = iter(flines.splitlines(True))
            for line in temp:
                if end_body in line:
                    outfl.write(begin_std + '\n')
                    write_msg(count_msg(count))
                    outfl.write(end_layout + '\n')
                outfl.write(line)
        else:
            outfl.write(flines)
        for line in infl:
            outfl.write(line)

    def count_msg(count):
        '''Build occurrence/replacement message.'''
        if (textmode or mathmode) and count > 0:
            msg = 'At least '
        else:
            msg = ''
        msg += str(count) + ' '
        msg += 'replacement'
        if count != 1:
            msg += 's'
        msg += ' of "' + find0 + '" by "' + repl0 + '"\n'

        return msg

    def re_flags(params):
        '''Return reg. exp. flag value.'''
        fgs = count = 0
        for char in params.upper():
            if char == 'I': # ignorecase
                fgs = fgs|re.I
            elif char == 'L': # locale
                fgs = fgs|re.L
            elif char == 'M': # mulitline
                fgs = fgs|re.M
            elif char in 'SD': # dotall
                fgs = fgs|re.S
            elif char == 'U': # unicode
                fgs = fgs|re.U
            elif char.isdigit():
                count = 10*count + int(char)
        return fgs, count

    def doublebs(strng):
        for term in lyxcmds:
            tmp = re.sub(r'\\' + term, r'\\\\' + term, strng)
        return tmp
    ######################################################                
    # write the prelims
    outfl.write(guff)
    guff = ''

    # get the options
    parser = argparse.ArgumentParser(description='Find & replace')

    parser.add_argument('-i', dest = 'inset', action ='store_true', \
                        default = False, help='Restricted inset search (settings only)')
    parser.add_argument('-m', '--math', dest = 'math', action ='store_true', \
                        default = False, help='Search math insets only')
    parser.add_argument('-t', '--text', dest = 'text', action ='store_true', \
                        default = False, help='Search text only (incl. inset text)')
    parser.add_argument('-x', dest = 'xclude', action ='store_true', \
                        default = False, help='Restrict search scope')
    
    parser.add_argument('-r', '--regexp', dest = 'regx', action ='store_true', \
                        default = False, help='Use regular expressions')
    parser.add_argument('-s', '--suppress', dest = 'suppress_msgs', action ='store_true', \
                        default = False, help='Suppress replacement messages')
    
    parser.add_argument('--placeholder', action='store', default = '#', \
                        help='Placeholder for find string when looping')
    parser.add_argument('--loop', action='store_true', default = False, \
                        help='Loop boolean')


    args = parser.parse_args(options)

    regexp = args.regx
    suppress = args.suppress_msgs
    if args.loop:
        datalen = 1
    else:
        datalen = 0

    lines = flines = params = ''
    count = status = insets = 0
    finding = changing = False
    stack = [1]
    last = 1

    for line in infl:
        if line in '\n':
            continue
        # scanning text, looking for f-&-r inset
        elif status == 0:
            if flex_fr in line:
                if finding:
                    if not mathmode:
                        outfl.write(flines)
                        flines = ''
                    if textmode and exclude:
                        write_msg('This search is unimplemented currently!')
                    # show count & turn off current search
                    if not args.suppress_msgs:
                        msg = count_msg(count)
                        write_msg(msg)
                    count = 0
                    finding = False
                outfl.write(line)
                params, temp = inset_contents()
                outfl.write(temp)
                status += 1
                
                if '-r' in params:
                    regexp = True
                    params = re.sub(r'\-\-regexp', '', params)
                    params = re.sub(r'\-r', '', params)
                else:
                    regexp = args.regx
                                
                if '-x' in params:
                    exclude = True
                    params = re.sub(r'\-e', '', params)
                else:
                    exclude = args.xclude

                if '-t' in params:
                    textmode = True
                    mathmode = False
                    params = re.sub(r'\-\-text', '', params)
                    params = re.sub(r'\-t', '', params)
                    if '-i' in params:
                        insetmode = True
                        mathmode = exclude = False
                        params = re.sub(r'\-\-inset', '', params)
                        params = re.sub(r'\-i', '', params)
                    else:
                        insetmode = args.inset
                elif '-i' in params:
                    insetmode = exclude = True
                    textmode = mathmode = False
                    params = re.sub(r'\-\-inset', '', params)
                    params = re.sub(r'\-i', '', params)
                elif '-m' in params:
                    mathmode = True
                    textmode = insetmode = False
                    params = re.sub(r'\-\-math', '', params)
                    params = re.sub(r'\-m', '', params)
                else:
                    textmode = args.text
                    mathmode = args.math
                    insetmode = args.inset
                
            elif finding:
                # mathmode but exclude control seq. & labels
                if mathmode and exclude:
                    if begin_inline in line:
                        outfl.write(begin_inline)
                        temp = re.split(r'(\\\w+)', line.split('$')[1])
                        flines = ''
                        for subline in temp:
                            if re_lyxcmds.match(subline):
                                flines += subline
                            elif (not regexp and find in subline) or \
                                 (regexp and re_find.search(subline)):
                                count += 1
                                if regexp:
                                    flines += re_find.sub(repl, subline)
                                else:
                                    flines += subline.replace(find, repl)
                            else:
                                flines += subline
                        outfl.write(flines)
                        flines = ''
                        outfl.write('$')
                    elif begin_formula in line:
                        lines, opening, closing = math_contents(line)
                        outfl.write(opening)
                        temp = re.split(r'(\\\w+)', lines)
                        flines = ''
                        label = False
                        for subline in temp:
                            if re.match(r'\\label', subline):
                                flines += subline
                                label = True
                            elif label:
                                flines += subline
                                label = False
                            elif re_lyxcmds.match(subline):
                                flines += subline
                            elif (not regexp and find in subline) or \
                                 (regexp and re_find.search(subline)):
                                count += 1
                                if regexp:
                                    flines += re_find.sub(repl, subline)
                                else:
                                    flines += subline.replace(find, repl)
                            else:
                                flines += subline
                        outfl.write(flines)
                        flines = ''
                        outfl.write(closing)
                    else:
                        if end_body in line:
                            write_last_count(line, count, suppress)
                        else:
                            outfl.write(line)
                            
                # math mode, no excluding            
                elif mathmode:
                    if begin_inline in line:
                        outfl.write(begin_inline)
                        flines = line.split('$')[1]
                        if (not regexp and find in flines) or \
                             (regexp and re_find.search(flines)):
                            count += 1
                            if regexp:
                                outfl.write(re_find.sub(repl, flines))
                            else:
                                outfl.write(flines.replace(find, repl))
                        else:
                            outfl.write(flines)
                        outfl.write('$')
                    elif begin_formula in line:
                        flines, opening, closing = math_contents(line)
                        outfl.write(opening)
                        if (not regexp and find in flines) or \
                             (regexp and re_find.search(flines)):
                            count += 1
                            if regexp:
                                outfl.write(re_find.sub(repl, flines))
                            else:
                                outfl.write(flines.replace(find, repl))
                        else:
                            outfl.write(flines)
                        outfl.write(closing)
                    else:
                        if end_body in line:
                            write_last_count(line, count, suppress)
                        else:
                            outfl.write(line)

                # text mode, inclusive -t
                # text in insets only -t -i
                # text not in insets -t -x
                elif textmode:
                    if begin_layout in line:
                        last = 1
                        outfl.write(line)
                        flines = ''
                    elif begin_inset in line:
                        stack.append(last)
                        last = 0
                        insets += 1
                        outfl.write(flines + '\n')
                        flines = ''
                        outfl.write(line)
                    elif end_inset in line:
                        last = stack.pop()
                        insets -= 1
                        outfl.write(line)
                    elif end_layout in line:
                        last = 0
                        outfl.write(flines + '\n')
                        outfl.write(line)
                        flines = ''
                    elif end_body in line:
                        write_last_count(line, count, suppress)
                    elif last == 0:
                        outfl.write(line)
                    elif last == 1 and re_lyxcmds.match(line):
                        outfl.write(flines + '\n')
                        flines = ''
                        outfl.write(line)
                    else:
                        # last == 1 & not lyxcmd
                        # text in & out insets
                        # or text in insets
                        # or text not in insets
                        if not (insetmode or exclude) \
                           or (insetmode and insets > 0) \
                           or (exclude and insets == 0):
                            flines = flines.rstrip()
                            flines += line
                            if (not regexp and find in flines) or \
                                 (regexp and re_find.search(flines)):
                                count += 1
                                if regexp:
                                    temp = re_find.sub(repl, flines)[:-1].rpartition('\n')
                                else:
                                    temp = flines.replace(find, repl)[:-1].rpartition('\n')
                                outfl.write(temp[0])
                                flines = temp[2]
                        else:
                            outfl.write(line)

                # inset mode (= inset settings), exclude text 
                # (inset mode with no excluding, not implemented)
                elif insetmode:
                    if begin_formula in line:
                        last = 2
                        outfl.write(flines)
                        flines = ''
                        outfl.write(line)
                    elif begin_inset in line:
                        stack.append(last)
                        last = 0
                        outfl.write(line)
                    elif begin_layout in line:
                        last = 1
                        outfl.write(flines)
                        outfl.write(line)
                        flines = ''
                    elif end_inset in line:
                        if last == 0: # not math inset
                            outfl.write(flines)
                        outfl.write(line)
                        flines = ''
                        if last == 2: # math inset
                            last = 1
                        else:
                            last = stack.pop()
                    elif end_layout in line:
                        outfl.write(line)
                        last = 0
                    elif end_body in line:
                        write_last_count(line, count, suppress)
                    elif last == 1:
                         outfl.write(line)
                    else: # last == 0
                        flines += line
                        lenf += 1
                        if (not regexp and find in flines) or \
                             (regexp and re_find.search(flines)):
                            count += 1
                            if regexp:
                                outfl.write(re_find.sub(repl, flines))
                            else:
                                outfl.write(flines.replace(find, repl))

                            flines = ''
                            lenf = 0
                        else:
                            if lenf >= flenmax:
                                temp = flines.partition('\n')
                                flines = temp[2]
                                outfl.write(temp[0] + '\n')
                                lenf -= 1
                                
                # default mode, everything, no excluding        
                else:
                    flines += line
                    lenf += 1
                    if end_body in line:
                        write_last_count(flines, count, suppress)
                    elif (not regexp and find in flines) or \
                         (regexp and re_find.search(flines)):
                        count += 1
                        if regexp:
                            outfl.write(re_find.sub(repl, flines))
                        else:
                            outfl.write(flines.replace(find, repl))

                        flines = ''
                        lenf = 0
                    else:
                        if lenf >= flenmax:
                            temp = flines.partition('\n')
                            flines = temp[2]
                            outfl.write(temp[0] + '\n')
                            lenf -= 1
 
            # otherwise write to file
            else:
                outfl.write(line)

        # looking for an argument inset (find)
        elif status == 1:
            outfl.write(line)
            if flex_arg in line:
                find0, temp = inset_contents()
                outfl.write(temp)
                find = re_backslash.sub(r'\\', find0).strip()
                find = re_squash.sub('\n', find)
                if regexp and not (textmode or mathmode or insetmode):
                    for i in range(len(lyxcmds)):
                        find = re.sub(lyxcmds[i], lyxcmdd[i], find)
                if find == '' and finding == False:
                    write_msg('Nothing to find!')
                    status -= 1
                elif find == '' and finding == True:
                    # turn off current search
                    finding = False
                    status -= 1
                else:
                    if not args.loop:
                        re_find = re.compile(find, flags = re_flags(params)[0])
                    finding = True
                    # check for replace inset
                    status += 1
                    repl = ''
            else:
                status -= 1
                finding = False
           
        # looking for an argument inset (replace)
        elif status == 2:
            outfl.write(line)
            # get replacement string
            if flex_arg in line:
                repl0, temp = inset_contents()
                outfl.write(temp)
                repl = re_backslash.sub(r'\\', repl0).strip()
                repl = re.sub(r'\\n', r'\n', repl)
                if regexp and not (mathmode or (insetmode and exclude)):
                    for i in range(len(lyxcmds)):
                        repl = re.sub(lyxcmds[i], lyxcmdd[i], repl)
                if textmode:
                    repl += '\n\n'
                if args.loop:
                    if datalen > 0:
                        status += 1
                else:
                    status = 0
            else:
                # no replacement inset
                outfl.write(begin_std + '\n')
                write_msg('Replace "' + find0 + '" with what?')
                outfl.write(end_layout)
                finding = False
                status = 0
            
            flines = ''
            lenf = 0
            flen = len(find.splitlines(True))
            flenmax = max(re_flags(params)[1], flen)

        # looking for an argument inset (data list)
        elif status == 3:
            if flex_arg in line:
                outfl.write(line)
                data0, temp = inset_contents()
                data = data0.strip('\n')
                datalist = data.split('\n')
                findrepl = datalist[0].split(args.placeholder)
                find0 = findrepl[0]
                if len(findrepl) == 2:
                    repl0 = findrepl[1]
                else:
                    repl0 = find0
                find = re.sub(args.placeholder, find0, find)
                repl = re.sub(args.placeholder, repl0, repl)
                datalen = len(datalist[1:])
                outfl.write('status open\n')
                for itm in datalist[1:]:
                    if len(itm) > 0:
                        outfl.write(begin_layout + ' Plain Layout\n')
                        outfl.write(itm + '\n')
                        outfl.write(end_layout + '\n')
                                    
                outfl.write(end_inset + '\n')
                
            re_find = re.compile(find, flags = re_flags(params)[0])           
            status = 0
            
    if datalen > 1:
        return 2
    else:
        return 1



                
                
            
            
    
