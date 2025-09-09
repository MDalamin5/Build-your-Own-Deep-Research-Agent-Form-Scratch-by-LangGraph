# Deep Research API Documentation

**Version:** 2.0.0
**Base URL:** `http://localhost:8000`

---

## 📖 Introduction

The **Deep Research API** is a conversational research framework built with **FastAPI** and **LangGraph**. It enables stateful, multi-turn research interactions where users can:

* Start a research request
* Engage in back-and-forth clarification
* Receive a structured, final research report

The system supports **persistent memory** using a checkpointing mechanism, making it ideal for complex research tasks requiring context.

---

## ✨ Features

* **Stateful Conversations** – Thread-based memory for multi-turn research.
* **Multi-Agent Supervision** – Modular design with supervisor agents.
* **Dynamic Scoping** – Automatically scopes research briefs before execution.
* **Structured Output** – Delivers final research in clear, report-style responses.
* **FastAPI Integration** – Easy to deploy, scale, and test with built-in Swagger UI.

---

## 📂 Directory Structure

```
gtr_deep_research/
├── .env
├── requirements.txt
├── main.py
├── multi_agent_supervisro.py
├── prompts.py
├── research_agent_full.py
├── research_agent_scope.py
├── research_agent.py
├── schemas.py
├── state_multi_agent_supervisro.py
├── state_research.py
├── state_scope.py
├── utils.py
```

---

## ⚙️ Setup Guide

### 1. Prerequisites

* Python 3.9+
* Virtual environment tool (`venv` or `conda`)
* FastAPI & Uvicorn

### 2. Installation

```bash
# Clone repository
git clone <your-repo-url>
cd gtr_deep_research

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory and configure required settings (e.g., database URL, API keys if added later).

Example:

```
APP_ENV=development
DEBUG=True
```

---

## 🚀 Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Access interactive API docs at:

* Swagger UI → `http://localhost:8000/docs`
* ReDoc → `http://localhost:8000/redoc`

---

## 🔗 API Endpoints

### 1. **Health Check**

`GET /health`

**Response**

```json
{
  "status": "I'm alive."
}
```

---

### 2. **Conduct Research**

`POST /research`

**Request Body**

```json
{
  "user_id": "string",
  "thread_id": "string (optional)",
  "content": "string"
}
```

**Response Body (200 OK)**

```json
{
  "thread_id": "string",
  "response_messages": [
    {
      "type": "string",
      "content": "string"
    }
  ],
  "is_final": true
}
```

**Example (Start New Research)**

```bash
curl -X POST "http://localhost:8000/research" \
-H "Content-Type: application/json" \
-d '{
    "user_id": "user_abc_123",
    "content": "Tell me about the future of multi-agent AI systems."
}'
```

---

### 3. **Check Thread State**

`POST /checkpointer_thread`

**Request Body**

```json
{
  "thread_id": "string"
}
```

**Response Body (200 OK)**

```json
{
  "thread_id": "string",
  "state": {
    "messages": [],
    "research_brief": "...",
    "supervisor_messages": [],
    "notes": [],
    "raw_notes": [],
    "research_iterations": 0
  }
}
```

---

## 📚 Example Workflows

### Case 1: Extract Top Software Companies in Bangladesh

**User Query:**

> Extract top software companies in Bangladesh including company name, location, CEO info, social media links, and other details.

**Agent Clarification:**

> I understand that you want to extract information about the top software companies in Bangladesh. This includes company names, locations, chairman or CEO information, social media links, and any other relevant data. Is this accurate, and should I proceed?

**Final Response:**

> Proceeds with generating structured research brief without further clarification.

---

### Case 2: HRM Software Market in Bangladesh

**User Query:**

> Evaluate the HRM software market in Bangladesh, focusing on leading solutions, adoption trends, compliance, and recommendations for GTR.

**Agent Clarification:**

> I understand your request and will analyze the HRM software market in Bangladesh, comparing local and global solutions, and provide a detailed assessment of GTR's current position.

**Final Response:**
Delivered structured report:

* Overview of HRM adoption
* AI adoption trends in HRM
* Leading HRM platforms (HR Sheba, PeopleDesk, PiHR, GTR)
* Limitations & Gaps
* Conclusion & Recommendations

---

## ⚠️ Error Handling

| HTTP Code                 | Description                       |
| ------------------------- | --------------------------------- |
| 200 OK                    | Request successful                |
| 404 Not Found             | Thread not found or state missing |
| 422 Unprocessable Entity  | Invalid request body              |
| 500 Internal Server Error | Unexpected server error           |

---

## 🧪 Testing

Run tests with cURL/Postman:

```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Start research
curl -X POST "http://localhost:8000/research" \
-H "Content-Type: application/json" \
-d '{"user_id": "test_user", "content": "Research AI adoption in HRM software"}'
```

Expected output includes:

* `thread_id` for conversation tracking
* `response_messages` array with agent’s response
* `is_final` flag for final reports

---

## 📌 Next Steps

* Add API authentication (API key / OAuth2)
* Add persistence layer (database-backed checkpointer)
* Expand test suite with automated unit tests

---
