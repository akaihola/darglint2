# Generated on 2023-02-05 17:17:17.235332

from darglint2.parse.grammar import (
    BaseGrammar,
    P,
)

from darglint2.errors import (
    IndentError,
)

from darglint2.token import (
    TokenType,
)

from darglint2.parse.identifiers import (
    NoqaIdentifier,
)

from darglint2.errors import (
    EmptyDescriptionError,
)

class VariablesSectionGrammar(BaseGrammar):
    productions = [
        P("variables-section", ([], "vhead", "variables-section1", 0), ([], "vhead-no-follow", "newlines", 0), ([EmptyDescriptionError], "colon", "vhead-no-follow1", 0), ([EmptyDescriptionError], "colon", "vhead-no-follow4", 0)),
        P("vhead", ([], "colon", "vhead0", 0), ([], "colon", "vhead2", 0)),
        P("vhead-no-follow", ([EmptyDescriptionError], "colon", "vhead-no-follow1", 0), ([EmptyDescriptionError], "colon", "vhead-no-follow4", 0)),
        P("variable-type-section", (TokenType.COLON, 0), (TokenType.HASH, 0), (TokenType.INDENT, 0), (TokenType.LPAREN, 0), (TokenType.RPAREN, 0), (TokenType.WORD, 0), (TokenType.RAISES, 0), (TokenType.ARGUMENTS, 0), (TokenType.ARGUMENT_TYPE, 0), (TokenType.RETURNS, 0), (TokenType.RETURN_TYPE, 0), (TokenType.YIELDS, 0), (TokenType.YIELD_TYPE, 0), (TokenType.VARIABLES, 0), (TokenType.VARIABLE_TYPE, 0), (TokenType.NOQA, 0), (TokenType.OTHER, 0), (TokenType.RECEIVES, 0), (TokenType.WARNS, 0), (TokenType.SEE, 0), (TokenType.ALSO, 0), (TokenType.NOTES, 0), (TokenType.EXAMPLES, 0), (TokenType.REFERENCES, 0), (TokenType.HEADER, 0)),
        P("item-body", ([], "line", "item-body0", 2), ([], "line", "item-body1", 2), ([], "line", "item-body2", 2), ([], "word", "line", 2), ([], "word", "noqa-maybe", 2), ([NoqaIdentifier], "hash", "noqa", 2), ([NoqaIdentifier], "noqa-head", "noqa-statement1", 2), (TokenType.INDENT, 2), (TokenType.COLON, 2), (TokenType.HASH, 2), (TokenType.LPAREN, 2), (TokenType.RPAREN, 2), (TokenType.WORD, 2), (TokenType.RAISES, 2), (TokenType.ARGUMENTS, 2), (TokenType.ARGUMENT_TYPE, 2), (TokenType.RETURNS, 2), (TokenType.RETURN_TYPE, 2), (TokenType.YIELDS, 2), (TokenType.YIELD_TYPE, 2), (TokenType.VARIABLES, 2), (TokenType.VARIABLE_TYPE, 2), (TokenType.NOQA, 2), (TokenType.OTHER, 2), (TokenType.RECEIVES, 2), (TokenType.WARNS, 2), (TokenType.SEE, 2), (TokenType.ALSO, 2), (TokenType.NOTES, 2), (TokenType.EXAMPLES, 2), (TokenType.REFERENCES, 2), (TokenType.HEADER, 2), ([IndentError], "line", "item-body7", 1)),
        P("block-indented", ([], "paragraph-indented", "block-indented0", 0), ([], "paragraph-indented", "block-indented1", 0), ([], "indented", "paragraph-indented0", 0), ([], "indented", "line", 0)),
        P("split-indented", ([], "newline", "split-indented0", 0), (TokenType.NEWLINE, 0)),
        P("paragraph-indented", ([], "indented", "paragraph-indented0", 0), ([], "indented", "line", 0)),
        P("indented", ([], "indent", "indents", 0), (TokenType.INDENT, 0)),
        P("block", ([], "paragraph", "block0", 0), ([], "indents", "paragraph0", 0), ([], "indents", "line", 0), ([], "line", "paragraph2", 0), ([], "word", "line", 0), ([], "word", "noqa-maybe", 0), ([NoqaIdentifier], "hash", "noqa", 0), ([NoqaIdentifier], "noqa-head", "noqa-statement1", 0), (TokenType.INDENT, 0), (TokenType.COLON, 0), (TokenType.HASH, 0), (TokenType.LPAREN, 0), (TokenType.RPAREN, 0), (TokenType.WORD, 0), (TokenType.RAISES, 0), (TokenType.ARGUMENTS, 0), (TokenType.ARGUMENT_TYPE, 0), (TokenType.RETURNS, 0), (TokenType.RETURN_TYPE, 0), (TokenType.YIELDS, 0), (TokenType.YIELD_TYPE, 0), (TokenType.VARIABLES, 0), (TokenType.VARIABLE_TYPE, 0), (TokenType.NOQA, 0), (TokenType.OTHER, 0), (TokenType.RECEIVES, 0), (TokenType.WARNS, 0), (TokenType.SEE, 0), (TokenType.ALSO, 0), (TokenType.NOTES, 0), (TokenType.EXAMPLES, 0), (TokenType.REFERENCES, 0), (TokenType.HEADER, 0), ([], "line", "paragraph1", 0)),
        P("paragraph", ([], "indents", "paragraph0", 0), ([], "indents", "line", 0), ([], "line", "paragraph2", 0), ([], "word", "line", 0), ([], "word", "noqa-maybe", 0), ([NoqaIdentifier], "hash", "noqa", 0), ([NoqaIdentifier], "noqa-head", "noqa-statement1", 0), (TokenType.INDENT, 0), (TokenType.COLON, 0), (TokenType.HASH, 0), (TokenType.LPAREN, 0), (TokenType.RPAREN, 0), (TokenType.WORD, 0), (TokenType.RAISES, 0), (TokenType.ARGUMENTS, 0), (TokenType.ARGUMENT_TYPE, 0), (TokenType.RETURNS, 0), (TokenType.RETURN_TYPE, 0), (TokenType.YIELDS, 0), (TokenType.YIELD_TYPE, 0), (TokenType.VARIABLES, 0), (TokenType.VARIABLE_TYPE, 0), (TokenType.NOQA, 0), (TokenType.OTHER, 0), (TokenType.RECEIVES, 0), (TokenType.WARNS, 0), (TokenType.SEE, 0), (TokenType.ALSO, 0), (TokenType.NOTES, 0), (TokenType.EXAMPLES, 0), (TokenType.REFERENCES, 0), (TokenType.HEADER, 0), ([], "line", "paragraph1", 0)),
        P("line", ([], "word", "line", 0), ([], "word", "noqa-maybe", 0), ([NoqaIdentifier], "hash", "noqa", 0), ([NoqaIdentifier], "noqa-head", "noqa-statement1", 0), (TokenType.INDENT, 0), (TokenType.COLON, 0), (TokenType.HASH, 0), (TokenType.LPAREN, 0), (TokenType.RPAREN, 0), (TokenType.WORD, 0), (TokenType.RAISES, 0), (TokenType.ARGUMENTS, 0), (TokenType.ARGUMENT_TYPE, 0), (TokenType.RETURNS, 0), (TokenType.RETURN_TYPE, 0), (TokenType.YIELDS, 0), (TokenType.YIELD_TYPE, 0), (TokenType.VARIABLES, 0), (TokenType.VARIABLE_TYPE, 0), (TokenType.NOQA, 0), (TokenType.OTHER, 0), (TokenType.RECEIVES, 0), (TokenType.WARNS, 0), (TokenType.SEE, 0), (TokenType.ALSO, 0), (TokenType.NOTES, 0), (TokenType.EXAMPLES, 0), (TokenType.REFERENCES, 0), (TokenType.HEADER, 0)),
        P("indents", ([], "indent", "indents", 0), (TokenType.INDENT, 0)),
        P("split", ([], "newline", "split0", 0)),
        P("newlines", ([], "newline", "newlines", 0), (TokenType.NEWLINE, 0)),
        P("word", (TokenType.COLON, 0), (TokenType.HASH, 0), (TokenType.INDENT, 0), (TokenType.LPAREN, 0), (TokenType.RPAREN, 0), (TokenType.WORD, 0), (TokenType.RAISES, 0), (TokenType.ARGUMENTS, 0), (TokenType.ARGUMENT_TYPE, 0), (TokenType.RETURNS, 0), (TokenType.RETURN_TYPE, 0), (TokenType.YIELDS, 0), (TokenType.YIELD_TYPE, 0), (TokenType.VARIABLES, 0), (TokenType.VARIABLE_TYPE, 0), (TokenType.NOQA, 0), (TokenType.OTHER, 0), (TokenType.RECEIVES, 0), (TokenType.WARNS, 0), (TokenType.SEE, 0), (TokenType.ALSO, 0), (TokenType.NOTES, 0), (TokenType.EXAMPLES, 0), (TokenType.REFERENCES, 0), (TokenType.HEADER, 0)),
        P("colon", (TokenType.COLON, 0)),
        P("hash", (TokenType.HASH, 0)),
        P("indent", (TokenType.INDENT, 0)),
        P("newline", (TokenType.NEWLINE, 0)),
        P("variables", (TokenType.VARIABLES, 0)),
        P("noqa", (TokenType.NOQA, 0)),
        P("noqa-maybe", ([NoqaIdentifier], "hash", "noqa", 0), ([NoqaIdentifier], "noqa-head", "noqa-statement1", 0)),
        P("noqa-head", ([], "hash", "noqa", 0)),
        P("words", ([], "word", "words", 0), (TokenType.COLON, 0), (TokenType.HASH, 0), (TokenType.INDENT, 0), (TokenType.LPAREN, 0), (TokenType.RPAREN, 0), (TokenType.WORD, 0), (TokenType.RAISES, 0), (TokenType.ARGUMENTS, 0), (TokenType.ARGUMENT_TYPE, 0), (TokenType.RETURNS, 0), (TokenType.RETURN_TYPE, 0), (TokenType.YIELDS, 0), (TokenType.YIELD_TYPE, 0), (TokenType.VARIABLES, 0), (TokenType.VARIABLE_TYPE, 0), (TokenType.NOQA, 0), (TokenType.OTHER, 0), (TokenType.RECEIVES, 0), (TokenType.WARNS, 0), (TokenType.SEE, 0), (TokenType.ALSO, 0), (TokenType.NOTES, 0), (TokenType.EXAMPLES, 0), (TokenType.REFERENCES, 0), (TokenType.HEADER, 0)),
        P("variables-section1", ([], "item-body", "newlines", 0), ([], "line", "item-body0", 2), ([], "line", "item-body1", 2), ([], "line", "item-body2", 2), ([], "word", "line", 2), ([], "word", "noqa-maybe", 2), ([NoqaIdentifier], "hash", "noqa", 2), ([NoqaIdentifier], "noqa-head", "noqa-statement1", 2), (TokenType.INDENT, 2), (TokenType.COLON, 2), (TokenType.HASH, 2), (TokenType.LPAREN, 2), (TokenType.RPAREN, 2), (TokenType.WORD, 2), (TokenType.RAISES, 2), (TokenType.ARGUMENTS, 2), (TokenType.ARGUMENT_TYPE, 2), (TokenType.RETURNS, 2), (TokenType.RETURN_TYPE, 2), (TokenType.YIELDS, 2), (TokenType.YIELD_TYPE, 2), (TokenType.VARIABLES, 2), (TokenType.VARIABLE_TYPE, 2), (TokenType.NOQA, 2), (TokenType.OTHER, 2), (TokenType.RECEIVES, 2), (TokenType.WARNS, 2), (TokenType.SEE, 2), (TokenType.ALSO, 2), (TokenType.NOTES, 2), (TokenType.EXAMPLES, 2), (TokenType.REFERENCES, 2), (TokenType.HEADER, 2), ([IndentError], "line", "item-body7", 1)),
        P("vhead0", ([], "variables", "vhead1", 0)),
        P("vhead1", ([], "word", "colon", 0)),
        P("vhead2", ([], "variables", "vhead3", 0)),
        P("vhead3", ([], "variable-type-section", "vhead4", 0)),
        P("vhead4", ([], "word", "colon", 0)),
        P("vhead-no-follow1", ([], "variables", "vhead-no-follow2", 0)),
        P("vhead-no-follow2", ([], "word", "colon", 0)),
        P("vhead-no-follow4", ([], "variables", "vhead-no-follow5", 0)),
        P("vhead-no-follow5", ([], "variable-type-section", "vhead-no-follow6", 0)),
        P("vhead-no-follow6", ([], "word", "colon", 0)),
        P("item-body0", ([], "newline", "block-indented", 0)),
        P("item-body1", ([], "newlines", "block-indented", 0), ([], "paragraph-indented", "block-indented0", 0), ([], "paragraph-indented", "block-indented1", 0), ([], "indented", "paragraph-indented0", 0), ([], "indented", "line", 0)),
        P("item-body2", ([], "newline", "item-body3", 0)),
        P("item-body3", ([], "indent", "item-body4", 0)),
        P("item-body4", ([], "newline", "item-body5", 0)),
        P("item-body5", ([], "newlines", "block-indented", 0), ([], "paragraph-indented", "block-indented0", 0), ([], "paragraph-indented", "block-indented1", 0), ([], "indented", "paragraph-indented0", 0), ([], "indented", "line", 0)),
        P("item-body7", ([], "newline", "block", 0)),
        P("block-indented0", ([], "split", "block-indented", 0)),
        P("block-indented1", ([], "split-indented", "block-indented", 0)),
        P("split-indented0", ([], "indents", "newlines", 0), ([], "newline", "newlines", 0), (TokenType.NEWLINE, 0), ([], "indent", "indents", 0), (TokenType.INDENT, 0)),
        P("paragraph-indented0", ([], "line", "paragraph-indented1", 0)),
        P("paragraph-indented1", ([], "newline", "paragraph-indented", 0)),
        P("block0", ([], "split", "block", 0)),
        P("paragraph0", ([], "line", "paragraph1", 0)),
        P("paragraph1", ([], "newline", "paragraph", 0)),
        P("paragraph2", ([], "newline", "paragraph", 0)),
        P("split0", ([], "newline", "newlines", 0), (TokenType.NEWLINE, 0)),
        P("noqa-statement1", ([], "colon", "words", 0)),
    ]
    start = "variables-section"