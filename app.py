import streamlit as st
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower
import plotly.graph_objects as go
import base64
from pathlib import Path

# ─── Page config ───
st.set_page_config(
    page_title="Lucent · Nudge Lab",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Brand tokens ───
BG, SURFACE, SURFACE_2 = "#07090D", "#0D1117", "#131921"
BORDER = "rgba(255,255,255,0.06)"
TEXT, TEXT_2, TEXT_3 = "#E8ECF1", "#9CA3AF", "#6B7280"
TEAL, INDIGO, PERIWINKLE, PURPLE = "#2DD4BF", "#6366F1", "#818CF8", "#A78BFA"
SUCCESS, WARN, DANGER = "#34D399", "#FBBF24", "#F87171"

# ─── Lucent theme CSS ───
st.markdown(f"""
<style>
    .stApp {{ background: {BG}; color: {TEXT}; }}
    .stApp::before {{
        content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
        background:
            radial-gradient(circle at 12% -8%, rgba(45,212,191,0.07), transparent 45%),
            radial-gradient(circle at 92% 8%, rgba(99,102,241,0.06), transparent 45%);
    }}
    h1, h2, h3, h4 {{ color: {TEXT}; letter-spacing: -0.02em; font-family: 'Sora', system-ui, sans-serif; }}
    .grad-title {{
        background: linear-gradient(135deg, {TEAL}, {PERIWINKLE}, {INDIGO});
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
        font-family: 'Sora', system-ui, sans-serif; font-weight: 700; letter-spacing: -0.03em;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 1px solid {BORDER}; }}
    .stTabs [data-baseweb="tab"] {{
        background: {SURFACE}; border: 1px solid {BORDER};
        border-radius: 10px; color: {TEXT_2}; padding: 12px 18px; font-weight: 500;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(45,212,191,0.14); color: {TEAL}; border-color: rgba(45,212,191,0.34);
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {TEAL}, {PERIWINKLE});
        color: {BG}; border: none; border-radius: 10px; font-weight: 600;
        padding: 10px 20px; transition: transform 0.2s, box-shadow 0.2s;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px); box-shadow: 0 8px 24px rgba(45,212,191,0.25); color: {BG};
    }}
    [data-testid="stMetricValue"] {{ color: {TEAL}; font-family: 'Sora', sans-serif; }}
    [data-testid="stMetricLabel"] {{ color: {TEXT_3}; }}
    .hero-card {{
        background: linear-gradient(135deg, {SURFACE} 0%, {SURFACE_2} 100%);
        border: 1px solid {BORDER}; border-radius: 18px;
        padding: 28px 32px; margin-bottom: 24px; position: relative; overflow: hidden;
    }}
    .hero-card::before {{
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, {TEAL}, {PERIWINKLE}, {INDIGO});
    }}
    .prereg {{
        background: {SURFACE}; border: 1px solid rgba(45,212,191,0.28);
        border-left: 3px solid {TEAL}; border-radius: 10px;
        padding: 18px 22px; font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px; color: {TEXT_2}; white-space: pre-wrap; line-height: 1.6;
    }}
    .intuition {{
        background: linear-gradient(135deg, rgba(129,140,248,0.08), rgba(45,212,191,0.08));
        border: 1px solid rgba(129,140,248,0.28); border-radius: 10px;
        padding: 16px 20px; color: {TEXT};
    }}
    .intuition .lbl {{
        font-family: 'JetBrains Mono', monospace; font-size: 11px;
        letter-spacing: 0.12em; text-transform: uppercase; color: {PERIWINKLE};
        margin-bottom: 8px;
    }}
    .intuition .num {{ color: {TEAL}; font-weight: 700; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .prereg-card {{
        background: rgba(45,212,191,0.03);
        border: 1px solid rgba(45,212,191,0.20);
        border-radius: 14px;
        padding: 26px 30px;
        position: relative;
        overflow: hidden;
    }}
    .prereg-card::before {{
        content: ''; position: absolute; top: 0; left: 0;
        width: 3px; height: 100%;
        background: linear-gradient(180deg, {TEAL}, {PERIWINKLE}, {INDIGO});
    }}
    .prereg-row {{
        display: grid; grid-template-columns: 130px 1fr;
        gap: 20px; padding: 7px 0;
    }}
    .prereg-key {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase;
        color: {TEAL}; padding-top: 3px;
    }}
    .prereg-val {{ color: {TEXT}; font-size: 13.5px; line-height: 1.55; }}
    .prereg-val .mono {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px; color: {PERIWINKLE}; font-weight: 500;
    }}
    .prereg-divider {{
        height: 1px; background: rgba(255,255,255,0.06); margin: 10px 0;
    }}
    .prereg-rules {{ display: flex; flex-direction: column; gap: 9px; }}
    .prereg-rule {{
        display: flex; align-items: flex-start; gap: 12px;
        font-size: 13px; color: {TEXT_2}; line-height: 1.5;
    }}
    .prereg-rule .tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
        padding: 3px 8px; border-radius: 5px;
        flex-shrink: 0; min-width: 64px; text-align: center;
    }}
    .prereg-rule .tag.launch {{ background: rgba(52,211,153,0.14); color: {SUCCESS}; border: 1px solid rgba(52,211,153,0.32); }}
    .prereg-rule .tag.hold   {{ background: rgba(251,191,36,0.14); color: {WARN};    border: 1px solid rgba(251,191,36,0.32); }}
    .prereg-rule .tag.kill   {{ background: rgba(248,113,113,0.14); color: {DANGER}; border: 1px solid rgba(248,113,113,0.32); }}
</style>
""", unsafe_allow_html=True)

# ─── Logo loader ───
def load_logo_b64():
    path = Path(__file__).parent / "assets" / "lucent-mark.png"
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = load_logo_b64()

# ─── Sampling helper ───
def sample_sessions(mean_min, std_min, n, seed=None):
    rng = np.random.default_rng(seed)
    cv = std_min / mean_min
    sigma = np.sqrt(np.log(1 + cv**2))
    mu = np.log(mean_min) - sigma**2 / 2
    return rng.lognormal(mu, sigma, size=n)

# ─── Hero ───
logo_img = (f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="width:64px; height:64px; filter: drop-shadow(0 0 20px rgba(45,212,191,0.4));" />'
            if logo_b64 else '')
st.markdown(f"""
<div class="hero-card">
    <div style="display:flex; align-items:center; gap:20px; position:relative; z-index:1;">
        {logo_img}
        <div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.14em; color:{TEAL}; text-transform:uppercase; margin-bottom:6px;">
                // LUCENT · NUDGE LAB
            </div>
            <div class="grad-title" style="font-size:34px; line-height:1.1;">
                Will the nudge actually work?
            </div>
            <div style="color:{TEXT_2}; font-size:15px; margin-top:10px; max-width:640px;">
                The experiment plan for Lucent's beta. How many users do I need? What mistakes am I most at risk of? Every knob is live.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "1. How many users?",
    "2. Run a simulation",
    "3. The peeking trap",
])

# ============================================================
# TAB 1 — SAMPLE SIZE
# ============================================================
with tab1:
    st.markdown("### How many users do I need?")
    st.markdown("Set the baseline and the smallest effect worth detecting. Get the sample size and how long the beta has to run.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### The assumptions")
        baseline_mean = st.slider("Baseline avg session (min)", 15, 90, 40, 1)
        baseline_std = st.slider("Baseline std dev (min)", 5, 60, 20, 1)
        mde_pct = st.slider("Smallest effect worth detecting (% cut)", 5, 40, 15, 1)
        alpha = st.select_slider("Alpha (false-positive tolerance)", options=[0.01, 0.05, 0.10], value=0.05)
        power = st.select_slider("Power (chance we catch a real effect)", options=[0.70, 0.80, 0.90, 0.95], value=0.80)
        weekly_signups = st.slider("Assumed weekly beta signups", 10, 500, 100, 10)

    with col_b:
        st.markdown("#### The verdict")
        mde_abs = baseline_mean * mde_pct / 100
        cohen_d = mde_abs / baseline_std
        analysis = TTestIndPower()
        n_per_arm = int(np.ceil(analysis.solve_power(
            effect_size=cohen_d, alpha=alpha, power=power,
            ratio=1.0, alternative='two-sided'
        )))
        total_n = n_per_arm * 2
        weeks_needed = total_n / weekly_signups

        st.metric("Users per arm", f"{n_per_arm:,}")
        st.metric("Total users needed", f"{total_n:,}")
        st.metric("Beta duration", f"{weeks_needed:.1f} weeks")
        st.caption(f"Effect size (Cohen's d): **{cohen_d:.2f}** · absolute MDE: **{mde_abs:.1f} min**")

    # ─── Pre-registration card ───
    st.markdown("---")
    st.markdown("#### Pre-registration (lock this in before you look at any data)")
    st.markdown("The single strongest habit in experimentation: write down the plan before the data comes in. This is the plan for the settings above. Copy it into the repo before the beta starts.")

    prereg_html = f"""
    <div class="prereg-card">
      <div class="prereg-row"><div class="prereg-key">Experiment</div><div class="prereg-val">Lucent nudge · does it reduce session length?</div></div>
      <div class="prereg-row"><div class="prereg-key">Metric</div><div class="prereg-val">Avg session length in target window (min, lower is better)</div></div>
      <div class="prereg-row"><div class="prereg-key">Guardrails</div><div class="prereg-val">7-day retention, uninstall rate</div></div>
      <div class="prereg-divider"></div>
      <div class="prereg-row"><div class="prereg-key">Hypothesis</div><div class="prereg-val">The nudge reduces avg session length by <span class="mono">≥ {mde_pct}%</span> vs no nudge.</div></div>
      <div class="prereg-divider"></div>
      <div class="prereg-row"><div class="prereg-key">Sample</div><div class="prereg-val"><span class="mono">{n_per_arm:,}</span> users per arm &nbsp;·&nbsp; <span class="mono">{total_n:,}</span> total</div></div>
      <div class="prereg-row"><div class="prereg-key">Duration</div><div class="prereg-val"><span class="mono">~{weeks_needed:.1f}</span> weeks at ~{weekly_signups}/week signups</div></div>
      <div class="prereg-row"><div class="prereg-key">Randomization</div><div class="prereg-val">50/50 on install, sticky by user_id</div></div>
      <div class="prereg-divider"></div>
      <div class="prereg-row"><div class="prereg-key">Test</div><div class="prereg-val">Welch's two-sample t-test on log-transformed session length</div></div>
      <div class="prereg-row"><div class="prereg-key">Alpha</div><div class="prereg-val"><span class="mono">{alpha}</span> &nbsp;·&nbsp; two-sided</div></div>
      <div class="prereg-row"><div class="prereg-key">Power</div><div class="prereg-val"><span class="mono">{power}</span></div></div>
      <div class="prereg-row"><div class="prereg-key">MDE</div><div class="prereg-val"><span class="mono">{mde_abs:.1f}</span> min ({mde_pct}%) &nbsp;·&nbsp; Cohen's d = <span class="mono">{cohen_d:.2f}</span></div></div>
      <div class="prereg-divider"></div>
      <div class="prereg-row">
        <div class="prereg-key">Decision</div>
        <div class="prereg-rules">
          <div class="prereg-rule"><span class="tag launch">LAUNCH</span><span>if p &lt; {alpha}, CI excludes 0, observed cut ≥ {mde_pct/2:.0f}%, guardrails move &lt; 2pp</span></div>
          <div class="prereg-rule"><span class="tag hold">HOLD</span><span>if p ≥ {alpha} or CI straddles 0</span></div>
          <div class="prereg-rule"><span class="tag kill">KILL</span><span>if guardrails degrade &gt; 2pp regardless of primary</span></div>
        </div>
      </div>
    </div>
    """
    st.markdown(prereg_html, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Sample size vs effect size")
    st.markdown("Bigger effect I'm willing to detect = fewer users needed. Diamond is the current setting.")

    mde_range = np.arange(5, 41, 1)
    n_range = []
    for m in mde_range:
        d = (baseline_mean * m / 100) / baseline_std
        n = analysis.solve_power(effect_size=d, alpha=alpha, power=power,
                                 ratio=1.0, alternative='two-sided')
        n_range.append(int(np.ceil(n)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mde_range, y=n_range, mode='lines',
                             line=dict(color=TEAL, width=3), name='Sample size'))
    fig.add_trace(go.Scatter(x=[mde_pct], y=[n_per_arm], mode='markers',
                             marker=dict(color=PURPLE, size=14, symbol='diamond'),
                             name=f'Now ({mde_pct}%)'))
    fig.update_layout(
        xaxis_title='Smallest effect worth detecting (%)',
        yaxis_title='Users per arm',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=SURFACE,
        font=dict(family="Outfit, sans-serif", color=TEXT_2), height=380
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2 — SIMULATION
# ============================================================
with tab2:
    st.markdown("### Run a simulated beta")
    st.markdown("Set the real effect of the nudge (I control it here). Generate data. Run the analysis. See if it caught the truth.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### The setup")
        sim_n = st.slider("Users per arm", 50, 3000, 500, 50, key='sim_n')
        sim_mean = st.slider("Baseline mean (min)", 15, 90, 40, 1, key='sim_mean')
        sim_std = st.slider("Baseline std (min)", 5, 60, 20, 1, key='sim_std')
        true_effect = st.slider("REAL effect of the nudge (% change)", -30, 20, -15, 1,
                                key='true_effect',
                                help="Negative = nudge cuts session length. Positive = nudge backfired.")
        seed = st.number_input("Random seed", value=42, step=1)

    with col_b:
        st.markdown("#### The analysis")
        control = sample_sessions(sim_mean, sim_std, sim_n, seed=seed)
        treat_mean = sim_mean * (1 + true_effect / 100)
        treatment = sample_sessions(treat_mean, sim_std, sim_n, seed=seed + 1)

        t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)
        observed_diff = treatment.mean() - control.mean()
        n1, n2 = len(control), len(treatment)
        s1, s2 = control.std(ddof=1), treatment.std(ddof=1)
        se_diff = np.sqrt(s1**2 / n1 + s2**2 / n2)
        df = (s1**2 / n1 + s2**2 / n2) ** 2 / (
            (s1**2 / n1) ** 2 / (n1 - 1) + (s2**2 / n2) ** 2 / (n2 - 1)
        )
        t_crit = stats.t.ppf(0.975, df)
        ci_low = observed_diff - t_crit * se_diff
        ci_high = observed_diff + t_crit * se_diff

        st.metric("Observed difference (min)", f"{observed_diff:+.2f}")
        st.metric("95% CI", f"[{ci_low:+.2f}, {ci_high:+.2f}]")
        st.metric("p-value", f"{p_value:.4f}")

        if p_value < 0.05:
            if true_effect != 0:
                st.success("Significant. The analysis caught the real effect.")
            else:
                st.error("Significant, but this is a FALSE POSITIVE. Truth was zero.")
        else:
            if true_effect == 0:
                st.info("Not significant. Correctly matches the truth (zero effect).")
            else:
                st.warning("Not significant, but truth is non-zero. False negative.")

    # ─── Real-life intuition ───
    if true_effect != 0:
        daily_change = sim_mean * true_effect / 100
        abs_daily = abs(daily_change)
        weekly = abs_daily * 7 / 60
        yearly = abs_daily * 365 / 60
        is_win = true_effect < 0
        st.markdown(f"""
        <div class="intuition" style="margin-top:20px;">
            <div class="lbl">What this effect looks like in real life</div>
            A {abs(true_effect)}% {"cut" if is_win else "increase"} on a {sim_mean}-minute baseline means each user
            {"saves" if is_win else "loses"} <span class="num">{abs_daily:.1f} min/day</span>,
            <span class="num">{weekly:.1f} h/week</span>,
            or <span class="num">{yearly:.0f} h/year</span> of screen time.
            {"That's the size of win Lucent needs to hit." if is_win else "That's how badly the nudge backfired."}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Distribution of session lengths")
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=control, name='Control (no nudge)',
                               marker_color=PERIWINKLE, opacity=0.6, nbinsx=40))
    fig.add_trace(go.Histogram(x=treatment, name='Treatment (nudge)',
                               marker_color=TEAL, opacity=0.6, nbinsx=40))
    fig.update_layout(
        barmode='overlay', xaxis_title='Session length (min)',
        yaxis_title='Number of sessions', template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=SURFACE,
        font=dict(family="Outfit, sans-serif", color=TEXT_2), height=360
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Power curve, empirically")
    st.markdown("Run 500 fresh experiments at the current sample size, across real effect sizes. Count how often we detect significance.")
    if st.button("Run power curve (~15 sec)"):
        with st.spinner("Running 8,500 t-tests..."):
            effect_grid = np.arange(-30, 21, 3)
            detection_rates = []
            for eff in effect_grid:
                hits = 0
                for _ in range(500):
                    c = sample_sessions(sim_mean, sim_std, sim_n)
                    t = sample_sessions(sim_mean * (1 + eff / 100), sim_std, sim_n)
                    _, p = stats.ttest_ind(c, t, equal_var=False)
                    if p < 0.05:
                        hits += 1
                detection_rates.append(hits / 500)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=effect_grid, y=detection_rates, mode='lines+markers',
                                     line=dict(color=TEAL, width=3), marker=dict(size=8)))
            fig.add_hline(y=0.8, line_dash='dash', line_color=WARN,
                          annotation_text='80% power', annotation_position='top left')
            fig.add_vline(x=0, line_dash='dash', line_color=DANGER,
                          annotation_text='Zero effect', annotation_position='top left')
            fig.update_layout(
                xaxis_title='Real effect (% change)',
                yaxis_title='P(detect significance)',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=SURFACE,
                font=dict(family="Outfit, sans-serif", color=TEXT_2), height=380
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("At real effect = 0 the detection rate should hover near 5%.")

# ============================================================
# TAB 3 — PEEKING TRAP
# ============================================================
with tab3:
    st.markdown("### The peeking trap")
    st.markdown("The most common way to blow up an A/B test: check every day and stop the moment p < 0.05. Below I simulate that on a nudge that actually does nothing. The false positive rate should be 5%. It won't be.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### The setup")
        peek_n_total = st.slider("Total users per arm (planned)", 200, 2000, 800, 100)
        peek_checks = st.slider("Number of times I peek", 1, 30, 15)
        peek_alpha = st.select_slider("Alpha", options=[0.01, 0.05, 0.10], value=0.05)
        peek_runs = st.select_slider("Simulated betas", options=[200, 500, 1000, 2000], value=1000)
        peek_mean, peek_std = 40, 20
        st.caption(f"Baseline: {peek_mean} min, std {peek_std}. Real effect: 0.")

    with col_b:
        st.markdown("#### The result")
        if st.button("Run peeking simulation"):
            with st.spinner("Simulating peeking..."):
                check_points = np.linspace(peek_n_total // peek_checks, peek_n_total, peek_checks).astype(int)
                naive_false_pos, wait_false_pos = 0, 0
                for _ in range(peek_runs):
                    c = sample_sessions(peek_mean, peek_std, peek_n_total)
                    t = sample_sessions(peek_mean, peek_std, peek_n_total)
                    for cp in check_points:
                        _, p = stats.ttest_ind(c[:cp], t[:cp], equal_var=False)
                        if p < peek_alpha:
                            naive_false_pos += 1
                            break
                    _, p_final = stats.ttest_ind(c, t, equal_var=False)
                    if p_final < peek_alpha:
                        wait_false_pos += 1

                naive_rate = naive_false_pos / peek_runs
                wait_rate = wait_false_pos / peek_runs

                st.metric("If I peek and stop early", f"{naive_rate*100:.1f}% false positives",
                          delta=f"{(naive_rate - peek_alpha)*100:+.1f} pp vs target",
                          delta_color="inverse")
                st.metric("If I wait for the full sample", f"{wait_rate*100:.1f}% false positives",
                          delta=f"{(wait_rate - peek_alpha)*100:+.1f} pp vs target",
                          delta_color="inverse")

                if naive_rate > peek_alpha * 2:
                    st.error(f"Peeking inflates false positives by **{naive_rate/peek_alpha:.1f}x** the target rate.")

    st.markdown("---")
    st.markdown("#### More peeks, more mistakes")
    st.markdown("Every extra check is another chance to hit p < 0.05 by luck.")
    if st.button("Run peek-frequency sweep (~30 sec)"):
        with st.spinner("Simulating..."):
            check_grid = [1, 2, 5, 10, 15, 20, 30]
            rates = []
            for n_checks in check_grid:
                cps = np.linspace(peek_n_total // n_checks, peek_n_total, n_checks).astype(int)
                false_pos = 0
                for _ in range(1000):
                    c = sample_sessions(peek_mean, peek_std, peek_n_total)
                    t = sample_sessions(peek_mean, peek_std, peek_n_total)
                    for cp in cps:
                        _, p = stats.ttest_ind(c[:cp], t[:cp], equal_var=False)
                        if p < 0.05:
                            false_pos += 1
                            break
                rates.append(false_pos / 1000)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=check_grid, y=[r*100 for r in rates],
                                     mode='lines+markers',
                                     line=dict(color=DANGER, width=3), marker=dict(size=10)))
            fig.add_hline(y=5, line_dash='dash', line_color=SUCCESS,
                          annotation_text='Target (5%)', annotation_position='top left')
            fig.update_layout(
                xaxis_title='Number of peeks', yaxis_title='False positive rate (%)',
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=SURFACE,
                font=dict(family="Outfit, sans-serif", color=TEXT_2), height=380
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Fix: pre-register when you'll analyze and don't peek. Or use sequential-testing methods that adjust for peeking.")

# ─── Footer ───
st.markdown("---")
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:16px 0; color:{TEXT_3}; font-family:'JetBrains Mono',monospace; font-size:12px; flex-wrap: wrap; gap: 12px;">
    <span>Built by <span style="color:{TEAL};">Wissam Ezzedine</span> as the experiment plan for Lucent's beta.</span>
    <span>
        <a href="https://wissam-ezzedine.netlify.app" target="_blank" style="color:{TEAL}; text-decoration:none;">portfolio</a> ·
        <a href="https://github.com/Wiss-21/lucent-nudge-experiment" target="_blank" style="color:{TEAL}; text-decoration:none;">github</a>
    </span>
</div>
""", unsafe_allow_html=True)
