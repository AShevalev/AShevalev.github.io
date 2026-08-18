(function () {
  /* Rec Instant: no $200k. No min trading days. 20% Best Day of Positive Days' Profit.
     6% trail never locks. 3% daily from the day's equity high. No fee refund.
     Lite funded max DD stays 8% (already in live pricingData).
     Weekly 70% is 6% of list. On Demand is 90% at 20% of list.
     Default is Bi-Weekly 80%. News is included on every plan. */
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
      + '    <div>'
      + '      <div class="phase-stat-lbl">' + i18nTxt('pricing.minTradingDays', 'Minimum Trading Days') + '</div>'
      + '      <div class="phase-stat-val-w">' + i18nTxt('pricing.none', 'None') + '</div>'
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
    if (type === 'valid-days' || type === 'first-request') {
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
      if (currentTab === 'instant') {
        titleEl.textContent = 'Instant payouts';
        contentEl.innerHTML = '<p>Every payout needs <strong>$100</strong>, Best Day ≤20% of Positive Days\' Profit, and the selected cycle. Instant has <strong>no minimum trading days</strong>.</p>'
          + '<p>Weekly: $100, 7 calendar days, Best Day ≤20% of Positive Days\' Profit.</p>'
          + '<p>Bi-Weekly: $100, 14 calendar days, Best Day ≤20% of Positive Days\' Profit.</p>'
          + '<p>On-Demand: $100. No minimum trading days. Best Day ≤20% of Positive Days\' Profit. A profitable day is a day that closes with more than 0.5% profit.</p>';
      } else if (currentTab === '1step') {
        titleEl.textContent = '1-Step payouts';
        contentEl.innerHTML = '<p>Every payout needs <strong>$100</strong>, Best Day ≤50% of Positive Days\' Profit, and the selected cycle. 1-Step has <strong>no minimum trading days</strong>.</p>'
          + '<p>Weekly: $100, 7 calendar days, Best Day ≤50% of Positive Days\' Profit.</p>'
          + '<p>Bi-Weekly: $100, 14 calendar days, Best Day ≤50% of Positive Days\' Profit.</p>'
          + '<p>On-Demand: $100. No minimum trading days. Best Day ≤50% of Positive Days\' Profit.</p>';
      } else {
        titleEl.textContent = '2-Step payouts';
        contentEl.innerHTML = '<p>Every payout needs <strong>$100</strong> and <strong>3 trading days</strong>, plus the selected cycle. The first payout and every payout after use this same rule.</p>'
          + '<p>Weekly: $100, 7 calendar days, and 3 trading days.</p>'
          + '<p>Bi-Weekly: $100, 14 calendar days, and 3 trading days.</p>'
          + '<p>On-Demand: $100 and 3 trading days.</p>';
      }
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
    applyNewsIncluded();
    var evalWeekendDesc = document.getElementById('evalWeekendDesc');
    if (evalWeekendDesc && currentTab === 'instant') {
      evalWeekendDesc.textContent = 'All open positions must close by 22:00 UTC Friday. Weekend holding requires the Weekend Holding Addon.';
    }
    applyRewardCycles();
  };

  function applyNewsIncluded() {
    var allowed = 'News trading is permitted.';
    var evalBadge = document.getElementById('evalNewsBadge');
    if (evalBadge) {
      evalBadge.className = 'badge badge-green';
      evalBadge.textContent = 'Allowed';
    }
    var evalNewsDesc = document.getElementById('evalNewsDesc');
    if (evalNewsDesc) evalNewsDesc.textContent = allowed;
    var qpfBadge = document.getElementById('qpfNewsBadge');
    if (qpfBadge) {
      qpfBadge.className = 'badge badge-green';
      qpfBadge.textContent = 'Allowed';
    }
    var qpfNewsDesc = document.getElementById('qpfNewsDesc');
    if (qpfNewsDesc) {
      qpfNewsDesc.textContent = allowed;
      var extra = qpfNewsDesc.nextElementSibling;
      if (extra && /News Trading Addon/i.test(extra.textContent || '')) extra.remove();
    }
    var funded = document.getElementById('fundedGuides');
    if (funded) {
      funded.querySelectorAll('.guide-card').forEach(function (card) {
        var name = card.querySelector('.guide-name');
        if (!name || name.textContent.indexOf('News Trading') === -1) return;
        var badge = card.querySelector('.badge');
        if (badge) {
          badge.className = 'badge badge-green';
          badge.textContent = 'Allowed';
        }
        var desc = card.querySelector('.guide-desc');
        if (desc) desc.textContent = allowed;
      });
    }
  }

  function applyRewardCycles() {
    document.querySelectorAll('[data-i18n="content.p6"]').forEach(function (p) {
      p.textContent = 'Default reward is Bi-Weekly 80%. Weekly 70% and On Demand 90% are paid add-ons.';
    });
    document.querySelectorAll('[data-i18n="content.p7"]').forEach(function (p) {
      p.textContent = 'All reward request intervals are calendar days, not trading days. Each cycle still needs that plan’s qualifying parameters.';
    });
    document.querySelectorAll('[data-i18n-html="content.p8"]').forEach(function (p) {
      p.innerHTML = currentTab === 'instant'
        ? '<strong>Payouts:</strong> Every payout: $100. No minimum trading days. Best Day ≤20% of Positive Days’ Profit (within 48 hrs)'
        : currentTab === '1step'
          ? '<strong>Payouts:</strong> Every payout: $100. No minimum trading days. Best Day ≤50% of Positive Days’ Profit (within 48 hrs)'
          : '<strong>Payouts:</strong> Every payout: $100 and 3 trading days (within 48 hrs)';
    });
    var refund = document.getElementById('refundHighlightCard');
    var rhGrid = document.querySelector('.reward-highlight-grid');
    if (refund) refund.hidden = currentTab === 'instant';
    if (rhGrid) rhGrid.classList.toggle('rh-no-refund', currentTab === 'instant');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { updateAll(); });
  } else {
    updateAll();
  }
})();
