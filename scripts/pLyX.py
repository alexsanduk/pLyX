# The 'master' script from which other scripts are called.
#
# pLyX.py
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
import re, sys, tempfile, os.path

re_lyxcmds = re.compile(r'(\\\w+)|(status (open|collapsed))')
re_script = re.compile(r'Flex \..*\|(.*)$')
run_script = r'\begin_inset Flex .Run script'
end_inset = r'\end_inset'
flex = r'\begin_inset Flex'
begin_body = r'\begin_body'

begin_note = r'''\end_layout
\begin_layout Standard
\begin_inset Note Note
status open
'''
end_note = r'''\end_inset
\end_layout
\begin_layout Standard
'''

h_v = ['-h', '--help', '-v', '--version']

def helpmsg(msg):
    '''Send a help message to a yellow note in LyX.'''
    return begin_note + msg + end_note

def ishelpversn(optlist):
    '''Test if optlist contains -h, --help, -v, --version'''
    for s in [x.lower() for x in optlist]:
        if s in h_v:
            return h_v.index(s)
    return -1

def help_routine(this_help, infl, guff):
    fout.write(guff)
    fout.write(helpmsg(this_help))
    for line in infl:
        fout.write(line)
        
compressed = '''Compressed file? To sort, clear the Document > Compressed
setting and re-save your document.'''

def error(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def get_pymods(infl):
    # store the prelims; get the modules and options
    scan = -1
    prelims = options = pymod = ''
    module_queue = []
    recorded = False
    for line in infl:
        # get contents of .Run script inset
        if scan > 0:
            prelims += line
            if end_inset in line:
                scan -= 1
                if scan > 0:
                    opts = options.split()
                    module_queue.append((pymod, opts))
                    pymod = options = ''
                    recorded = True
                else:
                    if not recorded:
                        opts = options.split()
                        module_queue.append((pymod, opts))
                        pymod = options = ''
                    return module_queue, prelims
            elif flex in line:
                scan += 1
                pymod = re_script.search(line).expand(r'\1')
            elif re_lyxcmds.match(line):
                continue
            else:
                options += line.strip('\n')

        # ".Run script" inset found
        elif run_script in line:
            scan += 1
            prelims += line

        # accumulate preliminary lines    
        elif scan == 0:
            prelims += line

        # doc. must not be in compressed format
        elif scan == -1:
            if re.search(r'LyX.*created', line):
                scan +=1
                prelims = line
            else:
                error(compressed)
    return [('',[])], ''

# Now run the scripts (if any)

def main(fin, fout):
    '''Run the scripts in the '.Run script(s)' inset'''
    scripts, prelims = get_pymods(fin)
    if scripts[0][0] == '':
        # "Run script" help or version info.
        from pLyX_help import helpnote
        
        if scripts[0][1] != []:
            opt = scripts[0][1][0]
            hv = ishelpversn(scripts[0][1])
            if hv > -1:
                help_routine(helpnote(hv), fin, prelims)
            else:
                # unknown option
                from pLyX_help import whatopt
                help_routine(whatopt(), fin, prelims)            
        else:    
            # unknown or no custom inset inserted!
            from pLyX_help import unknown
            fin.seek(0)
            prelims = ''
            for line in fin:
                if begin_body in line:
                    prelims += line
                    help_routine(unknown(), fin, prelims)
                else:
                    prelims += line
    else:
        # run the script(s): is first command a loop?
        num_scripts = len(scripts)
        if scripts[0][0] == 'loop':
            if scripts[0][1] == []:
                scripts[0][1].append('50')
            num_scripts += eval(scripts[0][1][0])
            num_scripts = max(num_scripts, 2)
            ftemp = ['' for k in range(num_scripts + 1)]
            i = j = 1
            loopy = 1
            ftemp[1] = fin
        else:
            i = j = 0
            loopy = 0
            ftemp = ['' for k in range(num_scripts + 1)]
            ftemp[0] = fin

        ftemp[num_scripts] = fout

        while i < num_scripts:
            if i > loopy:
                toss, prelims = get_pymods(ftemp[i])
                
            if i < num_scripts - 1:
                ftemp[i + 1] = tempfile.TemporaryFile(mode = 'w+t')

            scr = scripts[j][0]
            opts = scripts[j][1]
            if loopy:
                opts.append('--loop')

            runner = __import__('subscripts.' + scr, globals(), locals(), \
                                [scr], 0)
            helper = __import__('subscripts.' + scr + '_help', globals(), locals(), \
                                [scr + '_help'], 0)
            hv = ishelpversn(opts)
            if hv > -1:
                help_routine(helper.helpnote(hv), ftemp[i], prelims)
                break
            else:
                if scr == 'break':
                    ftemp[i + 1] = fout
                x = runner.main(ftemp[i], ftemp[i + 1], opts, prelims)
                ftemp[i].close()
                if x == 0:
                    break
                elif x == 1:
                    ftemp[i + 1].seek(0)
                    if loopy:
                        num_scripts = min(num_scripts, i + 2)
                        ftemp[num_scripts] = fout
                    else:
                        j += 1
                elif x == 2:
                    ftemp[i + 1].seek(0)
                    j = 1
            i += 1
     
    fout.close()

if __name__ == "__main__":
    fin = open(sys.argv[1], 'r')    # $$i
    fout = open(sys.argv[2], 'w')   # $$o
    main(fin, fout)



    
