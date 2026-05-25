# EggSurrogatePay.com

Egg donor and surrogate compensation calculator and application platform.

**Live site:** https://eggsurrogatepay.com (domain to be connected)  
**Cloudflare Pages:** https://eggsurrogatepay.pages.dev (after first deploy)

---

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Homepage | `/index.html` | Hero, comparison table, how it works |
| Egg Donor Calculator | `/egg-donor-pay.html` | Zip → state tier + education + experience |
| Surrogate Calculator | `/surrogate-pay.html` | Zip → state tier + experience + prior births |
| Egg Donor Application | `/egg-donor-application.html` | 5-step multi-step form |
| Surrogate Application | `/surrogate-application.html` | 5-step multi-step form |
| Thank You | `/thank-you.html` | Post-submission confirmation |

---

## Setup

1. Clone repo
2. Open `index.html` locally to test (no build step required)
3. Deploy via Cloudflare Pages — auto-deploys on push to `main`

---

## Configuration

### Formspree
- **Endpoint:** `https://formspree.io/f/XXXXXXXX` (replace in both application forms)
- Forms: `egg-donor-application.html`, `surrogate-application.html`
- Success redirect: `/thank-you.html`

To update: search for `XXXXXXXX` in both application HTML files and replace with your real Formspree endpoint ID.

### GA4
- **Property ID:** `G-XXXXXXXXXX` (replace in all pages)
- Events tracked: `calculator_viewed`, `calculator_completed`, `application_started`, `step_1_completed` through `step_5_completed`, `application_submitted`, `thank_you_viewed`

To update: search & replace `G-XXXXXXXXXX` across all HTML files with your real GA4 Measurement ID.

---

## Color Scheme

| Variable | Hex | Usage |
|----------|-----|-------|
| `--primary` | `#2D5F5D` | Headers, buttons, links |
| `--secondary` | `#E8956F` | CTA buttons, accents |
| `--accent` | `#F4E8D8` | Background highlights |
| `--text` | `#2C2C2C` | Body text |

---

## File Structure

```
eggsurrogatepay/
├── index.html
├── egg-donor-pay.html
├── surrogate-pay.html
├── egg-donor-application.html
├── surrogate-application.html
├── thank-you.html
├── assets/
│   ├── styles.css          # All styles, mobile-first
│   ├── calculator.js       # Calculator logic (egg donor + surrogate)
│   ├── form.js             # Multi-step form logic + validation
│   └── zip-lookup.js       # Zip code → state lookup (all 50 states)
├── CNAME                   # Add after domain purchase: eggsurrogatepay.com
├── .gitignore
└── README.md
```

---

## Deployment

### Cloudflare Pages Setup
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages → Create project
2. Connect to Git → select `eggsurrogatepay` repo
3. Settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
   - **Branch:** `main`
4. Deploy — auto-deploys on every push to `main`

### Domain Setup (after purchasing eggsurrogatepay.com)
1. Add `CNAME` file to repo root containing just: `eggsurrogatepay.com`
2. In Cloudflare Pages → Custom domains → Add `eggsurrogatepay.com`
3. Update DNS to point to Cloudflare Pages

---

## Local Development

Open any `.html` file directly in a browser. No build process, no server required.

For live-reload dev experience:
```bash
npx serve .
# or
python3 -m http.server 8080
```

---

## Compensation Logic

### Egg Donor State Tiers
| Tier | States | First-Time | Repeat |
|------|--------|-----------|--------|
| 1 | CA, NY, MA, CT, NJ | $10k–$15k | $12k–$20k |
| 2 | WA, OR, IL, TX, CO, FL, GA | $8k–$12k | $10k–$15k |
| 3 | All others | $6k–$10k | $8k–$12k |

Education bonuses: Bachelor's +$1k to max · Master's+ +$2k to max

### Surrogate State Tiers
| Tier | States | First-Time | Experienced |
|------|--------|-----------|-------------|
| 1 | CA, NY, MA, CT, NJ, DE | $60k–$80k | +$10k–$20k |
| 2 | WA, OR, IL, TX, CO, FL, GA | $50k–$65k | +$10k–$15k |
| 3 | All others | $40k–$55k | +$5k–$10k |

---

## Contact

hello@eggsurrogatepay.com
