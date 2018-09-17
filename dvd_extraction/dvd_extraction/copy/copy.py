"""
Usage:
    copy.py --series=<name> --season=<season> --from=<first> --to=<last>
    copy.py -h | --help

Options:
    --series <name>    name of the serie
    --season <season>  number of the season
    --from <first>     number of the first episode
    --to <last>        number of the last episode

"""

from docopt import docopt
import subprocess
import os

arguments = docopt(__doc__)

name   = arguments.get('--series')
season = arguments.get('--season')
first  = int(arguments.get('--from'))
last   = int(arguments.get('--to'))
path = '/vol/work3/maurice/'

with open(os.devnull, mode='w') as f:
    subprocess.call([
        'dvdbackup', '-M',
        '-o', f'{path}dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}', '-p'
    ])

    subprocess.Popen(
        'mv ' + f'{path}dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}/*/* ' + f'{path}dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}', shell=True)

    subprocess.Popen('eject', shell=True)

    #subprocess.Popen(
        #'rm -r ' + f'/vol/work3/maurice/dvd/{name}.Season{int(season):02d}.Episodes{first:02d}to{last:02d}/* ', shell=True)


