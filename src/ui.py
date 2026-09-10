"""Executive Off-White Interactive Dashboard & Educational Walkthrough for FairTalent-Engine.

Provides an intuitive UI explaining EEOC 4/5ths Rule, NYC LL144, EU AI Act,
Classical Test Theory (CTT), and interactive cohort simulations with real-time API calls.
"""


def render_fairness_dashboard() -> str:
    """Generate modern, responsive HTML/CSS/JS dashboard for FairTalent-Engine."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FairTalent-Engine ⚡ Algorithmic Bias & Psychometric Audit Platform</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #0b0f19;
      --surface: #111827;
      --surface-card: #162032;
      --border: #1f293d;
      --border-focus: #3b82f6;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --purple: #a855f7;
      --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-main);
      line-height: 1.6;
      padding: 0 0 80px 0;
    }

    .header-bar {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 20px;
      color: white;
    }
    .brand-name {
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .brand-subtitle {
      font-size: 0.75rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    .nav-links {
      display: flex;
      gap: 16px;
      align-items: center;
    }
    .btn-nav {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 8px;
      transition: all 0.2s ease;
    }
    .btn-nav:hover {
      border-color: var(--primary);
      background: var(--surface);
    }

    .container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 32px 24px;
    }

    /* Hero */
    .hero-banner {
      background: linear-gradient(180deg, rgba(30, 41, 59, 0.5) 0%, rgba(17, 24, 39, 0) 100%);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px 32px;
      margin-bottom: 32px;
      position: relative;
      overflow: hidden;
    }
    .hero-banner::before {
      content: '';
      position: absolute;
      top: -50px;
      right: -50px;
      width: 250px;
      height: 250px;
      background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(0,0,0,0) 70%);
      pointer-events: none;
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
      margin-bottom: 14px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .hero-title {
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.2;
      margin-bottom: 12px;
    }
    .hero-desc {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 850px;
    }

    /* Educational Section */
    .edu-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 18px;
      margin-bottom: 36px;
    }
    .edu-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      position: relative;
    }
    .edu-card h3 {
      font-size: 1.05rem;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .edu-card p {
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.5;
    }
    .formula-tag {
      font-family: var(--font-mono);
      font-size: 0.78rem;
      background: rgba(0, 0, 0, 0.4);
      padding: 4px 8px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      display: inline-block;
      margin-top: 10px;
      color: #93c5fd;
    }

    /* Simulation Controls */
    .controls-panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 32px;
    }
    .controls-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 20px;
    }
    .controls-title {
      font-size: 1.15rem;
      font-weight: 700;
    }
    .scenario-selector {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .scenario-btn {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text);
      font-family: var(--font-main);
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .scenario-btn:hover {
      border-color: var(--primary);
    }
    .scenario-btn.active {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--primary);
      color: #93c5fd;
    }

    .slider-row {
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 20px;
      align-items: center;
      background: var(--surface-card);
      padding: 16px 20px;
      border-radius: 10px;
      border: 1px solid var(--border);
      margin-top: 14px;
    }
    .slider-label {
      font-size: 0.9rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    input[type=range] {
      width: 100%;
      accent-color: var(--primary);
      cursor: pointer;
    }
    .slider-val {
      font-family: var(--font-mono);
      font-size: 1.1rem;
      font-weight: 700;
      color: #60a5fa;
      min-width: 50px;
      text-align: right;
    }

    /* KPI Metrics Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 18px;
      margin-bottom: 32px;
    }
    .kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      position: relative;
      transition: transform 0.2s ease;
    }
    .kpi-label {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 6px;
    }
    .kpi-value {
      font-size: 1.8rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }
    .kpi-status-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
    }
    .badge-pass {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-fail {
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-warn {
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Tables */
    .table-container {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 32px;
      overflow-x: auto;
    }
    .table-title {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.9rem;
    }
    th {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    td {
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    tr:last-child td {
      border-bottom: none;
    }

    /* Actions Bar */
    .actions-bar {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 36px;
    }
    .btn-action {
      background: var(--primary);
      color: white;
      border: none;
      padding: 14px 24px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: background 0.2s ease, transform 0.1s ease;
    }
    .btn-action:hover {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }
    .btn-action.secondary {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text);
    }
    .btn-action.secondary:hover {
      border-color: var(--primary);
      background: var(--surface);
    }

    /* Modal / Certificate Output */
    .cert-box {
      background: #060911;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: #94a3b8;
      max-height: 280px;
      overflow-y: auto;
      white-space: pre-wrap;
      margin-top: 14px;
    }

    .footer {
      border-top: 1px solid var(--border);
      padding: 32px 0 0 0;
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
    }
  </style>
</head>
<body>

  <header class="header-bar">
    <div class="brand">
      <div class="brand-logo">FT</div>
      <div>
        <div class="brand-name">FairTalent-Engine</div>
        <div class="brand-subtitle">Algorithmic Bias & Psychometric Validity Platform</div>
      </div>
    </div>
    <div class="nav-links">
      <a href="/docs" target="_blank" class="btn-nav">Swagger /docs</a>
      <a href="https://github.com/neurodeveloper11" target="_blank" class="btn-nav">GitHub Profile</a>
    </div>
  </header>

  <main class="container">
    <!-- Hero Banner -->
    <section class="hero-banner">
      <div class="hero-badge">Verified Regulatory Compliance Framework</div>
      <h1 class="hero-title">Fair ML & Psychometric Audit Engine</h1>
      <p class="hero-desc">
        Engineered by <b>Fabio Torres</b> (M.Sc. Data Engineering & Cloud Infrastructure • 10+ Years Behavioral & Cognitive Science Leadership).
        Audits candidate pools against the <b>EEOC Four-Fifths Rule (29 CFR § 1607.4)</b>, <b>NYC Local Law 144</b>, and <b>EU AI Act (Annex III High-Risk AI)</b>, combining Classical Test Theory (Cronbach's α) with automated threshold mitigation.
      </p>
    </section>

    <!-- Educational Grid -->
    <section class="edu-grid">
      <div class="edu-card">
        <h3>⚖️ EEOC 4/5ths (80%) Rule</h3>
        <p>A selection rate for any protected demographic group that is less than 80% of the highest group rate constitutes prima facie evidence of <b>Adverse Impact</b> under US Federal Law.</p>
        <span class="formula-tag">DIR = Rate(minority) / Rate(majority) ≥ 0.80</span>
      </div>

      <div class="edu-card">
        <h3>🏛️ NYC Local Law 144</h3>
        <p>Mandates annual independent bias audits for any Automated Employment Decision Tool (AEDT) prior to deployment, requiring published impact ratios and demographic distributions.</p>
        <span class="formula-tag">Audit Trail: Sex & Race Impact Ratios</span>
      </div>

      <div class="edu-card">
        <h3>🇪🇺 EU AI Act (High-Risk)</h3>
        <p>AI recruiting systems are classified under <b>Annex III (Employment & Worker Management)</b> as High-Risk AI Systems, requiring strict risk management, fairness telemetry, and human oversight.</p>
        <span class="formula-tag">Conformity Assessment & Post-Market Telemetry</span>
      </div>

      <div class="edu-card">
        <h3>🧠 Psychometric Construct Validity</h3>
        <p>Under Title VII, biased testing cannot be defended if the instrument lacks scientific reliability. Cronbach's α ensures items measure a single, consistent competency construct.</p>
        <span class="formula-tag">α = (K / (K-1)) * (1 - Σs²_i / s²_X) ≥ 0.70</span>
      </div>
    </section>

    <!-- Controls Panel -->
    <section class="controls-panel">
      <div class="controls-header">
        <div class="controls-title">Interactive Audit Simulator</div>
        <div class="scenario-selector">
          <button class="scenario-btn active" onclick="loadScenario('biased_tech_ats', this)">Scenario 1: Biased Tech ATS (Gender)</button>
          <button class="scenario-btn" onclick="loadScenario('age_penalized_exec', this)">Scenario 2: Exec Screening (Age Penalty)</button>
          <button class="scenario-btn" onclick="loadScenario('compliant_fair_pipeline', this)">Scenario 3: Calibrated Pipeline</button>
        </div>
      </div>

      <div class="slider-row">
        <span class="slider-label">Selection Cutoff Threshold (Score):</span>
        <input type="range" id="cutoffSlider" min="50" max="92" value="75" step="1" oninput="updateCutoffDisplay(this.value)" onchange="recalculateAudit()" />
        <span class="slider-val" id="cutoffValue">75.0</span>
      </div>
    </section>

    <!-- KPI Summary Grid -->
    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Evaluated Cohort (N)</div>
        <div class="kpi-value" id="kpiTotal">500</div>
        <span class="kpi-status-badge badge-pass">Vectorized Polars Engine</span>
      </div>

      <div class="kpi-card">
        <div class="kpi-label">Lowest Impact Ratio (DIR)</div>
        <div class="kpi-value" id="kpiDIR">0.46</div>
        <span class="kpi-status-badge badge-fail" id="badgeDIR">Adverse Impact Violation</span>
      </div>

      <div class="kpi-card">
        <div class="kpi-label">Psychometric Reliability (α)</div>
        <div class="kpi-value" id="kpiAlpha">0.82</div>
        <span class="kpi-status-badge badge-pass" id="badgeAlpha">GOOD Construct Validity</span>
      </div>

      <div class="kpi-card">
        <div class="kpi-label">Regulatory Status</div>
        <div class="kpi-value" id="kpiStatus" style="font-size: 1.35rem; color: #ef4444;">NON-CONFORMANT</div>
        <span class="kpi-status-badge badge-fail" id="badgeLegal">EEOC 4/5ths Breach</span>
      </div>
    </section>

    <!-- Detailed Demographic Disparities -->
    <section class="table-container">
      <div class="table-title">
        <span>Protected Class Breakdown: Gender & Adverse Impact</span>
        <span id="genderReferenceBadge" class="kpi-status-badge badge-pass">Reference: MALE</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Demographic Group</th>
            <th>Total Applicants</th>
            <th>Selected</th>
            <th>Selection Rate</th>
            <th>Impact Ratio (DIR)</th>
            <th>EEOC 80% Compliance</th>
          </tr>
        </thead>
        <tbody id="tableGenderBody">
          <!-- Populated dynamically via JS -->
        </tbody>
      </table>
    </section>

    <!-- Action Buttons -->
    <section class="actions-bar">
      <button class="btn-action" onclick="executeMitigation()">
        ⚡ Run Automated Fair-ML Mitigation (Pareto Tuning)
      </button>
      <button class="btn-action secondary" onclick="downloadCertificate()">
        📄 Export Official Compliance Certificate (JSON)
      </button>
    </section>

    <!-- Output Terminal -->
    <section class="table-container" id="certContainer" style="display: none;">
      <div class="table-title">
        <span>Official Audit Log & Mitigation Telemetry</span>
        <button class="btn-nav" onclick="document.getElementById('certContainer').style.display='none'">Close</button>
      </div>
      <div class="cert-box" id="certOutput"></div>
    </section>

    <footer class="footer">
      <p><b>FairTalent-Engine</b> • High-Performance Data Engineering & Algorithmic Ethics</p>
      <p>Designed and Built by <b>Fabio Torres</b> • Licensed Psychologist & M.Sc. Data Engineering</p>
    </footer>
  </main>

  <script>
    let currentScenario = 'biased_tech_ats';
    let currentThreshold = 75.0;
    let latestReport = null;

    function updateCutoffDisplay(val) {
      document.getElementById('cutoffValue').textContent = parseFloat(val).toFixed(1);
      currentThreshold = parseFloat(val);
    }

    async function loadScenario(scenarioName, btnElement) {
      currentScenario = scenarioName;
      document.querySelectorAll('.scenario-btn').forEach(btn => btn.classList.remove('active'));
      if (btnElement) btnElement.classList.add('active');
      await recalculateAudit();
    }

    async function recalculateAudit() {
      try {
        const response = await fetch(`/api/v1/simulate/${currentScenario}?threshold=${currentThreshold}`);
        const data = await response.json();
        latestReport = data;
        renderReport(data);
      } catch (err) {
        console.error("Failed to fetch simulation:", err);
      }
    }

    function renderReport(report) {
      document.getElementById('kpiTotal').textContent = report.total_evaluated;
      
      const genderAudit = report.audits_by_attribute.gender;
      const lowestDIR = genderAudit ? genderAudit.lowest_impact_ratio : 1.0;
      document.getElementById('kpiDIR').textContent = lowestDIR.toFixed(2);

      const badgeDIR = document.getElementById('badgeDIR');
      if (lowestDIR >= 0.80) {
        badgeDIR.className = 'kpi-status-badge badge-pass';
        badgeDIR.textContent = 'EEOC 80% Compliant';
      } else {
        badgeDIR.className = 'kpi-status-badge badge-fail';
        badgeDIR.textContent = 'Adverse Impact Violation';
      }

      const alpha = report.psychometrics.cronbach_alpha;
      document.getElementById('kpiAlpha').textContent = alpha.toFixed(2);
      const badgeAlpha = document.getElementById('badgeAlpha');
      badgeAlpha.textContent = `${report.psychometrics.internal_consistency} Construct`;

      const kpiStatus = document.getElementById('kpiStatus');
      const badgeLegal = document.getElementById('badgeLegal');
      if (report.overall_compliance) {
        kpiStatus.textContent = 'COMPLIANT';
        kpiStatus.style.color = '#34d399';
        badgeLegal.className = 'kpi-status-badge badge-pass';
        badgeLegal.textContent = 'Full Regulatory Clearance';
      } else {
        kpiStatus.textContent = 'NON-CONFORMANT';
        kpiStatus.style.color = '#ef4444';
        badgeLegal.className = 'kpi-status-badge badge-fail';
        badgeLegal.textContent = 'Action Required';
      }

      // Populate Gender Table
      if (genderAudit) {
        document.getElementById('genderReferenceBadge').textContent = `Reference Group: ${genderAudit.reference_group}`;
        const tbody = document.getElementById('tableGenderBody');
        tbody.innerHTML = '';

        for (const [groupName, metric] of Object.entries(genderAudit.group_metrics)) {
          const row = document.createElement('tr');
          const isCompliant = metric.eeoc_compliant;
          const statusBadge = isCompliant 
            ? '<span class="kpi-status-badge badge-pass">PASSED (≥ 0.80)</span>' 
            : '<span class="kpi-status-badge badge-fail">VIOLATION (&lt; 0.80)</span>';

          row.innerHTML = `
            <td><b>${metric.group_name}</b></td>
            <td>${metric.total_applicants}</td>
            <td>${metric.total_selected}</td>
            <td>${(metric.selection_rate * 100).toFixed(1)}%</td>
            <td><b style="color:${isCompliant ? '#34d399' : '#f87171'}">${metric.impact_ratio.toFixed(2)}</b></td>
            <td>${statusBadge}</td>
          `;
          tbody.appendChild(row);
        }
      }
    }

    async function executeMitigation() {
      try {
        const targetAttr = currentScenario === 'age_penalized_exec' ? 'age_group' : 'gender';
        const payload = {
          target_attribute: targetAttr,
          desired_min_impact_ratio: 0.80,
          baseline_threshold: currentThreshold
        };

        const response = await fetch('/api/v1/mitigate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const res = await response.json();
        const box = document.getElementById('certBox');
        const container = document.getElementById('certContainer');
        container.style.display = 'block';
        document.getElementById('certOutput').textContent = JSON.stringify(res, null, 2);
        container.scrollIntoView({ behavior: 'smooth' });
      } catch (err) {
        alert("Mitigation failed: " + err);
      }
    }

    async function downloadCertificate() {
      try {
        const response = await fetch(`/api/v1/compliance/certificate?scenario=${currentScenario}&threshold=${currentThreshold}`);
        const data = await response.json();
        const container = document.getElementById('certContainer');
        container.style.display = 'block';
        document.getElementById('certOutput').textContent = JSON.stringify(data, null, 2);
        container.scrollIntoView({ behavior: 'smooth' });
      } catch (err) {
        alert("Certificate export failed: " + err);
      }
    }

    // Auto initialize on load
    window.addEventListener('DOMContentLoaded', () => {
      loadScenario('biased_tech_ats', null);
    });
  </script>
</body>
</html>
"""
