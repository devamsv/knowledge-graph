
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.graph_transformers import LLMGraphTransformer

from load_documents import load_government_document

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Add OPENAI_API_KEY to your .env file.")

# 1. Load the government website
documents = load_government_document()

# 2. Split the document into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)
print(f"\nCreated {len(chunks)} text chunks.")

# 3. Configure the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# 4. Create the graph extraction transformer
graph_transformer = LLMGraphTransformer(
    llm=llm
)

# 5. Extract entities and relationships
graph_documents = graph_transformer.convert_to_graph_documents(
    chunks
)

# 6. Display the extracted graph data
print("\n========== EXTRACTED KNOWLEDGE GRAPH ==========")

for index, graph_doc in enumerate(graph_documents, start=1):
    print(f"\n--- Chunk {index} ---")

    print("\nEntities / Nodes:")
    for node in graph_doc.nodes:
        print({
            "id": node.id,
            "type": node.type,
            "properties": node.properties
        })

    print("\nRelationships:")
    for relationship in graph_doc.relationships:
        print({
            "source": relationship.source.id,
            "relationship": relationship.type,
            "target": relationship.target.id
        })

    print("\nNode count:", len(graph_doc.nodes))
    print("Relationship count:", len(graph_doc.relationships))

print("\nGraph extraction completed.")
print("Note: Data has not been saved to Neo4j yet.")
