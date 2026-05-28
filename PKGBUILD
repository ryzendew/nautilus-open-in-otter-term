# Maintainer: GustavoWidman <gustavowidman@gmail.com>

pkgname=nautilus-open-in-otter-term
pkgver=1.0.0
pkgrel=1
pkgdesc="Open current directory in Otter Term from Nautilus context menu"
arch=('any')
url="https://github.com/ryzendew/nautilus-open-in-otter-term"
license=('GPL3')
depends=('python-nautilus>=4.0')
makedepends=('git')

source=("$pkgname-latest.tar.gz::https://github.com/ryzendew/nautilus-open-in-otter-term/archive/refs/heads/main.tar.gz")

sha256sums=('SKIP')

package() {
    cd "$pkgname-main"
    install -Dm644 -t "$pkgdir/usr/share/nautilus-python/extensions" nautilus-open-in-otter-term.py
}
