dotfiles = Parsing.png Overview.png ExampleAST.png

all: $(dotfiles)

$(dotfiles): %.png: %.dot
	dot -Tpng $< -o $@
