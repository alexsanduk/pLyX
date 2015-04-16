# Word frequency counter. Part of the pLyX 
# system; not an independent script.
#
# wordfreq.py
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
#################################################
import re, argparse, os.path, sys
from operator import itemgetter


# LyX commands
re_lyxcmds = re.compile(r'\\\w+')

begin_inset = r'\begin_inset'
end_inset = r'\end_inset'
begin_plain = '\\begin_layout Plain Layout\n'
begin_std = '\\begin_layout Standard\n'
end_layout = '\\end_layout\n'
end_body = r'\end_body'

def para_contents(iterable):
        '''Get contents of paragraph with no formatting.'''
        
        text = lines = ''
        insets = 0
        status = True
        for line in iterable:
            lines += line
            # lose empties & status line
            if line == '\n':
                continue
            elif begin_inset in line:
                insets += 1
            elif end_inset in line:
                insets -= 1
            elif insets > 0:
                continue
            elif end_layout == line:
                return text, lines
            elif re_lyxcmds.match(line):
                continue
            else:
                text += line

  
def main(infl, outfl, opts, guff):
    '''Determine the frequency of words or phrases.'''

    wdict = {}
        
    parser = argparse.ArgumentParser(description = 'Word frequency options')

    parser.add_argument('--alpha', dest='a', action='store_true',\
                    default = False, help="Sort words alphab. (default: word length)")
    parser.add_argument('--num', dest='n', action='store_true',\
                    default = False, help="Also count numerals (default: False)")
    parser.add_argument('--hyph', dest='y', action='store_true',\
                        default = False, help="Treat hyphens as letters (default: False)")
    parser.add_argument('--incl', dest = 'i', nargs='*', default=[''], choices=['h','hyphens','n','numerals','numbers'], \
                        help="Include: numerals, hyphens")
    parser.add_argument('--env', nargs='*', default=['Standard'], \
                        help="Space-separated list of environments  to scan (default: Standard")
    parser.add_argument('--min', dest='m', action ='store', type = int, \
                        default = 1, help="Minimum word length")
    parser.add_argument('--style', dest='s', action='store', choices=['text','note','ert'], \
                    help="Present results as text, Note, or ERT?")

    sort_alpha = parser.parse_args(opts).a
    min_word_len = parser.parse_args(opts).m
    hyphens = numerals = False
    includes = parser.parse_args(opts).i
    for i in includes:
        if len(i) > 0:
            if 'h'==i[0]:
                hyphens = True
            if 'n'==i[0]:
                numerals = True
    # regexp to look for individual words: the complication comes 
    # from apostrophes within words to be counted (e.g. don't), 
    # and LaTeX commands in text (e.g. \ldots), and whether
    # to include numerals and hyphens as (part of) words.
    if numerals and hyphens:
        re_word = re.compile(r"(?<!\\)\b(\w[-\w]*('[-\w]+)*)")
    elif numerals:
        re_word = re.compile(r"(?<!\\)\b(\w+('\w+)*)")
    elif hyphens:
        re_word = re.compile(r"(?<!\\)\b([-A-Za-z]+('[-A-Za-z]+)*)")
    else:
        re_word = re.compile(r"(?<!\\)\b([A-Za-z]+('[A-Za-z]+)*)")

    style = parser.parse_args(opts).s
    temp = parser.parse_args(opts).env
    if 'All' in temp or 'all' in temp:
        environs = ''
    else:
        environs = temp[0]
        for ev in temp[1:]:
            environs += '|' + ev
        if '|' in environs:
            environs = '(' + environs + ')'
    re_layout = re.compile(r'\\begin_layout ' + environs)
    

    def lyxwrite(blah, note_ert):
        if note_ert:
            outfl.write(begin_plain)
        else:
            outfl.write(begin_std)
        outfl.write(blah)
        outfl.write(end_layout)

    def scan_text(blah, minlen):
        '''Count words (of sufficient length) in unformatted text.'''
        
        words = re_word.findall(blah)
        for w in words:
            if len(w[0]) >= minlen:
                lw = w[0].lower()
                if lw in wdict:
                    wdict[lw] += 1
                else:
                    wdict[lw] = 1
        return len(words)


    # no change to LyX header material required
    outfl.write(guff)
    guff = ''
    ####################
    totalwords = 0
    for line in infl:
        if line == '\n':
            continue

        elif re_layout.match(line):
            outfl.write(line)
            text, lines = para_contents(infl)
            outfl.write(lines)
            totalwords += scan_text(text, min_word_len)

        elif end_body in line:
            # present results at end of document, either verbosely
            # (default) or as a list of number pairs, either as part
            # of the text (default) or in a LyX (yellow) Note
            outfl.write(begin_std)
            if style == 'note':
                outfl.write(begin_inset + ' Note Note\n')
                outfl.write('status open\n')
            elif style == 'ert':
                outfl.write(begin_inset + ' ERT\n')
                outfl.write('status open\n')
            else:
                lyxwrite('========================', style == 'text')

            # sort the results by frequency of occurrence;
            # display the words sorted either by word length
            # (the default) or alphabetically
            pairs = list(wdict.iteritems())
            if sort_alpha:
                triples = [p + (p[0],) for p in pairs]
            else:
                triples = [p + (len(p[0]),) for p in pairs]
            # do the secondary sort (word length or alphabetical)
            triples.sort(key=itemgetter(2))
            # do the primary sort, from most to least frequent
            triples.sort(key=itemgetter(1), reverse=True)
            # write to the LyX file
            tot = 0
            freq = 0
            wcount = 0
            wds = ': '
            for item in triples:
                if wcount != item[1]:
                    if wcount > 0:
                        if style == 'ert':
                            lyxwrite(str(wcount) + ',' + str(freq) + '\n', True)
                        else:
                            lyxwrite(str(wcount) + ' occ. (' + str(freq) + ' inst.)' \
                                     + wds, style == 'note')
##                            lyxwrite('------------------', style == 'note')
                    freq = 1
                    wcount = item[1]
                    wds = ': ' + item[0]
                else:
                    freq += 1
                    wds += ', ' + item[0]
                tot += item[1]
            if style == 'ert':
                lyxwrite(str(wcount) + ',' + str(freq) + '\n', True)
            else:
                lyxwrite(str(wcount) + ' occ. (' + str(freq) + ' inst.)' + wds, style == 'note')
                lyxwrite('============', style == 'note')
                lyxwrite('Number of different words of '  + str(min_word_len) + \
                         ' or more chars.: ' + str(len(pairs)), style == 'note')
                lyxwrite('Total number of words of ' + str(min_word_len) + \
                         ' or more chars.: ' + str(tot), style == 'note')
                lyxwrite('Total number of all words: ' + str(totalwords), style == 'note')
            if style == 'note' or style == 'ert':
                outfl.write(end_inset + '\n')
                outfl.write(end_layout)
            
            outfl.write(line)   # end body

        else:
            outfl.write(line)
            
    return 1
