# Decision 005: QR Code for Site URL

**Date**: 2026-04-05
**Status**: Generated (not embedded on site)

## Decision
Generated a QR code for `https://japanmobilesim.com` in Rakuten pink (#FF008C).

## File
`assets/qr-japanmobilesim.png`

## Generation
- Python `qrcode` library with Pillow
- Error correction: HIGH (allows partial obstruction)
- Box size: 20px, border: 2
- Color: #FF008C fill on white background

## Usage
Available for printing, social media sharing, or embedding on the site. Not currently displayed on any page.
