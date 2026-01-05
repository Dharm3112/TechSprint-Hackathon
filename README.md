# Customer Complaint Resolver AI Agent

> **Enterprise-Grade AI Agent for Automated Complaint Resolution using Google Gemini & ADK**

## 🚀 Overview
The **Customer Complaint Resolver** is an intelligent, multi-agent system designed to handle complex customer service workflows. It uses a swarm of specialized agents to categorize, prioritize, and resolve complaints with human-level reasoning and self-correcting capabilities.

Built for the **TechSprint Hackathon**, this solution demonstrates:
- **Multi-Agent Orchestration**: Specialized agents for Classification, Sentiment, Risk Assessment, Decision Making, and Drafting.
- **Adaptive Reasoning**: Self-correction loops to refine responses based on confidence scores.
- **Memory & RAG**: Vector-based memory (using local JSON store + Gemini Embeddings) to recall similar past cases.
- **Enterprise Readiness**: Structured data models (Pydantic), API-driven architecture, and scalable design.

## 🏗️ Architecture
The system follows a pipeline architecture orchestrated by a `CoordinatorAgent`:

1.  **Input Processing**: Customer complaint is ingested.
2.  **Memory Recall**: Agent checks for similar resolved cases.
3.  **Parallel Analysis**:
    *   `ClassificationAgent`: Identifies Intent & Category.
    *   `SentimentAgent`: Assess Urgency & Sentiment Score.
4.  **Prioritization**: `PrioritizationAgent` assigns a Risk Level & Priority Score.
5.  **Decision Making**: `DecisionAgent` determines the next action (Reply, Escalate, Refund).
6.  **Drafting**: `ResponseDraftingAgent` creates a context-aware response.
7.  **Self-Correction**: System evaluates draft confidence; flags for human review if low.
8.  **Resolution**: Ticket is saved to memory for future learning.

## 🛠️ Tech Stack
-   **Orchestration**: Python-based Custom Coordinator (Simulating ADK patterns)
-   **LLM**: Google Gemini 1.5 Flash (`google-generativeai`)
-   **Embeddings**: Gemini Text Embedding 004
-   **Memory**: Lightweight Vector Store (NumPy + JSON)
-   **Data Validation**: Pydantic

## 📂 Structure
```
├── agents/             # Specialized Agent Definitions
│   ├── base_agent.py   # Gemini Wrapper
│   ├── classification_agent.py
│   ├── sentiment_agent.py
│   ├── prioritization_agent.py
│   ├── decision_agent.py
│   └── response_agent.py
├── memory/             # Vector Database Logic
│   └── vector_db.py
├── models.py           # Pydantic Data Models
├── coordinator.py      # Main Orchestrator
├── main.py             # Demo Entry Point
└── config.py           # Configuration
```

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment:
    Create `.env` file and add:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

### Run Demo
```bash
python main.py
```

## 🔮 Future Enhancements
-   **Voice Interface**: Integrate Gemini Multimodal capabilities for audio complaints.
-   **CRM Integration**: Connect to Salesforce/Zendesk APIs.
-   **Real-time Dashboard**: Streamlit UI for monitoring agent decisions.
