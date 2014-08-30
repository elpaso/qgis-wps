# Makefile for a PyQGIS plugin

all: compile

dist: package

install: copy2qgis

PY_FILES = WPS.py WPSDialog.py __init__.py
EXTRAS = icons/icon.png
UI_FILES = Ui_WPS.py
                                                                                                                                                                                                                                                                                                                                                                                                               RESOURCE_FILES =

compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@ $<

%.py : %.ui
	pyuic4 -o $@ $<



clean:
	find ./ -name "*.pyc" -exec rm -rf \{\} \;
	rm -f ../WPS.zip
	rm -f Ui_WPS.py

package:
	cd .. && find WPS/  -print|grep -v Make | grep -v zip | grep -v .git | zip WPS.zip -@

localrepo:
	cp ../WPS.zip ~/public_html/qgis/WPS.zip

copy2qgis: package
	unzip -o ../WPS.zip -d ~/.qgis/python/plugins

check test:
	@echo "Sorry: not implemented yet."
