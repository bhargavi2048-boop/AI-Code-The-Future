<div align="center">

<br/>

```
██████╗ ███████╗███████╗██╗   ██╗███╗   ███╗███████╗
██╔══██╗██╔════╝██╔════╝██║   ██║████╗ ████║██╔════╝
██████╔╝█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
██╔══██╗██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
██║  ██║███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
         A N A L Y Z E R   P R O
```

**AI-powered resume analysis that helps you land the job.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![spaCy](https://img.shields.io/badge/spaCy-3.7.2-09A3D5?style=flat-square&logo=spacy&logoColor=white)](https://spacy.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Demo](https://img.shields.io/badge/Watch-Demo-FF4444?style=flat-square&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1Dm3n3Np5PFrVkeiiBwUySND_Xs8KwPxw/view?usp=sharing)

<br/>


Demo Video: "https://drive.google.com/file/d/1Dm3n3Np5PFrVkeiiBwUySND_Xs8KwPxw/view?usp=sharing"


</div>

---

## What is Resume Analyzer Pro?

Resume Analyzer Pro is a full-stack web application that uses NLP and custom AI algorithms to evaluate resumes, score them against industry criteria, and give job seekers clear, prioritized steps to improve. Upload a PDF, optionally paste a job description, and get a detailed breakdown in seconds.

> Built for the **Code the Future: AI Edition** challenge.

---

## Features

### Resume Analysis
- Extracts and parses text directly from PDF resumes
- Identifies and categorizes skills automatically using spaCy NLP
- Evaluates project descriptions for action language, tech keywords, and impact statements
- Scores the full resume out of 10 across four weighted dimensions

### Job Description Alignment
- Compares your resume against any job description you paste in
- Shows exactly which required skills you have and which are missing
- Outputs an alignment score so you can track progress

### AI Recommendations
- Generates a professional summary tailored to your resume content
- Provides prioritized improvement suggestions (High / Medium / Low)
- Interactive task checklist that updates your score in real time as you complete items

### Interface
- Drag-and-drop PDF upload
- Clean teal-blue responsive UI (Bootstrap 5)
- Multi-step navigation: Upload → Analyze → Compare → Improve
- Real-time score updates without page reloads

---

## Scoring Breakdown

| Component | Max Points | What's Evaluated |
|---|---|---|
| Skills Coverage | 3 | Breadth and relevance of identified skills |
| Project Quality | 3 | Action verbs, technologies mentioned, measurable impact |
| Resume Length | 2 | Word count relative to completeness targets |
| Formatting | 2 | Sections present, bullet point usage, readability signals |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8+, Flask 2.3.3 |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| PDF Processing | PyMuPDF (`fitz`) |
| NLP | spaCy 3.7.2, NLTK 3.8.1 |
| Icons | Font Awesome 6 |

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip`
- A virtual environment (recommended)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/bhargavi2048-boop/resume-analyzer-pro.git
cd resume-analyzer-pro

# 2. Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the spaCy language model
python -m spacy download en_core_web_sm

# 5. Start the app
python app.py
```

Then open **http://localhost:5000** in your browser.

### Dependencies (`requirements.txt`)

```text
flask==2.3.3
pymupdf==1.23.8
spacy==3.7.2
nltk==3.8.1
```

---

## How It Works

```
Upload PDF  →  Text Extraction (PyMuPDF)
                    ↓
           NLP Processing (spaCy)
           ├── Skill identification
           ├── Project quality scoring
           └── Resume length + formatting checks
                    ↓
           Score Calculation (out of 10)
                    ↓
    ┌───────────────┴───────────────┐
    │                               │
    ↓                               ↓
Summary & Recommendations    Job Description Comparison
(AI-generated, priority-tagged)  (alignment score, gap analysis)
```

---

## User Flow

1. **Upload** — Drag and drop your PDF resume. Optionally add a job title and description.
2. **Analyze** — The app extracts text, runs NLP, and calculates your score.
3. **Review** — See your skill tags, project assessment cards, overall score, and AI-generated summary.
4. **Compare** (optional) — Paste a job description to get a match score and skill gap report.
5. **Improve** — Work through the prioritized checklist and watch your score update live.

---

## Security

- Server-side file validation and sanitization
- Session-based storage — no data persists between sessions
- Automatic file cleanup after analysis completes
- 16 MB file size limit enforced at upload

---

## Roadmap

- [ ] Multi-language resume support
- [ ] Export analysis report as PDF
- [ ] User accounts with saved history
- [ ] Bulk resume analysis (batch mode)
- [ ] Industry-specific keyword databases
- [ ] Job board integrations (LinkedIn, Indeed)
- [ ] REST API for third-party developers
- [ ] Mobile app (iOS / Android)

---

## Contributing

Contributions are welcome.

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add your feature"
git push origin feature/your-feature-name
# Open a Pull Request
```

Please keep PRs focused — one feature or fix per PR makes review faster.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contact

**Bhargavi N**

[![Email](https://img.shields.io/badge/Email-bhargavi2048%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:bhargavi2048@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Bhargavi_Nagaraj-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bhargavi-nagaraj-967811381)
[![GitHub](https://img.shields.io/badge/GitHub-bhargavi2048--boop-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/bhargavi2048-boop)

---

<div align="center">

Made with care by Bhargavi N · © 2026 Resume Analyzer Pro

</div>
