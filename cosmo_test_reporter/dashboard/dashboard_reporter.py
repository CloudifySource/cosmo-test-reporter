import json
import logging
import requests
import xml.etree.ElementTree as et
import sys

__author__ = 'nirb'

logging.basicConfig()
logger = logging.getLogger('DASHBOARD')
logger.setLevel(logging.DEBUG)

dashboard_server = 'pc-lab130'
auth_token = 'cosmo'

if len(sys.argv) != 2:
    logger.error('No report file recieved. Usage: dashboard_reporter.py <xml_test_report>')
    raise ValueError

report_file = sys.argv[1]


def send_number_of_passed_tests():
    url = 'http://{0}:3030/widgets/passed_tests'.format(dashboard_server)
    runtime_properties = {
        'auth_token': auth_token,
        'current': get_number_of_succeeded_tests(report_file)
    }

    requests.post(url,
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(runtime_properties))


def send_number_of_failed_tests():
    url = 'http://{0}:3030/widgets/failed_tests'.format(dashboard_server)
    runtime_properties = {
        'auth_token': auth_token,
        'current': get_number_of_failed_tests(report_file)
    }

    requests.post(url,
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(runtime_properties))


def send_success_rate():
    url = 'http://{0}:3030/widgets/success_rate'.format(dashboard_server)

    success = get_number_of_succeeded_tests(report_file)
    failed = get_number_of_failed_tests(report_file)
    total = success + failed
    rate = (success + failed) / total * 100

    #TODO fix props
    runtime_properties = {
        'auth_token': auth_token,
        'current': 5
    }

    response = requests.post(url,
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(runtime_properties))

    print response.status_code


def get_number_of_succeeded_tests(report_xml):
    tree = et.parse(report_xml)
    root = tree.getroot()
    passed_number = 0

    for test in root.iter('Pass'):
        passed_number += 1

    return passed_number


def get_number_of_failed_tests(report_xml):
    tree = et.parse(report_xml)
    root = tree.getroot()
    failed_number = 0

    for test in root.iter('Fail'):
        failed_number += 1

    return failed_number


def update_dashboard():
    logger.info('updating dashboard')
    send_number_of_passed_tests()
    send_number_of_failed_tests()

update_dashboard()