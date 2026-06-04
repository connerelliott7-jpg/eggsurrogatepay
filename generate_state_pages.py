#!/usr/bin/env python3
"""
Generate 100 state-level HTML pages for eggsurrogatepay.com
50 egg donor pages + 50 surrogate pages
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(BASE_DIR, 'guides')

os.makedirs(GUIDES_DIR, exist_ok=True)

states = [
  {'code':'AL','name':'Alabama','slug':'alabama','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'AK','name':'Alaska','slug':'alaska','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'AZ','name':'Arizona','slug':'arizona','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'AR','name':'Arkansas','slug':'arkansas','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'CA','name':'California','slug':'california','tier':'tier1','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'CO','name':'Colorado','slug':'colorado','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'CT','name':'Connecticut','slug':'connecticut','tier':'tier1','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'DE','name':'Delaware','slug':'delaware','tier':'tier1','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'FL','name':'Florida','slug':'florida','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'GA','name':'Georgia','slug':'georgia','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'HI','name':'Hawaii','slug':'hawaii','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'ID','name':'Idaho','slug':'idaho','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'IL','name':'Illinois','slug':'illinois','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'IN','name':'Indiana','slug':'indiana','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'IA','name':'Iowa','slug':'iowa','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'KS','name':'Kansas','slug':'kansas','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'KY','name':'Kentucky','slug':'kentucky','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'LA','name':'Louisiana','slug':'louisiana','tier':'tier3','surrogateLegal':False,'surrogateRestricted':False},
  {'code':'ME','name':'Maine','slug':'maine','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'MD','name':'Maryland','slug':'maryland','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'MA','name':'Massachusetts','slug':'massachusetts','tier':'tier1','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'MI','name':'Michigan','slug':'michigan','tier':'tier3','surrogateLegal':False,'surrogateRestricted':False},
  {'code':'MN','name':'Minnesota','slug':'minnesota','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'MS','name':'Mississippi','slug':'mississippi','tier':'tier3','surrogateLegal':True,'surrogateRestricted':True},
  {'code':'MO','name':'Missouri','slug':'missouri','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'MT','name':'Montana','slug':'montana','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'NE','name':'Nebraska','slug':'nebraska','tier':'tier3','surrogateLegal':False,'surrogateRestricted':False},
  {'code':'NV','name':'Nevada','slug':'nevada','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'NH','name':'New Hampshire','slug':'new-hampshire','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'NJ','name':'New Jersey','slug':'new-jersey','tier':'tier1','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'NM','name':'New Mexico','slug':'new-mexico','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'NY','name':'New York','slug':'new-york','tier':'tier1','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'NC','name':'North Carolina','slug':'north-carolina','tier':'tier3','surrogateLegal':True,'surrogateRestricted':True},
  {'code':'ND','name':'North Dakota','slug':'north-dakota','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'OH','name':'Ohio','slug':'ohio','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'OK','name':'Oklahoma','slug':'oklahoma','tier':'tier3','surrogateLegal':True,'surrogateRestricted':True},
  {'code':'OR','name':'Oregon','slug':'oregon','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'PA','name':'Pennsylvania','slug':'pennsylvania','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'RI','name':'Rhode Island','slug':'rhode-island','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'SC','name':'South Carolina','slug':'south-carolina','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'SD','name':'South Dakota','slug':'south-dakota','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'TN','name':'Tennessee','slug':'tennessee','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'TX','name':'Texas','slug':'texas','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'UT','name':'Utah','slug':'utah','tier':'tier3','surrogateLegal':True,'surrogateRestricted':True},
  {'code':'VT','name':'Vermont','slug':'vermont','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'VA','name':'Virginia','slug':'virginia','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'WA','name':'Washington','slug':'washington','tier':'tier2','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'WV','name':'West Virginia','slug':'west-virginia','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'WI','name':'Wisconsin','slug':'wisconsin','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
  {'code':'WY','name':'Wyoming','slug':'wyoming','tier':'tier3','surrogateLegal':True,'surrogateRestricted':False},
]

# Compensation data
EGG_DONOR = {
    'tier1': {'first_min': 10000, 'first_max': 15000, 'repeat_min': 12000, 'repeat_max': 20000},
    'tier2': {'first_min': 8000,  'first_max': 12000, 'repeat_min': 10000, 'repeat_max': 15000},
    'tier3': {'first_min': 6000,  'first_max': 10000, 'repeat_min': 8000,  'repeat_max': 12000},
}

SURROGATE = {
    'tier1': {'first_min': 60000, 'first_max': 80000, 'exp_min': 70000, 'exp_max': 100000},
    'tier2': {'first_min': 50000, 'first_max': 65000, 'exp_min': 60000, 'exp_max': 80000},
    'tier3': {'first_min': 40000, 'first_max': 55000, 'exp_min': 50000, 'exp_max': 70000},
}

TIER_LABELS = {
    'tier1': 'Above Average',
    'tier2': 'Above Average',
    'tier3': 'Standard',
}

# Tier1 surrogacy-friendly states
TIER1_FRIENDLY = {'CA', 'CT', 'DE', 'NJ', 'NY', 'WA', 'MA', 'IL', 'NV'}

def fmt(n):
    return f"${n:,}"

NAV = """<nav class="nav">
  <div class="container">
    <div class="nav__inner">
      <a href="/" class="nav__logo">EggSurrogate<span>Pay</span></a>
      <button class="nav__toggle" id="nav-toggle" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>
      <div class="nav__links" id="nav-links">
        <a href="../egg-donor-pay.html">Egg Donor Pay</a>
        <a href="../surrogate-pay.html">Surrogate Pay</a>
        <a href="../egg-donor-application.html" class="btn--nav">Apply Now</a>
      </div>
    </div>
  </div>
</nav>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div>
        <div class="footer__brand">EggSurrogate<span>Pay</span></div>
        <p class="footer__desc">Free compensation calculators and application platform for egg donors and surrogates.</p>
      </div>
      <div class="footer__col">
        <h4>Egg Donation</h4>
        <a href="../egg-donor-pay.html">Pay Calculator</a>
        <a href="../egg-donor-requirements.html">Requirements</a>
        <a href="../how-egg-donation-works.html">How It Works</a>
        <a href="../egg-donor-application.html">Apply Now</a>
      </div>
      <div class="footer__col">
        <h4>Surrogacy</h4>
        <a href="../surrogate-pay.html">Pay Calculator</a>
        <a href="../surrogate-requirements.html">Requirements</a>
        <a href="../how-surrogacy-works.html">How It Works</a>
        <a href="../surrogate-application.html">Apply Now</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 EggSurrogatePay.com · hello@eggsurrogatepay.com</span>
      <div class="footer__legal">
        <a href="../privacy-policy.html">Privacy Policy</a>
        <a href="../terms-of-service.html">Terms of Service</a>
        <a href="../disclaimer.html">Disclaimer</a>
        <a href="../methodology.html">Methodology</a>
        <a href="../faq.html">FAQ</a>
        <a href="../about.html">About</a>
        <a href="../data-sources.html">Data Sources</a>
        <a href="mailto:hello@eggsurrogatepay.com">Contact</a>
      </div>
    </div>
  </div>
</footer>
<script>
  document.getElementById('nav-toggle').addEventListener('click', function() {
    document.getElementById('nav-links').classList.toggle('open');
  });
</script>"""

EGG_COMPARE_LINKS = """<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px;">
  <a href="egg-donor-pay-california.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>California</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$11,000–$17,000</span></a>
  <a href="egg-donor-pay-new-york.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>New York</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$11,000–$17,000</span></a>
  <a href="egg-donor-pay-texas.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Texas</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$9,000–$14,000</span></a>
  <a href="egg-donor-pay-florida.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Florida</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$9,000–$14,000</span></a>
  <a href="egg-donor-pay-illinois.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Illinois</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$9,000–$14,000</span></a>
  <a href="egg-donor-pay-colorado.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Colorado</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$9,000–$14,000</span></a>
</div>"""

SURROGATE_COMPARE_LINKS = """<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px;">
  <a href="surrogate-pay-california.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>California</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$67,000–$98,000</span></a>
  <a href="surrogate-pay-new-york.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>New York</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$67,000–$98,000</span></a>
  <a href="surrogate-pay-texas.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Texas</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
  <a href="surrogate-pay-florida.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Florida</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
  <a href="surrogate-pay-illinois.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Illinois</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
  <a href="surrogate-pay-colorado.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Colorado</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
</div>"""


def get_tier_content_egg(state_name, tier, repeat_min, repeat_max):
    if tier == 'tier1':
        return f"""<p style="color:var(--text-light); margin-bottom:16px;">{state_name} is one of the highest-paying states for egg donors in the US. Several factors drive compensation above the national average:</p>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">💰</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">High Cost of Living</h3><p style="font-size:0.88rem; color:var(--text-light);">Agencies in {state_name} adjust compensation to reflect higher living costs.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">🏥</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">High Clinic Density</h3><p style="font-size:0.88rem; color:var(--text-light);">More fertility clinics means more competition for qualified donors.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">📈</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Strong Demand</h3><p style="font-size:0.88rem; color:var(--text-light);">High demand from intended parents requiring diverse donor profiles.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">⭐</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Premium Market</h3><p style="font-size:0.88rem; color:var(--text-light);">Intended parents can pay premium agency fees, enabling higher donor pay.</p></div>
</div>"""
    elif tier == 'tier2':
        return f"""<p style="color:var(--text-light); margin-bottom:16px;">{state_name} offers above-average egg donor compensation driven by a growing fertility industry and strong demand from intended parents.</p>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">🏥</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Growing Clinic Network</h3><p style="font-size:0.88rem; color:var(--text-light);">Expanding fertility clinic presence in {state_name}'s major metro areas.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">📈</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Active Agency Presence</h3><p style="font-size:0.88rem; color:var(--text-light);">Multiple licensed agencies operate in {state_name} and compete for donors.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">💰</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Rising Demand</h3><p style="font-size:0.88rem; color:var(--text-light);">Increasing demand from intended parents drives above-average rates.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">🌟</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Accessible Location</h3><p style="font-size:0.88rem; color:var(--text-light);">Donors in {state_name} can access clinics in nearby major markets as well.</p></div>
</div>"""
    else:
        return f"""<p style="color:var(--text-light); margin-bottom:16px;">{state_name} offers standard egg donor compensation consistent with national averages. The process and requirements are identical to higher-paying states.</p>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">✅</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Standard Compensation</h3><p style="font-size:0.88rem; color:var(--text-light);">Consistent with national averages across all agencies.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">💵</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Lower Cost of Living</h3><p style="font-size:0.88rem; color:var(--text-light);">Your compensation goes further in {state_name} than in coastal markets.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">🤝</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Agency Access</h3><p style="font-size:0.88rem; color:var(--text-light);">Work with agencies serving {state_name} or travel to a nearby major market.</p></div>
  <div class="feature-card" style="text-align:left; padding:24px;"><div style="font-size:1.4rem; margin-bottom:8px;">🔁</div><h3 style="font-size:0.95rem; font-weight:700; color:var(--primary); margin-bottom:6px;">Repeat Earnings</h3><p style="font-size:0.88rem; color:var(--text-light);">Repeat donors earn {fmt(repeat_min)}–{fmt(repeat_max)}, above the national average for repeats.</p></div>
</div>"""


def get_legal_content(state_name, code, tier):
    if code in TIER1_FRIENDLY or tier == 'tier1':
        return f"""<p style="color:var(--text-light); margin-bottom:16px;">{state_name} is one of the most surrogacy-friendly states in the US. Surrogacy contracts are fully enforceable, pre-birth orders are available, and agencies actively prioritize surrogates in {state_name} due to the strong legal framework.</p>
<p style="color:var(--text-light);">A reproductive attorney will be provided and funded by the agency before any procedures begin.</p>"""
    else:
        return f"""<p style="color:var(--text-light); margin-bottom:16px;">Gestational surrogacy is practiced in {state_name}. Agreements are recognized, and agencies actively recruit surrogates here. A reproductive attorney — funded by the agency — will review your contract before any procedures begin.</p>"""


def get_legal_faq(state_name, code, tier):
    if code in TIER1_FRIENDLY or tier == 'tier1':
        return f"Yes. {state_name} is one of the most surrogacy-friendly states in the US, with fully enforceable contracts and pre-birth orders available."
    else:
        return f"Yes, gestational surrogacy is practiced in {state_name}. A reproductive attorney will be involved to ensure your contract is legally sound before proceeding."


def get_restricted_banner(state_name):
    return f"""
<section class="section">
  <div class="container container--narrow">
    <div style="background:#fff3cd; border:1px solid #ffc107; border-radius:var(--radius-sm); padding:24px;">
      <h3 style="color:#856404; font-weight:700; margin-bottom:8px;">⚠️ Surrogacy Restrictions in {state_name}</h3>
      <p style="color:#856404; font-size:0.95rem;">{state_name} has limited legal protections for surrogacy. While surrogacy is practiced here, contracts may have limited enforceability and agency options may be more limited than in other states. We recommend consulting with a {state_name} reproductive attorney before proceeding.</p>
    </div>
  </div>
</section>"""


def get_tier_label(tier):
    if tier == 'tier1':
        return 'Above the National Average'
    elif tier == 'tier2':
        return 'Above Average'
    else:
        return 'Standard Rates'


def generate_egg_donor_page(state):
    name = state['name']
    slug = state['slug']
    tier = state['tier']
    code = state['code']

    ed = EGG_DONOR[tier]
    first_min = ed['first_min']
    first_max = ed['first_max']
    repeat_min = ed['repeat_min']
    repeat_max = ed['repeat_max']
    first_total_min = first_min + 1000
    first_total_max = first_max + 2000
    repeat_total_min = repeat_min + 1000
    repeat_total_max = repeat_max + 2000

    tier_content = get_tier_content_egg(name, tier, repeat_min, repeat_max)
    tier_label = get_tier_label(tier)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} Egg Donor Pay 2026: Earn {fmt(first_min)}–{fmt(first_max)}</title>
  <meta name="description" content="Earn {fmt(first_min)}–{fmt(first_max)} as an egg donor in {name}. See requirements, timeline, and how to apply for 2026 programs.">
  <link rel="canonical" href="https://eggsurrogatepay.com/guides/egg-donor-pay-{slug}.html">
  <link rel="stylesheet" href="../assets/styles.css">
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-RR00CQ3CMS');
    gtag('event', 'state_page_viewed', {{
      'state': '{name}',
      'service_type': 'egg_donor',
      'state_tier': '{tier}'
    }});
  (function() {
    function _loadGA() {
      var s = document.createElement('script');
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-RR00CQ3CMS';
      s.async = true;
      s.onload = function() { gtag('event', 'page_engaged'); };
      document.head.appendChild(s);
    }
    ['mousedown','scroll','touchstart','keydown'].forEach(function(e) {
      document.addEventListener(e, _loadGA, {once: true, passive: true});
    });
  })();
  </script>
</head>
<body>

{NAV}

<div class="page-hero">
  <div class="container">
    <h1 class="page-hero__title">Egg Donor Pay in {name} (2026)</h1>
    <p class="page-hero__subtitle">First-time egg donors in {name} earn {fmt(first_min)}–{fmt(first_max)}. See full compensation breakdown, requirements, and how to apply.</p>
  </div>
</div>

<section class="section">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Compensation</span>
      <h2 class="section__title">Egg Donor Compensation in {name}</h2>
    </div>

    <div class="calculator" style="margin-bottom:32px;">
      <div class="calculator__header">
        <h3>First-Time Egg Donor</h3>
      </div>
      <div class="calculator__body">
        <table style="width:100%; border-collapse:collapse;">
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:12px 8px; color:var(--text-light);">Base Compensation</td>
            <td style="padding:12px 8px; text-align:right; font-weight:600;">{fmt(first_min)} – {fmt(first_max)}</td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:12px 8px; color:var(--text-light);">Travel &amp; Expenses</td>
            <td style="padding:12px 8px; text-align:right; font-weight:600;">$1,000 – $2,000</td>
          </tr>
          <tr style="background:var(--bg-accent);">
            <td style="padding:12px 8px; font-weight:700; color:var(--primary);">Total Potential</td>
            <td style="padding:12px 8px; text-align:right; font-weight:800; color:var(--primary); font-size:1.1rem;">{fmt(first_total_min)} – {fmt(first_total_max)}</td>
          </tr>
        </table>
      </div>
    </div>

    <div class="calculator" style="margin-bottom:32px;">
      <div class="calculator__header">
        <h3>Repeat Egg Donor</h3>
      </div>
      <div class="calculator__body">
        <table style="width:100%; border-collapse:collapse;">
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:12px 8px; color:var(--text-light);">Base Compensation</td>
            <td style="padding:12px 8px; text-align:right; font-weight:600;">{fmt(repeat_min)} – {fmt(repeat_max)}</td>
          </tr>
          <tr style="border-bottom:1px solid var(--border);">
            <td style="padding:12px 8px; color:var(--text-light);">Travel &amp; Expenses</td>
            <td style="padding:12px 8px; text-align:right; font-weight:600;">$1,000 – $2,000</td>
          </tr>
          <tr style="background:var(--bg-accent);">
            <td style="padding:12px 8px; font-weight:700; color:var(--primary);">Total Potential</td>
            <td style="padding:12px 8px; text-align:right; font-weight:800; color:var(--primary); font-size:1.1rem;">{fmt(repeat_total_min)} – {fmt(repeat_total_max)}</td>
          </tr>
        </table>
      </div>
    </div>

    <div class="results" style="display:block; padding:16px; background:var(--bg-accent); border-radius:var(--radius-sm); font-size:0.85rem; color:var(--text-muted);">
      ⚠️ Estimated ranges based on average compensation in {name}. Actual compensation is set by the agency based on your profile and current demand. Sources: Industry surveys of 30+ agencies, 2024–2026 data.
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">About {name}</span>
      <h2 class="section__title">Why {name} Pays {tier_label}</h2>
    </div>
    {tier_content}
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Requirements</span>
      <h2 class="section__title">Egg Donor Requirements in {name}</h2>
    </div>
    <p style="color:var(--text-light); margin-bottom:16px;">Requirements are set by agencies and consistent across all states:</p>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Age: 21–31 years old</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>BMI under 32</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>High school diploma minimum (bachelor's preferred)</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Non-smoker</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>No disqualifying health conditions</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>U.S. citizen or permanent resident</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Able to commit to 10–15 clinic visits over 3–6 months</span></div>
    </div>
    <p style="margin-top:16px; font-size:0.85rem; color:var(--text-muted);">Final eligibility is determined by the agency's medical team.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">The Process</span>
      <h2 class="section__title">How Egg Donation Works in {name}</h2>
    </div>
    <div class="steps-list">
      <div class="step-item"><div class="step-item__icon">📋</div><div><div class="step-item__title">Apply</div><p class="step-item__text">Complete application in 10–15 minutes. We match you with agencies in {name} within 48 hours.</p></div></div>
      <div class="step-item"><div class="step-item__icon">🩺</div><div><div class="step-item__title">Medical Screening</div><p class="step-item__text">Physical exam, bloodwork, and genetic testing — coordinated and paid by the agency.</p></div></div>
      <div class="step-item"><div class="step-item__icon">🧠</div><div><div class="step-item__title">Psychological Evaluation</div><p class="step-item__text">Standard psych assessment included at no cost to you.</p></div></div>
      <div class="step-item"><div class="step-item__icon">📄</div><div><div class="step-item__title">Legal Contract</div><p class="step-item__text">Review and sign donor agreement. Legal fees covered by the agency.</p></div></div>
      <div class="step-item"><div class="step-item__icon">💉</div><div><div class="step-item__title">Stimulation &amp; Retrieval</div><p class="step-item__text">10–14 days of hormone injections, then a 30-minute outpatient retrieval procedure.</p></div></div>
      <div class="step-item"><div class="step-item__icon">💰</div><div><div class="step-item__title">Compensation</div><p class="step-item__text">Paid within 2–4 weeks of retrieval. Total: {fmt(first_total_min)}–{fmt(first_total_max)} for first-time donors.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">FAQ</span>
      <h2 class="section__title">Egg Donor FAQ: {name}</h2>
    </div>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">Do I have to live in {name} to donate eggs here?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">Not necessarily. Some agencies work with donors who travel from nearby states. However, you'll need to attend 10–15 clinic appointments locally over 3–6 months, so proximity matters.</p>
      </details>
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">Is egg donation taxable in {name}?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">Yes. Egg donor compensation is considered taxable income at the federal level. You'll receive a 1099 from the agency. Consult a tax professional for {name}-specific guidance.</p>
      </details>
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">How many times can I donate in {name}?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">The ASRM recommends a maximum of 6 donation cycles per donor. Most agencies follow this guideline. Repeat donors often earn higher compensation.</p>
      </details>
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">How long does the process take?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">From application to receiving compensation: 3–6 months. This includes agency screening, medical evaluation, legal review, and the donation cycle.</p>
      </details>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Compare States</span>
      <h2 class="section__title">Egg Donor Pay by State</h2>
      <p class="section__subtitle">See how {name} compares to other states</p>
    </div>
    {EGG_COMPARE_LINKS}
    <div class="text-center" style="margin-top:24px;">
      <a href="../egg-donor-pay.html" class="btn btn--outline">View All States + Calculator →</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div style="text-align:center; background:var(--bg-accent); border-radius:var(--radius); padding:48px 32px;">
      <h2 style="font-size:1.6rem; font-weight:800; color:var(--primary); margin-bottom:12px;">Ready to Apply in {name}?</h2>
      <p style="color:var(--text-light); margin-bottom:32px;">Complete our 10-minute application. We'll connect you with licensed agencies serving {name}.</p>
      <div class="btn-group" style="justify-content:center;">
        <a href="../egg-donor-application.html" class="btn btn--primary btn--lg" onclick="gtag('event','application_started',{{'source':'state_page','state':'{name}','service_type':'egg_donor'}});">Start Your Application →</a>
        <a href="../egg-donor-pay.html" class="btn btn--outline">Calculate Your Pay</a>
      </div>
    </div>
  </div>
</section>

{FOOTER}
</body>
</html>"""

    path = os.path.join(GUIDES_DIR, f'egg-donor-pay-{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


def generate_surrogate_page_illegal(state):
    """For states where surrogacy is illegal (MI, LA, NE)"""
    name = state['name']
    slug = state['slug']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Surrogacy in {name} (2026) | EggSurrogatePay.com</title>
  <meta name="description" content="Learn about surrogacy laws in {name} and egg donor opportunities available to residents. Egg donors in {name} earn $7,000–$12,000.">
  <link rel="canonical" href="https://eggsurrogatepay.com/guides/surrogate-pay-{slug}.html">
  <link rel="stylesheet" href="../assets/styles.css">
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-RR00CQ3CMS');
    gtag('event', 'state_page_viewed', {{'state': '{name}', 'service_type': 'surrogate', 'surrogate_legal': false}});
  (function() {
    function _loadGA() {
      var s = document.createElement('script');
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-RR00CQ3CMS';
      s.async = true;
      s.onload = function() { gtag('event', 'page_engaged'); };
      document.head.appendChild(s);
    }
    ['mousedown','scroll','touchstart','keydown'].forEach(function(e) {
      document.addEventListener(e, _loadGA, {once: true, passive: true});
    });
  })();
  </script>
</head>
<body>

{NAV}

<div class="page-hero">
  <div class="container">
    <h1 class="page-hero__title">Surrogacy in {name}: What Residents Need to Know</h1>
    <p class="page-hero__subtitle">Surrogacy laws in {name} are restrictive. Learn about your options — including egg donation, which is available in all 50 states.</p>
  </div>
</div>

<section class="section">
  <div class="container container--narrow">
    <div style="background:#f8d7da; border:1px solid #f5c6cb; border-radius:var(--radius-sm); padding:24px; margin-bottom:32px;">
      <h2 style="color:#721c24; font-weight:700; margin-bottom:8px;">⚠️ Surrogacy Laws in {name}</h2>
      <p style="color:#721c24;">Commercial surrogacy has significant legal restrictions in {name}. Surrogacy contracts may not be enforceable. Residents interested in surrogacy typically work with agencies and attorneys in more surrogacy-friendly states.</p>
      <p style="color:#721c24; margin-top:8px;">We recommend consulting with a reproductive attorney if you are interested in surrogacy as a {name} resident.</p>
    </div>

    <div style="background:var(--bg-accent); border:1px solid rgba(45,95,93,0.15); border-radius:var(--radius); padding:32px; text-align:center;">
      <h2 style="font-size:1.3rem; font-weight:800; color:var(--primary); margin-bottom:12px;">Egg Donation Is Available in {name}</h2>
      <p style="color:var(--text-light); margin-bottom:24px;">Egg donation is fully legal in {name}. First-time egg donors earn $7,000–$12,000, plus travel and expense reimbursement.</p>
      <a href="egg-donor-pay-{slug}.html" class="btn btn--primary">Learn About Egg Donation in {name} →</a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Nearby Options</span>
      <h2 class="section__title">Surrogacy in Nearby States</h2>
      <p class="section__subtitle">Many {name} residents pursue surrogacy in neighboring states with clear legal frameworks</p>
    </div>
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px;">
      <a href="surrogate-pay-illinois.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Illinois</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
      <a href="surrogate-pay-colorado.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Colorado</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
      <a href="surrogate-pay-nevada.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Nevada</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
      <a href="surrogate-pay-california.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>California</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$67,000–$98,000</span></a>
      <a href="surrogate-pay-washington.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Washington</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
      <a href="surrogate-pay-oregon.html" class="feature-card" style="text-align:center; padding:16px; text-decoration:none;"><strong>Oregon</strong><br><span style="color:var(--text-muted); font-size:0.88rem;">$57,000–$83,000</span></a>
    </div>
  </div>
</section>

{FOOTER}
</body>
</html>"""

    path = os.path.join(GUIDES_DIR, f'surrogate-pay-{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


def generate_surrogate_page(state):
    name = state['name']
    slug = state['slug']
    tier = state['tier']
    code = state['code']
    restricted = state['surrogateRestricted']

    sp = SURROGATE[tier]
    first_min = sp['first_min']
    first_max = sp['first_max']
    exp_min = sp['exp_min']
    exp_max = sp['exp_max']
    first_total_min = first_min + 7000
    first_total_max = first_max + 18000
    exp_total_min = exp_min + 7000
    exp_total_max = exp_max + 18000

    legal_content = get_legal_content(name, code, tier)
    legal_faq = get_legal_faq(name, code, tier)
    restricted_banner = get_restricted_banner(name) if restricted else ''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} Surrogate Pay 2026: Earn {fmt(first_min)}–{fmt(first_max)}</title>
  <meta name="description" content="Earn {fmt(first_min)}–{fmt(first_max)} as a surrogate in {name}. See base pay, allowances, and requirements for 2026 placements.">
  <link rel="canonical" href="https://eggsurrogatepay.com/guides/surrogate-pay-{slug}.html">
  <link rel="stylesheet" href="../assets/styles.css">
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-RR00CQ3CMS');
    gtag('event', 'state_page_viewed', {{
      'state': '{name}',
      'service_type': 'surrogate',
      'state_tier': '{tier}',
      'surrogate_legal': true
    }});
  (function() {
    function _loadGA() {
      var s = document.createElement('script');
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-RR00CQ3CMS';
      s.async = true;
      s.onload = function() { gtag('event', 'page_engaged'); };
      document.head.appendChild(s);
    }
    ['mousedown','scroll','touchstart','keydown'].forEach(function(e) {
      document.addEventListener(e, _loadGA, {once: true, passive: true});
    });
  })();
  </script>
</head>
<body>

{NAV}

<div class="page-hero">
  <div class="container">
    <h1 class="page-hero__title">Surrogate Pay in {name} (2026)</h1>
    <p class="page-hero__subtitle">First-time surrogates in {name} earn {fmt(first_min)}–{fmt(first_max)} base compensation plus monthly allowances. See full breakdown below.</p>
  </div>
</div>

<section class="section">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Compensation</span>
      <h2 class="section__title">Surrogate Compensation in {name}</h2>
    </div>

    <div class="calculator" style="margin-bottom:32px;">
      <div class="calculator__header"><h3>First-Time Surrogate</h3></div>
      <div class="calculator__body">
        <table style="width:100%; border-collapse:collapse;">
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Base Compensation</td><td style="padding:12px 8px; text-align:right; font-weight:600;">{fmt(first_min)} – {fmt(first_max)}</td></tr>
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Monthly Allowance</td><td style="padding:12px 8px; text-align:right; font-weight:600;">$3,000 – $6,000</td></tr>
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Maternity Clothing</td><td style="padding:12px 8px; text-align:right; font-weight:600;">$1,000 – $2,000</td></tr>
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Lost Wages</td><td style="padding:12px 8px; text-align:right; font-weight:600;">$3,000 – $10,000</td></tr>
          <tr style="background:var(--bg-accent);"><td style="padding:12px 8px; font-weight:700; color:var(--primary);">Total Potential</td><td style="padding:12px 8px; text-align:right; font-weight:800; color:var(--primary); font-size:1.1rem;">{fmt(first_total_min)} – {fmt(first_total_max)}</td></tr>
        </table>
      </div>
    </div>

    <div class="calculator" style="margin-bottom:32px;">
      <div class="calculator__header"><h3>Experienced Surrogate</h3></div>
      <div class="calculator__body">
        <table style="width:100%; border-collapse:collapse;">
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Base Compensation</td><td style="padding:12px 8px; text-align:right; font-weight:600;">{fmt(exp_min)} – {fmt(exp_max)}</td></tr>
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Monthly Allowance</td><td style="padding:12px 8px; text-align:right; font-weight:600;">$3,000 – $6,000</td></tr>
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Maternity Clothing</td><td style="padding:12px 8px; text-align:right; font-weight:600;">$1,000 – $2,000</td></tr>
          <tr style="border-bottom:1px solid var(--border);"><td style="padding:12px 8px; color:var(--text-light);">Lost Wages</td><td style="padding:12px 8px; text-align:right; font-weight:600;">$3,000 – $10,000</td></tr>
          <tr style="background:var(--bg-accent);"><td style="padding:12px 8px; font-weight:700; color:var(--primary);">Total Potential</td><td style="padding:12px 8px; text-align:right; font-weight:800; color:var(--primary); font-size:1.1rem;">{fmt(exp_total_min)} – {fmt(exp_total_max)}</td></tr>
        </table>
      </div>
    </div>

    <div class="results" style="display:block; padding:16px; background:var(--bg-accent); border-radius:var(--radius-sm); font-size:0.85rem; color:var(--text-muted);">
      ⚠️ Estimated ranges based on average compensation in {name}. Actual compensation is determined by the agency. Sources: Industry surveys of 30+ agencies, 2024–2026 data.
    </div>
  </div>
</section>

{restricted_banner}

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Legal</span>
      <h2 class="section__title">Surrogacy Laws in {name}</h2>
    </div>
    {legal_content}
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Requirements</span>
      <h2 class="section__title">Surrogate Requirements in {name}</h2>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Age: 21–40 years old</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Have given birth to at least one healthy child</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>BMI under 32</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Non-smoker</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>No disqualifying health conditions</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>U.S. citizen or permanent resident</span></div>
      <div class="feature-card" style="padding:14px 20px; display:flex; gap:12px; align-items:center;"><span>✅</span><span>Financially stable (not receiving government assistance)</span></div>
    </div>
    <p style="margin-top:16px; font-size:0.85rem; color:var(--text-muted);">Final eligibility is determined by the agency's medical team.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">The Process</span>
      <h2 class="section__title">How Surrogacy Works in {name}</h2>
    </div>
    <div class="steps-list">
      <div class="step-item"><div class="step-item__icon">📋</div><div><div class="step-item__title">Apply</div><p class="step-item__text">Complete application in 10–15 minutes. Agency contacts you within 48 hours.</p></div></div>
      <div class="step-item"><div class="step-item__icon">🩺</div><div><div class="step-item__title">Medical Screening</div><p class="step-item__text">Physical exam, bloodwork, and uterine evaluation — paid for by the agency.</p></div></div>
      <div class="step-item"><div class="step-item__icon">👨‍👩‍👧</div><div><div class="step-item__title">Match with Intended Parents</div><p class="step-item__text">Review profiles and meet potential intended parents. You always have the right to say no.</p></div></div>
      <div class="step-item"><div class="step-item__icon">📄</div><div><div class="step-item__title">Legal Contract</div><p class="step-item__text">Surrogacy agreement reviewed by your own attorney, funded by the agency.</p></div></div>
      <div class="step-item"><div class="step-item__icon">🍼</div><div><div class="step-item__title">Embryo Transfer &amp; Pregnancy</div><p class="step-item__text">Monthly compensation begins immediately after transfer. All medical costs covered.</p></div></div>
      <div class="step-item"><div class="step-item__icon">💰</div><div><div class="step-item__title">Delivery &amp; Final Payment</div><p class="step-item__text">Remaining compensation disbursed around delivery. Post-delivery allowances continue up to 6 weeks.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">FAQ</span>
      <h2 class="section__title">Surrogate FAQ: {name}</h2>
    </div>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">Is surrogacy legal in {name}?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">{legal_faq}</p>
      </details>
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">Do I have to live in {name} to be a surrogate here?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">Typically yes. Most agencies require you to live in the state where you carry the pregnancy, as medical care and legal jurisdiction are state-specific.</p>
      </details>
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">Is surrogate pay taxable in {name}?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">Base compensation is generally taxable at the federal level. Expense reimbursements (travel, maternity clothes) are typically not taxable. Consult a tax professional for {name}-specific guidance.</p>
      </details>
      <details style="background:white; border:1px solid var(--border); border-radius:var(--radius-sm); padding:20px;">
        <summary style="font-weight:700; cursor:pointer; color:var(--primary);">How long does surrogacy take in {name}?</summary>
        <p style="margin-top:12px; color:var(--text-light); line-height:1.7;">18–24 months from application to delivery: matching (1–6 months), medical screening, legal review, and the full pregnancy term.</p>
      </details>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow">
    <div class="text-center mb-8">
      <span class="badge">Compare States</span>
      <h2 class="section__title">Surrogate Pay by State</h2>
    </div>
    {SURROGATE_COMPARE_LINKS}
    <div class="text-center" style="margin-top:24px;">
      <a href="../surrogate-pay.html" class="btn btn--outline">View All States + Calculator →</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div style="text-align:center; background:var(--bg-accent); border-radius:var(--radius); padding:48px 32px;">
      <h2 style="font-size:1.6rem; font-weight:800; color:var(--primary); margin-bottom:12px;">Ready to Apply in {name}?</h2>
      <p style="color:var(--text-light); margin-bottom:32px;">Complete our 10-minute application. We'll connect you with licensed agencies serving {name}.</p>
      <div class="btn-group" style="justify-content:center;">
        <a href="../surrogate-application.html" class="btn btn--primary btn--lg" onclick="gtag('event','application_started',{{'source':'state_page','state':'{name}','service_type':'surrogate'}});">Start Your Application →</a>
        <a href="../surrogate-pay.html" class="btn btn--outline">Calculate Your Pay</a>
      </div>
    </div>
  </div>
</section>

{FOOTER}
</body>
</html>"""

    path = os.path.join(GUIDES_DIR, f'surrogate-pay-{slug}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path


# Generate all pages
egg_count = 0
surrogate_count = 0

for state in states:
    # Generate egg donor page
    generate_egg_donor_page(state)
    egg_count += 1

    # Generate surrogate page
    if not state['surrogateLegal']:
        generate_surrogate_page_illegal(state)
    else:
        generate_surrogate_page(state)
    surrogate_count += 1

print(f"Generated {egg_count} egg donor pages")
print(f"Generated {surrogate_count} surrogate pages")
print(f"Total: {egg_count + surrogate_count} pages")
print(f"Pages written to: {GUIDES_DIR}")
