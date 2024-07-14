import os
import google.generativeai as genai
from flask import jsonify
from logger_debug import logger

def send_request_subqueries(query):
  req_subqueries = make_request_subqueries(query)
  model = init_genai_client()
  subqueries = model.generate_content(req_subqueries)
  return subqueries

def send_request_main(query, docs):
  req_main = make_request_main(query, docs)
  model = init_genai_client()
  res_main = model.generate_content(req_main)
  return res_main

def make_request_subqueries(user_query):
    messages = [
        {
            'role': 'system',
            'content': 'You are a helpful expert research assistance specializing in salesforce software development in the apex programming language. '
                'Your users are asking questions about apex programming syntax and best practices. '
                'Suggest up to five additional questions they could ask to find the best answer. '
                'Suggest only short questions without compound sentences. '
                'Make sure they are compelte questions, and that they are closely related to the original question. '
                'Output one question per line. Do not number questions. '
        }, {
            'role': 'user',
            'query': f'Question: {user_query}'
        }
    ]
    return str(messages)

def make_request_main(query, context_documents):
    information = '\n\n'.join(context_documents)

    messages = [
      {
        'role': 'system',
        'content': 'You are a helpful expert in software development for the Salesforce platform using the Apex coding language. Your users are asking questions about information contained in the apex documentation and apex programming best practices. '
        'You will be shown the user\'s query and relevant contexual information. Answer the user\'s query using only the provided contextual information. '
        'Provide a code example when relevant. '
      },
      {
        'role': 'user',
        'query': f'Question: {query}.'
      },
      {
        'role': 'user',
        'context': f'{information}'
      }
    ]
    return str(messages)

def init_genai_client():
  api_key = get_genai_key()
  genai.configure(api_key=api_key)
  return genai.GenerativeModel('gemini-pro')

def get_genai_key():
    api_key = os.getenv('GEMINI_API_KEY')  
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    return api_key

__all__ = ['send_request_subqueries', 'send_request_main']