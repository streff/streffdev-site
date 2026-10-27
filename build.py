#!/usr/bin/env python3
"""
Builds the streffdev website into ./site

1. Fill in the CONFIG values below. Anything still in [square brackets]
   is a placeholder: it shows highlighted in yellow on the pages and the
   build lists it, so nothing slips through.
2. Run:  python3 build.py
3. Upload the contents of ./site to your host.
"""
import html
import re
import shutil
from pathlib import Path

CONFIG = {
    # Company details, exactly as on Companies House / your certificate of incorporation
    "company_name": "Streffdev Ltd",
    "company_number": "SC906973",
    "registered_office": "122b Woodside Way, Glenrothes, Scotland, KY7 5DP",
    "incorporated": "25 October 2026",
    # Website + contact
    "domain": "streffdev.co.uk",            # e.g. streffdev.co.uk (no https://)
    "email_user": "hello",                     # gives hello@yourdomain
    "privacy_email_user": "privacy",           # gives privacy@yourdomain (can be the same mailbox)
    # Optional: leave as "" to hide the line
    "ico_number": "",                          # ICO data protection fee registration, e.g. ZB123456
    "vat_number": "",                          # leave "" if not VAT registered
    # Dates shown on the legal pages
    "legal_updated": "27 October 2026",
}

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"
placeholders_found = set()


def v(key):
    """Config value, HTML-escaped; placeholders are highlighted."""
    val = CONFIG[key]
    if val.startswith("["):
        placeholders_found.add(f"{key} = {val}")
        return f'<span class="todo">{html.escape(val)}</span>'
    return html.escape(val)


def email(user_key="email_user"):
    dom = CONFIG["domain"]
    addr = f'{CONFIG[user_key]}@{dom}'
    if dom.startswith("["):
        placeholders_found.add(f"domain = {dom}")
        return f'<span class="todo">{html.escape(addr)}</span>'
    return f'<a href="mailto:{addr}">{addr}</a>'


def ch_link():
    num = CONFIG["company_number"]
    if num.startswith("["):
        return "https://find-and-update.company-information.service.gov.uk/"
    return f"https://find-and-update.company-information.service.gov.uk/company/{num}"


NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("apps.html", "Apps"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]
LEGAL = [
    ("company.html", "Company information"),
    ("privacy.html", "Privacy notice"),
    ("cookies.html", "Cookies"),
    ("terms.html", "Website terms"),
]


def page(path, title, description, body, nav_key=None):
    depth = path.count("/")
    p = "../" * depth
    nav_items = "\n".join(
        f'<li><a href="{p}{href}"{" aria-current=\"page\"" if href == nav_key else ""}>{label}</a></li>'
        for href, label in NAV
    )
    legal_items = "\n".join(f'<li><a href="{"" if href.startswith("http") else p}{href}">{label}</a></li>' for href, label in LEGAL)
    full_title = "streffdev — apps for people and businesses" if path == "index.html" else f"{title} | streffdev"
    canon = "" if CONFIG["domain"].startswith("[") else \
        f'<link rel="canonical" href="https://{CONFIG["domain"]}/{"" if path == "index.html" else path}">'
    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
{canon}
<link rel="icon" href="{p}brand/streffdev-icon.svg" type="image/svg+xml">
<link rel="icon" href="{p}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preload" href="{p}assets/fonts/JetBrainsMono-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/style.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"{CONFIG['company_name']}","alternateName":"streffdev","logo":"brand/streffdev-icon.svg"}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{p}index.html" aria-label="streffdev home">
      <img class="logo-light" src="{p}brand/streffdev-logo.svg" alt="streffdev" width="160" height="28">
      <img class="logo-dark" src="{p}brand/streffdev-logo-on-dark.svg" alt="" width="160" height="28">
    </a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{nav_items}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
  <div class="wrap">
{body}
  </div>
</main>
<footer class="site-footer">
  <div class="wrap cols">
    <div>
      <img class="logo-light" src="{p}brand/streffdev-logo.svg" alt="streffdev" width="120" height="21">
      <img class="logo-dark" src="{p}brand/streffdev-logo-on-dark.svg" alt="" width="120" height="21">
      <p class="legal-line">{v('company_name')} is a private limited company registered in Scotland,
      company number {v('company_number')}. Registered office: {v('registered_office')}.</p>
    </div>
    <nav aria-label="Legal">
      <ul>
{legal_items}
      </ul>
    </nav>
  </div>
</footer>
</body>
</html>
"""
    dest = OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)


# ---------------------------------------------------------------- pages

def build_pages():
    page("index.html", "Home",
         "streffdev builds focused mobile and web apps for individuals and businesses. A small software company registered in Scotland.",
         f"""
<section class="hero">
  <h1>Small, useful software for people and <span class="nowrap">businesses<span class="cursor" aria-hidden="true"></span></span></h1>
  <p class="lede">streffdev designs and builds mobile apps, web apps and bespoke tools. Each one is built to do a specific job well, without clutter, ads or needless data collection.</p>
  <div class="actions">
    <a class="button" href="services.html">See what we build</a>
    <a class="button quiet" href="contact.html">Get in touch</a>
  </div>
</section>

<div class="split">
  <section>
    <h2>For individuals</h2>
    <p>Apps for the everyday jobs that general-purpose tools handle badly. They keep your data on your own device and are sold for a one-off price where possible, not a subscription.</p>
    <p><a href="apps.html">See our apps</a></p>
  </section>
  <section>
    <h2>For businesses</h2>
    <p>Bespoke mobile and web apps, internal tools that replace spreadsheets and paper forms, and integrations that connect the systems you already use. Every project starts with understanding how your work actually happens.</p>
    <p><a href="services.html">How we work with businesses</a></p>
  </section>
</div>

<section class="app" aria-labelledby="dt">
  <div class="app-mark" aria-hidden="true">Dt</div>
  <div>
    <h2 id="dt">DoseTempo</h2>
    <p class="status">Coming soon to Android and iPhone</p>
    <p>A medication reminder app built around real-world dosing: medicines taken every few hours, not just at fixed times of day. Everything stays on your phone.</p>
    <p><a href="apps.html#dosetempo">More about DoseTempo</a></p>
  </div>
</section>
""", "index.html")

    page("services.html", "Services",
         "Mobile apps, web apps, bespoke business tools and requirements work from streffdev.",
         f"""
<h1>Services</h1>
<p class="lede">We build software for two kinds of customer: people who want an app that does one thing properly, and organisations that need a tool shaped around the way they work.</p>

<div class="prose">
<h2>Apps for individuals</h2>
<p>Our own apps start from a real problem, usually one that the existing options make harder than it needs to be. They are designed to be simple to use, respectful of your privacy, and fairly priced.</p>
<ul>
  <li>Data stays on your device unless you choose to export it.</li>
  <li>No adverts and no selling of personal information.</li>
  <li>One-off purchases rather than subscriptions wherever the app allows it.</li>
</ul>

<h2>Software for businesses</h2>
<h3>Mobile apps</h3>
<p>Native-quality apps for iPhone and Android, built from a single codebase where that makes sense and published under your own name or ours.</p>
<h3>Web apps</h3>
<p>Browser-based tools for customers or staff, from booking and enquiry forms to dashboards and self-service portals.</p>
<h3>Bespoke business tools</h3>
<p>Replacements for the spreadsheets, shared inboxes and paper forms that an expanding team outgrows, plus integrations that move data between the systems you already pay for.</p>
<h3>Process and requirements</h3>
<p>Before anything is built, we map how the work happens today, agree what needs to change, and write it down as clear requirements you can check. It is the cheapest point in a project to get things right.</p>

<h2>How a project runs</h2>
</div>
<ol class="steps">
  <li><strong>Understand the problem</strong>A conversation about what you need, who will use it and what success looks like.</li>
  <li><strong>Agree what to build</strong>A short written specification with scope, cost and timescale, so there are no surprises.</li>
  <li><strong>Build in small releases</strong>You see working software early and often, and can change direction before it costs much.</li>
  <li><strong>Hand over and support</strong>Documentation, app store publishing if needed, and an agreed level of ongoing support.</li>
</ol>
<p><a class="button" href="contact.html">Talk to us about a project</a></p>
""", "services.html")

    page("apps.html", "Apps",
         "Apps published by streffdev, including DoseTempo, a medication reminder app for Android and iPhone.",
         f"""
<h1>Apps</h1>
<p class="lede">Apps designed, built and published by {v('company_name')}.</p>

<section class="app" id="dosetempo" aria-labelledby="dt">
  <div class="app-mark" aria-hidden="true">Dt</div>
  <div class="prose">
    <h2 id="dt">DoseTempo</h2>
    <p class="status">Coming soon to Google Play and the App Store</p>
    <p>DoseTempo reminds you when your next dose is due. It was built for people juggling several medicines on different schedules, including ones taken every few hours rather than at set times of day.</p>
    <ul>
      <li>Reminders at any interval, from every few hours to every few days.</li>
      <li>Doses due at the same time are grouped into one reminder.</li>
      <li>Missed doses keep reminding you until you respond.</li>
      <li>Every dose is logged as taken, skipped or missed.</li>
      <li>No account, no adverts and no tracking. Your medicines and history stay on your phone, with password-protected backups for moving to a new one.</li>
    </ul>
    <p>Free for up to four medicines. A single one-off purchase of £2.99 unlocks unlimited medicines, PDF dose reports for your GP or pharmacist, stock tracking with repeat-prescription warnings, and tapering plans. There is no subscription.</p>
    <p class="note">DoseTempo does not give medical advice, calculate doses or check interactions. Always follow your doctor's or pharmacist's instructions.</p>
    <p><a href="https://www.dosetempo.co.uk/">Visit dosetempo.co.uk</a> or read the <a href="https://www.dosetempo.co.uk/privacy">DoseTempo privacy policy</a>.</p>
  </div>
</section>
""", "apps.html")

    page("about.html", "About",
         "About streffdev.",
         f"""
<h1>About streffdev</h1>
<div class="prose">
<p class="lede">streffdev is the trading name of {v('company_name')}, a software company registered in Scotland. It was set up to build and publish focused apps for people and businesses.</p>

<h2>How we build</h2>
<p>We understand the real problem first, keep the solution as simple as it can be, and test it properly before anyone relies on it.</p>

<h2>What we believe</h2>
<ul>
  <li>Software should do its job and then get out of the way.</li>
  <li>Your data belongs to you. We collect as little as possible.</li>
  <li>Prices should be clear and fair, especially for apps people rely on for their health.</li>
</ul>

<h2>Company details</h2>
<dl class="facts">
  <dt>Registered name</dt><dd>{v('company_name')}</dd>
  <dt>Company number</dt><dd>{v('company_number')}</dd>
  <dt>Registered in</dt><dd>Scotland</dd>
  <dt>Registered office</dt><dd>{v('registered_office')}</dd>
</dl>
<p><a href="company.html">Full company information</a></p>
</div>
""", "about.html")

    page("contact.html", "Contact",
         "Contact streffdev about a project, an app or a privacy request.",
         f"""
<h1>Contact</h1>
<div class="prose">
<p class="lede">Email is the quickest way to reach us. We aim to reply within two working days.</p>
<dl class="facts">
  <dt>General and project enquiries</dt><dd>{email()}</dd>
  <dt>App support</dt><dd>{email()}</dd>
  <dt>Privacy and data requests</dt><dd>{email('privacy_email_user')}</dd>
  <dt>Post</dt><dd>{v('company_name')}<br>{v('registered_office')}</dd>
</dl>
<h2>About a project</h2>
<p>It helps to include a sentence or two on what you need, who will use it, and any deadline you're working to. There's no charge for an initial conversation.</p>
</div>
""", "contact.html")

    vat_line = f"<dt>VAT number</dt><dd>{v('vat_number')}</dd>" if CONFIG["vat_number"] else \
        "<dt>VAT</dt><dd>Not currently registered for VAT</dd>"
    ico_line = f"<dt>ICO registration</dt><dd>{v('ico_number')}</dd>" if CONFIG["ico_number"] else ""
    page("company.html", "Company information",
         "Legal and company information for Streffdev Ltd.",
         f"""
<h1>Company information</h1>
<div class="prose">
<p>This website is operated by {v('company_name')}, which trades as streffdev.</p>
<dl class="facts">
  <dt>Registered name</dt><dd>{v('company_name')}</dd>
  <dt>Trading name</dt><dd>streffdev</dd>
  <dt>Company type</dt><dd>Private company limited by shares</dd>
  <dt>Registered in</dt><dd>Scotland</dd>
  <dt>Company number</dt><dd>{v('company_number')}</dd>
  <dt>Incorporated</dt><dd>{v('incorporated')}</dd>
  <dt>Registered office</dt><dd>{v('registered_office')}</dd>
  {vat_line}
  {ico_line}
  <dt>Email</dt><dd>{email()}</dd>
</dl>
<p>You can check these details on the <a href="{ch_link()}">Companies House register</a>.</p>
</div>
""")

    page("privacy.html", "Privacy notice",
         "How Streffdev Ltd handles personal information through this website.",
         f"""
<h1>Privacy notice</h1>
<div class="prose">
<p class="updated">Last updated {v('legal_updated')}</p>
<p>This notice explains how {v('company_name')} ("we", "us") handles personal information when you visit this website or contact us. Each of our apps has its own privacy policy, linked from the <a href="apps.html">Apps</a> page.</p>

<h2>Who we are</h2>
<p>{v('company_name')} is the data controller for the information described here. We are a company registered in Scotland, number {v('company_number')}, with our registered office at {v('registered_office')}. You can contact us about privacy at {email('privacy_email_user')}.</p>

<h2>What we collect</h2>
<h3>When you browse this site</h3>
<p>This site does not use cookies, analytics or tracking tools, and it does not load content from third parties. Like any website, our hosting provider automatically records basic technical information for each request, such as your IP address, browser type, the page requested and the time. This is used only to deliver the site, keep it secure and diagnose faults.</p>
<h3>When you email us</h3>
<p>We receive your email address, your name if you include it, and whatever you choose to tell us. We use this only to reply to you and, if you become a customer, to deliver and manage our work for you.</p>

<h2>Our lawful basis</h2>
<p>Under the UK General Data Protection Regulation we rely on:</p>
<ul>
  <li><strong>legitimate interests</strong> for running and securing the website and replying to enquiries;</li>
  <li><strong>contract</strong> where we are providing, or taking steps to provide, services you have asked for;</li>
  <li><strong>legal obligation</strong> where we must keep records, for example for tax.</li>
</ul>

<h2>Who we share it with</h2>
<p>We do not sell personal information or share it for marketing. We use a small number of service providers who process data on our behalf under contract: our website hosting provider and our email provider. We will also disclose information where the law requires it.</p>
<p>Some providers may process data outside the UK. Where they do, we make sure appropriate safeguards are in place, such as UK adequacy regulations or the International Data Transfer Agreement.</p>

<h2>How long we keep it</h2>
<ul>
  <li>Enquiries that don't lead to work: up to two years after our last contact.</li>
  <li>Customer records: six years after the end of the relevant financial year, to meet tax and company law requirements.</li>
  <li>Hosting logs: for the period set by our hosting provider, normally no more than a few weeks.</li>
</ul>

<h2>Your rights</h2>
<p>You have the right to ask for a copy of your information, to have it corrected or deleted, to restrict or object to how we use it, and to receive it in a portable format. Email {email('privacy_email_user')} and we will respond within one month.</p>
<p>If you are unhappy with how we have handled your information, please tell us first so we can try to put it right. You also have the right to complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk</a> or on 0303 123 1113.</p>

<h2>Changes to this notice</h2>
<p>We will update this page if the way we handle information changes. The date at the top shows when it was last revised.</p>
</div>
""")

    page("cookies.html", "Cookies",
         "Cookie statement for the streffdev website.",
         f"""
<h1>Cookies</h1>
<div class="prose">
<p class="updated">Last updated {v('legal_updated')}</p>
<p>This website does not set any cookies and does not use similar technologies such as local storage, tracking pixels or fingerprinting. We do not use analytics or advertising services, and our fonts and images are served from this site rather than from third parties.</p>
<p>Because nothing is stored on your device, there is no cookie banner and nothing to accept or decline.</p>
<p>If we ever introduce cookies that are not strictly necessary, we will update this page and ask for your consent before setting them, as required by the Privacy and Electronic Communications Regulations.</p>
<p>See our <a href="privacy.html">privacy notice</a> for how we handle personal information more generally.</p>
</div>
""")

    page("terms.html", "Website terms",
         "Terms of use for the streffdev website.",
         f"""
<h1>Website terms of use</h1>
<div class="prose">
<p class="updated">Last updated {v('legal_updated')}</p>
<p>These terms apply to your use of this website. By using the site you agree to them. They do not cover our apps, which have their own terms in the relevant app store, or work we do for customers, which is covered by a separate written agreement.</p>

<h2>About us</h2>
<p>This site is operated by {v('company_name')}, a company registered in Scotland, number {v('company_number')}. Registered office: {v('registered_office')}. Contact: {email()}.</p>

<h2>Using the site</h2>
<p>You may view, download and print pages for your own reference. You must not misuse the site, for example by attempting to gain unauthorised access to it, introducing malicious code, or using it in any way that breaks the law.</p>

<h2>Intellectual property</h2>
<p>The content of this site, including text, design, the streffdev name and logo, is owned by or licensed to {v('company_name')}. You may not copy or reuse it for commercial purposes without our written permission. App store badges and third-party names belong to their respective owners.</p>

<h2>Information on this site</h2>
<p>We keep the site accurate and up to date, but it is provided for general information only. Nothing here is professional or medical advice, and descriptions of products in development may change before release.</p>

<h2>Links to other sites</h2>
<p>Where we link to other websites, we do so for your convenience. We have no control over those sites and are not responsible for their content.</p>

<h2>Our liability</h2>
<p>To the extent the law allows, we are not liable for any loss or damage arising from your use of, or inability to use, this website. Nothing in these terms limits or excludes our liability for death or personal injury caused by our negligence, for fraud or fraudulent misrepresentation, or for any other liability that cannot be limited or excluded under the law of Scotland.</p>

<h2>Changes</h2>
<p>We may update these terms from time to time. The version on this page at the time you use the site is the one that applies.</p>

<h2>Governing law</h2>
<p>These terms are governed by the law of Scotland, and the Scottish courts have jurisdiction over any dispute about them. If you live elsewhere in the UK, you may also bring proceedings in the courts of the part of the UK where you live.</p>
</div>
""")

    page("404.html", "Page not found", "Page not found.",
         """
<h1>That page doesn't exist<span class="cursor" aria-hidden="true"></span></h1>
<p class="lede">The link may be out of date, or the address may have been mistyped.</p>
<p><a class="button" href="index.html">Go to the home page</a></p>
""")


def build_extras():
    dom = CONFIG["domain"]
    base = f"https://{dom}/"
    urls = ["", "services.html", "apps.html", "about.html", "contact.html"] + [h for h, _ in LEGAL if not h.startswith("http")]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{base}{u}</loc></url>\n" for u in urls)
        + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n")


def main():
    # Keep the generated brand folder and PNG icons; replace everything else
    OUT.mkdir(exist_ok=True)
    shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
    build_pages()
    build_extras()
    print(f"Built {len(list(OUT.rglob('*.html')))} pages into {OUT}")
    if placeholders_found:
        print("\nStill to fill in (edit CONFIG at the top of build.py):")
        for p in sorted(placeholders_found):
            print("  -", p)


if __name__ == "__main__":
    main()
