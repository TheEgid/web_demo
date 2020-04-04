import sys
import os
from os.path import dirname


try:
    from django.conf import settings
    from django.test.utils import get_runner

    if not os.environ.get('DJANGO_SETTINGS_MODULE'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask.settings")

    try:
        import django
        # tp = abspath(join(dirname(__file__), '.'))
        sys.path.append(dirname(__file__))
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError('To fix this error, maybe run `pipenv install`')


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests.test_one']

    testrunner = get_runner(settings)
    test_runner = testrunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(test_args)
    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
