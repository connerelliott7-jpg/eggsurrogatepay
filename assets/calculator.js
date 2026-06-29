// ===========================
// EggSurrogatePay Calculator Logic
// ===========================

document.addEventListener('DOMContentLoaded', function () {

  // ---- Zip Code → State Detection ----
  const zipInputs = document.querySelectorAll('[data-zip-input]');

  zipInputs.forEach(function (zipInput) {
    const detectEl = document.getElementById(zipInput.dataset.detectTarget || 'zip-detect');
    const stateHidden = document.getElementById(zipInput.dataset.stateTarget || 'state-hidden');

    zipInput.addEventListener('input', function () {
      const val = this.value.replace(/\D/g, '').slice(0, 5);
      this.value = val;

      if (val.length === 5) {
        const result = getStateFromZip(val);
        if (result && detectEl) {
          detectEl.textContent = '📍 Detected: ' + result.name;
          detectEl.style.display = 'flex';
          if (stateHidden) stateHidden.value = result.code;
        } else if (detectEl) {
          detectEl.textContent = '';
          if (stateHidden) stateHidden.value = '';
        }
      } else if (detectEl) {
        detectEl.textContent = '';
        if (stateHidden) stateHidden.value = '';
      }
    });
  });

  // ---- Egg Donor Calculator ----
  const eggDonorForm = document.getElementById('egg-donor-calc');
  if (eggDonorForm) {
    initEggDonorCalc(eggDonorForm);
    if (typeof gtag === 'function') {
      gtag('event', 'calculator_viewed', { service_type: 'egg_donor' });
    }
  }

  // ---- Surrogate Calculator ----
  const surrogateForm = document.getElementById('surrogate-calc');
  if (surrogateForm) {
    initSurrogateCalc(surrogateForm);
    if (typeof gtag === 'function') {
      gtag('event', 'calculator_viewed', { service_type: 'surrogate' });
    }
  }

});

// ===========================
// EGG DONOR CALCULATOR
// ===========================
function initEggDonorCalc(form) {
  const btn = form.querySelector('[data-calc-btn]');
  const resultsEl = document.getElementById('egg-donor-results');

  btn.addEventListener('click', function () {
    const zip = document.getElementById('ed-zip').value.trim();
    const experience = form.querySelector('input[name="ed-experience"]:checked');
    const education = document.getElementById('ed-education').value;
    const age = parseInt(document.getElementById('ed-age').value, 10);

    // Basic validation
    let valid = true;
    if (zip.length !== 5) {
      showFieldError('ed-zip', 'Please enter a valid 5-digit zip code');
      valid = false;
    } else {
      clearFieldError('ed-zip');
    }

    if (!experience) {
      document.getElementById('ed-experience-error').classList.add('show');
      valid = false;
    } else {
      document.getElementById('ed-experience-error').classList.remove('show');
    }

    if (!education) {
      showFieldError('ed-education', 'Please select your education level');
      valid = false;
    } else {
      clearFieldError('ed-education');
    }

    if (!age) {
      showFieldError('ed-age', 'Please select your age');
      valid = false;
    } else {
      clearFieldError('ed-age');
    }

    if (!valid) return;

    // Get state
    const stateResult = getStateFromZip(zip);
    const stateCode = stateResult ? stateResult.code : null;
    const stateName = stateResult ? stateResult.name : 'Your State';
    const tier = stateCode ? getStateTier(stateCode, 'egg_donor') : 'tier3';
    const expValue = experience.value;

    // Save inputs so the application form can pre-fill
    try {
      localStorage.setItem('esp_egg_prefill', JSON.stringify({
        zip: zip, state: stateCode || '', stateName: stateName,
        education: education, experience: expValue,
        age: document.getElementById('ed-age').value
      }));
    } catch(e) {}

    // Base compensation by tier
    let baseMin, baseMax;
    if (expValue === 'first') {
      if (tier === 'tier1') { baseMin = 10000; baseMax = 15000; }
      else if (tier === 'tier2') { baseMin = 8000; baseMax = 12000; }
      else { baseMin = 6000; baseMax = 10000; }
    } else if (expValue === 'once') {
      if (tier === 'tier1') { baseMin = 12000; baseMax = 20000; }
      else if (tier === 'tier2') { baseMin = 10000; baseMax = 15000; }
      else { baseMin = 8000; baseMax = 12000; }
    } else { // 2+
      if (tier === 'tier1') { baseMin = 14000; baseMax = 20000; }
      else if (tier === 'tier2') { baseMin = 11000; baseMax = 16000; }
      else { baseMin = 9000; baseMax = 13000; }
    }

    // Education bonus (to max)
    let eduBonus = 0;
    if (education === 'bachelors') eduBonus = 1000;
    else if (education === 'masters') eduBonus = 2000;
    baseMax += eduBonus;

    // Expenses
    const expMin = 1000;
    const expMax = 2000;

    const totalMin = baseMin + expMin;
    const totalMax = baseMax + expMax;

    const expLabel = expValue === 'first' ? 'First-Time Egg Donor' : expValue === 'once' ? 'Experienced Egg Donor (1 prior)' : 'Experienced Egg Donor (2+)';
    const eduLabel = education === 'bachelors' ? ' · Bachelor\'s Bonus Applied' : education === 'masters' ? ' · Master\'s Bonus Applied' : '';

    // Render results
    resultsEl.innerHTML = `
      <a href="/egg-donor-application" class="btn btn--secondary btn--full" style="font-size:1.05rem;padding:16px;margin-bottom:12px;" onclick="trackAppStart('egg_donor')">
        Apply Now — Earn Up to ${fmt(totalMax)} →
      </a>
      <div class="results-card">
        <div class="results-card__title">YOUR ESTIMATED COMPENSATION</div>
        <div class="results-card__label">💰 ${expLabel} in ${stateName}${eduLabel}</div>
        <div class="results-breakdown">
          <div class="results-row">
            <span class="results-row__label">Base Compensation</span>
            <span class="results-row__amount">${fmt(baseMin)} – ${fmt(baseMax)}</span>
          </div>
          <div class="results-row">
            <span class="results-row__label">+ Travel &amp; Expenses</span>
            <span class="results-row__amount">${fmt(expMin)} – ${fmt(expMax)}</span>
          </div>
          <div class="results-row total">
            <span class="results-row__label">TOTAL POTENTIAL</span>
            <span class="results-row__amount">${fmt(totalMin)} – ${fmt(totalMax)}</span>
          </div>
        </div>
        <div class="results-meta">
          <span>⏱ Timeline: 3–6 months from application</span>
          <span>📋 Commitment: 10–15 clinic visits</span>
        </div>
      </div>
      <a href="#how-it-works" class="btn btn--outline btn--full" style="margin-bottom:12px;">
        Learn More About the Process
      </a>
      <div class="results-disclaimer" id="egg-disclaimer">
        <div onclick="var b=document.getElementById('egg-disclaimer-body');b.style.display=b.style.display==='none'?'block':'none';this.querySelector('.disc-arrow').textContent=b.style.display==='none'?'▸':'▾';" style="cursor:pointer;display:flex;align-items:center;gap:6px;user-select:none;">
          <strong style="margin:0;">ℹ️ Compensation Disclaimer</strong>
          <span class="disc-arrow" style="margin-left:auto;font-size:0.85rem;">▸</span>
        </div>
        <div id="egg-disclaimer-body" style="display:none;margin-top:10px;font-size:0.85rem;line-height:1.55;">This is an estimate based on average market rates. Actual compensation is determined by the agency you work with based on current demand and your qualifications. Sources: Industry surveys of 30+ agencies, 2024–2026 data.</div>
      </div>
    `;

    btn.style.display = 'none';

    resultsEl.classList.add('show');
    resultsEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    if (typeof gtag === 'function') {
      gtag('event', 'calculator_completed', {
        service_type: 'egg_donor',
        state: stateCode || 'unknown',
        tier: tier,
        experience: expValue
      });
    }
  });
}

// ===========================
// SURROGATE CALCULATOR
// ===========================
function initSurrogateCalc(form) {
  const btn = form.querySelector('[data-calc-btn]');
  const resultsEl = document.getElementById('surrogate-results');

  btn.addEventListener('click', function () {
    const zip = document.getElementById('sur-zip').value.trim();
    const experience = form.querySelector('input[name="sur-experience"]:checked');
    const births = document.getElementById('sur-births').value;
    const age = parseInt(document.getElementById('sur-age').value, 10);

    let valid = true;
    if (zip.length !== 5) {
      showFieldError('sur-zip', 'Please enter a valid 5-digit zip code');
      valid = false;
    } else {
      clearFieldError('sur-zip');
    }

    if (!experience) {
      document.getElementById('sur-experience-error').classList.add('show');
      valid = false;
    } else {
      document.getElementById('sur-experience-error').classList.remove('show');
    }

    if (!births) {
      showFieldError('sur-births', 'Please select your number of prior births');
      valid = false;
    } else {
      clearFieldError('sur-births');
    }

    if (!age) {
      showFieldError('sur-age', 'Please select your age');
      valid = false;
    } else {
      clearFieldError('sur-age');
    }

    if (!valid) return;

    const stateResult = getStateFromZip(zip);
    const stateCode = stateResult ? stateResult.code : null;
    const stateName = stateResult ? stateResult.name : 'Your State';
    const tier = stateCode ? getStateTier(stateCode, 'surrogate') : 'tier3';
    const expValue = experience.value;

    // Base by tier
    let baseMin, baseMax;
    if (tier === 'tier1') { baseMin = 60000; baseMax = 80000; }
    else if (tier === 'tier2') { baseMin = 50000; baseMax = 65000; }
    else { baseMin = 40000; baseMax = 55000; }

    // Experience bonus
    if (expValue === 'once') { baseMin += 10000; baseMax += 10000; }
    else if (expValue === 'two_plus') { baseMin += 15000; baseMax += 15000; }

    const monthlyMin = 3000, monthlyMax = 6000;
    const clothesMin = 1000, clothesMax = 2000;
    const wagesMin = 3000, wagesMax = 10000;

    const totalMin = baseMin + monthlyMin + clothesMin + wagesMin;
    const totalMax = baseMax + monthlyMax + clothesMax + wagesMax;

    const expLabel = expValue === 'first' ? 'First-Time Surrogate' : expValue === 'once' ? 'Experienced Surrogate (1 prior)' : 'Experienced Surrogate (2+)';

    resultsEl.innerHTML = `
      <a href="/surrogate-application" class="btn btn--secondary btn--full" style="font-size:1.05rem;padding:16px;margin-bottom:12px;" onclick="trackAppStart('surrogate')">
        Apply Now — Earn Up to ${fmt(totalMax)} →
      </a>
      <div class="results-card">
        <div class="results-card__title">YOUR ESTIMATED COMPENSATION</div>
        <div class="results-card__label">💰 ${expLabel} in ${stateName}</div>
        <div class="results-breakdown">
          <div class="results-row">
            <span class="results-row__label">Base Compensation</span>
            <span class="results-row__amount">${fmt(baseMin)} – ${fmt(baseMax)}</span>
          </div>
          <div class="results-row">
            <span class="results-row__label">+ Monthly Allowance</span>
            <span class="results-row__amount">${fmt(monthlyMin)} – ${fmt(monthlyMax)}</span>
          </div>
          <div class="results-row">
            <span class="results-row__label">+ Maternity Clothes</span>
            <span class="results-row__amount">${fmt(clothesMin)} – ${fmt(clothesMax)}</span>
          </div>
          <div class="results-row">
            <span class="results-row__label">+ Lost Wages</span>
            <span class="results-row__amount">${fmt(wagesMin)} – ${fmt(wagesMax)}</span>
          </div>
          <div class="results-row total">
            <span class="results-row__label">TOTAL POTENTIAL</span>
            <span class="results-row__amount">${fmt(totalMin)} – ${fmt(totalMax)}</span>
          </div>
        </div>
        <div class="results-meta">
          <span>⏱ Timeline: 18–24 months total</span>
          <span>📋 Commitment: Full pregnancy + 6 weeks post</span>
        </div>
      </div>
      <a href="#how-it-works" class="btn btn--outline btn--full" style="margin-bottom:12px;">
        Learn More About the Process
      </a>
      <div class="results-disclaimer" id="sur-disclaimer">
        <div onclick="var b=document.getElementById('sur-disclaimer-body');b.style.display=b.style.display==='none'?'block':'none';this.querySelector('.disc-arrow').textContent=b.style.display==='none'?'▸':'▾';" style="cursor:pointer;display:flex;align-items:center;gap:6px;user-select:none;">
          <strong style="margin:0;">ℹ️ Compensation Disclaimer</strong>
          <span class="disc-arrow" style="margin-left:auto;font-size:0.85rem;">▸</span>
        </div>
        <div id="sur-disclaimer-body" style="display:none;margin-top:10px;font-size:0.85rem;line-height:1.55;">This is an estimate based on average market rates. Actual compensation is determined by the agency you work with based on current demand and your qualifications. Sources: Industry surveys of 30+ agencies, 2024–2026 data.</div>
      </div>
    `;

    btn.style.display = 'none';

    resultsEl.classList.add('show');
    resultsEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    if (typeof gtag === 'function') {
      gtag('event', 'calculator_completed', {
        service_type: 'surrogate',
        state: stateCode || 'unknown',
        tier: tier,
        experience: expValue
      });
    }
  });
}

// ===========================
// Helpers
// ===========================
function fmt(n) {
  return '$' + n.toLocaleString('en-US');
}

function showFieldError(inputId, msg) {
  const input = document.getElementById(inputId);
  if (input) input.classList.add('error');
  const errEl = document.getElementById(inputId + '-error');
  if (errEl) { errEl.textContent = msg; errEl.classList.add('show'); }
}

function clearFieldError(inputId) {
  const input = document.getElementById(inputId);
  if (input) input.classList.remove('error');
  const errEl = document.getElementById(inputId + '-error');
  if (errEl) { errEl.classList.remove('show'); }
}

function trackAppStart(serviceType) {
  if (typeof gtag === 'function') {
    gtag('event', 'cta_click', {
      cta_type: 'start_application',
      page_location: window.location.pathname
    });
  }
}
