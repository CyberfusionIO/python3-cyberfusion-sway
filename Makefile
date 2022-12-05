PREFIX=$(CURDIR)/debian/

install: python3-cyberfusion-sway

python3-cyberfusion-sway: PKGNAME       := python3-cyberfusion-sway
python3-cyberfusion-sway: PKGPREFIX     := $(PREFIX)/$(PKGNAME)
python3-cyberfusion-sway: SDIR          := python

python3-cyberfusion-sway:
	rm -rf $(CURDIR)/build
	python3 setup.py install --force --root=$(PKGPREFIX) --no-compile -O0 --install-layout=deb

clean:
	rm -rf $(PREFIX)/python3-cyberfusion-sway/
	rm -rf $(PREFIX)/*debhelper*
	rm -rf $(PREFIX)/*substvars
	rm -rf $(PREFIX)/files
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/src/*.egg-info
