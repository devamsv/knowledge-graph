
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph

load_dotenv()

# Connect to Neo4j Aura
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database="6bc76416",
)

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


def retrieve_graph_context(question):
    """Retrieve matching entities and their graph connections."""

    cypher = """
    MATCH (n:__Entity__)
    WHERE toLower(coalesce(n.id, ''))
          CONTAINS toLower($keyword)
    OPTIONAL MATCH (n)-[r]-(related)
    RETURN
        n.id AS entity,
        labels(n) AS entity_types,
        collect(
            DISTINCT {
                relationship: type(r),
                related_entity: related.id
            }
        )[0..10] AS connections
    LIMIT 10
    """

    # Use important words from the question as search terms.
    stop_words = {
        "what", "which", "where", "when", "who",
        "is", "are", "the", "a", "an", "of",
        "for", "in", "on", "to", "tell", "me",
        "about", "explain", "show", "find"
    }

    keywords = [
        word.strip(".,?!:;()")
        for word in question.split()
        if word.strip(".,?!:;()").lower() not in stop_words
    ]

    context = []

    for keyword in keywords[:5]:
        if len(keyword) < 3:
            continue

        rows = graph.query(
            cypher,
            params={"keyword": keyword}
        )

        for row in rows:
            context.append(str(row))

    # Remove duplicate records while preserving order.
    context = list(dict.fromkeys(context))

    return "\n".join(context)


def ask_question(question):
    context = retrieve_graph_context(question)

    if not context.strip():
        return (
            "I couldn't find matching information in the knowledge "
            "graph. Try another keyword or verify the source website."
        )

    prompt = f"""
You are a Tamil Nadu Government Schemes assistant.

Answer the user's question using ONLY the retrieved graph context.
Do not invent scheme names, eligibility rules, benefits, or amounts.
If the context does not contain enough information, clearly say so.
Mention that official government information should be verified.

Retrieved graph context:
{context}

User question:
{question}

Answer clearly and simply.
"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    try:
        print("Tamil Nadu Government Schemes - Graph RAG")
        print("Type 'exit' to stop.")

        while True:
            question = input("\nAsk your question: ").strip()

            if question.lower() in {"exit", "quit"}:
                break

            if not question:
                continue

            answer = ask_question(question)
            print("\nAnswer:")
            print(answer)

    except Exception as error:
        print("Error:", error)

    finally:
        graph.close()
