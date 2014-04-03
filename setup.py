########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'boris'

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

version = '0.1'

setup(
    name='cosmo-test-reporter',
    version=version,
    author='boris',
    author_email='boris@gigaspaces.com',
    packages=['cosmo_test_reporter', 'cosmo_test_reporter.cosmo_nose_reporter_plugin',
              'cosmo_test_reporter.tests_logger', 'cosmo_test_reporter.utils', 'cosmo_test_reporter.dashboard'],
    license='LICENSE',
    description='cosmo tests reporter plugin',
    entry_points = {
        'nose.plugins.0.10': [
            'xmlout = cosmo_test_reporter.cosmo_nose_reporter_plugin.cosmo_nose_xml_reporter_plugin:XMLReporter'
        ]
    },
    install_requires=['requests', 'nose', 'boto']
)
