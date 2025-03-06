import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(page_title="Web Content Q&A Tool", layout="wide")

if "ingested_content" not in st.session_state:
    st.session_state["ingested_content"] = {}

# Initialize Groq client with API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("Please set the GROQ_API_KEY environment variable.")
    st.stop()
groq_client = Groq(api_key=groq_api_key)

@st.cache_data(show_spinner=False)
def fetch_url_content(url: str) -> str:
    """
    Fetches and caches webpage content from a given URL.
    Removes scripts and styles to extract plain text.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL {url}: {e}")
        return ""


def groq_query(context: str, question: str) -> str:
    """
    Uses the Groq API to answer a question based on ingested content.
    Splits the context into chunks to handle large content and avoid "Payload Too Large" errors.
    """
    if len(question.split()) < 3:
        return "Please provide a more detailed question."

    if not context.strip():
        return "No ingested content available. Please ingest valid URLs first."

    # Chunk the context into smaller pieces (e.g., 1000 words per chunk)
    words = context.split()
    chunk_size = 1000  # Adjust chunk size as needed
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    all_answers = []
    for chunk in chunks:
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Answer the following question based on the context provided. Question: {question} Context: {chunk}",
                    }
                ],
                model="llama3-8b-8192",  # Or another suitable Groq model
            )
            answer = chat_completion.choices[0].message.content
            all_answers.append(answer.strip())
        except Exception as e:
            st.error(f"Error querying Groq API for a chunk: {e}")
            return "Could not generate a complete answer due to an error processing content chunks."

    # Combine answers from all chunks (you can modify this combination strategy)
    if all_answers:
        # For now, let's just return the first answer we get back.
        # You might want to implement a more sophisticated combination strategy,
        # like concatenating answers or summarizing them if needed.
        final_answer = all_answers[0]
        return final_answer
    else:
        return "Could not generate an answer from the provided content."


def main():
    st.title("Web Content Q&A Tool")
    st.markdown("### Ingest URLs and Ask Questions Based on Their Content")

    # Section 1: URL Ingestion
    with st.expander("1. Ingest URLs", expanded=True):
        urls_input = st.text_area("Enter URLs (one per line):", height=150)
        if st.button("Ingest URLs"):
            urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
            if not urls:
                st.warning("Please enter at least one URL to ingest.")
            else:
                ingestion_results = {}
                with st.spinner("Fetching and ingesting URLs..."):
                    for url in urls:
                        content = fetch_url_content(url)
                        if content:
                            st.session_state["ingested_content"][url] = content
                            ingestion_results[url] = "Success"
                        else:
                            ingestion_results[url] = "Failed to fetch content"
                st.write("Ingestion Results:")
                st.json(ingestion_results)
                if ingestion_results:
                    st.write("Ingested URLs:")
                    st.write(list(st.session_state["ingested_content"].keys()))


    # Section 2: Ask a Question
    with st.expander("2. Ask a Question", expanded=True):
        question_input = st.text_input("Enter your question:")
        if st.button("Ask Question"):
            if not question_input:
                st.warning("Please enter a question.")
            elif not st.session_state["ingested_content"]:
                st.warning("Please ingest URLs first before asking questions.")
            else:
                context = "\n".join(st.session_state["ingested_content"].values())
                with st.spinner("Generating answer..."):
                    answer = groq_query(context, question_input)
                st.markdown("#### Answer:")
                st.write(answer)

if __name__ == "__main__":
    main()