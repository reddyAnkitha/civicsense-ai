# 🏙️ CivicSense AI

AI for Better Living and Smarter Communities

CivicSense AI is an AI-powered decision intelligence platform that helps analyze community reports, identify key issues, and provide actionable recommendations for smarter urban planning and public services.

---

## 🚀 Live Demo

**Streamlit App:**
https://civicsense-ai-w2ywyhwwfd6yztwg5tthep.streamlit.app/

---

## ✨ Features

- 📄 Upload Community Reports (PDF)
- 🤖 AI-powered report analysis using Gemini AI
- 📊 Interactive Community Dashboard
- 🚦 Traffic Risk Analysis
- 🌿 Air Quality Assessment
- 🚌 Public Transport Insights
- 💡 AI-generated Recommendations
- 📅 30-Day Action Plan
- 📈 Community Indicator Charts
- 📥 Download PDF Report
- 📥 Download TXT Report

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Pandas
- PyPDF
- ReportLab
- Python-dotenv

---

## 📂 Project Structure

```
civicsense-ai/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── utils/
│   └── pdf_generator.py
│── data/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/reddyAnkitha/civicsense-ai.git
```

Go to the project folder:

```bash
cd civicsense-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Run the application:

```bash
streamlit run app.py
```

---

## 📋 How to Use

1. Launch the application.
2. Upload a community report in PDF format.
3. Enter a question about the report.
4. Click **Analyze**.
5. View the AI-generated insights.
6. Explore the dashboard and charts.
7. Download the generated PDF or TXT report.

---

## 📷 Screenshots


### 🏠 Home Page
Displays the CivicSense AI landing page where users can upload a community report and begin analysis.

![Home](docs/Stremlit.png)

---

### 📄 Upload Community Report
Shows a PDF report uploaded successfully with a preview of the extracted content.

![Upload PDF](docs/pdf%20upload.png)

---

### ❓ Ask a Question
Users can ask questions about the uploaded community report and receive AI-powered insights.

![Ask Question](docs/Ask%20a%20question.png)

---

### 📊 Community Dashboard
Displays Community Score, Traffic Risk, Air Quality, Public Transport status, and Priority Area.

![Dashboard](docs/Dashboard.png)

---

### 📈 Community Indicators
Visualizes community metrics using an interactive bar chart.

![Chart](docs/chart.png)
---

## 👩‍💻 Author

**Reddy Ankitha**

GitHub:
https://github.com/reddyAnkitha

---

## 📄 License

This project is created for educational and hackathon purposes.