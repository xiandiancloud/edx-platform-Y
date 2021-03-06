"""
Run acceptance tests that use the bok-choy framework
http://bok-choy.readthedocs.org/en/latest/
"""
from paver.easy import task, needs, cmdopts, sh
from pavelib.utils.test.suites.bokchoy_suite import BokChoyTestSuite
from pavelib.utils.envs import Env
from optparse import make_option

try:
    from pygments.console import colorize
except ImportError:
    colorize = lambda color, text: text  # pylint: disable-msg=invalid-name

__test__ = False  # do not collect


@task
@needs('pavelib.prereqs.install_prereqs')
@cmdopts([
    ('test_spec=', 't', 'Specific test to run'),
    ('fasttest', 'a', 'Skip some setup'),
    ('extra_args=', 'e', 'adds as extra args to the test command'),
    make_option("--verbose", action="store_const", const=2, dest="verbosity"),
    make_option("-q", "--quiet", action="store_const", const=0, dest="verbosity"),
    make_option("-v", "--verbosity", action="count", dest="verbosity"),
])
def test_bokchoy(options):
    """
    Run acceptance tests that use the bok-choy framework.
    Skips some setup if `fasttest` is True.

    `test_spec` is a nose-style test specifier relative to the test directory
    Examples:
    - path/to/test.py
    - path/to/test.py:TestFoo
    - path/to/test.py:TestFoo.test_bar
    It can also be left blank to run all tests in the suite.
    """
    opts = {
        'test_spec': getattr(options, 'test_spec', None),
        'fasttest': getattr(options, 'fasttest', False),
        'verbosity': getattr(options, 'verbosity', 2),
        'extra_args': getattr(options, 'extra_args', ''),
        'test_dir': 'tests',
    }

    test_suite = BokChoyTestSuite('bok-choy', **opts)
    test_suite.run()


@task
@needs('pavelib.prereqs.install_prereqs')
@cmdopts([
    ('test_spec=', 't', 'Specific test to run'),
    ('fasttest', 'a', 'Skip some setup'),
    ('imports_dir=', 'd', 'Directory containing (un-archived) courses to be imported'),
    make_option("--verbose", action="store_const", const=2, dest="verbosity"),
    make_option("-q", "--quiet", action="store_const", const=0, dest="verbosity"),
    make_option("-v", "--verbosity", action="count", dest="verbosity"),
])
def perf_report_bokchoy(options):
    """
    Generates a har file for with page performance info.
    """
    opts = {
        'test_spec': getattr(options, 'test_spec', None),
        'fasttest': getattr(options, 'fasttest', False),
        'imports_dir': getattr(options, 'imports_dir', None),
        'verbosity': getattr(options, 'verbosity', 2),
        'test_dir': 'performance',
        'ptests': True,
    }

    test_suite = BokChoyTestSuite('bok-choy', **opts)
    test_suite.run()


@task
def bokchoy_coverage():
    """
    Generate coverage reports for bok-choy tests
    """
    Env.BOK_CHOY_REPORT_DIR.makedirs_p()
    coveragerc = Env.BOK_CHOY_COVERAGERC

    msg = colorize('green', "Combining coverage reports")
    print(msg)

    sh("coverage combine --rcfile={}".format(coveragerc))

    msg = colorize('green', "Generating coverage reports")
    print(msg)

    sh("coverage html --rcfile={}".format(coveragerc))
    sh("coverage xml --rcfile={}".format(coveragerc))
    sh("coverage report --rcfile={}".format(coveragerc))
