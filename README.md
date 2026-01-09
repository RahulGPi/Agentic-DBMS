<p align="center">
  <img src="https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Ollama-Qwen_2.5-FF6F00?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/Tailwind_CSS-4.1-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
</p>

<h1 align="center">🎙️ Agentic DBMS</h1>

<h3 align="center">Voice-Activated & Visual Database Management System</h3>

<p align="center">
  <em>Build, modify, and query complex schemas without writing a single line of SQL.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/Made%20with-❤️-red.svg?style=flat-square" alt="Made with Love">
</p>

---

## 📖 Overview

**Agentic DBMS** is a cutting-edge, hybrid platform designed to revolutionize how developers and data analysts interact with relational databases. It bridges the gap between intuitive **visual design** and powerful, **natural language-driven** database management.

This project leverages the power of **local AI models** (Ollama running Qwen 2.5 Coder 3B) to ensure **data privacy** and **offline capability**, making it a secure and robust solution for modern development environments.

> 💡 **Why Agentic DBMS?**  
> Traditional database management requires SQL expertise. Agentic DBMS democratizes database interaction—speak your queries, design visually, and let AI handle the complexity.

---

## ✨ Key Features

### 🎨 No-Code Visual Schema Designer

| Feature | Description |
|---------|-------------|
| **Interactive Canvas** | Create tables, define columns, and manage data types using a drag-and-drop interface powered by React Flow concepts |
| **Dynamic Relationships** | Visualize Foreign Key constraints with auto-routing Bezier curves—*Cyan* for cross-table, *Emerald* for self-referencing links |
| **Smart Layouts** | Built-in collision detection ensures your entity-relationship diagram remains clean and organized |

### 🤖 AI-Powered SQL Agent (Local LLM)

| Feature | Description |
|---------|-------------|
| **Natural Language Querying** | Chat with your database in plain English (e.g., *"Show me the top 5 customers by sales volume"*) |
| **RAG Architecture** | Uses Retrieval-Augmented Generation to inject your live database schema (DDL) into the LLM context, virtually eliminating hallucinations |
| **Data Privacy First** | Powered by a locally hosted Ollama instance. **No data leaves your machine** |

### 🎤 Voice Interaction

Hands-free operation using the browser's **Web Speech API**. Speak your commands, and watch the agent execute complex SQL operations instantly.

### 🔄 Autonomic Repair Loop

A self-healing mechanism that intercepts SQL execution errors from the backend. The error and the failed query are fed back to the AI agent to **recursively correct** syntax or logical errors without user intervention.

### ⚡ Real-time Synchronization

Changes made in the Visual Designer are **immediately reflected** in the PostgreSQL database, and vice versa. True bi-directional sync.

---

## 🏗️ System Architecture

The system follows a modern, decoupled **client-server architecture**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │ Visual Canvas   │  │  Chat Interface │  │ Voice Processor │         │
│  │   (React Flow)  │  │   (AI Agent)    │  │ (Web Speech API)│         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
│           │                    │                    │                   │
│           └────────────────────┴────────────────────┘                   │
│                                │                                        │
│                    React.js + Tailwind CSS + Lucide React               │
└────────────────────────────────┼────────────────────────────────────────┘
                                 │ REST API
                                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      FastAPI Server                              │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐   │   │
│  │  │ DB Manager  │  │ LLM Service  │  │ Autonomic Repair Loop │   │   │
│  │  │ (psycopg)   │  │   (Ollama)   │  │   (Self-Healing)      │   │   │
│  │  └──────┬──────┘  └──────┬───────┘  └───────────────────────┘   │   │
│  └─────────┼────────────────┼──────────────────────────────────────┘   │
└────────────┼────────────────┼──────────────────────────────────────────┘
             │                │
             ▼                ▼
┌────────────────────┐  ┌────────────────────────────────────────────────┐
│    PostgreSQL      │  │              Ollama (Local LLM)                │
│    Database        │  │         Qwen 2.5 Coder 3B Model               │
│                    │  │              localhost:11434                   │
└────────────────────┘  └────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 19.2, Tailwind CSS 4.1, Lucide React | UI, styling, and icons |
| **Backend** | Python, FastAPI | REST API, business logic |
| **Database** | PostgreSQL | Data persistence |
| **AI Engine** | Ollama + Qwen 2.5 Coder 3B | Natural language processing |
| **Build Tool** | Vite 7.2 | Frontend bundling & HMR |

---

## 🚀 Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

Ensure you have the following installed:

- **Node.js** (v18+) & npm
- **Python** (v3.10+)
- **PostgreSQL** (Local installation or Docker container)
- **Ollama** ([Download Ollama](https://ollama.com/download))

---

### Step 1: Setup Local LLM (Ollama)

Ensure Ollama is installed and pull the required model:

```bash
# Pull the Qwen 2.5 Coder 3B model
ollama pull qwen2.5-coder:3b

# Start the Ollama server (usually runs on port 11434)
ollama serve
```

> 📝 **Note:** Keep this terminal window open. The Ollama server must be running for the AI features to work.

---

### Step 2: Backend Setup

Navigate to the backend directory and set up the Python environment:

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configuration

Create a `.env` file in the `backend` directory:

```env
# Database Connection String
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/your_db_name

# Ollama API URL (Default)
OLLAMA_BASE_URL=http://localhost:11434/v1
```

#### Run the Server

```bash
uvicorn main:app --reload --port 8000
```

✅ Backend is now running at `http://localhost:8000`

---

### Step 3: Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend

# Install Node modules
npm install
```

#### Configuration

Create a `.env` file in the `frontend` directory:

```env
# Point to your FastAPI backend
VITE_API_BASE=http://localhost:8000
```

#### Run the Development Server

```bash
npm run dev
```

✅ Frontend is now running. Open your browser to `http://localhost:5173`

---

## 🖥️ Usage Guide

### 📐 Visual Design Mode

1. Navigate to the **"Design"** tab
2. Drag tables onto the canvas
3. Click **"Add Column"** to define schema attributes
4. Drag from one column to another to create **Foreign Key relationships**
5. Watch your ERD auto-organize with collision detection!

### 💬 AI Chat Mode

1. Switch to the **"Agent"** tab
2. Type or speak a command:
   - *"Create a users table with id, name, and email"*
   - *"Show me all orders from last month"*
   - *"Add a foreign key from orders to customers"*
3. The agent generates and executes SQL automatically

### 🎤 Voice Mode

1. Click the **microphone icon** in the chat input
2. Speak your query clearly
3. Watch the system:
   - Transcribe your voice → Generate SQL → Execute on database
   - All in real-time! 🚀

---

## 📁 Project Structure

```
MiniProject/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # PostgreSQL connection & operations
│   ├── llm_service.py       # Ollama LLM integration
│   ├── requirements.txt     # Python dependencies
│   └── docker-compose.yml   # PostgreSQL Docker configuration
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Component styles
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # React entry point
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
│
├── Pg_data/                 # PostgreSQL data volume
└── README.md                # This file!
```

---

## 🔧 Configuration Reference

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | *Required* |
| `OLLAMA_BASE_URL` | Ollama API endpoint | `http://localhost:11434/v1` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE` | FastAPI backend URL | `http://localhost:8000` |

---

## 🐳 Docker Support

For PostgreSQL, you can use the included `docker-compose.yml`:

```bash
cd backend
docker-compose up -d
```

This will spin up a PostgreSQL container with persistent data storage.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👥 Contributors

<table>
  <tr>
    <td align="center">
      <strong>Rahul Girish Pai</strong><br>
      <sub>4SF23CI116</sub>
    </td>
    <td align="center">
      <strong>Vineeth KHM</strong><br>
      <sub>4SF23CI067</sub>
    </td>
    <td align="center">
      <strong>Goutham Nayak</strong><br>
      <sub>4SF24CI403</sub>
    </td>
    <td align="center">
      <strong>Chirag Shetty</strong><br>
      <sub>4SF23CI045</sub>
    </td>
  </tr>
</table>

### 🎓 Guidance

This project was developed under the guidance of **Mrs. Chaithrika Aditya**, Assistant Professor, Dept. of CSE (AI&ML), Sahyadri College of Engineering & Management, Mangaluru.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If you found this project interesting or helpful, please give it a ⭐ on GitHub!

---

<p align="center">
  <em>Built with ❤️ by the Agentic DBMS Team</em>
</p>
