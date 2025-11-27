##**AI Career Transition & Skill-Building Agent**

A LangChain-powered AI agent that helps users with career guidance, skill development, and resume analysis.
Built using **Streamlit**, **Gemini AI**, and **OCR** for real-world career assistance.

---

## **Overview**

This AI agent is designed to support users transitioning into software careers.
It provides:

* Career Q&A
* Skill gap analysis
* Resume image analysis
* Weekly learning plans
* Web search integration

The goal is to offer **practical, actionable, personalized guidance** to students and professionals.

---

## **Features**

### **1. Career Q&A**

Ask any career-related question:

* Roadmaps
* Job preparation
* Placement guidance
* Skill suggestions
* Career transitions

### **2. Resume Analyzer**

Upload a resume image (JPG/PNG).
The agent extracts information using:

* Gemini Vision (when available)
* Tesseract OCR (fallback)

Provides:

* Key skills
* Strengths & weaknesses
* Missing skills
* ATS improvements

### **3. LangChain Tools**

Integrated tools:

* `web_search` — DuckDuckGo search
* `resume_analysis_tool` — vision + OCR
* `skill_gap_tool` — missing skills
* `task_generator_tool` — learning roadmap

---

## **Tech Stack**

* **Python**
* **Streamlit**
* **LangChain**
* **Gemini 2.5 Flash (LLM + Vision)**
* **Tesseract OCR**
* **DuckDuckGo Search API**

---

## **Project Structure**

```
career_coach_agent/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── agent/
│   ├── agent_builder.py
│   ├── tools.py
│   ├── prompts.py
│   ├── memory_manager.py
│   └── __init__.py
│
└── data/
    └── uploads/
```

---

## **Setup Instructions**

### 1. Clone the repository

```bash
git clone https://github.com/TanviPhaltankar/AI-Agent.git
cd AI-Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## **Usage**

### **Career Q&A**

* Open the app
* Choose **Text Mode**
* Ask your question
* The agent provides an actionable answer

### **Resume Analyzer**

* Select **Resume Analyzer**
* Upload a resume image
* View strengths, improvements, and skill gaps

---

## **Why This Project?**

Students and early-career professionals often struggle with:

* Career direction
* Resume quality
* Skill roadmap
* Switching domains

This AI agent acts as a **practical career coach** that is accessible anytime.

---

## **Acknowledgments**

* Google Gemini
* LangChain
* Streamlit
* DuckDuckGo API
* Tesseract OCR

---

## **Author**

**Tanvi Phaltankar**

---

I
