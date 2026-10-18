# GraphHire 🎯
### Connecting Student Skills to Career Opportunities

GraphHire is a graph-powered career recommendation platform that helps students and fresh graduates discover suitable jobs, identify missing skills, and find relevant learning resources.

## 🚀 Problem Statement

Students often struggle to understand which jobs match their current skills and what they need to learn to become job-ready. GraphHire connects skills, students, jobs, and courses to make career planning easier.

## 💡 Our Solution

GraphHire uses a knowledge graph powered by **FalkorDB** to connect student skills with job requirements and learning resources. It helps users explore career opportunities and identify skill gaps.

### ✨ Key Features

- 🎓 Student-focused career recommendations
- 💼 Job matching based on skills
- 🧠 Knowledge graph connecting skills, jobs, and courses
- 📚 Learning resource suggestions
- 📈 Skill-gap identification
- 🖥️ Interactive web interface built with Streamlit

## 🛠️ Tech Stack

- **Python** — application logic
- **Streamlit** — user interface
- **FalkorDB** — graph database
- **Cypher** — graph queries
- **python-dotenv** — environment configuration

## 🏗️ Project Structure

```text
graphhire-ai/
├── app.py
├── graph_engine.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd graphhire-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using `.env.example` as a template. Configure your FalkorDB connection details there.

Never commit passwords, API keys, or other secrets to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## 🌐 Deployment

The application can be deployed using Streamlit Community Cloud. Configure the required FalkorDB connection variables in the deployment's secrets settings and ensure the database is reachable from the hosted app.

## 🎯 Target Users

- College students
- Fresh graduates
- Job seekers
- Learners preparing for industry roles

## 🌟 Project Vision

Our goal is to make career planning more accessible by connecting education, skills, and employment through graph-powered recommendations.

## 👥 Built For

A student-focused hackathon project exploring graph technology for education and career discovery.
