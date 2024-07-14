
from logger_app import AppLogger
from callouts import send_request_subqueries, send_request_main
from knowledge_base import query_documents
from document_crossencoder import score_documents, select_top_documents

def handle_user_query(user_input):
    log = AppLogger()
    try: 
        query = user_input
        log.user_input(query)

        # Generate subqueries
        subqueries = send_request_subqueries(query)
        log.subqueries_response(subqueries.text)

        # Query embeddings db for documents matching the queries
        all_queries = [query] + subqueries.text.split('\n')
        unique_documents = query_documents(all_queries)

        # Select the most relevant docs via cross-encorder scoring
        unique_documents_scored = score_documents(query, unique_documents)
        log.embeddings_scored(unique_documents_scored)

        top_docs = select_top_documents(unique_documents_scored)
        log.embeddings_top(top_docs)

        # Send main request
        res_main = send_request_main(query, top_docs)
        log.main_response(res_main.text)

        log.success()
        log.commit()
        return res_main.text
    except Exception as ex:
        log.error(ex)
        raise ex