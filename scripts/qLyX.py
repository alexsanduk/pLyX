# Undo for pLyX system. Writes the backup 
# file over the current buffer. Called thus:
#
# python <path to>/qLyX.py [-b <path to backup directory>] $$r $$f $$o
#
# Andrew Parsloe (aparsloe@clear.net.nz) 13 Oct 2012, 16 Nov 2013
# (with advice from Robert Siemer)
#

import argparse, re

parser = argparse.ArgumentParser(description='pLyX undo-er', version='1.0')

parser.add_argument('-b', '--backup', action = 'store', dest = 'backup_dir', default = '', \
                    help="Backup directory with path e.g. E:/Lymbo")
parser.add_argument('filepath', action='store', \
                    help='$$r Full pathname to the LyX file being processed e.g. D:/Documents/')
parser.add_argument('filename', action ='store', \
                    help='$$f Filename (with extension) of the LyX file e.g. myfile.lyx')

parser.add_argument('outfile', type=argparse.FileType('w'), \
                        help='Output file.')

args = parser.parse_args()
fout = args.outfile

if args.backup_dir != '':
    backup_filename = re.sub(r':|/', r'!', args.filepath) + args.filename + '~'
else:
    backup_filename = args.filename + '~'
    args.backup_dir = args.filepath

fin = open(args.backup_dir + '/' + backup_filename, 'r')

while True:
  more = fin.read(50000)
  if more:
    fout.write(more)
  else:
    break
    
fin.close()
fout.close()

   






