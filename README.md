# 🚀 Signals from Students

> A data pipeline to surface innovation signals from student-led projects across universities — starting with Devpost.

![Badge: ML/NLP Ready](https://img.shields.io/badge/status-NLP%20Ready-blue)
![Badge: Internship Ready](https://img.shields.io/badge/portfolio-Internship%20Showcase-green)
![Badge: Devpost](https://img.shields.io/badge/source-Devpost-informational)

---

## 🧠 What is this project?

**Signals from Students** is a pipeline that scrapes, enriches, and analyzes student-led technical projects from hackathons and competitions — starting with Devpost. It aims to identify early signals of **technical trends**, **tool adoption**, and **research interests** emerging from universities worldwide.

This project reflects my interest in **machine learning, open data, and platform intelligence** — and is a demonstration of my engineering abilities across **web scraping, data cleaning, and NLP-driven analysis**.

---

## 📊 What kind of data do we extract?

We scraped **288+ Devpost projects** and enriched them with metadata that helps us infer innovation signals:

| Column Name           | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `title`               | Project title                                                               |
| `url`                 | Project URL on Devpost                                                      |
| `short_description`   | Meta description (used as high-level summary)                               |
| `submitted_to`        | The hackathon or competition the project was submitted to                  |
| `built_with`          | List of technologies (cleaned + normalized)                                 |
| `inspiration`         | Short paragraph on what inspired the project                                |
| `what_it_does`        | Plaintext description of functionality                                      |
| `how_we_built_it`     | Tools, APIs, libraries used                                                 |
| `host_institution`    | Institution that hosted the hackathon                                       |
| `project_date`        | Project submission date (MM/DD/YYYY)                                        |
| `signal_.*`           | (Added in `devpost_cleaner`) Binary or normalized features for downstream analysis |

---

## 🧱 Architecture

signals-from-students/
│
├── scrapers/ ← Devpost scraping + enrichment logic
│ ├── devpost_scraper.py # Scrapes titles, summaries, URLs
│ └── devpost_enricher.py # Adds deeper fields like institution, description, stack
│
├── data/ ← Cleaned & enriched datasets
│ ├── devpost_projects.csv # Raw scrape
│ ├── devpost_projects_enriched.csv # With host institution, descriptions, etc.
│ └── devpost_projects_cleaned.csv # Fully cleaned and signal-tagged
│
├── notebooks/ ← Will be used for EDA + NLP signal modeling
│
├── app/ ← (Reserved) Dashboard/Streamlit app folder
│
├── devpost_cleaner.py # Data normalization and signal creation logic
├── requirements.txt # Environment dependencies
├── README.md # You're reading this!


---

## 🧠 Why I Built This

- 🔭 To explore how student-led hackathon projects can reveal **early indicators** of technical innovation
- 🛠️ To showcase my skills in **data engineering**, **Selenium scraping**, and **pipeline design**
- 🎯 To use this as a foundation for **NLP-based trend detection** and **university innovation mapping**
- 🎓 To better understand what tech stacks are favored by early-stage builders

---

## 🛠️ Skills + Tools Demonstrated

| Category               | Tools / Frameworks                                       |
|------------------------|----------------------------------------------------------|
| Web Scraping           | `Selenium`, `requests`, `re`, `tqdm`                     |
| Data Engineering       | `pandas`, feature normalization, tag cleaning            |
| NLP Preprocessing      | Custom text fields (`inspiration`, `what_it_does`, etc) |
| Automation             | Modular scraping and enrichment scripts                  |
| Project Structuring    | GitHub-ready repo layout, CLI-ready scripts              |

---

## ✅ Example Use Cases

- 📡 Identify early adoption of APIs (e.g., `Twilio`, `GCP`, `OpenAI`) in student projects
- 🔬 Research student-led tech trends across regions or universities
- 🧬 Build ML models to predict innovation hotbeds by school or year
- 📈 Visualize how toolkits (e.g., `LangChain`, `Flutter`, `HuggingFace`) enter student ecosystems

---

## 🔮 Next Steps

- [ ] 🧠 NLP modeling: Topic modeling & embeddings for project summaries
- [ ] 🗺️ University mapping: Group signals by geography and institution type
- [ ] 📊 Trend dashboard: Streamlit app to track tech adoption & project clusters
- [ ] 🔌 Add new sources: GitHub stars + Google Scholar + Student startup databases

---

## 🧑‍💻 About Me

I’m a **rising sophomore at the University of Illinois Urbana-Champaign**, majoring in Data Science + Info Sciences. I built this project to show that innovation signals can come from the student level — and to apply my ML/data skills to a problem I care about.

You can view more of my work [on GitHub](https://github.com/RajnandiniSen) or connect with me on [LinkedIn](https://linkedin.com/in/rajnandinisen).

---

## 📦 Setup

```bash
git clone https://github.com/RajnandiniSen/signals-from-students
cd signals-from-students
pip install -r requirements.txt

# Step 1: Run scraper
python scrapers/devpost_scraper.py

# Step 2: Enrich data
python scrapers/devpost_enricher.py

# Step 3: Clean and extract signals
python data/devpost_cleaner.py

---
