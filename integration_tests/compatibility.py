"""Tests for compatibility with other flake8 plugins."""

import re
from collections import defaultdict
import subprocess
from unittest import (TestCase)
import os
from typing import (
    Dict,
    Iterable,
    Set,
)

ERROR = re.compile(r'[A-Z]{1,3}\d{3}')


class CompatibilityTest(TestCase):
    """A simple compatibility test for Darglint2.

    This test attempts to ensure that the error
    checks with darglint2 are a superset of the errors
    reported without darglint2. (That is, darglint2
    does not hide any errors.)

    """

    STRICTNESS_FILE = 'integration_tests/files/strictness_example.py'

    def create_darglint_setup(self, strictness=None):
        try:
            with open(".darglint2", "w") as fout:
                fout.write("[darglint2]\n")
                if strictness:
                    fout.write('strictness={}\n'.format(strictness))
        except Exception:
            # Do Nothing.
            pass

    def create_flake8_setup(self, strictness=None):
        try:
            with open('.flake8', 'w') as fout:
                if strictness:
                    fout.write('[flake8]\n')
                    fout.write('strictness={}\n'.format(strictness))
        except Exception:
            # Do Nothing.
            pass

    def create_no_darglint_setup(self):
        try:
            with open(".darglint2", "w") as fout:
                fout.write("[darglint2]\nignore=*\n")
        except Exception:
            # Do Nothing.
            pass

    @classmethod
    def remove_configs(cls):
        try:
            os.remove(".darglint2")
            os.remove('.flake8')
        except Exception:
            # Do Nothing.
            pass

    @classmethod
    def setUpClass(cls):
        cls.remove_configs()

    @classmethod
    def tearDownClass(cls):
        cls.remove_configs()

    def yield_modules(self):
        # type: () -> Iterable[str]
        for path, folders, filenames in os.walk('integration_tests/repos'):
            for filename in filenames:
                if not filename.endswith('.py'):
                    continue
                yield os.path.join(path, filename)

    def record_errors(self, collection, filename, config=None):
        # type: (Dict[str, Set[str]], str) -> None
        if config:
            command = [
                'flake8',
                '--config={}'.format(config),
            ]
        else:
            command = [
                'flake8',
                '--isolated',
                '--enable-extensions=TRUE',
            ]
        proc = subprocess.run(
            command + [filename],
            stdout=subprocess.PIPE
        )
        result = proc.stdout.decode('utf8')
        errors = ERROR.findall(result)
        collection[filename] |= set(errors)

    def record_darglint_errors(self, collection, filename):
        proc = subprocess.run([
            "darglint2",
            filename,
        ], stdout=subprocess.PIPE)
        result = proc.stdout.decode('utf8')
        errors = ERROR.findall(result)
        collection[filename] |= set(errors)

    def test_with_darglint_is_superset(self):
        errors = defaultdict(lambda: set())  # type: Dict[str, Set[str]]
        self.create_no_darglint_setup()
        for filename in self.yield_modules():
            self.record_errors(errors, filename)

        errors_with = defaultdict(lambda: set())  # type: Dict[str, Set[str]]  # noqa: E501
        self.create_darglint_setup()
        for filename in self.yield_modules():
            self.record_errors(errors_with, filename)

        for filename in errors.keys():
            self.assertTrue(
                len(errors[filename] - errors_with[filename]) == 0,
            )

    def test_defaults_taken_from_darglint_config(self):
        self.create_darglint_setup(strictness='short')
        self.create_flake8_setup()

        flake8_errors = defaultdict(lambda: set())
        self.record_errors(flake8_errors, self.STRICTNESS_FILE, config='.flake8')

        # The error D100, which isn't a part of darglint2,
        # appears in flake8 with the use of a config file.
        # So, we need to remove it.
        flake8_errors[self.STRICTNESS_FILE].discard('D100')

        darglint_errors = defaultdict(lambda: set())
        self.record_darglint_errors(darglint_errors, self.STRICTNESS_FILE)

        self.assertEqual(
            flake8_errors[self.STRICTNESS_FILE],
            darglint_errors[self.STRICTNESS_FILE],
        )

    def test_defaults_overriden_from_darglint_config(self):
        self.create_darglint_setup(strictness='short')
        self.create_flake8_setup(strictness='full')
        errors = defaultdict(lambda: set())

        flake8_errors = defaultdict(lambda: set())
        self.record_errors(flake8_errors, self.STRICTNESS_FILE, config='.flake8')

        # The error D100, which isn't a part of darglint2,
        # appears in flake8 with the use of a config file.
        # So, we need to remove it.
        flake8_errors[self.STRICTNESS_FILE].discard('D100')

        darglint_errors = defaultdict(lambda: set())
        self.record_darglint_errors(darglint_errors, self.STRICTNESS_FILE)

        self.assertNotEqual(
            flake8_errors[self.STRICTNESS_FILE],
            darglint_errors[self.STRICTNESS_FILE],
        )
