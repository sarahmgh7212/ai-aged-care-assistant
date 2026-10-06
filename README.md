# AI Aged Care Information Assistant

An AI-powered information assistant that uses Retrieval-Augmented Generation
(RAG) to answer questions using the Australian Aged Care Quality Standards
as its knowledge base.

The project combines a Next.js frontend, FastAPI backend, ChromaDB vector
search, OpenAI embeddings, and an OpenRouter-hosted language model.

The system is designed to demonstrate practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Vector search and semantic retrieval
- LLM-based answer generation
- Answerability and relevance checks
- Conversational context
- Source attribution and evidence transparency
- Prompt injection protection
- Automated AI evaluation
- Responsible AI guardrails

> **Portfolio project:** This application is an independent technical
> demonstration and is not an official Aged Care Quality and Safety
> Commission product or service.

## Key Features

- **Knowledge-grounded answers** using the Australian Aged Care Quality
  Standards
- **Semantic search** using ChromaDB and OpenAI embeddings
- **RAG-based generation** using an OpenAI-compatible API through OpenRouter
- **Answerability gate** to determine whether retrieved evidence is sufficient
- **Conversational context** for follow-up questions
- **Source citations** showing the document and page used for an answer
- **Out-of-scope handling** for questions outside the knowledge base
- **Prompt injection protection**
- **Automated evaluation suite** covering retrieval, grounding, relevance,
  completeness, citation accuracy, and hallucination resistance
- **Automated backend tests** using pytest
- **Evaluation dashboard** for inspecting system performance

## Architecture

User
│
▼
Next.js Frontend
│
│ POST /api/chat
▼
FastAPI Backend
│
├── Conversation Context
│
├── ChromaDB Semantic Retrieval
│     │
│     └── Aged Care Quality Standards
│
├── Answerability Check
│
└── LLM Generation
    │
    ▼
    OpenRouter API
    │
    ▼
    Grounded Response
    │
    ▼
    Next.js Frontend
    │
    └── Answer + Knowledge-base Sources

## RAG Pipeline

The knowledge base is processed through the following pipeline:

1. **Document ingestion**
   - The Australian Aged Care Quality Standards PDF is stored in the
     knowledge-base.

2. **Text extraction**
   - Text is extracted from the source PDF while preserving page information.

3. **Chunking**
   - The document is divided into overlapping chunks to improve retrieval
     quality.

4. **Embedding generation**
   - Chunks are converted into vector embeddings using
     `text-embedding-3-small`.

5. **Vector storage**
   - Embeddings and metadata are stored in a persistent ChromaDB collection.

6. **Semantic retrieval**
   - A user's question is converted into an embedding and compared against
     the knowledge base using cosine distance.

7. **Answerability check**
   - Retrieved evidence is evaluated to determine whether it contains enough
     information to answer the question.

8. **Grounded generation**
   - If sufficient evidence is available, the LLM generates an answer using
     the retrieved passages.

9. **Source attribution**
   - The response includes references to the source passages and page numbers
     used to generate the answer.

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI / RAG

- OpenRouter API
- `gpt-5-mini`
- OpenAI `text-embedding-3-small`
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### Testing and Evaluation

- pytest
- Automated RAG evaluation
- LLM-based answer evaluation
- Evaluation dashboard

### Development

- Git
- VS Code
- Python virtual environment

## Evaluation

The project includes an automated evaluation suite covering both
answerable and out-of-scope questions.

The evaluation dataset includes:

- Direct aged care knowledge questions
- Conversational follow-up questions
- Questions requiring contextual conversation history
- Legal, medical, financial and political questions outside the knowledge base
- Unrelated questions such as car maintenance and weather
- Prompt injection attempts

### Evaluation Metrics

The system evaluates:

| Metric                 | Description                                                                      |
| ---------------------- | -------------------------------------------------------------------------------- |
| Retrieval accuracy     | Whether relevant knowledge-base evidence was retrieved for answerable questions  |
| Out-of-scope rejection | Whether questions outside the knowledge base were correctly rejected             |
| Grounded answers       | Whether generated claims were supported by retrieved evidence                    |
| Relevant answers       | Whether the response directly addressed the question                             |
| Complete answers       | Whether the response sufficiently answered the question using available evidence |
| Citation accuracy      | Whether source references correctly supported the associated claims              |
| No hallucination       | Whether the assistant avoided unsupported answers to out-of-scope questions      |

Evaluation results are generated automatically by:

```bash
cd backend
python run_evaluation.py
```

### Current Evaluation Results

The latest evaluation run covers 20 questions across answerable,
conversational, and out-of-scope scenarios.

| Metric                 |     Result |
| ---------------------- | ---------: |
| Retrieval accuracy     |  **83.3%** |
| Out-of-scope rejection |  **75.0%** |
| Grounded answers       |  **91.7%** |
| Relevant answers       | **100.0%** |
| Complete answers       | **100.0%** |
| Citation accuracy      |  **83.3%** |
| No hallucination       | **100.0%** |

The evaluation is intentionally designed to identify weaknesses rather than
only demonstrate successful responses. Retrieval and citation accuracy
remain areas for further improvement, while the current evaluation achieved
100% on relevance, completeness, and avoiding hallucinated answers for
out-of-scope questions.

## Local Setup

### Prerequisites

- Python 3.12+
- Node.js
- npm
- An OpenRouter API key

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-aged-care-assistant
```

### 2. Set up the backend

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```env
OPENROUTER_API_KEY=your_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-5-mini
RAG_TOP_K=5
RAG_MAX_DISTANCE=0.6
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### 3. Set up the frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Create a `.env.local` file based on `.env.example`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Start the Next.js development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:3000
```

### 4. Run automated tests

Open a terminal in the backend directory with the virtual environment activated:

```bash
cd backend
pytest
```

The test suite currently contains 6 automated backend tests covering API endpoints, conversation history, retrieval filtering, and answerability checks.

### 5. Run the AI evaluation

From the `backend` directory:

```bash
python run_evaluation.py
```

The evaluation suite tests answerable, conversational, and out-of-scope questions and saves the results to:

```text
knowledge-base/evaluation/results.json
```

The results can also be viewed through the application's Evaluation Dashboard.

### Environment Variables

The following environment files are used locally:

```text
backend/.env
frontend/.env.local
```

These files contain local configuration and API credentials and should **not** be committed to the repository.

Example configuration files are provided as:

```text
backend/.env.example
frontend/.env.example
```

## Responsible AI and Safety

This project was designed with several safeguards to reduce unsupported,
misleading, or inappropriate AI-generated responses.

The guardrail concepts are informed by responsible AI practices commonly
used in enterprise AI systems, including approaches associated with
Microsoft Copilot Studio and Azure AI. This project does not currently
use Microsoft Copilot Studio or Azure AI services directly.

### Grounded responses

The assistant uses retrieval-augmented generation (RAG). Before generating
an answer, it retrieves relevant passages from the aged care knowledge base.

The language model is instructed to base its response only on the retrieved
evidence and not to invent information that is not supported by the
knowledge base.

### Answerability and relevance checks

Retrieved information is not automatically treated as sufficient evidence.

An answerability gate evaluates whether the retrieved evidence contains
enough relevant information to answer the user's question.

This helps prevent the assistant from answering questions that are only
loosely related to the aged care knowledge base.

For example, a question about making a complaint may be answerable from the
knowledge base, while a question asking for legal action against a provider
may be rejected if the available evidence does not provide sufficient
information.

### Evidence and transparency

Generated responses include references to the knowledge-base passages used
to produce the answer.

The user can expand the "Knowledge-base sources" section in the interface
to inspect the retrieved evidence, including the source document and page
number.

This provides greater transparency into where an answer came from.

### Out-of-scope questions

The assistant is intentionally limited to the information available in its
aged care knowledge base.

It does not attempt to answer unrelated questions such as:

- Car maintenance
- Weather forecasts
- Political voting recommendations
- Questions requiring information outside the knowledge base

Instead, the system is designed to acknowledge when relevant information
cannot be found.

### Medical, legal and financial limitations

The assistant is not designed to provide medical, legal, financial, or
other professional advice.

Questions requiring professional judgement should be referred to an
appropriately qualified professional or relevant official service.

The system should not make assumptions about an individual's personal
circumstances.

### Prompt injection protection

Retrieved documents are treated as information to support an answer, not as
instructions for the language model.

The system prompt explicitly instructs the model not to follow instructions
contained within retrieved documents.

This reduces the risk of a malicious or unexpected piece of retrieved
content changing the assistant's intended behaviour.

```

```

```

```
