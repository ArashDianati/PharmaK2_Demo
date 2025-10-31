import streamlit as st
import re
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PharmaK2 — Core PK Reasoning Demo", layout="centered")

st.title("PharmaK2 — Core PK Reasoning Demo")
st.write("Paste a short pharmacokinetic description below and click **Run Extraction**.")

text = st.text_area("Input Text", height=180)

def extract_values(txt):
    # very simple pattern-based extraction
    C0_match = re.search(r"(\d+)\s*mg", txt)
    k_match = re.search(r"k\s*=\s*([0-9]*\.?[0-9]+)", txt, re.IGNORECASE)
    tau_match = re.search(r"(\d+)\s*hour", txt, re.IGNORECASE)

    C0 = float(C0_match.group(1)) if C0_match else None
    k = float(k_match.group(1)) if k_match else None
    tau = float(tau_match.group(1)) if tau_match else None

    return C0, k, tau

def pk_concentration(C0, k, t):
    return C0 * np.exp(-k * t)

def simulate(C0, k, tau, hours=48):
    times = np.arange(0, hours+1, 1)
    conc = np.zeros_like(times, dtype=float)
    for i, t in enumerate(times):
        doses = range(0, t+1, tau)
        conc[i] = sum(pk_concentration(C0, k, t-d) for d in doses)
    Css = (C0/tau)/k if k and k>0 else None
    return times, conc, Css

if st.button("Run Extraction"):
    C0, k, tau = extract_values(text)

    if None in (C0, k, tau):
        st.error("Could not extract all parameters. Try a sentence like: 'The initial plasma concentration was 95 mg/L. The elimination rate constant was k = 0.18 hr⁻¹. Repeated dosing every 6 hours.'")
    else:
        st.subheader("Extracted Parameters")
        st.write(f"**C₀:** {C0} mg/L")
        st.write(f"**k:** {k} hr⁻¹")
        st.write(f"**τ:** {tau} hours")

        times, conc, Css = simulate(C0, k, tau)

        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(times, conc, linewidth=2, label="C(t)")
        if Css:
            ax.axhline(Css, color='red', linestyle='--', label=f"Css ≈ {Css:.2f}")
        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Concentration (mg/L)")
        ax.set_title("PK Simulation")
        ax.legend()
        st.pyplot(fig)

        if Css:
            st.info(f"Estimated Steady-State Concentration (Css): **{Css:.2f} mg/L**")

