==============
DVD Extraction
==============


.. image:: https://img.shields.io/pypi/v/dvd_extraction.svg
        :target: https://pypi.python.org/pypi/dvd_extraction

.. image:: https://img.shields.io/travis/mbouteiller/dvd_extraction.svg
        :target: https://travis-ci.org/mbouteiller/dvd_extraction

.. image:: https://readthedocs.org/projects/dvd-extraction/badge/?version=latest
        :target: https://dvd-extraction.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python package for extracting video, audio and subtitles from DVDs


* Free software: MIT license
* Documentation: https://dvd-extraction.readthedocs.io.


Features
--------

copying the dvd :
    cd /vol/work3/[name]/dvd_extraction
    python dvd_extraction/copy/copy.py --series= --season= --from= --to=

To make sure the dvd can be read :
    umount /dev/dvd (each time you change a disk)

before extraction, run this command each time you turn on your computer:
    export TESSDATA_PREFIX=/vol/work3/[name]/

extracting the files :
    cd /vol/work3/[name]/extracted
    python /vol/work3/[name]/dvd_extraction/dvd_extraction/dvd_extraction.py --series= --season= --from= --to=

** [name] is the name of your vol/work3 directory

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
