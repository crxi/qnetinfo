PY ?= python3

.PHONY: svg png pdf all clean

svg: output/spectrum.svg

output/spectrum.svg: data.yaml render.py
	$(PY) render.py

png: ; $(PY) render.py --format png
pdf: ; $(PY) render.py --format pdf
all: svg png pdf

clean:
	rm -f output/spectrum.svg output/spectrum.png output/spectrum.pdf
