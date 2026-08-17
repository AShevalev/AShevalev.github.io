(function () {
  var $ = function (sel) { return document.querySelector(sel); };

  var PRICING = {
    instant: {
      label: 'Instant',
      sizes: {
        '5000': { price: 75 }, '10000': { price: 106 }, '25000': { price: 229 },
        '50000': { price: 368 }, '100000': { price: 675 }
      }
    },
    '1step': {
      label: '1-Step',
      sizes: {
        '5000': { price: 69 }, '10000': { price: 106 }, '25000': { price: 198 },
        '50000': { price: 337 }, '100000': { price: 583 }, '200000': { price: 1075 }
      }
    },
    '2steplite': {
      label: '2-Step Lite',
      sizes: {
        '5000': { price: 60 }, '10000': { price: 85 }, '25000': { price: 152 },
        '50000': { price: 229 }, '100000': { price: 423 }, '200000': { price: 845 }
      }
    },
    '2steppro': {
      label: '2-Step Pro',
      sizes: {
        '5000': { price: 69 }, '10000': { price: 91 }, '25000': { price: 168 },
        '50000': { price: 260 }, '100000': { price: 475 }, '200000': { price: 952 }
      }
    }
  };

  var selectedPlan = '1step';
  var selectedSize = '5000';
  var selectedQty = 1;
  var QTY_MAX = 4;
  var activeAddons = {};
  var addonModalOpen = false;
  var COMPETITION = null;
  var DISCOUNT_CAP_PCT = 35;
  var appliedCoupon = { code: 'VERO35', pct: 35 };
  var paymentMethod = 'card';

  /* Weekly 80% XOR On Demand and XOR 90%. Default is Bi-Weekly 80%.
     On Demand + 90% is the 90% On Demand bundle. 90% Weekly is not offered. */
  var PAYOUT_UPGRADES = ['on-demand-payout', 'split-90'];

  var BUNDLES = [
    {
      name: '90% On Demand',
      ids: ['on-demand-payout', 'split-90'],
      chargeId: 'on-demand-payout',
      pct: function () { return selectedPlan === 'instant' ? 0.35 : 0.25; },
      summaryLabel: 'On Demand Rewards with 90% Split'
    }
  ];

  var ADDONS = [
    {
      id: 'weekend-holding',
      label: 'Weekend Holding',
      pct: 0.15,
      desc: 'Hold positions over the weekend with zero restrictions.',
      tooltip: function () {
        return 'Exempts all open positions from the 22:00 UTC Friday liquidation rule so you may hold through the weekend on evaluation and funded accounts. Perfect for swing traders, position traders, and multi-day strategies.';
      }
    },
    {
      id: 'weekly-payout',
      label: 'Weekly Rewards with 80% Reward Split',
      pct: 0.10,
      desc: 'Withdraw your 80% profit share every 7 calendar days',
      tooltip: function () {
        var days = minDaysCopy();
        return 'Weekly Rewards with 80% Split\n\nKeep the same 80% reward share as the default Bi-Weekly cycle, requested every 7 calendar days instead of 14. Minimum reward $100.\n\n'
          + days + '\n\n'
          + 'Cannot be combined with On Demand Rewards or the 90% Reward Split.';
      }
    },
    {
      id: 'on-demand-payout',
      label: 'On Demand Rewards with 80% Split',
      pct: 0.15,
      instantPct: 0.18,
      desc: 'Withdraw your 80% profit share anytime after the plan trading-day rule',
      tooltip: function () {
        return 'On Demand Rewards with 80% Split\n\nRequest your 80% reward share anytime after you meet the plan trading-day rule — no waiting for a 7- or 14-day cycle. Minimum reward $100.\n\n'
          + minDaysCopy() + '\n\n'
          + 'Cannot be combined with Weekly Rewards.';
      }
    },
    {
      id: 'split-90',
      label: '90% Reward Split',
      pct: 0.15,
      instantPct: 0.18,
      desc: 'Keep 90% of profits on the default Bi-Weekly schedule',
      tooltip: function () {
        return '90% Reward Split\n\nKeep 90% of profits on the default Bi-Weekly cycle (every 14 calendar days). Minimum reward $100.\n\n'
          + minDaysCopy() + '\n\n'
          + 'Pair with On Demand Rewards to withdraw that 90% share anytime after the plan trading-day rule.\n\n'
          + 'Cannot be combined with Weekly Rewards.';
      }
    }
  ];

  function minDaysCopy() {
    return selectedPlan === 'instant'
      ? 'Payouts after 5 valid trading days (0.5% vs start-of-day equity).'
      : 'First request after 3 funded trading days.';
  }

  var HIDDEN_COUNTRY_CODES = { US: 1, PR: 1, GU: 1, VI: 1, AS: 1, MP: 1 };

  function escHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function getBasePrice() {
    if (COMPETITION) return COMPETITION.amountUsd;
    return PRICING[selectedPlan].sizes[selectedSize].price;
  }

  function bundlePct(b) {
    return typeof b.pct === 'function' ? b.pct() : b.pct;
  }

  function bundleOn(b) {
    return b.ids.every(function (id) { return !!activeAddons[id]; });
  }

  function bundleOnName(name) {
    for (var i = 0; i < BUNDLES.length; i++) {
      if (BUNDLES[i].name === name && bundleOn(BUNDLES[i])) return true;
    }
    return false;
  }

  function activeBundleFor(id) {
    for (var i = 0; i < BUNDLES.length; i++) {
      if (BUNDLES[i].ids.indexOf(id) === -1) continue;
      if (bundleOn(BUNDLES[i])) return BUNDLES[i];
    }
    return null;
  }

  function soloPct(a) {
    if (selectedPlan === 'instant' && typeof a.instantPct === 'number') return a.instantPct;
    return a.pct;
  }

  function addonPct(a) {
    var b = activeBundleFor(a.id);
    if (b) return a.id === b.chargeId ? bundlePct(b) : 0;
    return soloPct(a);
  }

  function addonPrice(a) {
    return Math.round(getBasePrice() * addonPct(a));
  }

  function addonIncluded(a) {
    var b = activeBundleFor(a.id);
    return !!(b && a.id !== b.chargeId);
  }

  function addonPriceTag(a) {
    var p = addonPrice(a);
    if (p > 0) return '+$' + p;
    if (addonIncluded(a)) return 'Incl.';
    return '+$0';
  }

  function addonLabel(a) {
    var b = activeBundleFor(a.id);
    if (b && a.id === b.chargeId && b.summaryLabel) return b.summaryLabel;
    return a.label;
  }

  function addonDesc(a) {
    var b = activeBundleFor(a.id);
    if (b) {
      if (a.id === b.chargeId) return 'Billed as ' + b.name + ' — not as two separate add-ons';
      return 'Included in ' + b.name;
    }
    return a.desc;
  }

  function addonTooltip(a) {
    return typeof a.tooltip === 'function' ? a.tooltip() : a.tooltip;
  }

  function getAddonsTotal() {
    if (COMPETITION) return 0;
    var t = 0;
    ADDONS.forEach(function (a) {
      if (activeAddons[a.id]) t += addonPrice(a);
    });
    return t;
  }

  function getCouponDiscount() {
    if (!appliedCoupon) return 0;
    var subtotal = getBasePrice() + getAddonsTotal();
    var pct = Math.min(appliedCoupon.pct, DISCOUNT_CAP_PCT);
    return Math.round(subtotal * pct / 100);
  }

  function unitPay() {
    return Math.max(0, getBasePrice() + getAddonsTotal() - getCouponDiscount());
  }

  function getTotal() {
    return unitPay() * selectedQty;
  }

  function timesTag(label) {
    return selectedQty > 1 ? (label + ' × ' + selectedQty) : label;
  }

  function applyAddonToggle(id, checked) {
    if (checked) {
      activeAddons[id] = true;
      if (id === 'weekly-payout') {
        PAYOUT_UPGRADES.forEach(function (x) { delete activeAddons[x]; });
      } else if (PAYOUT_UPGRADES.indexOf(id) !== -1) {
        delete activeAddons['weekly-payout'];
      }
    } else {
      delete activeAddons[id];
    }
  }

  function renderAddons() {
    var wrap = $('#coAddons');
    if (!wrap) return;
    var html = '';
    ADDONS.forEach(function (a) {
      var checked = activeAddons[a.id] ? ' checked' : '';
      var active = activeAddons[a.id] ? ' active' : '';
      html += '<div class="co-addon' + active + '" data-addon="' + a.id + '">'
        + '<div class="co-addon-info">'
        + '<span class="co-addon-name">' + addonLabel(a) + ' <span class="co-addon-price-tag">' + addonPriceTag(a) + '</span></span>'
        + '<div class="co-addon-desc-row">'
        + '<span class="co-addon-desc-text">' + escHtml(addonDesc(a)) + '</span>'
        + '<button type="button" class="co-addon-info-btn" data-addon-id="' + a.id + '">'
        + '<span class="co-addon-info-glyph" aria-hidden="true">&#9432;</span>'
        + '<span class="co-sr-only">Full details: ' + escHtml(a.label) + '</span>'
        + '</button>'
        + '</div>'
        + '</div>'
        + '<label class="co-toggle">'
        + '<input type="checkbox" data-addon-id="' + a.id + '"' + checked + '>'
        + '<span class="co-toggle-slider"></span>'
        + '</label>'
        + '</div>';
    });
    wrap.innerHTML = html;
    wrap.querySelectorAll('.co-addon-info-btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var aid = btn.getAttribute('data-addon-id');
        var addon = null;
        for (var i = 0; i < ADDONS.length; i++) {
          if (ADDONS[i].id === aid) { addon = ADDONS[i]; break; }
        }
        if (addon) openAddonModal(addon);
      });
    });
    wrap.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
      cb.addEventListener('change', function () {
        applyAddonToggle(cb.dataset.addonId, cb.checked);
        renderAddons();
        updateSummary();
      });
    });
  }

  function money(n) {
    return n % 1 === 0 ? String(n) : n.toFixed(2);
  }

  function updateSummary() {
    var plan = PRICING[selectedPlan];
    var sizeNum = parseInt(selectedSize, 10);
    var sizeLabel = '$' + (sizeNum >= 1000 ? Math.round(sizeNum / 1000) + 'K' : selectedSize);
    var challengeEl = $('#sumChallenge');
    var sizeEl = $('#sumSize');
    var baseEl = $('#sumBase');
    if (challengeEl) challengeEl.textContent = plan.label;
    if (sizeEl) sizeEl.textContent = timesTag(sizeLabel);
    if (baseEl) baseEl.textContent = timesTag('$' + getBasePrice());

    var addonsWrap = $('#sumAddonsWrap');
    if (addonsWrap) {
      var addonsHtml = '';
      ADDONS.forEach(function (a) {
        if (!activeAddons[a.id]) return;
        addonsHtml += '<div class="co-summary-addon-row"><span>' + addonLabel(a) + '</span><span>' + timesTag(addonPriceTag(a)) + '</span></div>';
      });
      addonsWrap.innerHTML = addonsHtml;
    }

    var dWrap = $('#sumDiscountWrap');
    var disc = getCouponDiscount() * selectedQty;
    if (dWrap) {
      if (appliedCoupon && disc > 0) {
        dWrap.innerHTML = '<div class="co-summary-discount visible"><span>Discount (' + appliedCoupon.code + ')</span><span>-$' + disc.toFixed(2) + '</span></div>';
      } else {
        dWrap.innerHTML = '';
      }
    }

    var totalEl = $('#sumTotal');
    if (totalEl) totalEl.textContent = '$' + money(getTotal());
    updateRefundCopy();
  }

  function updateRefundCopy() {
    var wrap = $('#coRefundable');
    var pill = $('#coRefundablePill');
    var label = $('#coRefundableLabel');
    var note = $('#coRefundNote');
    if (!wrap) return;
    var instant = selectedPlan === 'instant';
    if (pill) pill.style.display = instant ? 'none' : '';
    if (label) label.textContent = 'Refundable on first payout excluding add-on fees.';
    if (note) {
      note.textContent = instant ? 'Instant purchases are not refundable.' : '';
      note.style.display = instant ? '' : 'none';
    }
  }

  function openAddonModal(addon) {
    var title = $('#coAddonModalTitle');
    var firstP = $('#coAddonModalText');
    if (!title || !firstP) return;
    title.textContent = addonLabel(addon);
    var parent = firstP.parentNode;
    var sib = firstP.nextSibling;
    while (sib) {
      var next = sib.nextSibling;
      if (sib.nodeType === 1 && sib.dataset && sib.dataset.coAddonExtra === '1') {
        parent.removeChild(sib);
      }
      sib = next;
    }
    var chunks = String(addonTooltip(addon) || '').split(/\n{2,}/);
    firstP.textContent = (chunks[0] || '').trim();
    var anchor = firstP;
    for (var i = 1; i < chunks.length; i++) {
      var p = document.createElement('p');
      p.dataset.coAddonExtra = '1';
      p.textContent = chunks[i].trim();
      anchor.insertAdjacentElement('afterend', p);
      anchor = p;
    }
    var el = $('#coAddonModal');
    el.classList.add('open');
    el.setAttribute('aria-hidden', 'false');
    addonModalOpen = true;
    var c = $('#coAddonModalClose');
    if (c) c.focus();
  }

  function closeAddonModal() {
    var el = $('#coAddonModal');
    if (!el || !el.classList.contains('open')) return;
    el.classList.remove('open');
    el.setAttribute('aria-hidden', 'true');
    addonModalOpen = false;
  }

  function bindAddonModal() {
    var overlay = $('#coAddonModal');
    var closeBtn = $('#coAddonModalClose');
    if (closeBtn) closeBtn.addEventListener('click', closeAddonModal);
    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeAddonModal();
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && addonModalOpen) {
        e.preventDefault();
        closeAddonModal();
      }
    });
  }

  function syncPlanTabs() {
    document.querySelectorAll('#coTabs .co-tab').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-plan') === selectedPlan);
    });
  }

  function renderSizes() {
    var sizes = PRICING[selectedPlan].sizes;
    var html = '';
    Object.keys(sizes).forEach(function (sz) {
      var n = parseInt(sz, 10);
      var label = n >= 1000 ? Math.round(n / 1000) + 'K' : sz;
      html += '<button type="button" class="co-size-btn' + (sz === selectedSize ? ' active' : '') + '" data-size="' + sz + '">'
        + '<span class="co-size-label">$' + label + '</span>'
        + '<span class="co-size-price">$' + sizes[sz].price + '</span>'
        + '</button>';
    });
    var wrap = $('#coSizes');
    wrap.innerHTML = html;
    wrap.querySelectorAll('.co-size-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        selectedSize = btn.getAttribute('data-size');
        renderSizes();
        renderAddons();
        updateSummary();
      });
    });
  }

  function renderQty() {
    var val = $('#coQtyValue');
    var minus = $('#coQtyMinus');
    var plus = $('#coQtyPlus');
    if (val) val.textContent = String(selectedQty);
    if (minus) minus.disabled = selectedQty <= 1;
    if (plus) plus.disabled = selectedQty >= QTY_MAX;
  }

  function bindQty() {
    var minus = $('#coQtyMinus');
    var plus = $('#coQtyPlus');
    if (minus) {
      minus.addEventListener('click', function () {
        if (selectedQty <= 1) return;
        selectedQty -= 1;
        renderQty();
        renderAddons();
        updateSummary();
      });
    }
    if (plus) {
      plus.addEventListener('click', function () {
        if (selectedQty >= QTY_MAX) return;
        selectedQty += 1;
        renderQty();
        renderAddons();
        updateSummary();
      });
    }
  }

  function fillCountries() {
    var sel = $('#co-country');
    if (!sel || typeof COUNTRIES === 'undefined') return;
    var html = '<option value="">Select country</option>';
    COUNTRIES.forEach(function (c) {
      var code = c[0];
      var name = c[1];
      if (HIDDEN_COUNTRY_CODES[code]) return;
      html += '<option value="' + code + '">' + name + '</option>';
    });
    sel.innerHTML = html;
  }

  function setCoupon(code, silent) {
    var fb = $('#coCouponFeedback');
    var raw = (code || '').trim().toUpperCase();
    if (!raw) {
      appliedCoupon = null;
      if (fb) {
        fb.className = 'co-coupon-feedback';
        fb.textContent = '';
      }
      updateSummary();
      return;
    }
    if (raw === 'VERO35') {
      appliedCoupon = { code: 'VERO35', pct: 35 };
      if (fb) {
        fb.className = 'co-coupon-feedback ok';
        fb.textContent = silent ? 'Coupon applied.' : 'Coupon applied.';
      }
    } else {
      appliedCoupon = null;
      if (fb) {
        fb.className = 'co-coupon-feedback err';
        fb.textContent = 'This coupon is not valid.';
      }
    }
    updateSummary();
  }

  function applyCoupon() {
    var input = $('#coCoupon');
    setCoupon(input ? input.value : '', false);
  }

  function validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function setInvalid(id, on) {
    var el = document.getElementById(id);
    if (!el) return;
    if (on) el.classList.add('invalid');
    else el.classList.remove('invalid');
  }

  function validateForm(show) {
    var ok = true;
    function req(fieldId, inputId, extra) {
      var input = document.getElementById(inputId);
      if (!input) return;
      var v = (input.value || '').trim();
      var bad = !v || (extra && !extra(v));
      if (show) setInvalid(fieldId, bad);
      if (bad) ok = false;
    }
    req('field-fname', 'co-fname');
    req('field-lname', 'co-lname');
    req('field-phone', 'co-phone');
    req('field-email', 'co-email', validEmail);
    req('field-country', 'co-country');
    req('field-address', 'co-address');
    req('field-city', 'co-city');
    req('field-state', 'co-state');
    req('field-postcode', 'co-postcode');
    var terms = $('#co-order-terms');
    var termsOk = !!(terms && terms.checked);
    if (!termsOk) ok = false;
    var btn = $('#coPurchaseBtn');
    if (btn) btn.disabled = !termsOk;
    return ok && termsOk;
  }

  function bindForm() {
    ['co-fname','co-lname','co-phone','co-email','co-country','co-address','co-city','co-state','co-postcode','co-order-terms']
      .forEach(function (id) {
        var el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('input', function () { validateForm(false); });
        el.addEventListener('change', function () { validateForm(false); });
      });
    var applyBtn = $('#coApplyCoupon');
    if (applyBtn) applyBtn.addEventListener('click', applyCoupon);
    var coupon = $('#coCoupon');
    if (coupon) {
      coupon.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') { e.preventDefault(); applyCoupon(); }
      });
      coupon.addEventListener('input', function () {
        var raw = (coupon.value || '').trim().toUpperCase();
        if (raw === 'VERO35') {
          setCoupon('VERO35', true);
          return;
        }
        appliedCoupon = null;
        var fb = $('#coCouponFeedback');
        if (fb) {
          fb.className = 'co-coupon-feedback';
          fb.textContent = '';
        }
        updateSummary();
      });
    }
    document.querySelectorAll('#coPaymentMethods .co-pm-option').forEach(function (lab) {
      lab.addEventListener('click', function () {
        paymentMethod = lab.getAttribute('data-method');
        document.querySelectorAll('#coPaymentMethods .co-pm-option').forEach(function (x) {
          x.classList.toggle('active', x === lab);
        });
      });
    });
    var purchase = $('#coPurchaseBtn');
    if (purchase) {
      purchase.addEventListener('click', function () {
        if (!validateForm(true)) return;
        var proc = $('#coProcessing');
        if (proc) proc.classList.add('open');
        setTimeout(function () {
          if (proc) proc.classList.remove('open');
          var success = $('#coSuccess');
          if (success) success.classList.add('open');
        }, 700);
      });
    }
  }

  function bindPlanTabs() {
    document.querySelectorAll('#coTabs .co-tab').forEach(function (btn) {
      btn.addEventListener('click', function () {
        selectedPlan = btn.getAttribute('data-plan');
        if (!PRICING[selectedPlan].sizes[selectedSize]) selectedSize = '100000';
        if (!PRICING[selectedPlan].sizes[selectedSize]) {
          selectedSize = Object.keys(PRICING[selectedPlan].sizes)[0];
        }
        syncPlanTabs();
        renderSizes();
        renderQty();
        renderAddons();
        updateSummary();
      });
    });
  }

  function applyDeepLink() {
    try {
      var qp = new URLSearchParams(window.location.search);
      var qPlan = (qp.get('plan') || '').trim().toLowerCase();
      var qSize = (qp.get('size') || '').trim();
      if (qPlan && PRICING[qPlan]) {
        selectedPlan = qPlan;
        if (qSize && PRICING[qPlan].sizes[qSize]) selectedSize = qSize;
        else selectedSize = Object.keys(PRICING[qPlan].sizes)[0];
      }
    } catch (e) {}
  }

  applyDeepLink();
  bindAddonModal();
  fillCountries();
  bindForm();
  bindPlanTabs();
  bindQty();
  syncPlanTabs();
  renderSizes();
  renderQty();
  renderAddons();
  updateSummary();
  validateForm(false);
})();
