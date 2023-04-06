import argparse
from pathlib import Path
from typing import Dict, Iterator, Optional, Union

from .node import Node
from .parser import Parser
from .translator import Translator
from .validate import Validator

parser = argparse.ArgumentParser(description="Convert BNF grammar to CNF")
parser.add_argument(
    "file",
    type=Path,
    help=("The file to read the grammar from."),
)
parser.add_argument(
    "-f",
    "--format",
    choices=["cyk", "py"],
    default="py",
    nargs="?",
    type=str,
    help=(
        'The output format.  Can be either "cyk" or "py".  "cyk" '
        "outputs the file in CYK format, as a .cyk file.  Py "
        "generates a grammar which can be read by darglint2."
    ),
)
parser.add_argument(
    "-o", "--output", nargs=1, type=str, default=None, help=("The output file.")
)


class Driver(object):
    def __init__(self):
        self.data: Optional[str] = None
        self.parser = Parser()
        self.validator = Validator()
        self.translator = Translator()
        self.tree: Optional[Node] = None

    def read(self, filename: Union[str, Path]) -> "Driver":
        with open(filename, "r") as fin:
            self.data = fin.read()
        return self

    def parse(self) -> "Driver":
        self.tree = self.parser.parse(self.data)
        return self

    def translate(self) -> "Driver":
        self.translator.translate(self.tree)
        return self

    def validate(self) -> "Driver":
        self.validator.validate(self.tree)
        return self

    def write(self, _format: str) -> str:
        assert self.tree is not None
        if _format == "cyk":
            return str(self.tree)
        elif _format == "py":
            return self.tree.to_python()
        else:
            raise Exception(f"Unrecognized format type {_format}")

    def get_imports(self) -> Iterator[str]:
        assert self.tree is not None
        for _import in self.tree.filter(Node.is_import):
            assert _import.value is not None
            yield _import.value

    def merge(self, driver: "Driver"):
        """Merge in the grammar at the given filename with this grammar.

        Args:
            driver: Another driver to merge into this one.

        """
        assert self.tree is not None
        assert driver.tree is not None
        self.tree.merge(driver.tree)


def load_script(filepath: Path, cache: Dict[str, Driver] = None):
    """Recursively load a script, parsing it and adding dependencies.

    Args:
        filepath: The path of the file to open.
        cache: A cache to avoid duplicate work.

    Returns:
        The fully parsed grammar.

    Raises:
        ValueError: If `filepath` is in `cache` already.

    """
    if cache is None:
        cache = {}

    filepath = filepath.resolve()
    filepath_str = str(filepath)

    if filepath_str in cache:
        raise ValueError(f"File {filepath_str} was already imported.")

    driver = Driver().read(filepath).parse()
    cache[filepath_str] = driver
    directory = filepath.parent

    # We know that merging doesn't introduce new imports,
    # so it's safe to immediately merge subgrammars.
    for imported_file in driver.get_imports():
        imported_path = (directory / imported_file).resolve()
        if str(imported_path) not in cache:
            # We skip already imported scripts, to avoid
            # having multiple copies of the productions.
            subdriver = load_script(imported_path, cache)
            driver.merge(subdriver)

    return driver


def main():
    args = parser.parse_args()
    driver = load_script(args.file)
    translated = driver.translate().validate().write(args.format)

    if args.output:
        with open(args.output[0], "w") as fout:
            fout.write(translated)
    else:
        print(translated)


if __name__ == "__main__":
    main()
