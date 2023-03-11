"""Tests for the Docstring class."""

from typing import (
    List,
    Tuple,
    Iterator,
)
import string
from unittest import TestCase
from random import (
    choice,
    randint,
    shuffle,
)

from darglint2.strictness import Strictness
from darglint2.docstring.sections import Sections
from darglint2.docstring.docstring import Docstring


class DocstringBaseMethodTests(TestCase):

    # A set of equivalent docstrings, in each of the representations.
    # These should evaluate to the same for each of the base methods.
    _equivalent_docstrings = [
        # (
        #     '\n'.join([
        #         'Only a short description.',
        #     ]),
        #     '\n'.join([
        #         'Only a short description.',
        #     ])
        # ),
        # (
        #     '\n'.join([
        #         'A single item and type.',
        #         '',
        #         'Args:',
        #         '    x (int): A number.',
        #         '',
        #     ]),
        #     '\n'.join([
        #         'A single item and type.',
        #         '',
        #         ':param x: A number.',
        #         ':type x: int',
        #         '',
        #     ])
        # ),
        (
            '\n'.join([
                'A docstring with noqas in it.',
                '',
                '# noqa: I203',
                '',
                '# noqa',
                '',
            ]),
            '\n'.join([
                'A docstring with noqas in it.',
                '',
                '# noqa: I203',
                '',
                '# noqa',
                '',
            ]),
            '\n'.join([
                'A docstring with noqas in it.',
                '',
                '# noqa: I203',
                '',
                '# noqa',
                '',
            ]),
        ),
        (
            '\n'.join([
                'A docstring with types in it.',
                '',
                'Args:',
                '    x (int): The number to double.',
                '',
                'Returns:',
                '    int: The number, doubled.',
                '',
            ]),
            '\n'.join([
                'A docstring with types in it.',
                '',
                ':param x: The number to double.',
                ':type x: int',
                ':returns: The number, doubled.',
                ':rtype: int',
                '',
            ]),
            '\n'.join([
                'A docstring with types in it.',
                '',
                'Parameters',
                '----------',
                'x : int',
                '    The number to double.',
                '',
                'Returns',
                '-------',
                'int',
                '    The number, doubled.',
                '',
            ]),
        ),
        (
            '\n'.join([
                'A very complete docstring.',
                '',
                'There is a long-description section.',
                '',
                '    code example',
                '',
                'And it continues over multiple lines.',
                '',
                'Args:',
                '    x (int): The first integer.  This description ',
                '        spans multiple lines.',
                '    y (int): The second integer.',
                '',
                'Raises:',
                '    InvalidNumberException: An exception for if it\'s '
                '        invalid.',
                '    Exception: Seemingly at random.',
                '',
                'Yields:',
                '    int: Numbers that were calculated somehow.',
                '',
            ]),
            '\n'.join([
                'A very complete docstring.',
                '',
                'There is a long-description section.',
                '',
                '    code example',
                '',
                'And it continues over multiple lines.',
                '',
                ':param x: The first integer.  This description ',
                '    spans multiple lines.',
                ':type x: int',
                ':param y: The second integer.',
                ':type y: int',
                ':raises InvalidNumberException: An exception for if it\'s '
                '    invalid.',
                ':raises Exception: Seemingly at random.',
                ':yields: Numbers that were calculated somehow.',
                ':ytype: int',
                '',
            ]),
            '\n'.join([
                'A very complete docstring.',
                '',
                'There is a long-description section.',
                '',
                '    code example',
                '',
                'And it continues over multiple lines.',
                '',
                'Parameters',
                '----------',
                'x : int',
                '    The first integer.  This description ',
                '        spans multiple lines.',
                'y : int',
                '    The second integer.',
                '',
                'Raises',
                '------',
                'InvalidNumberException',
                '    An exception for if it\'s '
                '        invalid.',
                'Exception',
                '    Seemingly at random.',
                '',
                'Yields',
                '------',
                'int',
                '    Numbers that were calculated somehow.',
                '',
            ]),
        ),
    ]

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(*args, **kwargs)
        cls.equivalent_docstrings = list()
        for google_doc, sphinx_doc, numpy_doc in cls._equivalent_docstrings:
            cls.equivalent_docstrings.append((
                Docstring.from_google(google_doc),
                Docstring.from_sphinx(sphinx_doc),
                Docstring.from_numpy(numpy_doc),
            ))

    def test_get_section_equivalency(self):
        for google_doc, sphinx_doc, numpy_doc in self.equivalent_docstrings:
            for section in [
                # Sections.SHORT_DESCRIPTION,
                Sections.LONG_DESCRIPTION,
                # Sections.NOQAS,
            ]:
                g = google_doc.get_section(section)
                s = sphinx_doc.get_section(section)
                n = numpy_doc.get_section(section)
                self.assertEqual(
                    g, s,
                    'Section {} differs for google and sphinx for "{}"'.format(
                        section,
                        google_doc.get_section(Sections.SHORT_DESCRIPTION),
                    ),
                )
                self.assertEqual(
                    g, n,
                    'Section {} differs for google and numpy for "{}"'.format(
                        section,
                        google_doc.get_section(Sections.SHORT_DESCRIPTION),
                    ),
                )

    def test_get_types_equivalency(self):
        for google_doc, sphinx_doc, numpy_doc in self.equivalent_docstrings:
            for section in [
                Sections.ARGUMENTS_SECTION,
                Sections.RETURNS_SECTION,
                Sections.YIELDS_SECTION,
            ]:
                google_types = google_doc.get_types(section)
                self.assertEqual(
                    google_types,
                    sphinx_doc.get_types(section),
                    'Sections differ for {} type'.format(
                        section,
                    ),
                )
                self.assertEqual(
                    google_types,
                    numpy_doc.get_types(section),
                    'Sections differ for {} type.'.format(
                        section
                    ),
                )

    def test_get_items_equivalency(self):
        for google_doc, sphinx_doc, numpy_doc in self.equivalent_docstrings:
            for section in [
                # Sections.ARGUMENTS_SECTION,
                Sections.RAISES_SECTION,
            ]:
                google_items = google_doc.get_items(section)
                self.assertEqual(
                    google_items,
                    sphinx_doc.get_items(section),
                    'Google and sphinx items differ.',
                )
                self.assertEqual(
                    google_items,
                    numpy_doc.get_items(section),
                    'Google and numpy items differ.',
                )

            google_noqas = google_doc.get_noqas()
            self.assertEqual(
                google_noqas,
                sphinx_doc.get_noqas(),
                'Google and sphinx items differ.',
            )
            self.assertEqual(
                google_noqas,
                numpy_doc.get_noqas(),
                'Google and numpy items differ.',
            )

    def test_type_and_name_always_associated(self):
        """Make sure the type goes to the correct name."""
        names = ['x', 'y', 'a', 'z', 'q']
        types = ['int', 'float', 'Decimal', 'str', 'Any']
        short_description = 'A short docstring.'

        # Change the types of the parameters.
        shuffle(names)
        shuffle(types)

        sphinx_params = [
            ':param {}: An explanation'.format(name)
            for name in names
        ] + [
            ':type {}: {}'.format(name, _type)
            for name, _type in zip(names, types)
        ]
        shuffle(sphinx_params)
        sphinx_docstring = '\n'.join([
            short_description,
            '',
            '\n'.join(sphinx_params)
        ])

        google_params = [
            '    {} ({}): An explanation.'.format(name, _type)
            for name, _type in zip(names, types)
        ]
        google_docstring = '\n'.join([
            short_description,
            '',
            'Args:',
            '\n'.join(google_params),
        ])

        numpy_params = [
            '{} : {}\n    An explanation'.format(name, _type)
            for name, _type in zip(names, types)
        ]
        numpy_docstring = '\n'.join([
            short_description,
            '',
            'Parameters',
            '----------',
            '\n'.join(numpy_params)
        ])

        google_doc = Docstring.from_google(google_docstring)
        sphinx_doc = Docstring.from_sphinx(sphinx_docstring)
        numpy_doc = Docstring.from_numpy(numpy_docstring)

        items = google_doc.get_items(Sections.ARGUMENTS_SECTION)
        self.assertTrue(
            items == sorted(items),
            'The items should be sorted.'
        )
        google_items = google_doc.get_items(Sections.ARGUMENTS_SECTION)
        self.assertEqual(
            google_items,
            sphinx_doc.get_items(Sections.ARGUMENTS_SECTION),
            'Google and Sphinx items should be the same.',
        )
        self.assertEqual(
            google_items,
            numpy_doc.get_items(Sections.ARGUMENTS_SECTION)
        )
        google_args_section = google_doc.get_types(Sections.ARGUMENTS_SECTION)
        self.assertEqual(
            google_args_section,
            sphinx_doc.get_types(Sections.ARGUMENTS_SECTION),
            'Google and Sphinx types should be the same.',
        )
        self.assertEqual(
            google_args_section,
            numpy_doc.get_types(Sections.ARGUMENTS_SECTION),
        )


class DocstringMethodTest(TestCase):
    """Tests for the Docstring class."""

    def test_global_noqa_no_body(self):
        """Ensure an empty noqa body means ignore everything."""
        root = '\n'.join([
            'A short explanation.',
            '',
            '    # noqa',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertTrue(docstring.ignore_all)

    def test_global_noqa_star_body(self):
        """Ensure noqa with * means ignore everything."""
        root = '\n'.join([
            'A short explanation.',
            '',
            '    # noqa: *',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertTrue(docstring.ignore_all)

    def test_get_short_description(self):
        """Ensure we can get the short description."""
        root = 'Nothing but a short description.'
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_section(Sections.SHORT_DESCRIPTION),
            'Nothing but a short description.'
        )

    def test_get_long_description(self):
        """Make sure we can get the long description."""
        root = '\n'.join([
            'Ignore short.',
            '',
            'Long description should be contiguous.',
            '',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_section(Sections.LONG_DESCRIPTION),
            'Long description should be contiguous.'
        )

    def test_get_arguments_description(self):
        """Make sure we can get the arguments description."""
        root = '\n'.join([
            'Something.',
            '',
            'Args:',
            '    x: An integer.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        section = docstring.get_section(Sections.ARGUMENTS_SECTION)
        self.assertEqual(
            section,
            'Args:\n    x: An integer.'
        )

    def test_get_argument_types(self):
        """Make sure we can get a dictionary of arguments to types."""
        root = '\n'.join([
            'Something.',
            '',
            'Args:',
            '    x (int): The first.',
            '    y (List[int], optional): The second.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        argtypes = dict(zip(
            docstring.get_items(Sections.ARGUMENTS_SECTION) or [],
            docstring.get_types(Sections.ARGUMENTS_SECTION) or [],
        ))
        self.assertEqual(
            argtypes['x'],
            'int',
        )
        self.assertEqual(
            argtypes['y'],
            'List[int], optional',
        )

    def test_get_return_section(self):
        """Make sure we can get the returns description."""
        root = '\n'.join([
            'Ferment corn.',
            '',
            'Returns:',
            '    Bourbon.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_section(Sections.RETURNS_SECTION),
            'Returns:\n    Bourbon.',
        )

    def test_get_return_type(self):
        """Make sure we can get the return type described."""
        root = '\n'.join([
            'Ferment potato.',
            '',
            'Returns:',
            '    Alcohol: Vodka.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_types(Sections.RETURNS_SECTION),
            'Alcohol',
        )

    def test_get_yields_description(self):
        """Make sure we can get the yields description."""
        root = '\n'.join([
            'To pedestrians.',
            '',
            'Yields:',
            '    To pedestrians.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_section(Sections.YIELDS_SECTION),
            'Yields:\n    To pedestrians.',
        )

    def test_get_yields_type(self):
        """Make sure we can get the yields type."""
        root = '\n'.join([
            'Get slavic cats.',
            '',
            'Yields:',
            '    Cat: The slavic ones.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_types(Sections.YIELDS_SECTION),
            'Cat',
        )

    def test_get_raises_description(self):
        """Make sure we can get the raises description."""
        root = '\n'.join([
            'Check if there\'s a problem.',
            '',
            'Raises:',
            '    ProblemException: if there is a problem.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_section(Sections.RAISES_SECTION),
            'Raises:\n    ProblemException: if there is a problem.'
        )

    def test_get_exception_types(self):
        """Make sure we can get the types of exceptions raised."""
        root = '\n'.join([
            'Problematic.',
            '',
            'Raises:',
            '    IndexError: Frequently.',
            '    DoesNotExist: Always.',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_items(Sections.RAISES_SECTION),
            sorted(['IndexError', 'DoesNotExist'])
        )

    def test_get_noqas(self):
        """Make sure we can get all of the noqas in the docstring."""
        root = '\n'.join([
            'Full of noqas.',
            '',
            '# noqa: I200',
            '# noqa: I201 y',
            '',
            'Args:',
            '    x: Something. # noqa: I201',
            '\n',
        ])
        docstring = Docstring.from_google(root)
        noqas = docstring.get_noqas()
        self.assertEqual(
            noqas,
            {
                'I200': [],
                'I201': ['x', 'y'],
            },
        )

    def test_get_noqas_with_exception(self):
        root = '\n'.join([
            'Noqa-full.',
            '',
            '# noqa',
            '# noqa: I325',
            '',
            'Raises:',
            '    MyException: Sometimes.  # noqa: I932',
            '',
        ])
        docstring = Docstring.from_google(root)
        self.assertEqual(
            docstring.get_noqas(),
            {
                '*': [],
                'I932': ['MyException'],
                'I325': [],
            },
        )

    def test_has_section(self):
        """Make sure the docstring can tell if it has the given sections."""
        has_everything_root = '\n'.join([
            'Short decscription.',
            '',
            'Long description.',
            '',
            'Args:',
            '    x: Some value.',
            '',
            'Raises:',
            '    IntegrityError: Sometimes.',
            '',
            'Yields:',
            '    The occasional value.',
            '',
            'Returns:',
            '    When it completes.',
        ])
        docstring = Docstring.from_google(has_everything_root)
        self.assertTrue(all([
            docstring.get_section(Sections.SHORT_DESCRIPTION),
            docstring.get_section(Sections.LONG_DESCRIPTION),
            docstring.get_section(Sections.ARGUMENTS_SECTION),
            docstring.get_section(Sections.RAISES_SECTION),
            docstring.get_section(Sections.YIELDS_SECTION),
            docstring.get_section(Sections.RETURNS_SECTION),
        ]))
        has_only_short_description = '\n'.join([
            'Short description'
        ])
        docstring = Docstring.from_google(has_only_short_description)
        self.assertTrue(
            docstring.get_section(Sections.SHORT_DESCRIPTION),
        )
        self.assertFalse(any([
            docstring.get_section(Sections.LONG_DESCRIPTION),
            docstring.get_section(Sections.ARGUMENTS_SECTION),
            docstring.get_section(Sections.RAISES_SECTION),
            docstring.get_section(Sections.YIELDS_SECTION),
            docstring.get_section(Sections.RETURNS_SECTION),
        ]))


class DocstringForSphinxTests(TestCase):

    def test_has_everything_for_sphinx(self):
        has_everything_root = '\n'.join([
            'Short decscription.',
            '',
            'Long description.',
            '',
            ':param x: Some value.',
            ':raises IntegrityError: Sometimes.',
            ':yields: The occasional value.',
            ':returns: When it completes.',
            ''
        ])
        docstring = Docstring.from_sphinx(has_everything_root)
        for section in [
            Sections.SHORT_DESCRIPTION,
            Sections.LONG_DESCRIPTION,
            Sections.ARGUMENTS_SECTION,
            Sections.RAISES_SECTION,
            Sections.YIELDS_SECTION,
            Sections.RETURNS_SECTION,
        ]:
            self.assertTrue(
                docstring.get_section(section),
                'Expected to have section {}, but it did not.'.format(
                    section,
                )
            )
        has_only_short_description = '\n'.join([
            'Short description'
        ])
        docstring = Docstring.from_google(has_only_short_description)
        self.assertTrue(
            docstring.get_section(Sections.SHORT_DESCRIPTION),
        )
        self.assertFalse(any([
            docstring.get_section(Sections.LONG_DESCRIPTION),
            docstring.get_section(Sections.ARGUMENTS_SECTION),
            docstring.get_section(Sections.RAISES_SECTION),
            docstring.get_section(Sections.YIELDS_SECTION),
            docstring.get_section(Sections.RETURNS_SECTION),
        ]))

    def test_has_everything_for_sphinx_multiline(self):
        has_everything_multiline_root = '\n'.join([
            'Short decscription.',
            '',
            'Long description.',
            '',
            ':param Test: Some value.',
            '    Over multiples lines.',
            ':raises IntegrityError: Sometimes.',
            '    Also over multiples lines',
            ':yields: The occasional value.',
            ':returns: When it completes.',
            '    But what about multiple lines?',
            ''
        ])
        docstring = Docstring.from_sphinx(has_everything_multiline_root)
        for section in [
            Sections.SHORT_DESCRIPTION,
            Sections.LONG_DESCRIPTION,
            Sections.ARGUMENTS_SECTION,
            Sections.RAISES_SECTION,
            Sections.YIELDS_SECTION,
            Sections.RETURNS_SECTION,
        ]:
            self.assertTrue(
                docstring.get_section(section),
                'Expected to have section {}, but it did not.'.format(
                    section,
                )
            )

    def test_arguments_section_with_newline(self):
        """Make sure we can parse an arguments section with a newline."""
        root = '\n'.join([
            'Something.',
            '',
            ':param condition:',
            '    The first.',
            '\n',
        ])
        docstring = Docstring.from_sphinx(root)
        items = docstring.get_items(Sections.ARGUMENTS_SECTION)
        self.assertEqual(items, ['condition'])

    def test_get_argument_types(self):
        """Make sure we can get a dictionary of arguments to types."""
        root = '\n'.join([
            'Something.',
            '',
            ':param x: The first.',
            ':param y: The second.',
            ':type x: int',
            ':type y: List[int], optional'
            '\n',
        ])
        docstring = Docstring.from_sphinx(root)
        argtypes = dict(zip(
            docstring.get_items(Sections.ARGUMENTS_SECTION) or [],
            docstring.get_types(Sections.ARGUMENTS_SECTION) or [],
        ))
        self.assertEqual(
            argtypes['x'],
            'int',
        )
        self.assertEqual(
            argtypes['y'],
            'List[int], optional',
        )


class DocstringForNumpyTest(TestCase):

    MAX_ARG_NUM = 3

    def _get_args(self):
        # type: () -> List[str]
        return list({
            choice(string.ascii_lowercase)
            for _ in range(randint(2, self.MAX_ARG_NUM))
        })

    def _get_types(self, args):
        # type: (List[str]) -> List[str]
        return [
            choice('AB')
            for _ in args
        ]

    def _get_argtype_pairs(self, args, types):
        # type: (List[str], List[str]) -> List[Tuple[str, str]]
        return list(zip(args, types))

    def _combine(self, argtype_pairs):
        # type: (List[Tuple[str, str]]) -> Iterator[List[Tuple[List[str], str]]]  # noqa: E501
        """Generate some permutations of joinings.

        For example, if two consecutive args have the same types,
        say
            [ ('a', 'A'), ('b', 'A') ]
        then we will get the following permutations from this
        function:
            [ (['a'], 'A'), (['b'], 'A') ]
            [ (['a', 'b'], 'A') ]

        We don't need it to generate all possible permutations
        of joinings -- that's too complicated for this test.
        For example, if we have three items with the same type,
        say
            [ ('a', 'A'), ('b', 'A'), ('c', 'A') ]
        We only need to generate the following
            [ (['a'], 'A'), (['b'], 'A), (['c'], 'A') ]
            [ (['a', 'b'], 'A'), (['c'], 'A') ]
            [ (['a', 'b', 'c'], 'A') ]
        But we don't need to generate
            [ (['a'], 'A'), (['b', 'c'], 'A') ]
        And we only really need to do it for each run
        independently, not at the same time.

        Args:
            argtype_pairs: A list of tuples containing
                arguments and their types.

        Yields:
            A list containing tuples with lists of
            args and types.

        """
        yield [([x], y) for x, y in argtype_pairs]
        i, j = 0, 0
        # Go through each of the items except the last one.
        while i < len(argtype_pairs) - 1:
            j = i + 1
            # Go forward from that item while you have an item
            #   of a different type.
            while (j < len(argtype_pairs) and
                    argtype_pairs[i][1] == argtype_pairs[j][1]):
                # For each of those, combine the ones up until the
                # second index.
                ret = [([x], y) for x, y in argtype_pairs[:i]]
                joined_args = [x for x, y in argtype_pairs[i:j+1]]
                ret.append((joined_args, argtype_pairs[j][1]))
                ret.extend([([x], y) for x, y in argtype_pairs[j+1:]])
                yield ret
                j += 1
            i += 1

    def generate_docstring(self, argtypes):
        # type: (List[Tuple[List[str], str]]) -> str
        doc = [
            'Short description',
            '',
            'Parameters',
            '----------',
        ]
        for args, _type in argtypes:
            doc.append(', '.join(args) + ': ' + _type)
            doc.append('    Some description')
        doc.append('')
        return '\n'.join(doc)

    def test_multiple_arguments_on_one_line(self):
        """Make sure we can extract from multiple args on one line."""
        # By forcing the individual elements to be sorted, we
        # force an overall sorting. (The docstring will be sorting
        # by the first element in a combined argument.  Once split,
        # the individual arguments will not necessarily be in order.)
        # This forces them to be.
        args = sorted(self._get_args())
        types = self._get_types(args)
        sorted_args = sorted(args)
        sorted_types = [
            _type for arg, _type in
            sorted(zip(args, types))
        ]
        argtypes = self._get_argtype_pairs(args, types)
        for combo in self._combine(argtypes):
            raw_docstring = self.generate_docstring(combo)
            docstring = Docstring.from_numpy(raw_docstring)
            items = docstring.get_items(Sections.ARGUMENTS_SECTION)
            types = docstring.get_types(Sections.ARGUMENTS_SECTION)
            self.assertEqual(
                items,
                sorted_args,
            )
            self.assertEqual(
                types,
                sorted_types,
            )

    def test_extract_simplest_raises_section(self):
        raw_docstring = '\n'.join([
            'Raises an error.',
            '',
            'Raises',
            '------',
            'AssertionError'
            '',
        ])
        docstring = Docstring.from_numpy(raw_docstring)
        self.assertTrue(
            docstring.get_section(Sections.RAISES_SECTION)
            is not None
        )

    def test_arguments_section_with_breaks_in_lines_and_indents(self):
        raw_docstring = '\n'.join([
            'Has arguments.',
            '',
            'Parameters',
            '----------',
            'x: int',
            '    The first parameter.',
            '    ',
            '    Can be the only parameter.',
            'y: Optional[int]',
            '    The second parameter.',
            '',
            '    Can also be added.',
            'z: Optional[int]',
            '    The third parameter.',
            '',
        ])
        docstring = Docstring.from_numpy(raw_docstring)
        self.assertTrue(
            docstring.get_section(Sections.ARGUMENTS_SECTION)
            is not None
        )
        self.assertEqual(
            docstring.get_items(Sections.ARGUMENTS_SECTION),
            ['x', 'y', 'z'],
        )
        self.assertEqual(
            docstring.get_types(Sections.ARGUMENTS_SECTION),
            ['int', 'Optional[int]', 'Optional[int]'],
        )

    def test_arguments_without_description(self):
        raw_docstring = '\n'.join([
            'Has arguments.',
            '',
            'Parameters',
            '----------',
            'x',
            '',
        ])
        docstring = Docstring.from_numpy(raw_docstring)
        self.assertEqual(
            docstring.get_items(Sections.ARGUMENTS_SECTION),
            ['x'],
        )

    def test_arguments_section_with_break_after_description(self):
        raw_docstring = '\n'.join([
            'Has arguments.',
            '',
            'Parameters',
            '----------',
            'x: int',
            '    The first parameter.',
            '',
            'y: Optional[int]',
            '    The second parameter.',
            '    ',
            'z: Optional[int]',
            '    The third parameter.',
            '',
        ])
        docstring = Docstring.from_numpy(raw_docstring)
        self.assertTrue(
            docstring.get_section(Sections.ARGUMENTS_SECTION)
            is not None
        )
        self.assertEqual(
            docstring.get_items(Sections.ARGUMENTS_SECTION),
            ['x', 'y', 'z'],
        )

    def test_satisfies_strictness_short_description(self):
        parameters = [
            (None, False),
            ('', False),
            ('Dostring with just title.', True),
            (
                '\n'.join([
                    'Dostring with title and parameters.',
                    '',
                    'Parameters',
                    '----------',
                    'x: int',
                    '    The first parameter.',
                    '',
                    'y: Optional[int]',
                    '    The second parameter.',
                    '',
                ]),
                False,
            ),
            (
                '\n'.join([
                    'Dostring with only long,',
                    'long, really long description.',
                    '',
                ]),
                False,
            ),
        ]
        for raw_docstring, is_strictness_satisfied in parameters:
            docstring = Docstring.from_numpy(raw_docstring)
            with self.subTest(raw_docstring):
                self.assertIs(
                    docstring.satisfies_strictness(
                        Strictness.SHORT_DESCRIPTION,
                    ),
                    is_strictness_satisfied,
                    msg=raw_docstring,
                )

    def test_satisfies_strictness_long_description(self):
        parameters = [
            (None, False),
            ('', False),
            ('Dostring with just title.', True),
            (
                '\n'.join([
                    'Dostring with title, long description and parameters.',
                    '',
                    'Long description goes here.',
                    '',
                    'Parameters',
                    '----------',
                    'x: int',
                    '    The only parameter.',
                    '',
                ]),
                False,
            ),
            (
                '\n'.join([
                    '',
                    'Dostring with only long,',
                    'long, really long description.',
                    '',
                    '',
                ]),
                True,
            ),
        ]
        for raw_docstring, is_strictness_satisfied in parameters:
            docstring = Docstring.from_numpy(raw_docstring)
            with self.subTest(raw_docstring):
                self.assertIs(
                    docstring.satisfies_strictness(
                        Strictness.LONG_DESCRIPTION,
                    ),
                    is_strictness_satisfied,
                    msg=raw_docstring,
                )

    def test_satisfies_strictness_full_description(self):
        parameters = [
            (None, False),
            ('', False),
            ('Dostring with just title.', False),
            (
                '\n'.join([
                    'Dostring with title, long description and parameters.',
                    '',
                    'Long description goes here.',
                    '',
                    'Parameters',
                    '----------',
                    'x: int',
                    '    The only parameter.',
                    '',
                    'Returns',
                    '-------',
                    'int',
                    '    Magic, random number.',
                    '',
                ]),
                False,
            ),
            (
                '\n'.join([
                    'Dostring with only long,',
                    'long, really long description.',
                    '',
                ]),
                False,
            ),
        ]
        for raw_docstring, is_strictness_satisfied in parameters:
            docstring = Docstring.from_numpy(raw_docstring)
            with self.subTest(raw_docstring):
                self.assertIs(
                    docstring.satisfies_strictness(
                        Strictness.FULL_DESCRIPTION,
                    ),
                    is_strictness_satisfied,
                    msg=raw_docstring,
                )
