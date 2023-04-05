nutrinews
=========

|latest PyPi version|

Use OpenAI’s GPT to make news more nutritious by removing bias. Based on
an `idea from Alexandros
Marinos <https://twitter.com/alexandrosM/status/1643291421582176256>`__.

Usage
-----

::

   usage: nutrinews [-h] [-m {3.5,4}] [-p PROMPT] [--url URL] [-f FILE] [-c] [-d DIFF]

   Remove bias from some text.

   options:
     -h, --help            show this help message and exit
     -m {3.5,4}, --model {3.5,4}
                           GPT model to use.
     -p PROMPT, --prompt PROMPT
                           File containing instructions for removing bias.
     --url URL             Get text from this URL.
     -f FILE, --file FILE  Get text from this file.
     -c, --clipboard       Get text from the clipboard.
     -d DIFF, --diff DIFF  Specify tool to diff the original and nutritious text.

Installation
------------

.. code:: bash

   pip install nutrinews

Requirements
~~~~~~~~~~~~

Python 3 and associated libraries.

License
-------

MIT license.

Authors
-------

``nutrinews`` was written by
```Dave Vandenbout <devb@xess.com>`` <mailto:devb@xess.com>`__.

.. |latest PyPi version| image:: https://img.shields.io/pypi/v/nutrinews.svg
   :target: https://pypi.python.org/pypi/nutrinews
