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

    const pct = Math.round(((step - 1) / totalSteps) * 100);
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
          gtag('event', 'step_' + fromStep + '_completed', { service_type: serviceType });
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

  // ---- Form submit ----
  const submitBtn = document.getElementById('submit-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', function (e) {
      e.preventDefault();
      if (!validateStep(5)) return;
      calculateHiddenFields();
      multiForm.submit();
    });
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

    // Step 5 required checkboxes
    if (step === 5) {
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

    if (tsHidden) tsHidden.value = new Date().toISOString();

    // GA4
    if (typeof gtag === 'function') {
      const stateEl = document.getElementById('form-state');
      gtag('event', 'application_submitted', {
        service_type: serviceType,
        age: ageEl ? ageEl.value : 'unknown',
        state: stateEl ? stateEl.value : 'unknown'
      });
    }
  }

  // Initialize
  showStep(1);
});
