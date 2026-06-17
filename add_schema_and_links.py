#!/usr/bin/env python3
"""
1. Fix footers on all guide pages (add Requirements + How It Works links)
2. Add cross-links between egg-donor and surrogate state guides
3. Add FAQ schema + HowTo schema to all guide pages
4. Fix footers on root pages that are missing links
5. Add Organization + WebSite schema to index.html
"""
import os
import re
import json
from pathlib import Path

ROOT = Path('/Users/connerelliott/Projects/VantageIntelligence/eggsurrogatepay')
GUIDES = ROOT / 'guides'

# ── canonical footer for guide pages (../relative) ──────────────────────────
NEW_FOOTER_GUIDE = '''<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div>
        <div class="footer__brand">EggSurrogate<span>Pay</span></div>
        <p class="footer__desc">Free compensation calculators and application platform for egg donors and surrogates.</p>
      </div>
      <div class="footer__col">
        <h4>Egg Donation</h4>
        <a href="../egg-donor-pay">Pay Calculator</a>
        <a href="../egg-donor-requirements">Requirements</a>
        <a href="../how-egg-donation-works">How It Works</a>
        <a href="../egg-donor-application">Apply Now</a>
      </div>
      <div class="footer__col">
        <h4>Surrogacy</h4>
        <a href="../surrogate-pay">Pay Calculator</a>
        <a href="../surrogate-requirements">Requirements</a>
        <a href="../how-surrogacy-works">How It Works</a>
        <a href="../surrogate-application">Apply Now</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 EggSurrogatePay.com · hello@eggsurrogatepay.com</span>
      <div class="footer__legal">
        <a href="../privacy-policy">Privacy Policy</a>
        <a href="../terms-of-service">Terms of Service</a>
        <a href="../disclaimer">Disclaimer</a>
        <a href="../methodology">Methodology</a>
        <a href="../faq">FAQ</a>
        <a href="../about">About</a>
        <a href="../data-sources">Data Sources</a>
        <a href="mailto:hello@eggsurrogatepay.com">Contact</a>
      </div>
    </div>
  </div>
</footer>
<script>
  document.getElementById('nav-toggle').addEventListener('click', function() {
    document.getElementById('nav-links').classList.toggle('open');
  });
</script>'''

# ── canonical footer for root pages (/absolute) ─────────────────────────────
NEW_FOOTER_ROOT = '''<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div>
        <div class="footer__brand">EggSurrogate<span>Pay</span></div>
        <p class="footer__desc">Free compensation calculators and application platform for egg donors and surrogates.</p>
      </div>
      <div class="footer__col">
        <h4>Egg Donation</h4>
        <a href="/egg-donor-pay">Pay Calculator</a>
        <a href="/egg-donor-requirements">Requirements</a>
        <a href="/how-egg-donation-works">How It Works</a>
        <a href="/egg-donor-application">Apply Now</a>
      </div>
      <div class="footer__col">
        <h4>Surrogacy</h4>
        <a href="/surrogate-pay">Pay Calculator</a>
        <a href="/surrogate-requirements">Requirements</a>
        <a href="/how-surrogacy-works">How It Works</a>
        <a href="/surrogate-application">Apply Now</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 EggSurrogatePay.com · hello@eggsurrogatepay.com</span>
      <div class="footer__legal">
        <a href="/privacy-policy">Privacy Policy</a>
        <a href="/terms-of-service">Terms of Service</a>
        <a href="/disclaimer">Disclaimer</a>
        <a href="/methodology">Methodology</a>
        <a href="/faq">FAQ</a>
        <a href="/about">About</a>
        <a href="/data-sources">Data Sources</a>
        <a href="mailto:hello@eggsurrogatepay.com">Contact</a>
      </div>
    </div>
  </div>
</footer>
<script>
  document.getElementById('nav-toggle').addEventListener('click', function() {
    document.getElementById('nav-links').classList.toggle('open');
  });
</script>'''

FOOTER_RE = re.compile(r'<footer class="footer">.*?</script>', re.DOTALL)


def replace_footer(content, new_footer):
    return FOOTER_RE.sub(new_footer, content)


# ── schema extraction helpers ─────────────────────────────────────────────────

FAQ_ITEM_RE = re.compile(
    r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>',
    re.DOTALL
)

STEP_RE = re.compile(
    r'<div class="step-item"><div class="step-item__icon">[^<]*</div>'
    r'<div><div class="step-item__title">(.*?)</div>'
    r'<p class="step-item__text">(.*?)</p></div></div>'
)

CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()


def extract_faq(content):
    items = []
    for m in FAQ_ITEM_RE.finditer(content):
        q = strip_html(m.group(1))
        a = strip_html(m.group(2))
        if q and a:
            items.append({'q': q, 'a': a})
    return items


def extract_steps(content):
    steps = []
    for m in STEP_RE.finditer(content):
        name = strip_html(m.group(1))
        text = strip_html(m.group(2))
        if name and text:
            steps.append({'name': name, 'text': text})
    return steps


def build_schema(page_url, page_type, state_name, faq_items, steps):
    schemas = []

    # BreadcrumbList
    if page_type == 'egg':
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://eggsurrogatepay.com/"},
                {"@type": "ListItem", "position": 2, "name": "Egg Donor Pay", "item": "https://eggsurrogatepay.com/egg-donor-pay"},
                {"@type": "ListItem", "position": 3, "name": f"Egg Donor Pay in {state_name}", "item": page_url}
            ]
        }
        howto_name = f"How to Become an Egg Donor in {state_name}"
        howto_desc = f"Step-by-step guide to becoming an egg donor in {state_name} and earning compensation."
    else:
        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://eggsurrogatepay.com/"},
                {"@type": "ListItem", "position": 2, "name": "Surrogate Pay", "item": "https://eggsurrogatepay.com/surrogate-pay"},
                {"@type": "ListItem", "position": 3, "name": f"Surrogate Pay in {state_name}", "item": page_url}
            ]
        }
        howto_name = f"How to Become a Surrogate in {state_name}"
        howto_desc = f"Step-by-step guide to becoming a gestational surrogate in {state_name} and earning compensation."

    schemas.append(breadcrumb)

    # FAQPage
    if faq_items:
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item['q'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item['a']
                    }
                }
                for item in faq_items
            ]
        }
        schemas.append(faq_schema)

    # HowTo
    if steps:
        howto_schema = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": howto_name,
            "description": howto_desc,
            "step": [
                {
                    "@type": "HowToStep",
                    "position": i + 1,
                    "name": step['name'],
                    "text": step['text']
                }
                for i, step in enumerate(steps)
            ]
        }
        schemas.append(howto_schema)

    lines = []
    for schema in schemas:
        lines.append(
            f'<script type="application/ld+json">\n'
            f'{json.dumps(schema, indent=2, ensure_ascii=False)}\n'
            f'</script>'
        )
    return '\n'.join(lines)


def insert_schema(content, schema_block):
    # Insert just before </head>
    return content.replace('</head>', schema_block + '\n</head>', 1)


def add_crosslink_egg(content, state_slug, state_name):
    """Add surrogate cross-link to egg-donor guide pages."""
    crosslink = (
        f'\n<section class="section">\n'
        f'  <div class="container container--narrow">\n'
        f'    <div style="display:flex; align-items:center; justify-content:space-between; '
        f'flex-wrap:wrap; gap:12px; padding:20px 24px; background:var(--bg-accent); '
        f'border-radius:var(--radius-sm);">\n'
        f'      <p style="margin:0; color:var(--text-light);">Also exploring surrogacy in {state_name}?</p>\n'
        f'      <a href="surrogate-pay-{state_slug}" '
        f'style="color:var(--primary); font-weight:600; text-decoration:none; white-space:nowrap;">'
        f'See Surrogate Pay in {state_name} &#8594;</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</section>\n'
    )
    # Insert before the final CTA section (contains "Ready to Apply")
    cta_marker = '\n<section class="section">\n  <div class="container container--narrow">\n    <div style="text-align:center; background:var(--bg-accent); border-radius:var(--radius); padding:48px 32px;">'
    return content.replace(cta_marker, crosslink + cta_marker, 1)


def add_crosslink_surrogate(content, state_slug, state_name):
    """Add egg-donor cross-link to surrogate guide pages."""
    crosslink = (
        f'\n<section class="section">\n'
        f'  <div class="container container--narrow">\n'
        f'    <div style="display:flex; align-items:center; justify-content:space-between; '
        f'flex-wrap:wrap; gap:12px; padding:20px 24px; background:var(--bg-accent); '
        f'border-radius:var(--radius-sm);">\n'
        f'      <p style="margin:0; color:var(--text-light);">Also exploring egg donation in {state_name}?</p>\n'
        f'      <a href="egg-donor-pay-{state_slug}" '
        f'style="color:var(--primary); font-weight:600; text-decoration:none; white-space:nowrap;">'
        f'See Egg Donor Pay in {state_name} &#8594;</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</section>\n'
    )
    cta_marker = '\n<section class="section">\n  <div class="container container--narrow">\n    <div style="text-align:center; background:var(--bg-accent); border-radius:var(--radius); padding:48px 32px;">'
    return content.replace(cta_marker, crosslink + cta_marker, 1)


# ── Organization + WebSite schema for index.html ─────────────────────────────
SITE_SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "EggSurrogatePay",
  "url": "https://eggsurrogatepay.com/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://eggsurrogatepay.com/egg-donor-pay?state={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "EggSurrogatePay",
  "url": "https://eggsurrogatepay.com/",
  "logo": "https://eggsurrogatepay.com/assets/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "hello@eggsurrogatepay.com",
    "contactType": "customer service"
  },
  "sameAs": []
}
</script>'''


# ── process guide pages ───────────────────────────────────────────────────────

guide_files = list(GUIDES.glob('*.html'))
updated = 0
skipped = 0

for filepath in sorted(guide_files):
    fname = filepath.name
    content = filepath.read_text(encoding='utf-8')

    # Skip if schema already present
    already_has_schema = 'application/ld+json' in content
    already_has_crosslink = 'Also exploring' in content

    # Determine page type and state
    if fname.startswith('egg-donor-pay-'):
        page_type = 'egg'
        state_slug = fname[len('egg-donor-pay-'):-5]  # remove prefix + .html
    elif fname.startswith('surrogate-pay-'):
        page_type = 'surrogate'
        state_slug = fname[len('surrogate-pay-'):-5]
    else:
        skipped += 1
        continue

    # Get canonical URL
    canon_m = CANONICAL_RE.search(content)
    page_url = canon_m.group(1) if canon_m else f'https://eggsurrogatepay.com/guides/{fname}'

    # Extract state name from title tag
    title_m = re.search(r'<title>(.*?)</title>', content)
    if title_m:
        title = title_m.group(1)
        # "Egg Donor Pay in California (2026) | EggSurrogatePay.com"
        state_m = re.search(r' in ([^(|]+)', title)
        state_name = state_m.group(1).strip() if state_m else state_slug.replace('-', ' ').title()
    else:
        state_name = state_slug.replace('-', ' ').title()

    original = content

    # 1. Replace footer
    content = replace_footer(content, NEW_FOOTER_GUIDE)

    # 2. Add cross-link (if not already present)
    if not already_has_crosslink:
        if page_type == 'egg':
            content = add_crosslink_egg(content, state_slug, state_name)
        else:
            content = add_crosslink_surrogate(content, state_slug, state_name)

    # 3. Add schema (if not already present)
    if not already_has_schema:
        faq_items = extract_faq(content)
        steps = extract_steps(content)
        schema_block = build_schema(page_url, page_type, state_name, faq_items, steps)
        if schema_block:
            content = insert_schema(content, schema_block)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        updated += 1

print(f'Guide pages: updated {updated}, skipped {skipped}')


# ── process root pages ────────────────────────────────────────────────────────

root_html = [f for f in ROOT.glob('*.html')
             if f.name not in ('thank-you.html', 'generate_state_pages.py')]

root_updated = 0
for filepath in sorted(root_html):
    content = filepath.read_text(encoding='utf-8')
    original = content
    content = replace_footer(content, NEW_FOOTER_ROOT)
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        root_updated += 1
        print(f'  Updated root: {filepath.name}')

print(f'Root pages: updated {root_updated}')


# ── add site schema to index.html ─────────────────────────────────────────────

index_path = ROOT / 'index.html'
index_content = index_path.read_text(encoding='utf-8')
if 'application/ld+json' not in index_content:
    index_content = index_content.replace('</head>', SITE_SCHEMA + '\n</head>', 1)
    index_path.write_text(index_content, encoding='utf-8')
    print('Added site schema to index.html')
else:
    print('index.html already has schema')


# ── update FOOTER constant in generator ───────────────────────────────────────

gen_path = ROOT / 'generate_state_pages.py'
gen_content = gen_path.read_text(encoding='utf-8')

old_footer_const = '''FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div>
        <div class="footer__brand">EggSurrogate<span>Pay</span></div>
        <p class="footer__desc">Free compensation calculators and application platform for egg donors and surrogates.</p>
      </div>
      <div class="footer__col">
        <h4>Egg Donation</h4>
        <a href="../egg-donor-pay">Compensation Calculator</a>
        <a href="../egg-donor-application">Apply as Egg Donor</a>
      </div>
      <div class="footer__col">
        <h4>Surrogacy</h4>
        <a href="../surrogate-pay">Compensation Calculator</a>
        <a href="../surrogate-application">Apply as Surrogate</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 EggSurrogatePay.com · hello@eggsurrogatepay.com</span>
      <div class="footer__legal">
        <a href="../privacy-policy">Privacy Policy</a>
        <a href="../terms-of-service">Terms of Service</a>
        <a href="../methodology">Methodology</a>
        <a href="mailto:hello@eggsurrogatepay.com">Contact</a>
      </div>
    </div>
  </div>
</footer>
<script>
  document.getElementById('nav-toggle').addEventListener('click', function() {
    document.getElementById('nav-links').classList.toggle('open');
  });
</script>"""'''

new_footer_const = '''FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div>
        <div class="footer__brand">EggSurrogate<span>Pay</span></div>
        <p class="footer__desc">Free compensation calculators and application platform for egg donors and surrogates.</p>
      </div>
      <div class="footer__col">
        <h4>Egg Donation</h4>
        <a href="../egg-donor-pay">Pay Calculator</a>
        <a href="../egg-donor-requirements">Requirements</a>
        <a href="../how-egg-donation-works">How It Works</a>
        <a href="../egg-donor-application">Apply Now</a>
      </div>
      <div class="footer__col">
        <h4>Surrogacy</h4>
        <a href="../surrogate-pay">Pay Calculator</a>
        <a href="../surrogate-requirements">Requirements</a>
        <a href="../how-surrogacy-works">How It Works</a>
        <a href="../surrogate-application">Apply Now</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 EggSurrogatePay.com · hello@eggsurrogatepay.com</span>
      <div class="footer__legal">
        <a href="../privacy-policy">Privacy Policy</a>
        <a href="../terms-of-service">Terms of Service</a>
        <a href="../disclaimer">Disclaimer</a>
        <a href="../methodology">Methodology</a>
        <a href="../faq">FAQ</a>
        <a href="../about">About</a>
        <a href="../data-sources">Data Sources</a>
        <a href="mailto:hello@eggsurrogatepay.com">Contact</a>
      </div>
    </div>
  </div>
</footer>
<script>
  document.getElementById('nav-toggle').addEventListener('click', function() {
    document.getElementById('nav-links').classList.toggle('open');
  });
</script>"""'''

if old_footer_const in gen_content:
    gen_content = gen_content.replace(old_footer_const, new_footer_const)
    gen_path.write_text(gen_content, encoding='utf-8')
    print('Updated FOOTER constant in generate_state_pages.py')
else:
    print('WARNING: Could not find old FOOTER constant in generator — skipping generator update')

print('Done.')
