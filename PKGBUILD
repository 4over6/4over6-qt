# Maintainer: Yichuan Gao <gaoyichuan000@gmail.com>
pkgname=4over6-qt
pkgver=1.0.0
pkgrel=1
pkgdesc="Client GUI for a custom 4over6 tunnel"
arch=('any')
url="https://github.com/4over6/4over6-qt"
license=('GPL3')
depends=('python-pyqt5' 'openvpn' 'systemd')
makedepends=('python-setuptools')
source=(https://github.com/4over6/4over6-qt/archive/v$pkgver.tar.gz)

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir"
}

# vim:set ts=2 sw=2 et:
