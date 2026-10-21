
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph

from load_documents import load_government_document


# ==================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()

required_vars = [
    "OPENAI_API_KEY",
    "NEO4J_URI",
    "NEO4J_USERNAME",
    "NEO4J_PASSWORD",
]

missing = [
    key for key in required_vars
    if not os.getenv(key)
]

if missing:
    raise ValueError(
        f"Missing variables in .env file: {missing}"
    )


# ==================================================
# 2. CONFIGURE NEO4J AURA
# ==================================================

NEO4J_DATABASE = "6bc76416"

graph = None

try:
    print("\nConnecting to Neo4j Aura...")

    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        database=NEO4J_DATABASE,
    )

    print("Connected to Neo4j Aura successfully!")


    # ==============================================
    # 3. LOAD GOVERNMENT WEBSITE DOCUMENTS
    # ==============================================

    print("\nLoading government scheme documents...")

    documents = load_government_document()

    print(f"Documents loaded: {len(documents)}")


    # ==============================================
    # 4. SPLIT DOCUMENTS INTO CHUNKS
    # ==============================================

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    print(f"Text chunks created: {len(chunks)}")


    # ==============================================
    # 5. CONFIGURE THE LLM
    # ==============================================

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    transformer = LLMGraphTransformer(llm=llm)


    # ==============================================
    # 6. EXTRACT ENTITIES AND RELATIONSHIPS
    # ==============================================

    print("\nExtracting graph data using the LLM...")

    graph_documents = (
        transformer.convert_to_graph_documents(chunks)
    )

    print(
        f"Graph documents extracted: "
        f"{len(graph_documents)}"
    )


    # ==============================================
    # 7. STORE GRAPH IN NEO4J AURA
    # ==============================================

    print("\nSaving graph to Neo4j Aura...")

    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True,
    )

    print("Graph data stored successfully!")


    # ==============================================
    # 8. VERIFY NODE COUNT
    # ==============================================

    node_result = graph.query("""
        MATCH (n)
        RETURN count(n) AS total_nodes
    """)

    total_nodes = node_result[0]["total_nodes"]

    print(f"\nTotal nodes in database: {total_nodes}")


    # ==============================================
    # 9. VERIFY RELATIONSHIP COUNT
    # ==============================================

    relationship_result = graph.query("""
        MATCH ()-[r]->()
        RETURN count(r) AS total_relationships
    """)

    total_relationships = (
        relationship_result[0]["total_relationships"]
    )

    print(
        "Total relationships in database: "
        f"{total_relationships}"
    )


    # ==============================================
    # 10. DISPLAY SAMPLE GRAPH DATA
    # ==============================================

    print("\nSample nodes and relationships:")

    sample_result = graph.query("""
        MATCH (a)-[r]->(b)
        RETURN
            labels(a) AS source_labels,
            a.id AS source,
            type(r) AS relationship,
            labels(b) AS target_labels,
            b.id AS target
        LIMIT 10
    """)

    for record in sample_result:
        print(record)

    print("\nKnowledge graph pipeline completed!")


except Exception as error:
    print("\nPipeline failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", error)


finally:
    if graph is not None:
        graph.close()
        print("\nNeo4j connection closed.")
