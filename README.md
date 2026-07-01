# Lucent Nudge Experiment

An interactive Streamlit app that plans the beta experiment for **Lucent**, an AI screen-time coaching app I'm building for iOS.

**Live app:** https://lucent-nudge-wissam-ezzedine.streamlit.app/
**Portfolio:** https://wissam-ezzedine.netlify.app

## Why this exists

Lucent's core thesis is that a well-timed coaching nudge reduces phone session length. Before rolling coaching out to real beta users, I need two answers:

1. How many users do I need in each arm to be confident the observed effect is real?
2. What analytical mistakes am I most at risk of making?

This app is the pre-registration document for that beta experiment. Three tabs:

- **Sample size** — Given assumptions about baseline session length, variance, and effect size, how large does the beta need to be?
- **Simulated experiment** — Set the true effect (I control it in simulation) and run the analysis I'd run on real data. Check whether the analysis correctly detects the truth.
- **The peeking problem** — Simulate what happens when someone "checks the data every day and stops when p < 0.05." False positive rate should be 5%. It won't be.

## Stack

- Streamlit for the interface
- scipy.stats for Welch's two-sample t-test
- statsmodels TTestIndPower for closed-form sample-size calculation
- numpy for log-normal session-length sampling
- plotly for visualization

## Run locally

    git clone https://github.com/Wiss-21/lucent-nudge-experiment
    cd lucent-nudge-experiment
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

## About Lucent

Lucent reads Apple's Screen Time data, names the user's behavioral pattern (e.g. "Late-Night Doom Scroller"), and coaches with a nudge before the pattern starts. This app plans how I'll prove the coaching feature actually works before shipping it.

---

Built by Wissam Ezzedine.
