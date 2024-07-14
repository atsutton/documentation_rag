from knowledge_base_init import get_chroma_collection

# Query the embeddings database; return only unique documents
# count: number of results to return per query
def query_documents(queries, count=5):
  collection = get_chroma_collection()
  retrieved_embeddings = collection.query(query_texts=queries, n_results=count)
  retrieved_documents = retrieved_embeddings['documents']

  # Dedupe - because the retrieved documents can overlap
  uniques = set()
  for docs in retrieved_documents:
      for doc in docs:
          uniques.add(doc)
  return uniques

__all__ = ['query_documents', 'get_chroma_collection']