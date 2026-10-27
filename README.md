# streffdev website

A static site (plain HTML and CSS, no JavaScript, no cookies) for Streffdev Ltd.

## What's here

- `site/` – the finished website. This folder is what you upload.
- `build.py` – regenerates `site/` from your company details. Edit the `CONFIG` block at the top.
- `src/assets/` – the stylesheet and self-hosted fonts (JetBrains Mono, SIL Open Font Licence).
- `site/brand/` – logo files: SVG wordmark (light and dark backgrounds), square icon, PNG exports.

## Before going live

1. Open `build.py` and fill in the `CONFIG` values still in [square brackets]:
   your domain (company details are already filled in).
   Optionally add your ICO registration number.
2. Run `python3 build.py`. It lists anything still unfilled; placeholders also show
   highlighted in yellow on the pages.
3. DoseTempo's privacy policy lives at https://www.dosetempo.co.uk/privacy; this site links to it
   rather than keeping a second copy.

## Hosting (free option)

1. Register the domain (for example through Cloudflare Registrar or another UK registrar).
2. Push this folder to a GitHub repo, then create a Cloudflare Pages (or GitHub Pages) project
   with **build output directory** set to `site` and no build command.
3. Attach your custom domain in the Pages settings.
4. Set up an email address on the domain (e.g. hello@ and privacy@) so the contact details work.
   Cloudflare Email Routing can forward these to your existing inbox for free.

## Google Play organisation account

- Dun & Bradstreet generates the company's D-U-N-S number automatically within about two days of
  Companies House registration. Look it up on their site and check the name and address match
  Companies House exactly before entering it in Play Console.
- In Play Console, go to Developer account > About you, verify the organisation website, then use
  **Change account type**. You'll need a new organisation payments profile.
- Use `https://www.dosetempo.co.uk/privacy` as DoseTempo's privacy policy URL.
