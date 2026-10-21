
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

# Official Tamil Nadu Government schemes page
URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

def load_government_document():
    print("Loading Tamil Nadu Government schemes...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    # Parse the webpage
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary page elements
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else "Tamil Nadu Government Schemes"

    # Extract readable text
    text = soup.get_text(separator="\n", strip=True)

    if not text:
        raise ValueError("No readable text found on the webpage.")

    # Convert webpage text into a LangChain Document
    document = Document(
        page_content=text,
        metadata={
            "source": URL,
            "title": title,
            "document_type": "government_scheme_list"
        }
    )

    print("\nDocument loaded successfully!")
    print("Title:", title)
    print("Characters extracted:", len(document.page_content))
    print("Metadata:", document.metadata)

    print("\n--- First 1500 characters ---\n")
    print(document.page_content[:1500])

    return [document]


if __name__ == "__main__":
    documents = load_government_document()
    print("\nTotal documents loaded:", len(documents))
