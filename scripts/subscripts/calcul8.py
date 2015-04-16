# Calculate (real or complex) mathematical expressions.
# Not an independent script: part of the pLyX system.
#
# calcul8.py 
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
import argparse, re
from math import *

re_floating = re.compile(r'((?<!(\.|\d))\d+(?!(\.|\d)))')
re_complex = re.compile(r'([A-IK-Za-ik-z]+)')
re_lyxcmds = re.compile(r'\\\w+ \w+')

flex_calc = r'\begin_inset Flex .calculate'
begin_layout = r'\begin_layout'
end_layout = r'\end_layout'
begin_inset = r'\begin_inset'
end_inset = r'\end_inset'

def main(infl, outfl, options, guff):

    def inset_contents():
        '''Get contents of inset minus formatting.'''
        contents = ''
        layouts, insets = 0, 1
        for line in infl:
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

    parser = argparse.ArgumentParser(description='Functions of a complex variable', \
                                     version='1.0')
    parser.add_argument('-j', action ='store_true', dest = "complex", default = False, \
                        help='Import cmath python module')
    parser.add_argument('-r', action ='store_true', dest = "retain", default = False, \
                        help='Retain expression in document')

    args = parser.parse_args(options)
    if args.complex:
        import cmath

    outfl.write(guff)
    guff = ''

    for line in infl:
        if flex_calc in line:
            calc = inset_contents()
            if args.retain:
                outfl.write(calc + ' = ') 
            calc = re_floating.sub(r'\1.0', calc)
            if args.complex:
                calc = re_complex.sub(r'cmath.\1', calc)
            
            outfl.write(str(eval(calc)))
        else:
            outfl.write(line)

    return 1
