import os
import torch
import chromadb
from logger_debug import logger
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter

def init_knowledge_base(print_stats=False):
  logger.debug(f'** Knowledgebase Initialization: Started **')

  collection = get_chroma_collection()
  if (collection.count() > 0):
    logger.debug(f'Chroma db previously initialized.')
    logger.debug(f'Collection size: {collection.count()}')
    logger.debug(f'** Knowledgebase Initialization: Complete **')
    return

  # Load pdfs
  pdf_pages = load_pdfs()
  logger.debug(f'Total pages: {len(pdf_pages)}')

  # Split by characters
  character_split_texts = character_split(pdf_pages)
  logger.debug(f'Total char chunks: {len(character_split_texts)}')

  # Split by tokens
  token_split_texts = token_split(character_split_texts)
  logger.debug(f'Total token chunks: {len(token_split_texts)}')

  # Generate embeddings
  embeddings_all = embed_chunks(token_split_texts)
  logger.debug(f'Total embeddings: {len(embeddings_all)}')

  # Init chroma db
  chroma_collection = init_chroma_db(embeddings_all, token_split_texts)

  if (print_stats):
    logger.debug(f'Total pages: {len(pdf_pages)}')
    logger.debug(f'Total char chunks: {len(character_split_texts)}')
    logger.debug(f'Total token chunks: {len(token_split_texts)}')
    logger.debug(f'Total embeddings: {len(embeddings_all)}')
    logger.debug(f'Total dimensions: {len(embeddings_all[0])}')
    logger.debug(f'Collection size: {chroma_collection.count()}')

  logger.debug(f'** Knowledgebase Initialization: Complete **')

def load_pdfs(pdf_folder='/pdfs'):
  pdf_folder_path = get_project_folder() + pdf_folder
  pdf_loader = PyPDFDirectoryLoader(pdf_folder_path)
  pdf_docs = pdf_loader.load()
  return [doc.page_content for doc in pdf_docs]

def character_split(pdf_pages):
  character_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', '. ', ' ', ''],
    chunk_size=1000,
    chunk_overlap=0
  )
  return character_splitter.split_text('\n\n'.join(pdf_pages))

def token_split(strings):
  token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
  splits = []
  for text in strings:
    splits += token_splitter.split_text(text)
  return splits

# Embed tokens
def embed_chunks(token_chunks, batch_size=512):
  # device = torch.device('cuda')
  # embedding_model = SentenceTransformerEmbeddingFunction(device=device)
  embedding_model = SentenceTransformerEmbeddingFunction()

  embeddings = []
  for i in range(0, len(token_chunks), batch_size):
    batch = token_chunks[i:i+batch_size]
    embeddings += embedding_model(batch)

  return embeddings

def init_chroma_db(embeddings, docs):
  # Initialize Chroma embedding database with ids
  collection = get_chroma_collection()
  if (collection.count() == 0):
    ids = [str(i) for i in range(len(docs))]
    collection.add(ids=ids, embeddings=embeddings, documents=docs)
  return collection

def get_chroma_collection():
  chroma_client = chromadb.PersistentClient(get_project_folder() + '/chroma')
  return chroma_client.get_or_create_collection('documentation_pdfs')

def get_project_folder():
  return os.environ.get('PROJECT_FOLDER')

__all__ = ['init_knowledge_base', 'get_chroma_collection']

init_knowledge_base(True)