import os
import re
import time
import json
import tempfile
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader
from google.api_core.exceptions import ResourceExhausted
from utils.pdf_generator import generate_pdf

# ===========================
# LOAD API KEY
# ===========================
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# ===========================
# STREAMLIT CONFIG
# ===========================
st.set_page_config(
    page_title="CivicSense AI",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ CivicSense AI")
st.subheader("AI for Better Living and Smarter Communities")

# ===========================
# PDF UPLOAD
# ===========================
uploaded_file = st.file_uploader("📄 Upload Community Report", type=["pdf"])

pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.success("PDF uploaded successfully!")
    st.subheader("Preview")
    st.write(pdf_text[:1000])

# ===========================
# QUESTION INPUT
# ===========================
question = st.text_area("Ask a question about the report")

# ===========================
# SAFE JSON PARSER
# ===========================
def safe_json_parse(text):
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None
    return None

# ===========================
# ANALYZE BUTTON
# ===========================
if st.button("🚀 Analyze"):

    if not uploaded_file:
        st.warning("Upload a PDF first")
        st.stop()

    if question.strip() == "":
        st.warning("Enter a question")
        st.stop()

    # ===========================
    # PROMPT (STRICT JSON)
    # ===========================
    prompt = f"""
You are a strict JSON generator.
Return ONLY valid JSON.

Schema:
{{
"community_score": "82/100",
"traffic_risk": "High",
"air_quality": "Moderate",
"public_transport": "72%",
"priority_area": "Traffic Management",
"key_issues": ["issue1", "issue2"],
"recommendations": ["rec1", "rec2"],
"action_plan": ["week1", "week2", "week3", "week4"]
}}

Community Report:
{pdf_text}

User Question:
{question}
"""

    # ===========================
    # GEMINI CALL (RETRY SAFE)
    # ===========================
    with st.spinner("Analyzing..."):

        for i in range(3):
            try:
                response = model.generate_content(prompt)
                break
            except ResourceExhausted:
                st.warning("Quota exceeded. Retrying in 20 seconds...")
                time.sleep(20)
        else:
            st.error("Gemini quota finished. Try later.")
            st.stop()

    # ===========================
    # PARSE JSON
    # ===========================
    data = safe_json_parse(response.text)

    if not data:
        st.error("AI did not return valid JSON.")
        st.text(response.text)
        st.stop()

    # ===========================
    # OUTPUT
    # ===========================
    st.markdown("## 🤖 AI Response")
    st.json(data)

    st.divider()

    # ===========================
    # DASHBOARD
    # ===========================
    st.header("📊 Community Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Community Score", data["community_score"])
    col2.metric("Traffic Risk", data["traffic_risk"])
    col3.metric("Air Quality", data["air_quality"])

    col4, col5 = st.columns(2)
    col4.metric("Public Transport", data["public_transport"])
    col5.metric("Priority Area", data["priority_area"])

    st.divider()

    # ===========================
    # KEY ISSUES
    # ===========================
    st.subheader("🧠 Key Issues")
    for issue in data["key_issues"]:
        st.error(issue)

    # ===========================
    # RECOMMENDATIONS
    # ===========================
    st.subheader("💡 Recommendations")
    for rec in data["recommendations"]:
        st.success(rec)

    st.divider()

    # ===========================
    # CHART
    # ===========================
    st.subheader("📈 Community Indicators")

    try:
        transport_val = int(data["public_transport"].replace("%", ""))
    except:
        transport_val = 70

    chart_df = pd.DataFrame({
        "Category": ["Traffic", "Air Quality", "Public Transport"],
        "Value": [80, 60, transport_val]
    })

    st.bar_chart(chart_df.set_index("Category"))

    st.divider()

    # ===========================
    # PDF DOWNLOAD
    # ===========================
    report_data = {
        "Community Score": data["community_score"],
        "Traffic Risk": data["traffic_risk"],
        "Air Quality": data["air_quality"],
        "Public Transport": data["public_transport"],
        "Priority": data["priority_area"]
    }

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    generate_pdf(temp_file.name, report_data)

    with open(temp_file.name, "rb") as f:
        st.download_button(
            "📥 Download PDF Report",
            f,
            file_name="CivicSense_Report.pdf",
            mime="application/pdf"
        )

    st.divider()

    # ===========================
    # ACTION PLAN
    # ===========================
    st.subheader("🗓️ 30-Day Action Plan")

    for step in data["action_plan"]:
        st.info(step)

    st.divider()

    # ===========================
    # TXT DOWNLOAD
    # ===========================
    full_report = f"""
CIVICSENSE AI REPORT

Score: {data['community_score']}
Traffic: {data['traffic_risk']}
Air Quality: {data['air_quality']}
Transport: {data['public_transport']}
Priority: {data['priority_area']}

Key Issues:
{data['key_issues']}

Recommendations:
{data['recommendations']}

Action Plan:
{data['action_plan']}
"""

    st.download_button(
        "📥 Download TXT Report",
        full_report,
        file_name="Decision_Report.txt",
        mime="text/plain"
    )