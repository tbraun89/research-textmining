all:
	ls sections/*.tex | awk '{printf "\\input{%s}\n", $$1}' > frames.tex 
	latexmk main.tex -f -pdf

clean:
	latexmk -C
	rm -f *.nav
	rm -f *.snm
	rm -f *.bbl

start:
	pdf-presenter-console main.pdf -z