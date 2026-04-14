# MSFoundryReasoningModel 🧠

[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI%20Foundry-0078D4?style=flat&logo=microsoft-azure&logoColor=white)](https://ai.azure.com)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-R1%20%7C%20V3-4A90D9?style=flat)](https://azure.microsoft.com/en-us/blog/deepseek-r1-is-now-available-on-azure-ai-foundry/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)


> Part of the **Microsoft Foundry Open-Source Series** — production-ready reference implementations for Microsoft Foundry.


## Overview

**MSFoundryReasoningModel** demonstrates how to integrate and invoke **DeepSeek reasoning models** (R1, V3) via **Microsoft Foundry** using the Python SDK. It covers how to configure the client, send prompts to a reasoning-capable model, parse the structured `<think>` / answer output, and surface both the chain-of-thought reasoning trace and the final response to downstream consumers.

Reasoning models differ from standard LLMs in a fundamental way: they expose an internal deliberation process before committing to an answer. This repo shows you how to capture and use that reasoning trace in production workloads — not just discard it.

### Why Reasoning Models?

| Capability | Standard LLM | Reasoning Model |
|---|---|---|
| Complex multi-step logic | Limited | ✅ Native |
| Mathematical problem solving | Moderate | ✅ High accuracy |
| Chain-of-thought transparency | Prompt engineering required | ✅ Built-in `<think>` block |
| Self-correction before answering | No | ✅ Yes |
| Enterprise audit / explainability | Hard | ✅ Reasoning trace available |

---

## Repository Structure

```
MSFoundryReasoningModel/
├── deepseek_reasoning_model.py   # Core reasoning model invocation patterns
├── .env                          # Environment configuration (not committed)
├── .pkvenv/                      # Virtual environment (local only)
└── README.md
```

---

## Prerequisites

- Python 3.11+
- Azure subscription with **Microsoft Foundry** project
- DeepSeek R1 or V3 model deployed via Microsoft Foundry model catalogue
- `azure-ai-inference` SDK (`>=1.0.0b9`)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/praveen11singh/MSFoundryReasoningModel.git
cd MSFoundryReasoningModel
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install azure-ai-inference azure-identity python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
AZURE_AI_FOUNDRY_ENDPOINT=https://<your-project>.services.ai.azure.com
AZURE_AI_FOUNDRY_API_KEY=<your-api-key>
AZURE_DEPLOYMENT_NAME=deepseek-r1          # or deepseek-v3
```

> **Production note:** For enterprise workloads, prefer `DefaultAzureCredential` over API keys. See the authentication section below.

### 5. Run the example

```bash
python deepseek_reasoning_model.py
```

---

## Core Pattern

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_AI_FOUNDRY_API_KEY"]),
)

response = client.complete(
    model=os.environ["AZURE_DEPLOYMENT_NAME"],
    messages=[
        SystemMessage(content="You are a helpful AI assistant."),
        UserMessage(content="Solve: If a train travels 120 km in 1.5 hours, what is its average speed?"),
    ],
)

# DeepSeek R1 separates reasoning from the final answer
message = response.choices[0].message
print("Reasoning trace:", getattr(message, "reasoning_content", None))
print("Final answer:   ", message.content)
```

---

## Reasoning Trace Handling

DeepSeek R1 returns two distinct fields on the response message:

| Field | Description |
|---|---|
| `message.reasoning_content` | The model's internal chain-of-thought (may be `None` for V3) |
| `message.content` | The final answer delivered to the user |

```python
message = response.choices[0].message

if hasattr(message, "reasoning_content") and message.reasoning_content:
    print("=== Reasoning Trace ===")
    print(message.reasoning_content)

print("=== Final Answer ===")
print(message.content)
```

Use `reasoning_content` for:

- **Audit logging** — store in Azure Monitor / Application Insights for traceability
- **Debugging** — surface reasoning when the final answer is unexpected
- **RAG pipelines** — pass reasoning context to downstream agents
- **Evaluation** — assess model quality beyond just the final answer

---

## Authentication

### Development (API Key)

```python
from azure.core.credentials import AzureKeyCredential

credential = AzureKeyCredential(os.environ["AZURE_AI_FOUNDRY_API_KEY"])
```

### Production (Recommended — Managed Identity)

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
```

`DefaultAzureCredential` supports Managed Identity in Azure-hosted workloads (App Service, Azure Functions, AKS, Container Apps) and developer credentials locally — no secrets in code or pipelines.

---

## Model Comparison

| Model | Reasoning Trace | Best For |
|---|---|---|
| `deepseek-r1` | ✅ `reasoning_content` field | Multi-step reasoning, maths, logic |
| `deepseek-v3` | ❌ (direct answer) | General-purpose, faster responses |
| `o3` / `o4-mini` (OpenAI) | ✅ via `reasoning_effort` | Mixed workloads on OpenAI stack |

Azure AI Foundry's model catalogue hosts both DeepSeek R1 and V3 as serverless API deployments — no GPU provisioning required.

---

## Related Repositories

This repo is part of the **Microsoft Foundry Open-Source Series**:

| Repository | Description |
|---|---|
| [MSFoundryAgentMemory](https://github.com/praveen11singh/MSFoundryAgentMemory) | Ephemeral, contextual, and persistent memory patterns |
---

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

---

## Author

**Praveen Kumar Singh**  
Azure Solutions Architect & AI Engineer | Associate Consultant @ TCS  
Triple Microsoft Certified: AZ-305 · AI-102 · AZ-104

[![LinkedIn]](https://www.linkedin.com/in/praveen-kumar-b52a1a1a0/)
[![GitHub]](https://github.com/praveen11singh)
---

