import re
from unittest import TestCase, skip

from bnf_to_cnf.parser import NodeType, Parser
from bnf_to_cnf.translator import Translator
from bnf_to_cnf.validate import Validator


class TranslatorTestCase(TestCase):
    def test_already_cnf_doesnt_change(self):
        """Make sure that it doesn't alter already cnf grammars."""
        examples = [
            '<args> ::= "Args"',
            '<colon> ::= ":"',
            "\n".join(['<one> ::= "1"', '<zero> ::= "0"']),
        ]
        for example in examples:
            tree = Parser().parse(example)
            translated = Translator().translate(tree)
            self.assertEqual(
                str(translated),
                example,
            )

    def test_start_symbol_not_reassigned(self):
        """Make sure the start symbol points to the start terminal."""
        tree = Parser().parse("start: <A>\n" "<A> ::= <B>\n" '<B> ::= "\\."')
        node = Translator().translate(tree)
        expected = 'start: <A>\n<A> ::= "\\."'
        self.assertEqual(
            str(node),
            expected,
            f"\n\nExpected:\n{expected}\n\nBut Got:\n{str(node)}\n\n",
        )

    def test_nonsolitary_terminals(self):
        """Make sure non-solitary terminals are factored out."""
        tree = Parser().parse('<arg-header> ::= <arg> ":"')
        node = Translator().translate(tree)
        self.assertEqual(
            str(node),
            "\n".join(
                [
                    "<arg-header> ::= <arg> <C>",
                    '<C> ::= ":"',
                ]
            ),
        )

    def test_nonsolitary_terminals_symbol_taken(self):
        """Make sure non-solitary teminals will have unique name."""
        tree = Parser().parse('<arg-header> ::= <arg> ":"\n' '<C> ::= "Another_value"')
        node = Translator().translate(tree)
        self.assertEqual(
            str(node),
            "<arg-header> ::= <arg> <C0>\n" '<C> ::= "Another_value"\n' '<C0> ::= ":"',
        )

    def test_factor_3plus_RHSs(self):
        """Make sure we refactor RHSs with more than two symbols."""
        tree = Parser().parse("<a> ::= <b> <c> <d>")
        node = Translator().translate(tree)
        self.assertEqual(str(node), "<a> ::= <b> <a0>\n" "<a0> ::= <c> <d>")

    def test_factor_five_length_RHS(self):
        """Make sure recursive calls function correctly."""
        tree = Parser().parse('<a2> ::= ":"\n' "<a> ::= <a2> <b> <c> <d> <e>")
        node = Translator().translate(tree)
        expected = (
            '<a2> ::= ":"\n'
            "<a> ::= <a2> <a0>\n"
            "<a0> ::= <b> <a1>\n"
            "<a1> ::= <c> <a3>\n"
            "<a3> ::= <d> <e>"
        )
        self.assertEqual(
            str(node),
            expected,
        )

    def test_eliminate_simplest_epsilon_form(self):
        tree = Parser().parse('<E> ::= "e" | ε')
        node = Translator().translate(tree)
        expected = '<E> ::= "e"'
        self.assertEqual(
            str(node),
            expected,
        )

    def test_removes_empty_productions_after_epsilon_elimination(self):
        tree = Parser().parse('<A> ::= "a"\n' "<B> ::= ε")
        node = Translator().translate(tree)
        expected = '<A> ::= "a"'
        self.assertEqual(
            str(node),
            expected,
        )

    def test_eliminate_epsilon_forms(self):
        """Make sure we can eliminate all ε-rules."""
        tree = Parser().parse("<S> ::= <A> <B>\n" '<B> ::= "b"\n' '<A> ::= "a" | ε')
        node = Translator().translate(tree)
        expected = '<S> ::= <A> <B> | "b"\n' '<B> ::= "b"\n' '<A> ::= "a"'
        self.assertEqual(
            str(node),
            expected,
        )

    def test_elimination_with_multiple_passes(self):
        """Make sure we can eliminate all ε-rules, even with mult. passes."""
        tree = Parser().parse(
            "<A> ::= <LETTER> <B>\n"
            "<B> ::= <C>\n"
            "<C> ::= <LETTER> | ε\n"
            '<LETTER> ::= "a"'
        )
        node = Translator().translate(tree)
        expected = (
            '<A> ::= <LETTER> <B> | "a"\n'
            '<B> ::= "a"\n'
            '<C> ::= "a"\n'
            '<LETTER> ::= "a"'
        )
        self.assertEqual(
            str(node),
            expected,
            f"\n\nExpected:\n{expected}\n\nBut Got:\n{str(node)}\n\n",
        )

    def test_remove_complex_unit_production(self):
        tree = Parser().parse(
            '<S> ::= <A> "a" | <B>\n' '<A> ::= "b" | <B>\n' '<B> ::= <A> | "a"'
        )
        node = Translator().translate(tree)
        expected = (
            '<S> ::= <A> <a> | "a" | "b"\n'
            '<A> ::= "b" | "a"\n'
            '<B> ::= "a" | "b"\n'
            '<a> ::= "a"'
        )
        self.assertEqual(
            str(node),
            expected,
            f"\n\nExpected:\n{expected}\n\nBut Got:\n{str(node)}\n\n",
        )

    def test_remove_single_unit_production(self):
        """Make sure we can at least remove a single unit production."""
        tree = Parser().parse("<A> ::= <B>\n" '<B> ::= "moch"')
        node = Translator().translate(tree)
        expected = '<A> ::= "moch"\n' '<B> ::= "moch"'
        self.assertEqual(
            str(node),
            expected,
            f"\n\nExpected:\n{expected}\n\nBut Got:\n{str(node)}\n\n",
        )

    def test_complete_conversion(self):
        """Test converting a complete example, and ensuring it's in CNF."""
        grammar = r"""
<Expr>    ::= <Term>
            | <Expr> <AddOp> <Term>
            | <AddOp> <Term>
<Term>    ::= <Factor>
            | <Term> <MulOp> <Factor>
<Factor>  ::= <Primary>
            | <Factor> "\^" <Primary>
<Primary> ::= <number>
            | <variable>
            | "\(" <Expr> "\)"
<AddOp>   ::= "\+" | "\-"
<MulOp>   ::= "\*" | "\/"
<number>  ::= <digit> | <digit> <number>
<digit>   ::= "0" | "1" | "2" | "3" | "4"
            | "5" | "6" | "7" | "8" | "9"
<variable> ::= "a" | "b" | "c" | "d" | "e" | "f"
             | "g" | "h" | "i" | "j" | "k" | "l"
             | "m" | "n" | "o" | "p" | "q" | "r"
             | "s" | "t" | "u" | "v" | "w" | "x"
             | "y" | "z"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        self.assertTrue(Validator(raise_exception=True).validate(node))

    def test_removes_unreachable_symbols(self):
        grammar = r"""
            start: <head>
            <head> ::= <a> <b>
            <a> ::= "-" | ε
            <b> ::= <a> <d>
            <d> ::= "1"
            <c> ::= "Q"
        """
        tree = Parser().parse(grammar)
        Translator().translate(tree)
        for node in tree.filter(lambda x: x.value == "c"):
            self.fail("Expected unused expressions to be removed.")

    def test_translate_retains_annotations(self):
        """Make sure that annotations are retained with the grammar."""
        grammar = r"""
            <A> ::= <B> <C>
            <B> ::= <C> | @Q <D>
            <C> ::= "C"
            <D> ::= "D"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        expected = Parser().parse(
            r"""
            <A> ::= <B> <C>
            <B> ::= "C" | @Q "D"
            <C> ::= "C"
            <D> ::= "D"
        """
        )
        self.assertTrue(
            node.equals(expected), f"Expected:\n{expected}\n\nBut got:\n{node}"
        )

    def test_translate_retains_annotations_up(self):
        """Make sure we retain annotations when moving up."""
        grammar = r"""
            start: <phone-number>

            <phone-number>
                ::= <confusion-number>

            <confusion-number>
                ::= @ConfusionError <number-group> <dot> <confusion-number>
                |   @ConfusionError <number-group> <dash> <confusion-number>
                |   <number-group>

            <number-group>
                ::= <number> <number-group>
                |   <number>

            <number> ::= "PN\.NUMBER"
            <dash> ::= "PN\.DASH"
            <dot> ::= "PN\.DOT"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        encountered_annotation = False
        for child in node.walk():
            if child.node_type in [NodeType.ANNOTATION, NodeType.ANNOTATIONS]:
                encountered_annotation = True
        self.assertTrue(
            encountered_annotation,
        )

    def test_translate_retains_probability(self):
        """Make sure that probabilities are retained in the grammar."""
        grammar = r"""
            start: <A>
            <A> ::= 70 <B> <B> <C> | 20 <B> <B> | 10 <B>
            <B> ::= "B"
            <C> ::= "C"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        expected = Parser().parse(
            r"""
            start: <A>
            <A> ::= 70 <B> <A1> | 20 <B> <B> | 10 "B"
            <B> ::= "B"
            <C> ::= "C"
            <A1> ::= <B> <C>
        """
        )
        self.assertTrue(
            node.equals(expected),
            f"Expected:\n{expected}\n\nBut got:\n{node}",
        )

    def test_translate_retains_start_annotation(self):
        """Make sure that an annotation on start is saved."""
        grammar = r"""
            @Q
            <start> ::= <A> <B>
            <B> ::= "b"
            <A> ::= "a"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        expected = Parser().parse(
            r"""
            @Q
            <start> ::= <A> <B>
            <B> ::= "b"
            <A> ::= "a"
        """
        )
        self.assertTrue(node.equals(expected), f"{node}\n\n{expected}")

    def test_translate_works_with_annotation_on_nonterminal(self):
        grammar = r"""
            <A> ::= "b"
                | @Q <B> <C>

            <B> ::= "b"
            <C> ::= <C>
        """
        tree = Parser().parse(grammar)
        Translator().translate(tree)

    def test_translate_with_recursion(self):
        grammar = r"""
            <start> ::= <b>

            <b> ::= <c> <b>
                | <c>

            <c> ::= "A"
        """
        tree = Parser().parse(grammar)
        Translator().translate(tree)

    @skip("Handle this eventually.")
    def test_translate_unending_lists(self):
        """Make sure we can encode an optional item-neverending list.

        This probably means there is something wrong with the epsilon
        reduction step. But, really, it's not necessary that it work with
        this rule, since it could be rewritten as

            <start> ::= <A>
            <A> ::= <B> <A> | ε
            <B> ::= "C"

        And mean the same thing.

        """
        grammar = r"""
            <start> ::= <A>
            <A>     ::= <B> <A> | ε
            <B>     ::= "C"     | ε
        """
        tree = Parser().parse(grammar)
        Translator().translate(tree)

    def test_external_imports_transferred_verbatim(self):
        grammar = r"""
            from darglint2.errors import (
                ItemIndentationError,
            )

            <start> ::= @ItemIndentationError <A>
            <A> ::= "A"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        self.assertTrue(node.equals(tree))

    def test_sequence_annotation(self):
        grammar = r"""
        start: <a>

        <a>
            ::= 100 <d>
            | @A <b> <c> <d>

        <c> ::= <b> <c> | <b>
        <d> ::= "d"
        <b> ::= "b"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        self.assertTrue(node)

    def test_nodes_not_leading_to_terminals_removed(self):
        grammar = r"""
        start: <a>
        <a> ::= "a" | <b>
        <b> ::= <c> <d>
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        self.assertFalse(list(node.filter(lambda x: x.value == "c")))

    def test_translate_annotation_follows_pattern(self):
        """Annotations should be the first item in the tuple."""
        grammar = r"""
        start: <d>

        <d> ::= <s>
        <s> ::= @Wrong <l>
              | @Wrong <l> <nl>
        <l> ::= "l"
        <nl> ::= "n" | ε
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        python = node.to_python()
        self.assertEqual(
            python.count(", [Wrong]"),
            0,
            python,
        )

    def test_no_unnamed_nodes(self):
        """Certain nodes, when translated, are missing names."""
        grammar = r"""
            Grammar: ArgumentsGrammar

            start: <arguments-section>

            <arguments-section>
                ::= <ahead> <line>
                # Causes an missing production name.
                | <ahead>

            # Simplified the remaning grammar.
            <line> ::= "TokenType\.LINE"
            <ahead> ::= "TokenType\.AHEAD"
        """
        tree = Parser().parse(grammar)
        node = Translator().translate(tree)
        python = node.to_python()
        unacceptable_pattern = re.compile(r'P\([^"]')
        self.assertEqual(
            unacceptable_pattern.findall(python),
            [],
            "Found production which doesn't begin with a name:\n{}".format(python),
        )
