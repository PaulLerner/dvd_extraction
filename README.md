# tvd

Copying the dvd :
    cd /vol/work3/[name]/dvd_extraction |
    change the path name in dvd_extraction/copy/copy.py |
    python dvd_extraction/copy/copy.py --series= --season= --from= --to=

To make sure the dvd can be read :
    umount /dev/dvd (each time you change a disk)

Before extraction, run this command each time you turn on your computer:
    export TESSDATA_PREFIX=/vol/work3/[name]/

Extracting the files :
    change the path name in dvd_extration/tvd/rip.py
    cd /vol/work3/[name]/extracted |
    python /vol/work3/[name]/dvd_extraction/dvd_extraction/dvd_extraction.py --series= --season= --from= --to=

[name] is the name of your vol/work3 directory
