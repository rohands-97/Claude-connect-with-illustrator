# ARDENT — premium sneaker banner (1080×1080)

- `ardent-banner-1080x1080.svg` — the master file. Open it in Adobe Illustrator (File → Open). All text is converted to outlines, so you don't need any fonts installed. The shoe photo is embedded in the file.
- `ardent-banner-1080x1080-preview.png` — PNG preview.
- `shoe.png` — the shoe photo with a transparent background, cropped to its edges.
- `make_banner.py` — generator script. To regenerate: `pip install fonttools`, put `Bebas.ttf` (Bebas Neue) and `Montserrat.ttf` (Montserrat variable) in a folder, then run
  `python3 make_banner.py <fonts-dir> ardent-banner-1080x1080.svg shoe.png`.

Fonts: Bebas Neue and Montserrat (SIL Open Font License), both from Google Fonts.
The brand name and logo mark were made up for this banner.
