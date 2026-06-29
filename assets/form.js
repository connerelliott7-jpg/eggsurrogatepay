// ===========================
// EggSurrogatePay Multi-Step Form Logic
// ===========================

document.addEventListener('DOMContentLoaded', function () {
  const multiForm = document.getElementById('multi-step-form');
  if (!multiForm) return;

  const serviceType = multiForm.dataset.serviceType || 'egg_donor';
  const totalSteps = parseInt(multiForm.dataset.totalSteps || '5', 10);
  let currentStep = 1;

  const progressFill = document.getElementById('progress-fill');
  const progressLabel = document.getElementById('progress-label');

  // Track page view
  if (typeof gtag === 'function') {
    gtag('event', 'application_viewed', { service_type: serviceType });
  }

  function showStep(step) {
    document.querySelectorAll('.form-step').forEach(function (el) {
      el.classList.remove('active');
    });
    const target = document.getElementById('step-' + step);
    if (target) target.classList.add('active');

    const pct = Math.round((step / totalSteps) * 100);
    if (progressFill) progressFill.style.width = pct + '%';
    if (progressLabel) progressLabel.textContent = 'Step ' + step + ' of ' + totalSteps;

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Next buttons
  document.querySelectorAll('[data-next-step]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const fromStep = parseInt(this.dataset.nextStep, 10) - 1;
      if (validateStep(fromStep)) {
        currentStep = fromStep + 1;
        showStep(currentStep);
        if (typeof gtag === 'function') {
          gtag('event', 'form_step_completed', { service_type: serviceType, step: fromStep });
        }
      }
    });
  });

  // Back buttons
  document.querySelectorAll('[data-prev-step]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      currentStep = parseInt(this.dataset.prevStep, 10);
      showStep(currentStep);
    });
  });

  // ---- Zip auto-detect in form ----
  const formZipInput = document.getElementById('form-zip');
  const formStateDisplay = document.getElementById('form-state-display');
  const formStateHidden = document.getElementById('form-state');

  if (formZipInput) {
    formZipInput.addEventListener('input', function () {
      const val = this.value.replace(/\D/g, '').slice(0, 5);
      this.value = val;
      if (val.length === 5) {
        const result = getStateFromZip(val);
        if (result) {
          if (formStateDisplay) formStateDisplay.textContent = '📍 ' + result.name;
          if (formStateHidden) formStateHidden.value = result.code;
        } else {
          if (formStateDisplay) formStateDisplay.textContent = '';
          if (formStateHidden) formStateHidden.value = '';
        }
      } else {
        if (formStateDisplay) formStateDisplay.textContent = '';
        if (formStateHidden) formStateHidden.value = '';
      }
    });
  }

  // ---- Phone formatter ----
  const phoneInput = document.getElementById('phone');
  if (phoneInput) {
    phoneInput.addEventListener('input', function () {
      let val = this.value.replace(/\D/g, '').slice(0, 10);
      if (val.length >= 7) {
        val = '(' + val.slice(0, 3) + ') ' + val.slice(3, 6) + '-' + val.slice(6);
      } else if (val.length >= 4) {
        val = '(' + val.slice(0, 3) + ') ' + val.slice(3);
      } else if (val.length > 0) {
        val = '(' + val;
      }
      this.value = val;
    });
  }

  // ---- Character counter for textarea ----
  const motivationTextarea = document.getElementById('motivation');
  const motivationCount = document.getElementById('motivation-count');
  if (motivationTextarea && motivationCount) {
    motivationTextarea.addEventListener('input', function () {
      motivationCount.textContent = this.value.length + '/500';
    });
  }

  // ---- Form submit (AJAX) ----
  const submitBtn = document.getElementById('submit-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', function (e) {
      e.preventDefault();
      if (!validateStep(totalSteps)) return;
      calculateHiddenFields();

      var stateVal = (document.getElementById('form-state') || {}).value || '';
      var serviceVal = multiForm.dataset.serviceType || '';

      // Honeypot check — bots fill the hidden website field, humans don't
      var honeypot = document.getElementById('website');
      if (honeypot && honeypot.value !== '') return;

      submitBtn.disabled = true;
      submitBtn.textContent = 'Submitting…';

      var formData = new FormData(multiForm);

      fetch(multiForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      })
      .then(function(res) {
        if (res.ok) {
          // Show inline success state
          var section = multiForm.closest('section') || multiForm.parentElement;
          var container = section.querySelector('.container') || section;
          container.innerHTML = [
            '<div style="max-width:560px;margin:0 auto;text-align:center;padding:48px 16px 80px;">',
            '  <div style="width:72px;height:72px;border-radius:50%;background:var(--bg-accent);display:flex;align-items:center;justify-content:center;margin:0 auto 24px;font-size:2rem;">✓</div>',
            '  <h1 style="font-size:clamp(1.6rem,4vw,2.2rem);font-weight:800;color:var(--primary);margin-bottom:16px;">You\'re on the list!</h1>',
            '  <p style="font-size:1.05rem;color:var(--text-light);line-height:1.7;margin-bottom:12px;">We\'ve got your information and we\'re glad you applied.</p>',
            '  <p style="font-size:0.95rem;color:var(--text-light);line-height:1.7;margin-bottom:12px;">We\'re building our agency network now. We\'ll reach out as opportunities become available in your area.</p>',
            stateVal ? compRangeHTML(stateVal, serviceVal) : '',
            '  <a href="/" style="display:inline-block;margin-top:28px;font-size:0.9rem;color:var(--primary);font-weight:600;text-decoration:none;">← Back to EggSurrogatePay</a>',
            '</div>'
          ].join('');

          if (typeof gtag === 'function') {
            gtag('event', 'lead_form_submit', {
              form_type: serviceVal === 'surrogate' ? 'surrogate_application' : 'egg_donor_application',
              state: stateVal || 'unknown'
            });
          }
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          throw new Error('Server error');
        }
      })
      .catch(function() {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit My Application →';
        alert('Something went wrong. Please try again or email us at hello@eggsurrogatepay.com');
      });
    });
  }

  function compRangeHTML(state, service) {
    var EGG = { CA:[8000,15000],NY:[8000,14000],MA:[7500,13000],CT:[7000,12000],NJ:[7000,12000],IL:[7000,12000],WA:[7000,12000],MD:[6500,11000],DC:[7000,12000],CO:[6500,11000],HI:[6500,11000],TX:[6000,10000],FL:[6000,10000],GA:[6000,10000],VA:[6000,10000],PA:[6000,10000],OR:[6000,10000],AZ:[6000,10000],NV:[6000,10000],MN:[5500,9000],OH:[5500,9000],MI:[5500,9000],NC:[5500,9000],TN:[5500,9000],WI:[5500,9000],MO:[5500,9000],IN:[5500,9000] };
    var SUR = { CA:[45000,65000],NY:[45000,60000],CT:[42000,58000],NJ:[42000,58000],IL:[40000,55000],WA:[40000,55000],CO:[38000,52000],TX:[35000,50000],FL:[35000,50000],GA:[35000,48000],OR:[35000,48000],NV:[35000,48000],PA:[33000,47000],VA:[33000,47000],NC:[30000,43000],OH:[30000,43000],MI:[30000,43000],MN:[30000,43000] };
    var NAMES = { AL:'Alabama',AK:'Alaska',AZ:'Arizona',AR:'Arkansas',CA:'California',CO:'Colorado',CT:'Connecticut',DE:'Delaware',DC:'Washington D.C.',FL:'Florida',GA:'Georgia',HI:'Hawaii',ID:'Idaho',IL:'Illinois',IN:'Indiana',IA:'Iowa',KS:'Kansas',KY:'Kentucky',LA:'Louisiana',ME:'Maine',MD:'Maryland',MA:'Massachusetts',MI:'Michigan',MN:'Minnesota',MS:'Mississippi',MO:'Missouri',MT:'Montana',NE:'Nebraska',NV:'Nevada',NH:'New Hampshire',NJ:'New Jersey',NM:'New Mexico',NY:'New York',NC:'North Carolina',ND:'North Dakota',OH:'Ohio',OK:'Oklahoma',OR:'Oregon',PA:'Pennsylvania',RI:'Rhode Island',SC:'South Carolina',SD:'South Dakota',TN:'Tennessee',TX:'Texas',UT:'Utah',VT:'Vermont',VA:'Virginia',WA:'Washington',WV:'West Virginia',WI:'Wisconsin',WY:'Wyoming' };
    var map = service === 'surrogate' ? SUR : EGG;
    var def = service === 'surrogate' ? [28000,42000] : [5000,8000];
    var r = map[state] || def;
    var label = service === 'surrogate' ? 'per pregnancy' : 'per cycle';
    var name = NAMES[state] || 'your area';
    function fmt(n) { return '$' + n.toLocaleString(); }
    return [
      '<div style="background:var(--bg-accent);border:1px solid rgba(45,95,93,0.2);border-radius:12px;padding:24px;margin:24px 0;text-align:left;">',
      '  <p style="font-size:0.75rem;font-weight:800;text-transform:uppercase;letter-spacing:0.07em;color:var(--primary);margin:0 0 8px;">Estimated range for ' + name + '</p>',
      '  <p style="font-size:1.9rem;font-weight:800;color:var(--text);margin:0 0 4px;">' + fmt(r[0]) + ' – ' + fmt(r[1]) + ' <span style="font-size:1rem;font-weight:500;color:var(--text-light);">' + label + '</span></p>',
      '  <p style="font-size:0.82rem;color:var(--text-light);margin:0;">First-time applicants. Actual compensation set by your matched agency.</p>',
      '</div>'
    ].join('');
  }

  // ---- Validation ----
  function validateStep(step) {
    let valid = true;
    const stepEl = document.getElementById('step-' + step);
    if (!stepEl) return true;

    // Clear previous errors
    stepEl.querySelectorAll('.form-control.error').forEach(function (el) {
      el.classList.remove('error');
    });
    stepEl.querySelectorAll('.field-error.show').forEach(function (el) {
      el.classList.remove('show');
    });

    // Required inputs
    stepEl.querySelectorAll('[required]').forEach(function (input) {
      if (input.type === 'radio' || input.type === 'checkbox') return; // handled separately
      if (!input.value.trim()) {
        input.classList.add('error');
        const errEl = document.getElementById(input.id + '-error');
        if (errEl) { errEl.textContent = 'This field is required'; errEl.classList.add('show'); }
        valid = false;
      }
    });

    // Email validation
    const emailInput = stepEl.querySelector('input[type="email"]');
    if (emailInput && emailInput.value) {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
        emailInput.classList.add('error');
        const errEl = document.getElementById(emailInput.id + '-error');
        if (errEl) { errEl.textContent = 'Please enter a valid email address'; errEl.classList.add('show'); }
        valid = false;
      }
    }

    // Zip validation step 2
    if (step === 2) {
      const zipEl = document.getElementById('form-zip');
      if (zipEl && zipEl.value.length !== 5) {
        zipEl.classList.add('error');
        const errEl = document.getElementById('form-zip-error');
        if (errEl) { errEl.textContent = 'Please enter a valid 5-digit zip code'; errEl.classList.add('show'); }
        valid = false;
      }
    }

    // Required radio groups
    stepEl.querySelectorAll('[data-radio-required]').forEach(function (group) {
      const name = group.dataset.radioRequired;
      const checked = stepEl.querySelector('input[name="' + name + '"]:checked');
      if (!checked) {
        const errEl = document.getElementById(name + '-error');
        if (errEl) { errEl.textContent = 'Please select an option'; errEl.classList.add('show'); }
        valid = false;
      }
    });

    // Final step required checkboxes
    if (step === totalSteps) {
      const requiredBoxes = stepEl.querySelectorAll('[data-consent-required]');
      requiredBoxes.forEach(function (box) {
        if (!box.checked) {
          const errEl = document.getElementById('consent-error');
          if (errEl) { errEl.textContent = 'Please check all required boxes to continue'; errEl.classList.add('show'); }
          valid = false;
        }
      });
    }

    return valid;
  }

  function calculateAgencyReady(formType, age, bmi, tobacco, education, priorBirths) {
    var flags = [];
    var ready = true;

    if (formType === 'egg_donor') {
      if (age < 21) { flags.push('Under 21'); ready = false; }
      if (age > 31) { flags.push('Over 31'); ready = false; }
      if (bmi > 32) { flags.push('BMI above 32'); ready = false; }
      if (tobacco === 'yes') { flags.push('Tobacco user'); ready = false; }
      if (education === 'high_school') { flags.push('High school only'); }
      if (age >= 30 && age <= 31) { flags.push('Age 30-31 limited options'); }
      if (bmi >= 29 && bmi <= 32) { flags.push('BMI borderline 29-32'); }
    }

    if (formType === 'surrogate') {
      if (age < 21) { flags.push('Under 21'); ready = false; }
      if (age > 40) { flags.push('Over 40'); ready = false; }
      if (bmi > 32) { flags.push('BMI above 32'); ready = false; }
      if (tobacco === 'yes') { flags.push('Tobacco user'); ready = false; }
      if (priorBirths !== null && parseInt(priorBirths) === 0) { flags.push('No prior births'); ready = false; }
      if (age >= 38 && age <= 40) { flags.push('Age 38-40 limited options'); }
      if (bmi >= 29 && bmi <= 32) { flags.push('BMI borderline 29-32'); }
    }

    return {
      agency_ready: ready ? 'YES' : 'NO',
      qualification_flags: flags.length > 0 ? flags.join(' | ') : 'None'
    };
  }

  function calculateHiddenFields() {
    // BMI
    const feetEl = document.getElementById('feet');
    const inchesEl = document.getElementById('inches');
    const weightEl = document.getElementById('weight');
    const ageEl = document.getElementById('form-age');
    const bmiHidden = document.getElementById('bmi-hidden');
    const ageFlag = document.getElementById('age-flag');
    const bmiFlag = document.getElementById('bmi-flag');
    const tsHidden = document.getElementById('timestamp');

    if (feetEl && inchesEl && weightEl) {
      const feet = parseInt(feetEl.value, 10) || 0;
      const inches = parseInt(inchesEl.value, 10) || 0;
      const weight = parseInt(weightEl.value, 10) || 0;
      const totalInches = (feet * 12) + inches;
      if (totalInches > 0 && weight > 0) {
        const bmi = (weight / (totalInches * totalInches)) * 703;
        if (bmiHidden) bmiHidden.value = bmi.toFixed(1);
        if (bmiFlag) bmiFlag.value = bmi > 32 ? 'BMI above 32' : '';
      }
    }

    if (ageEl && ageFlag) {
      const age = parseInt(ageEl.value, 10);
      if (serviceType === 'surrogate') {
        ageFlag.value = age < 21 ? 'Under 21' : age > 40 ? 'Over 40' : '';
      } else {
        ageFlag.value = age < 21 ? 'Under 21' : age > 31 ? 'Over 31' : '';
      }
    }

    // Birth flag (surrogate only)
    var birthFlagEl = document.getElementById('birth-flag');
    var priorBirthsEl = document.getElementById('prior_births');
    if (birthFlagEl && priorBirthsEl) {
      birthFlagEl.value = parseInt(priorBirthsEl.value, 10) === 0 ? 'No prior births' : '';
    }

    // Agency ready + qualification flags
    var agencyReadyEl = document.getElementById('agency-ready');
    var qualFlagsEl = document.getElementById('qualification-flags');
    if (agencyReadyEl && qualFlagsEl) {
      var bmiVal = parseFloat(bmiHidden ? bmiHidden.value : 0) || 0;
      var ageVal = ageEl ? parseInt(ageEl.value, 10) : 0;
      var tobaccoEl = document.getElementById('tobacco_use') || document.querySelector('input[name="tobacco_use"]:checked');
      var tobaccoVal = tobaccoEl ? (tobaccoEl.tagName === 'SELECT' ? tobaccoEl.value : tobaccoEl.value) : '';
      var educationEl = document.getElementById('education');
      var educationVal = educationEl ? educationEl.value : '';
      var priorBirthsVal = priorBirthsEl ? parseInt(priorBirthsEl.value, 10) : null;
      var qual = calculateAgencyReady(serviceType, ageVal, bmiVal, tobaccoVal, educationVal, priorBirthsVal);
      agencyReadyEl.value = qual.agency_ready;
      qualFlagsEl.value = qual.qualification_flags;
    }

    if (tsHidden) tsHidden.value = new Date().toISOString();
    // NOTE: lead_form_submit fires only on confirmed Formspree success (see submit handler below) —
    // do not fire a submit-tracking event here, this runs before the fetch is even attempted.
  }

  // Initialize
  showStep(1);
});
