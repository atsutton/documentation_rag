# RAG Web Application 

This project demonstrates a Retrieval-Augmented Generation (RAG) web application that combines a language model (LLM) with a ChromaDB vector database. This approach enables the system to provide accurate, context-aware responses to user queries by grounding the LLM's responses in relevant information retrieved from the database.

## Features

* **Retrieval-Augmented Generation (RAG):** The core of the application. This process involves:

    1. **Sub-Query Generation:** The user's initial query is sent to the LLM to generate relevant sub-queries, expanding the search     space.

    2. **Vector Retrieval:** Embeddings of the query and subqueries are used to retrieve semantically similar documents from the ChromaDB vector database.

    3. **Cross-Encoder Scoring:** Retrieved documents are scored and ranked based on their relevance to the original user query using a cross-encoder model. This model directly compares the text of the query and documents to assess their semantic similarity.

    4. **Contextualized Main Query**: The original user query, combined with the highest-scoring documents, is sent to the LLM for final response generation. This ensures the response is informed by relevant context.

* **Chatbot-like Interface:**  A user-friendly chat interface, built with React, facilitates seamless interaction with the RAG system.

* **PostgreSQL Logging:**  User interactions, including queries, subqueries, retrieved documents, scores, and responses, are logged in a PostgreSQL database for analysis.

## Technology Stack

* **Frontend:** React (using Material UI)
* **Backend:** Flask (Python)
* **Database:** PostgreSQL
* **Vector Database:** ChromaDB
* **Containerization:** Docker
* **Language Model (LLM):** Google Gemini (gemini-pro)

## Additional Notes

* This project is a work in progress. I am actively developing and refining its features. 

* The current design provides answers about Apex, the Java-like proprietary programming language from Salesforce. A future design will allow users to easily configure any topic for which pdf documents can be obtained. 

* The application relies on the Google Gemini API and the gemini-pro model, for which you will will need <a href="https://aistudio.google.com/app/apikey" target="_blank">an api key</a>. 

## Installation and Setup

**Prerequisites:**

* Docker and Docker Compose installed on your system.
* Google Gemini API key

**Steps:**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/atsutton/documentation_rag.git
   ```

2. **Set the Gemini API Key:**

    Edit the file at ./documentation_rag/rag_server/docker-compose.yml to set the GEMINI_API_KEY environment variable.
    ```
    environment:
      - GEMINI_API_KEY=[* YOUR API KEY *]
    ```

3. **Start the Flask & PostgreSQL Servers:**
    
    Build and run the containers:
    ```bash
    docker compose -f ./documentation_rag/rag_server/docker-compose.yml up
    ```
    Leave the teriminal open to view logs.     

   **Note**: this step may take 10-20 minutes to complete on first run, depending on system resources. This is due buliding of the Chroma database and ingestion of pdf files. The Chroma database is configured to persist, so it's not re-built in subsequent runs. The step is complete when the terminal shows: "\*\* Knowledgebase Initialization: Complete \*\*" and "\*\* Flask Initialization: Complete \*\*"

   **Note**: the containers will persist for future use and will not be deleted when you call docker-compose down.

4. **Start the React UI:**

    Open a second terminal. Build and run the React app container:
    ```bash
    docker compose -f ./documentation_rag/rag_ui/docker-compose.yml up
    ```
    **Note**: the containers will persist for future use and will not be deleted when you call docker-compose down.

5. **Access the Application:**

    Open your web browser and go to 
    ```
    http://localhost:8888
    ```

### Installation Notes:

* The first time you run these commands, it might take a while to download the necessary Docker images and build the Chroma database. Subsequent runs will be faster.

* Ensure that the port numbers specified in the docker-compose.yml files don't conflict with any other applications running on your system.

## License

Copyright 2024 Adam Sutton

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.