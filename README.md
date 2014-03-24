cosmo-test-reporter
===================

Prerequisites:
 * Python 2.7 is installed
 * pip is installed
 * nose is intsalled (simply type `pip install nose` after pip is installed)

Steps to do In order to run your tests with XML reporter:
 1. CD to the plugin project directory
 2. Install the plugin and it's dependencies by executing: `python setup.py install` or `pip install cosmo_nose_reporter_plugin`
 3. CD to your tests directory and execute: `nosetests -s --nologcapture --with-xml-reporter`

 * It's possible to change the output file location by adding --report-file <new-path> (the default is results.xml in the working directory)
