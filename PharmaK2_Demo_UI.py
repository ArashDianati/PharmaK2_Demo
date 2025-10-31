import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(
    page_title="PharmaK2 Reasoning Demo",
    page_icon="🧪",
    layout="wide"
)

# --- Custom CSS (for Clean Scientific Layout) ---
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #DCF2FF;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 6px 0;
    text-align: right;
}
.chat-bubble-ai {
    background-color: #F4F4F4;
    padding: 10px 15px;
    border-radius: 12px;
    margin: 6px 0;
}
.section-title {
    font-size: 20px;
    font-weight: 650;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("🧪 PharmaK2 – Clinical PK Reasoning Demonstration")
st.write("این نسخه برای **ارائه و داوری** بهینه شده است.")

# --- Input Box ---
st.markdown("<div class='section-title'>ورودی</div>", unsafe_allow_html=True)
user_input = st.text_area("سناریو / دوز / مشاهده بالینی را وارد کنید:", height=120)

# --- Processing ---
if st.button("Run Clinical Reasoning"):
    
    if user_input.strip() == "":
        st.warning("ورودی نمی‌تواند خالی باشد.")
    else:
        st.markdown("<div class='section-title'>🧠 مرحله 1 — استخراج داده‌های کلیدی</div>", unsafe_allow_html=True)
        st.write(f"متن ورودی:")
        st.markdown(f"<div class='chat-bubble-user'>{user_input}</div>", unsafe_allow_html=True)

        # (برای دمو — در نسخه کامل، این قسمت با مدل جایگزین می‌شود)
        extracted = {
            "Dose": "Assumed IV 2g",
            "Half-life": "Estimated 3.4h",
            "Interval (τ)": "8h dosing",
        }

        st.json(extracted)

        st.markdown("<div class='section-title'>🔬 مرحله 2 — استدلال فارماکوکینتیک</div>", unsafe_allow_html=True)
        st.markdown("""
در این مرحله، مدل فارماکوکینتیک یک **کمپارتمان + حذف درجه اول** را فرض می‌کند.
""")

        # Simple calculation demo
        t = np.linspace(0, 12, 100)
        k = 0.2
        C0 = 15
        Ct = C0 * np.exp(-k * t)

        fig, ax = plt.subplots()
        ax.plot(t, Ct)
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("Plasma Concentration")
        ax.set_title("Predicted Concentration Curve")
        st.pyplot(fig)

        st.markdown("<div class='section-title'>✅ مرحله 3 — نتیجه نهایی</div>", unsafe_allow_html=True)
        st.success("دوز فعلی احتمالاً منجر به غلظت زیر حد درمانی در انتهای دوز می‌شود. پیشنهاد: بازبینی فاصله دوز یا دوز بارگذاری.")

else:
    st.info("برای اجرا، ابتدا سناریو را وارد کرده و سپس روی **Run Clinical Reasoning** کلیک کنید.")
