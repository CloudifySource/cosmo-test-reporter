from nose.plugins.logcapture import MyMemoryHandler
from nose.plugins.xunit import escape_cdata, Tee
from nose.util import safe_str

__author__ = 'boris'

import sys
import traceback
import logging
from nose.plugins import Plugin
from StringIO import StringIO
from time import time
import os

log = logging.getLogger('nose.plugins.xml_reporter')


class XMLReporter(Plugin):

    failed_tests = []
    passed_tests = []
    total_duration = 0

    """Output test results as XML file
        """
    name = 'xml-reporter'
    encoding = 'UTF-8'
    logformat = '%(name)s: %(levelname)s: %(message)s'
    logdatefmt = None
    clear = False
    filters = ['-nose']

    def __init__(self):
        super(XMLReporter, self).__init__()
        self.xml = ['<Report>', '<Title>Tests output</Title>', '<ModuleReport>']
        self._capture_stack = []
        self._currentStdout = None
        self._currentStderr = None
        self.old_cwd = os.getcwd() # tests sometimes overrides this and delete the cwd so we save it before tests run
        #added code

    def options(self, parser, env):
        """Sets additional command line options."""
        Plugin.options(self, parser, env)
        parser.add_option('--report-file', action='store',
                          dest='report_file', metavar="FILE",
                          default=self.old_cwd + os.path.sep + 'results.xml',
                          help=("Path to xml file to store the report in. "
                                "Default is results.xml in the working directory"))
        #added
        parser.add_option("--logging-level", action="store",
                          default='NOTSET', dest="logcapture_level",
                          help="Set the log level to capture")
        parser.add_option("--logging-clear-handlers", action="store_true",
                          default=False, dest="logcapture_clear",
                          help="Clear all other logging handlers")
        parser.add_option("--logging-datefmt", action="store", dest="logcapture_datefmt",
                          default=env.get('NOSE_LOGDATEFMT') or self.logdatefmt,
                          metavar="FORMAT",
                          help="Specify custom date/time format to print statements. "
                               "Uses the same format as used by standard logging handlers."
                               " [NOSE_LOGDATEFMT]")
        # parser.add_option("--logging-format", action="store", dest="logcapture_format",
        #                   default=env.get('NOSE_LOGFORMAT') or self.logformat,
        #                   metavar="FORMAT",
        #                   help="Specify custom format to print statements. "
        #                        "Uses the same format as used by standard logging handlers."
        #                        " [NOSE_LOGFORMAT]")
        parser.add_option("--logging-filter", action="store", dest="logcapture_filters",
                          default=env.get('NOSE_LOGFILTER'),
                          metavar="FILTER",
                          help="Specify which statements to filter in/out. "
                               "By default, everything is captured. If the output is too"
                               " verbose,\nuse this option to filter out needless output.\n"
                               "Example: filter=foo will capture statements issued ONLY to\n"
                               " foo or foo.what.ever.sub but not foobar or other logger.\n"
                               "Specify multiple loggers with comma: filter=foo,bar,baz.\n"
                               "If any logger name is prefixed with a minus, eg filter=-foo,\n"
                               "it will be excluded rather than included. Default: "
                               "exclude logging messages from nose itself (-nose)."
                               " [NOSE_LOGFILTER]\n")

    def configure(self, options, config):
        """Configures the xunit plugin."""
        Plugin.configure(self, options, config)
        self.config = config
        self.report_file_name = options.report_file
        #added code
        self.logformat = options.logcapture_format
        self.logdatefmt = options.logcapture_datefmt
        self.clear = options.logcapture_clear
        self.loglevel = options.logcapture_level

    def addSuccess(self, test):
        self.xml.append('<TestResult> Passed </TestResult>')
        self.passed_tests.append(str(test))

    #Error can be skipped or error - both cases are covered by this method
    def addError(self, test, err):
        err = self.formatErr(err)
        self.xml.append('<TestResult> ERROR </TestResult>')
        self.xml.append('<CauseOfError><![CDATA[%s]]></CauseOfError>' % escape_cdata(err))
        self.failed_tests.append(str(test))

    def addFailure(self, test, err):
        err = self.formatErr(err)
        self.xml.append('<TestResult> FAIL </TestResult>')
        self.xml.append('<CauseOfFailure><![CDATA[%s]]></CauseOfFailure>' % escape_cdata(err))
        #self.xml.append('<CauseOfFailure>%s</CauseOfFailure>' % self._getCapturedStderr())
        self.failed_tests.append(str(test))

    def finalize(self, result):
        self._endCapture()

        self.xml.append('<SummaryRun>')
        self.xml.append("\tRan %d test%s." %
                        (result.testsRun, result.testsRun != 1 and "s" or ""))

        self.xml.append('\t<Failures>')
        for failed in self.failed_tests:
            self.xml.append('\t\t<Fail> {0} </Fail>'.format(failed))
        self.xml.append('\t</Failures>')
        self.xml.append('\t<Passed>')
        for passed in self.passed_tests:
            self.xml.append('\t\t<Pass> {0} </Pass>'.format(passed))
        self.xml.append('\t</Passed>')

        self.xml.append('\t<TotalDuration> {0} </TotalDuration>'.format(self.total_duration))
        self.xml.append('</SummaryRun>')
        if not result.wasSuccessful():
            self.xml.extend(['<FailureSummary>FAILED: ',
                             'failures=%d ' % len(result.failures),
                             'errors=%d' % len(result.errors),
                             '</FailureSummary>'])
        else:
            self.xml.append('<FailureSummary> NONE_FAILED </FailureSummary>')
        self.xml.append('</ModuleReport></Report>')
        with open(self.report_file_name, 'a') as f:
            for l in self.xml:
                f.write('{0}\n'.format(l))
                print l

    def formatErr(self, err):
        exctype, value, tb = err
        return ''.join(traceback.format_exception(exctype, value, tb))

    def setOutputStream(self, stream):
        self.stream = stream

    def startTest(self, test):
        self.xml.extend(['<Test>',
                         test.shortDescription() or str(test)])

    def beforeTest(self, test):
        """Initializes a timer before starting a test."""
        self._timer = time()
        self._startCapture()
        self.setupLoghandler()

    def afterTest(self, test):
        taken = self._timeTaken()
        test.capturedLogging = records = self.formatLogRecords()

        logs = '<Logs>\n'
        for log_line in records:
            logs = logs + '\t<Log> ' + log_line + ' </Log>\n'
        logs += '</Logs>'

        # std_output = '<Stdout>%s</Stdout>' % records
        self.handler.truncate()
        self._endCapture()
        self._currentStdout = None
        self._currentStderr = None
        self.xml.append(logs)
        self.xml.append('<Duration>%s seconds</Duration>' % taken)
        self.total_duration += taken
        self.xml.append('</Test>')

    def _startCapture(self):
        self._capture_stack.append((sys.stdout, sys.stderr))
        self._currentStdout = StringIO()
        self._currentStderr = StringIO()
        sys.stdout = Tee(self.encoding, self._currentStdout, sys.stdout)
        sys.stderr = Tee(self.encoding, self._currentStderr, sys.stderr)

    def _endCapture(self):
        if self._capture_stack:
            sys.stdout, sys.stderr = self._capture_stack.pop()

    def _getCapturedStdout(self):
        if self._currentStdout:
            value = self._currentStdout.getvalue()
        if value:
            return '<![CDATA[%s]]>' % escape_cdata(value)
        return ''

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            taken = time() - self._timer
        else:
            # test died before it ran (probably error in setup())
            # or success/failure added before test started probably
            # due to custom TestResult munging
            taken = 0.0
        return taken

    #added
    def begin(self):
        """Set up logging handler before test run begins.
        """
        self.start()

    def start(self):
        self.handler = MyMemoryHandler(self.logformat, self.logdatefmt,
                                       self.filters)
        self._startCapture()
        self.setupLoghandler()

    def setupLoghandler(self):
        # setup our handler with root logger
        root_logger = logging.getLogger()
        if self.clear:
            if hasattr(root_logger, "handlers"):
                for handler in root_logger.handlers:
                    root_logger.removeHandler(handler)
            for logger in logging.Logger.manager.loggerDict.values():
                if hasattr(logger, "handlers"):
                    for handler in logger.handlers:
                        logger.removeHandler(handler)
        # make sure there isn't one already
        # you can't simply use "if self.handler not in root_logger.handlers"
        # since at least in unit tests this doesn't work --
        # LogCapture() is instantiated for each test case while root_logger
        # is module global
        # so we always add new MyMemoryHandler instance
        for handler in root_logger.handlers[:]:
            if isinstance(handler, MyMemoryHandler):
                root_logger.handlers.remove(handler)
        root_logger.addHandler(self.handler)
        # to make sure everything gets captured
        loglevel = getattr(self, "loglevel", "NOTSET")
        root_logger.setLevel(getattr(logging, loglevel))

    def formatLogRecords(self):
        return map(safe_str, self.handler.buffer)