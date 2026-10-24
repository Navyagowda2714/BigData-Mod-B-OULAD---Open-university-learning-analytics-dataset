<!-- ===================================================== -->
<!--   OULAD Learning Analytics — README.md (Premium)       -->
<!--   Classy • Visual • Interactive • Recruiter-Ready      -->
<!-- ===================================================== -->

<div align="center">

<!-- ✅ SAME BRAND BANNER STYLE (consistent across projects) -->
<img width="100%" alt="OULAD Learning Analytics premium header"
src="https://capsule-render.vercel.app/api?type=waving&color=0:070A12,45:1E3A8A,75:4F46E5,100:06B6D4&height=230&section=header&text=OULAD%20Learning%20Analytics&fontSize=52&fontColor=FFFFFF&fontAlignY=40&desc=Student%20Performance%20Prediction%20%E2%80%A2%20Feature%20Engineering%20%E2%80%A2%20Classification%20%E2%80%A2%20Explainability%20%E2%80%A2%20Insights&descAlignY=70&descSize=18&animation=fadeIn" />

<br/>

<img alt="Python" src="https://img.shields.io/badge/Python-111827?style=for-the-badge&logo=python&logoColor=ffd43b"/>
<img alt="Pandas" src="https://img.shields.io/badge/Pandas-111827?style=for-the-badge&logo=pandas&logoColor=white"/>
<img alt="NumPy" src="https://img.shields.io/badge/NumPy-111827?style=for-the-badge&logo=numpy&logoColor=3B82F6"/>
<img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-111827?style=for-the-badge&logo=scikit-learn&logoColor=F59E0B"/>
<img alt="ML" src="https://img.shields.io/badge/ML%20Task-Classification-111827?style=for-the-badge"/>
<img alt="Analytics" src="https://img.shields.io/badge/Learning%20Analytics-111827?style=for-the-badge"/>

<br/><br/>

<a href="#-quickstart"><b>Quickstart</b></a> •
<a href="#-project-overview"><b>Overview</b></a> •
<a href="#-problem-framing"><b>Problem</b></a> •
<a href="#-creative-workflow"><b>Workflow</b></a> •
<a href="#-modeling-playbook"><b>Modeling</b></a> •
<a href="#-evaluation--insights"><b>Insights</b></a> •
<a href="#-contact"><b>Contact</b></a>

</div>

---


<!-- quickstart:start -->
# 🚀 Quickstart

[![notebooks](https://github.com/Navyagowda2714/BigData-Mod-B-OULAD---Open-university-learning-analytics-dataset/actions/workflows/notebooks.yml/badge.svg)](https://github.com/Navyagowda2714/BigData-Mod-B-OULAD---Open-university-learning-analytics-dataset/actions/workflows/notebooks.yml)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Navyagowda2714/BigData-Mod-B-OULAD---Open-university-learning-analytics-dataset/blob/main/OULAD.ipynb)

**Requirements:** Python 3.10+ and the [Open University Learning Analytics Dataset](https://analyse.kmi.open.ac.uk/open_dataset) (7 CSV files, ~450 MB, CC-BY 4.0 — not committed to this repo).

```bash
git clone https://github.com/Navyagowda2714/BigData-Mod-B-OULAD---Open-university-learning-analytics-dataset.git oulad
cd oulad
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# put courses.csv, assessments.csv, studentAssessment.csv, studentInfo.csv,
# studentRegistration.csv, studentVle.csv and vle.csv in ./data
mkdir data   # or: export OULAD_DATA_DIR=/path/to/oulad/csvs

streamlit run streamlit_oulad_app.py      # interactive dashboard → http://localhost:8501
jupyter notebook OULAD.ipynb              # full analysis
```

| File | What it is |
|---|---|
| `OULAD.ipynb` | EDA, feature engineering, SMOTE, clustering, classification (RF / XGBoost) and time-series forecasting |
| `streamlit_oulad_app.py` | Streamlit dashboard of the analysis |
| `OULAD_NAVY_TEAM.html` | Rendered notebook — open it to read results without running anything |
| `Oulad.pdf`, `OULAD.pptx`, `streamlit_oulad_Team_navy.pdf` | Report, slides and dashboard screenshots |
<!-- quickstart:end -->

---

## ✨ Project Overview

This project applies **learning analytics** to the **OULAD dataset (Open University Learning Analytics Dataset)** to predict student outcomes and extract signals that can support:

- early risk detection
- targeted academic interventions
- course design improvement

This repository is written to be **portfolio-grade**: clear problem framing, measurable evaluation, and insight-driven interpretation.

---

## 🎓 Problem Framing

<details open>
<summary><b>🧩 What are we predicting? (click to collapse)</b></summary>
<br/>

**Goal:** predict student outcome (e.g., pass/fail/withdrawal or success vs risk) from behavioral + academic signals.

**Why it matters:** institutions can intervene earlier to improve retention and student success.

**Key challenge:** learning data is *longitudinal* + *sparse* + *behavior-driven* (clickstream-style).

</details>

---

## 🎛️ Creative Workflow

<details open>
<summary><b>🧠 Learning Intelligence Flow (click to collapse)</b></summary>
<br/>

```mermaid
flowchart LR

  %% ===== DATA BAND =====
  subgraph DATA["📥 Data Layer"]
    direction LR
    D1["Students"]
    D2["Assessments"]
    D3["VLE Activity Logs"]
  end

  %% ===== PROCESS BAND =====
  subgraph PROCESS["🧠 Intelligence Layer"]
    direction LR
    P1["Data Cleaning"]
    P2["Feature Engineering"]
    P3["Temporal Aggregation"]
    P4["Model Training"]
  end

  %% ===== INSIGHT BAND =====
  subgraph INSIGHT["🚀 Insight Layer"]
    direction LR
    I1["Performance Prediction"]
    I2["Risk Classification"]
    I3["Feature Importance"]
    I4["Intervention Signals"]
  end

  %% ===== FLOW =====
  DATA --> PROCESS --> INSIGHT

  %% ===== STYLE =====
  classDef data fill:#0B1220,stroke:#60A5FA,color:#E5E7EB,stroke-width:2px;
  classDef process fill:#0F172A,stroke:#A78BFA,color:#E5E7EB;
  classDef insight fill:#062a1d,stroke:#16A34A,color:#E5E7EB;

  class D1,D2,D3 data;
  class P1,P2,P3,P4 process;
  class I1,I2,I3,I4 insight;
```

</details>

---

## 🧠 Modeling Playbook

<details open>
<summary><b>🧪 “Model Ladder” (click to collapse)</b></summary>
<br/>

```mermaid
sequenceDiagram
  autonumber
  participant D as Dataset
  participant B as Baseline Model
  participant T as Tuned Model
  participant E as Evaluation
  participant I as Insights

  D->>B: Train baseline classifier
  B->>E: Measure F1 / ROC-AUC
  D->>T: Train tuned models + selection
  T->>E: Compare metrics + stability
  E->>I: Identify top drivers (features)
  I-->>E: Validate with error analysis
```

</details>

**What this demonstrates**
- Model selection thinking (not “one model and done”)
- Proper evaluation for imbalanced outcomes (precision/recall/F1)
- Insight extraction for practical interventions

---

## 📊 Evaluation & Insights

<div align="center">

<table>
<tr>
<td width="33%" align="center" valign="top">

### 🎯 Objective
Predict student risk/success

<img src="https://img.shields.io/badge/Goal-Outcome%20Prediction-0EA5E9?style=for-the-badge"/>

</td>
<td width="33%" align="center" valign="top">

### 🧠 Approach
Behavior + assessments → model

<img src="https://img.shields.io/badge/Approach-Feature%20Engineering-7C3AED?style=for-the-badge"/>

</td>
<td width="33%" align="center" valign="top">

### 🚀 Output
Actionable intervention signals

<img src="https://img.shields.io/badge/Output-Insights%20for%20Interventions-16A34A?style=for-the-badge"/>

</td>
</tr>
</table>

</div>

<details open>
<summary><b>🔍 What insights can you extract? (click to expand)</b></summary>
<br/>

- Engagement decay (drop in activity over time)
- Late/early submission patterns
- Consistency of study (regularity vs bursts)
- Module-level differences (presentation effects)
- Segments of “quiet risk” students (low activity, not yet failing)

</details>

---

## ✅ Recruiter Snapshot

<table>
<tr>
<td width="50%" valign="top">

## 🎯 Why This Project Matters

<div align="center">

<table>
<tr>
<td width="33%" align="center" valign="top">

### 🧠 Technical Depth

- End-to-end ML pipeline design  
- Time-aware feature engineering  
- Proper validation & leakage control  
- Imbalanced classification handling  
- Metric-driven evaluation (F1 / ROC-AUC)

<img src="https://img.shields.io/badge/Signal-ML%20Engineering%20Maturity-0EA5E9?style=for-the-badge"/>

</td>

<td width="33%" align="center" valign="top">

### 🔎 Analytical Thinking

- Behavioral pattern extraction  
- Temporal engagement modeling  
- Risk segmentation logic  
- Feature importance interpretation  
- Error analysis mindset

<img src="https://img.shields.io/badge/Signal-Analytical%20Rigor-7C3AED?style=for-the-badge"/>

</td>

<td width="33%" align="center" valign="top">

### 🚀 Real-World Impact

- Early student risk detection  
- Data-driven intervention signals  
- Retention strategy support  
- Decision-enabling insights  
- EdTech personalization potential

<img src="https://img.shields.io/badge/Signal-Actionable%20Insights-16A34A?style=for-the-badge"/>

</td>
</tr>
</table>

</div>

---

### 📌 What a Recruiter Sees

- Not just a model — a **complete decision-support system**
- Clear separation between data, modeling, and impact
- Business-oriented ML thinking
- Portfolio-level documentation quality
- Insight-first approach, not metric-only obsession
---

## 🤝 Contact

<div align="center">

<a href="https://www.linkedin.com/in/navyashree-byregowda-472821196/">
  <img src="https://img.shields.io/badge/LinkedIn-Connect-1E40AF?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

<a href="https://github.com/Navyagowda2714">
  <img src="https://img.shields.io/badge/GitHub-Portfolio-111827?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<a href="mailto:navyashreebyregowda@gmail.com">
  <img src="https://img.shields.io/badge/Email-Let's%20Talk-DC2626?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>

<br/><br/>
<sub>OULAD Learning Analytics — built to demonstrate ML + insight-driven decision thinking.</sub>

</div>
