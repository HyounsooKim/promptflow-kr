
from promptflow import tool
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv
load_dotenv()

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(embedding: list):
    endpoint    = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
    credential  = AzureKeyCredential(os.getenv('AZURE_AI_SEARCH_API_KEY'))
    index_name  = os.getenv('AZURE_AI_SEARCH_INDEX')
    api_version = os.getenv('AZURE_AI_SEARCH_API_VERSION')

    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential, api_version=api_version)

    vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=3, fields="content_vector", exhaustive=True)

    results = search_client.search(  
        search_text=None,  
        vector_queries= [vector_query],
        select=["id", "url", "title", "text"],
    )

    # Azure AI Search 검색결과를 리스트로 변환
    search_results = []
    for result in results:
        if result['@search.score'] > 0.7:
            search_results.append(result['text'])

    return search_results