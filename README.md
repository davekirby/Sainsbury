sainsbury_to_json.py
====================

This is a Python script to retrieve product data from the Sainsbury website and convert
it to JSON format.

Dependencies
------------

This code is written in Python 2.7, but should run unchanged with Python 3.x

It uses the following 3rd party libraries, installable via pip:

[**requests**](http://docs.python-requests.org/en/master/): http request handling.
Version 2.9.1 was used for development.

[**BeautifulSoup**](https://www.crummy.com/software/BeautifulSoup/): HTML parsing library.
Version 4.3.2 was used for development.


Running The Script
------------------
The script can be run as follows:

    python sainsbury_to_json.py [url]

or on a UNIX system where the file has been made executable:

    sainsbury_to_json.py [url]

The URL defaults to the value given in the original problem statement if
it is not specified.

Running Unit tests
------------------

The tests are in the tests subdirectory and can be run as

    python test_s_to_j.py

However you may need to add the parent directory to the PYTHONPATH environment
variable first.

Future Improvements
-------------------

This script is very bare bones due to time constraints and there are several
improvements that could be made:

1. Error handling.  At the moment exceptions are propagated to the caller. If
this was to become part of a production system then it would need proper error
handling and logging.

2. Handle multiple pages.  The top level page that was given only had 7 items on it.
If it had more than 20 items then it be split across multiple pages and the code would
need to handle this by retrieving each page in turn.

3. Concurrency.  The pages for each product are retrieved sequentially, which is
fine for the small number of pages in the exercise.  If this was to be run against
the entire Sainsbury web site then it should be rewritten to scrape pages concurrently
to improve performance, perhaps using the [Scrapy](http://scrapy.org/) library.