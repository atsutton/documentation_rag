from sentence_transformers import CrossEncoder

# Score the relevance of each doc to the original query
def score_documents(query, documents):
  cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
  pairs = [[query, doc] for doc in documents]
  scores = cross_encoder.predict(pairs)
  docs_scored = list(zip(scores, documents))
  docs_scored.sort(reverse=True)
  return docs_scored

def select_top_documents(docs_scored, count=5):
  top_docs_scored = docs_scored[:count]
  return [doc[1] for doc in top_docs_scored]

__all__ = ['score_documents', 'select_top_documents']