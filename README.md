# Web Content Q&A Tool - End-to-End Workflow

This project is a Streamlit-based web application that ingests content from user-provided URLs and answers questions based solely on that ingested content using the Groq API. This document outlines the complete workflow of the tool, from setup to answer generation.

## Overview

The Web Content Q&A Tool is designed to:
- **Ingest URLs:** Fetch and process text content from one or more websites.
- **Process Content:** Clean and cache the text by removing extraneous elements such as scripts and styles.
- **Answer Questions:** Generate answers based on the ingested content by querying the Groq API.
- **Provide an Intuitive UI:** Offer a simple, single-page interface built with Streamlit for a smooth user experience.

## Workflow

1. **Setup and Configuration**
   - **Clone the Repository:** Get the project files on your local machine.
   - **Install Dependencies:** Install the required Python packages.
   - **Configure Environment Variables:** Set up a `.env` file to store your `GROQ_API_KEY`.

2. **URL Ingestion**
   - **User Input:** The user enters one or more URLs in the application.
   - **Fetching Content:** The application fetches the webpage content via HTTP requests.
   - **Content Cleaning:** Using BeautifulSoup, the application removes unwanted tags (e.g., scripts, styles) to extract clean text.
   - **Caching:** The cleaned content is cached for efficient future queries.

3. **Question Asking**
   - **User Query:** The user enters a question based on the ingested content.
   - **Context Combination:** The tool combines all ingested content to form a comprehensive context.
   - **Chunking (if needed):** The context is split into manageable chunks to handle large texts.
   - **API Query:** The Groq API is queried for each chunk to generate an answer.
   - **Answer Aggregation:** Answers from different chunks are combined (currently, the first answer is returned) and displayed to the user.

4. **Error Handling**
   - The tool provides clear warnings or error messages if:
     - No URLs are provided.
     - URL ingestion fails.
     - The user question is too generic.
     - The Groq API encounters errors.

## Prerequisites

- **Python Version:** Python 3.6 or higher.
- **Groq API Key:** A valid API key for accessing the Groq API.
