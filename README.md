# Tamil Nadu Government Schemes — Knowledge Graph RAG

A Python-based Knowledge Graph RAG project that uses **LangChain, Neo4j Aura, and OpenAI** to extract, store, retrieve, and answer questions about Tamil Nadu Government schemes.

## Project Overview

This project extracts information from the Tamil Nadu Government schemes webpage, uses an LLM to identify entities and relationships, stores the knowledge graph in Neo4j Aura, and retrieves relevant information to answer natural-language questions.

## Architecture

```text
Tamil Nadu Government Website
            |
            v
     Web Data Extraction
            |
            v
      Text Chunking
            |
            v
    LLM Graph Extraction
            |
            v
      Neo4j Aura DB
            |
            v
      Cypher Queries
            |
            v
      Retrieved Context
            |
            v
        OpenAI LLM
            |
            v
       Final Answer
```

## Technologies Used

- **Python** — application development
- **LangChain** — document processing and LLM integration
- **OpenAI API** — graph extraction and answer generation
- **Neo4j Aura** — cloud-hosted graph database
- **Cypher** — graph querying language
- **BeautifulSoup** — webpage text extraction
- **python-dotenv** — environment variable management

## Data Source

Tamil Nadu Government — Schemes List:

https://www.tn.gov.in/scheme_list.php?dep_id=Mg==

## Project Structure

```text
knowledge-graph/
├── .env
├── .gitignore
├── load_documents.py
├── extract_graph.py
├── store_graph.py
├── query_graph.py
├── graph_rag.py
└── README.md
```

## Prerequisites

- Python 3.10 or a compatible Python version supported by the installed dependencies
- OpenAI API key
- Neo4j Aura account and database
- Internet connectivity
- Git (optional)

## Installation

### 1. Open your project folder

```bash
cd knowledge-graph
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install langchain langchain-community langchain-openai langchain-experimental langchain-neo4j langchain-text-splitters neo4j python-dotenv requests beautifulsoup4 lxml
```

## Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
NEO4J_URI=your_neo4j_aura_uri
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

Replace the example values with your actual credentials.

**Security:** Never upload `.env` or expose your API keys and database passwords on GitHub.

## How to Run

Run the scripts in the following order.

### Step 1: Load website documents

```bash
python load_documents.py
```

Extracts readable text and metadata from the government webpage.

### Step 2: Extract graph information

```bash
python extract_graph.py
```

Uses an LLM to identify entities and relationships from the extracted text.

### Step 3: Store the knowledge graph

```bash
python store_graph.py
```

Stores graph entities, relationships, and source-document connections in Neo4j Aura.

### Step 4: Query the knowledge graph

```bash
python query_graph.py
```

Runs Cypher queries and searches for entities already stored in Neo4j.

### Step 5: Run the Graph RAG chatbot

```bash
python graph_rag.py
```

Accepts natural-language questions, retrieves matching graph entities and connections, and uses an LLM to generate answers.

## Example Questions

- What government schemes are listed on the website?
- What information is available about agriculture?
- Find entities related to farmers.
- What information is available about subsidies?

The answers depend on the entities and relationships extracted from the source webpage.

## How It Works

1. **Data extraction:** Fetches webpage content and removes common navigation elements.
2. **Text splitting:** Divides the extracted text into smaller chunks.
3. **Graph extraction:** Uses an LLM to identify entities and relationships.
4. **Graph storage:** Stores the extracted knowledge graph in Neo4j Aura.
5. **Graph retrieval:** Uses Cypher queries to retrieve matching information.
6. **Answer generation:** Sends retrieved graph context to the LLM to generate a response.

## Current Limitations

- The webpage may contain only scheme names or limited descriptions.
- LLM-extracted relationships may be inaccurate or unsupported by the source.
- The current chatbot uses keyword-based graph retrieval, so it may miss relevant entities.
- Eligibility criteria, benefits, and application procedures may not be available in the extracted data.
- Answers should be verified against official government information.

## Future Improvements

- Improve graph retrieval and entity matching.
- Add source citations to generated answers.
- Validate extracted entities and relationships against official documents.
- Build a Streamlit chatbot interface.
- Support Tamil and English questions.
- Add evaluation tests for retrieval accuracy and answer quality.
- Deploy the application with suitable security controls.

## Learning Outcomes

This project provides practical experience with:

- Retrieval-Augmented Generation (RAG)
- Knowledge graphs and graph databases
- LangChain
- LLM-based entity and relationship extraction
- Cypher queries
- Python API integration
- Building AI-powered question-answering applications

## Disclaimer

This is an educational project, not an official Tamil Nadu Government service. Generated answers may be incomplete or inaccurate. Always consult the official government website for authoritative information.

## Author

**DEVENDHIRAN M**  
AI & GenAI Trainer | AI Developer | Data Science Enthusiast
