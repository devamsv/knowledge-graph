
import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

# Neo4j Aura configuration
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database="6bc76416",
)


def show_all_schemes():
    """List entities identified as schemes."""

    query = """
    MATCH (n:__Entity__:Scheme)
    RETURN n.id AS scheme
    ORDER BY scheme
    LIMIT 50
    """

    results = graph.query(query)

    print("\nGOVERNMENT SCHEMES")
    print("-" * 40)

    for row in results:
        print(row["scheme"])


def find_department_schemes():
    """Find schemes connected to the Agriculture department."""

    query = """
    MATCH (d:__Entity__)-[r]->(s:__Entity__:Scheme)
    WHERE toLower(d.id) CONTAINS 'agriculture'
    RETURN d.id AS department,
           type(r) AS relationship,
           s.id AS scheme
    ORDER BY scheme
    LIMIT 50
    """

    results = graph.query(query)

    print("\nAGRICULTURE DEPARTMENT CONNECTIONS")
    print("-" * 40)

    for row in results:
        print(
            f"{row['department']} "
            f"--[{row['relationship']}]--> "
            f"{row['scheme']}"
        )


def search_entity(keyword):
    """Search for entities by name."""

    query = """
    MATCH (n:__Entity__)
    WHERE toLower(n.id) CONTAINS toLower($keyword)
    RETURN labels(n) AS labels, n.id AS name
    LIMIT 20
    """

    results = graph.query(
        query,
        params={"keyword": keyword},
    )

    print(f"\nSEARCH RESULTS FOR: {keyword}")
    print("-" * 40)

    if not results:
        print("No matching entities found.")
        return

    for row in results:
        print(f"{row['name']} | Types: {row['labels']}")


if __name__ == "__main__":
    try:
        show_all_schemes()
        find_department_schemes()
        search_entity("farmers")

    except Exception as error:
        print("Query failed:", error)

    finally:
        graph.close()
