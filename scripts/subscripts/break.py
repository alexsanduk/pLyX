# Part of the pLyX.py system.
#
# Andrew Parsloe (aparsloe@clear.net.nz)
# version 1.0 (3 December 2012)
#
# break.py 
#
import argparse

flex_stop = r'\begin_inset Flex .stop|break'
end_inset = r'\end_inset'

def main(infl, outfl, options, guff):
    '''Prevent the running of following scripts'''

    parser = argparse.ArgumentParser(description = 'erase inset?', version = '1.0')

    parser.add_argument('-x', dest='x', action ='store_true', default = False, \
                        help="Deletes .stop inset from .Run script(s)")
    excise = parser.parse_args(options).x

    if excise:
        newguff = ''
        delete = done = False
        for line in guff.splitlines(True):
            if line in '\n':
                continue
            elif flex_stop in line and (not done):
                delete = True
            elif delete:
                if end_inset in line:
                    delete = False
                    done = True
                else:
                    continue
            else:
                newguff += line
                
        guff = newguff
            
    
    outfl.write(guff)
    for line in infl:
        outfl.write(line)
    
    return 0
