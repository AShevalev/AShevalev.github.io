(function () {
  /* Rec Instant: no $200k. Valid day = closed PnL ≥ 0.5% of SOD equity.
     6% trail never locks. 3% daily from the day's equity high. No fee refund.
     Lite funded max DD stays 8% (already in live pricingData).
     Weekly cycle is 80% (same split as Bi-Weekly), not live's 70% decoy. */
  if (typeof pricingData === 'undefined') return;

  delete pricingData.instant['200000'];

  var origInstantCard = instantCardHTML;
  instantCardHTML = function (d) {
    return ''
      + '<div class="phase-card">'
      + '  <div class="phase-header"><div>'
      + '    <div class="phase-name">' + i18nTxt('pricing.fundedAccount', 'Funded Account') + '</div>'
      + '  </div></div>'
      + '  <div class="phase-stats">'
      + '    <div>'
      + '      <div class="phase-stat-lbl">' + i18nTxt('pricing.profitTarget', 'Profit Target') + '</div>'
      + '      <div class="phase-stat-val-w">' + i18nTxt('pricing.none', 'None') + '</div>'
      + '    </div>'
      + '    <div onclick="showModal(\'valid-days\')" style="cursor:pointer;">'
      + '      <div class="phase-stat-lbl">Valid Days <i class="fa-solid fa-circle-info perf-info-icon"></i></div>'
      + '      <div class="phase-stat-val-w">5</div>'
      + '    </div>'
      + '    <div onclick="showModal(\'best-day\')" style="cursor:pointer;">'
      + '      <div class="phase-stat-lbl">' + i18nTxt('pricing.bestDayRule', 'Best Day Rule') + ' <i class="fa-solid fa-circle-info perf-info-icon"></i></div>'
      + '      <div class="phase-stat-val-w">' + d.bestDay + '</div>'
      + '    </div>'
      + '  </div>'
      + '  <div class="phase-meta">'
      + '    <div>' + i18nTxt('pricing.leveragePrefix', 'Leverage:') + ' <span>' + d.leverage + '</span></div>'
      + '    <div>' + i18nTxt('pricing.tradingPeriodPrefix', 'Trading Period:') + ' <span>' + i18nTxt('pricing.unlimited', 'Unlimited') + '</span></div>'
      + '  </div>'
      + '  <div class="phase-dd">'
      + '    <div class="sub-label sub-label-red" style="margin-bottom:0.5rem;">' + i18nTxt('pricing.trailingDrawdown', 'Trailing Drawdown Rules') + '</div>'
      + '    <p style="font-size:0.72rem;color:var(--text-secondary);line-height:1.5;margin:0 0 0.75rem;">6% trailing max from the equity high-water mark — it never locks. 3% daily from the day\'s equity high.</p>'
      + '    <div class="phase-dd-cards">'
      + '      <div class="dd-card" onclick="showModal(\'drawdown\')">'
      + '        <div class="dd-card-row">'
      + '          <div class="dd-card-lbl">' + i18nTxt('pricing.maxDrawdown', 'Maximum Drawdown') + ' <i class="fa-solid fa-circle-info perf-info-icon"></i></div>'
      + '          <span class="badge badge-red">' + fmt(d.maxDrawdown) + '</span>'
      + '        </div>'
      + '      </div>'
      + '      <div class="dd-card" onclick="showModal(\'daily-loss\')">'
      + '        <div class="dd-card-row">'
      + '          <div class="dd-card-lbl">' + i18nTxt('pricing.maxDailyDrawdown', 'Maximum Daily Drawdown') + ' <i class="fa-solid fa-circle-info perf-info-icon"></i></div>'
      + '          <span class="badge badge-red">' + fmt(d.dailyDrawdown) + '</span>'
      + '        </div>'
      + '      </div>'
      + '    </div>'
      + '  </div>'
      + '</div>';
  };

  var origShowModal = showModal;
  showModal = function (type) {
    if (type === 'valid-days') {
      var overlay = document.getElementById('modal');
      var titleEl = document.getElementById('modal-title');
      var contentEl = document.getElementById('modal-content');
      var canvas = document.getElementById('modal-chart');
      var chartWrap = document.getElementById('modal-chart-wrap');
      var exEl = document.getElementById('modal-example');
      overlay.classList.add('open');
      if (typeof currentChart !== 'undefined' && currentChart) {
        currentChart.destroy();
        currentChart = null;
      }
      if (chartWrap) chartWrap.style.display = 'none';
      if (canvas) canvas.style.display = 'none';
      if (exEl) exEl.innerHTML = '';
      titleEl.textContent = '5 Valid Days';
      contentEl.innerHTML = '<p>You must complete <strong>5 valid days</strong> before you can request a reward.</p>'
        + '<p>A valid day is a calendar day whose <strong>closed-trade PnL is at least 0.5%</strong> of that day\'s start-of-day equity. Unrealized PnL does not count. There is no 2% max-risk rule and no first-reward percent cap — the minimum reward is $100.</p>';
      return;
    }
    origShowModal(type);
  };

  var origUpdateAll = updateAll;
  updateAll = function () {
    var hide200 = currentTab === 'instant';
    document.querySelectorAll('.size-btn[data-size="200000"]').forEach(function (btn) {
      btn.hidden = hide200;
    });
    if (hide200 && currentSize === '200000') {
      currentSize = '100000';
      document.querySelectorAll('.size-btn').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-size') === '100000');
      });
    }
    origUpdateAll();
    var evalNewsDesc = document.getElementById('evalNewsDesc');
    if (evalNewsDesc) {
      evalNewsDesc.textContent = currentTab === 'instant'
        ? 'News trading is permitted on Instant funded accounts.'
        : 'News trading is permitted during evaluation phases.';
    }
    var evalWeekendDesc = document.getElementById('evalWeekendDesc');
    if (evalWeekendDesc && currentTab === 'instant') {
      evalWeekendDesc.textContent = 'All open positions must close by 22:00 UTC Friday. Weekend holding requires the Weekend Holding Addon.';
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { updateAll(); applyRewardCycles(); });
  } else {
    updateAll();
    applyRewardCycles();
  }

  function ensureHowRow(card, value) {
    var details = card.querySelector('.rc-details');
    if (!details || details.querySelector('[data-rc-how]')) return;
    var row = document.createElement('div');
    row.className = 'rc-detail-row';
    row.setAttribute('data-rc-how', '1');
    row.innerHTML = '<span>How</span><span>' + value + '</span>';
    details.appendChild(row);
  }

  function applyRewardCycles() {
    var cards = document.querySelectorAll('.reward-cycle-card');
    if (cards[0]) {
      var pct = cards[0].querySelector('.rc-pct');
      if (pct) pct.textContent = '80%';
      ensureHowRow(cards[0], 'Add-on');
    }
    if (cards[1]) ensureHowRow(cards[1], 'Included');
    if (cards[2]) ensureHowRow(cards[2], 'Add-on');
    document.querySelectorAll('[data-i18n="content.p7"]').forEach(function (p) {
      p.textContent = 'All reward request intervals are based on calendar days, not trading days. Pick one combination. Weekly and On Demand cannot be combined.';
    });
  }
})();
