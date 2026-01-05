# ⚡ NOVUS: ADK-Powered Autonomous Resolution Engine

![ADK](https://img.shields.io/badge/Agent_Development_Kit-Enabled-blue?style=for-the-badge&logo=google)
![AI Model](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange?style=for-the-badge&logo=google)
![Architecture](https://img.shields.io/badge/Architecture-Declarative_Swarm-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)

> **The Next Generation of Enterprise Support: Built 100% on the Agent Development Kit (ADK).**

---

## 🧠 The Concept
**NOVUS** is a deterministic, multi-agent orchestration system built entirely using the **Agent Development Kit (ADK)** framework. 

By leveraging the power of ADK's declarative nature, NOVUS moves beyond fragile code-based orchestration. Instead, it defines behaviors, instructions, and tools in structured configuration files (`root_agent.yaml`), allowing for a rapidly scalable "Swarm Architecture." Specialized agents collaborate, critique, and refine outcomes before ever interacting with a customer.

---

## 🌟 Key Differentiators

### 🛡️ ADK-Native "Critic Loop"
Using ADK's sub-agent capabilities, we implemented a dedicated **Critic Agent** guardrail.
* **Workflow:** The `Drafter` agent outputs a response, which is immediately routed to the `Critic` agent.
* **Logic:** The Critic evaluates the draft against the computed **Risk Score**.
* **Self-Correction:** If the tone is mismatched (e.g., too casual for a legal threat), the Critic rejects the output and instructs the swarm to retry.
* *Result:* Zero "hallucinations" or tone-deaf replies.

### 🧩 Declarative Agent Definitions
Unlike traditional implementations where agent logic is buried in Python scripts, NOVUS defines its brain in **YAML**.
* **Modularity:** New agents can be added by simply appending to `sub_agents` in the configuration.
* **Transparency:** The prompt engineering and instructions are decoupled from the execution logic.

### 🧠 Semantic Memory Integration
Integrated directly into the ADK flow, NOVUS utilizes **Vector Embeddings** to recall historical resolutions.
* *Recurring Issue Detection:* "This complaint matches the pattern of the Server Outage from last Tuesday."
* *Consistency:* Ensures uniform policy enforcement across thousands of tickets.

---

## 🏗️ ADK Architecture

The system follows a **Hierarchical Swarm Pattern** orchestrated by the ADK Runtime.

```mermaid
graph TD
    User[User Input] -->|ADK Runtime| Root[Root Agent (sdd)]
    Root -->|Delegation| Class[Classification Agent]
    Root -->|Delegation| Prio[Prioritization Agent]
    Root -->|Delegation| Draft[Response Agent]
    Draft -->|Draft Text| Critic[🕵️ Critic Agent]
    Critic -->|Reject| Draft
    Critic -->|Approve| Root
    Root -->|Final Output| User

```

---

## 🤖 The Swarm Configuration

Agents are defined declaratively in `Novus/root_agent.yaml`, ensuring strict adherence to the **LlmAgent** class structure.

| Agent | Type | Role |
| --- | --- | --- |
| **Root (sdd)** | `LlmAgent` | The Orchestrator. Managed by ADK to coordinate the sub-agent pipeline. |
| **Classification** | `LlmAgent` | Identifies Intent (e.g., "Refund") and Business Category. |
| **Prioritization** | `LlmAgent` | Computes the `Risk Score` (0-100) based on sentiment and keywords. |
| **Decision** | `LlmAgent` | Determines the *Next Best Action* (Reply, Escalate, Refund). |
| **Critic** | `LlmAgent` | **The Gatekeeper.** Reviews drafts for empathy and safety. |

---

## 🛠️ Technical Stack

* **Framework:** **Agent Development Kit (ADK)**
* **Model:** Google Gemini 2.5 Flash
* **Configuration:** YAML-based Agent Definitions
* **Runtime:** Python 3.10+
* **Memory:** Local Vector Store (ADK Session Integration)

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* Agent Development Kit installed
* Google Gemini API Key

### Installation

1. **Clone the Repository**
```bash
git clone [https://github.com/dharm3112/techsprint-hackathon.git](https://github.com/dharm3112/techsprint-hackathon.git)
cd techsprint-hackathon

```


2. **Install Dependencies**
```bash
pip install -r requirements.txt

```


3. **Configure Environment**
Create a `.env` file in the root directory:
```ini
GEMINI_API_KEY="your_google_api_key_here"

```



### Running the ADK Agent

Initialize the ADK runtime to start the agent swarm.

```bash
# Run the demo script which initializes the ADK coordinator
python main.py

```

---

## 📂 Project Structure

The project adheres to the strict ADK directory structure:

```text
/
├── Novus/                  # 📦 ADK Project Root
│   ├── root_agent.yaml     # ⚙️ Master Agent Configuration
│   ├── critic.py           # Custom Tool/Agent Logic
│   ├── response_agent.py   # Drafting Logic
│   └── .adk/               # ADK Session Data
├── agents/                 # Specialized Tool Definitions
├── memory/                 # Vector Database Implementation
├── main.py                 # ADK Runtime Entry Point
└── requirements.txt        # Dependencies

```

### Agent Configuration Snippet (`root_agent.yaml`)

```yaml
name: sdd
model: gemini-2.5-flash
agent_class: LlmAgent
instruction: You are the root agent that coordinates other agents.
sub_agents: 
  - classification_agent
  - prioritization_agent
  - critic_agent

```

---

## 🔮 Future Roadmap

* [ ] **ADK Web UI:** Integrate with the ADK visualization dashboard for real-time trace monitoring.
* [ ] **Multimodal Inputs:** Enable image/audio processing via Gemini 2.5 Flash within the ADK pipeline.
* [ ] **Enterprise Connectors:** Add Salesforce/Zendesk tools to the agent configuration.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
Built with ❤️ using the <b>Agent Development Kit</b> for the TechSprint Hackathon
</p>

```

```
