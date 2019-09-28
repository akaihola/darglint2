dotfiles = Overview.png ExampleAST.png

all: $(dotfiles)

$(dotfiles): %.png: %.dot
	dot -Tpng $< -o $@
