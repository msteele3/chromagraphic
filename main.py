import eel
from my_chroma_library import *
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
import json


#Globals
key = os.environ.get('OPENAI_API_KEY')
current_path = "chroma_database"
current_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=current_path 
    ))
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=key,model_name="text-embedding-ada-002")
current_client.persist()
print(str(current_client.heartbeat()))
current_collection = None
current_document = None
current_document_id = None
current_document_text = None



@eel.expose
def remake_client(new_path):
    current_path = "./" + new_path
    new_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=current_path 
    ))

    #update collections list
    
@eel.expose
def get_collection_document_count(collection_name):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=key,model_name="text-embedding-ada-002")
    current_collection = current_client.get_collection(collection_name, embedding_function=openai_ef)
    return current_collection.count()



@eel.expose
def get_collections_list():
    stringy_list = []
    collections_list = current_client.list_collections()
    for collection in collections_list:
        stringy_list.append(collection.name)
    print(stringy_list)
    return stringy_list

@eel.expose
def choose__collection():
    print("TODO")

@eel.expose
def add_new_collection(collection_name):
    current_client.get_or_create_collection(collection_name, embedding_function=openai_ef)
    print("Success")

@eel.expose
def remove_collection(collection_name):
    current_client.delete_collection(collection_name)
    print("done")


@eel.expose
def get_document_ids(collection_name):
    collection = current_client.get_collection(collection_name)
    collection_ids = collection.get()["ids"]
    return collection_ids

@eel.expose
def get_document_info(collection_name, id):
    current_collection = current_client.get_collection(collection_name, embedding_function=openai_ef)
    document = current_collection.get(ids=id)
    contentd = document['documents']
    sourced = document['metadatas'][0]["source"]  
    returnObj = {
        "source": sourced,
        "content": contentd
    } 
    return json.dumps(returnObj)


#CODE FOR LATER collection.get( include=["documents"])
@eel.expose
def get_document(collection_name, document_id):
    current_collection = current_client.get_collection(collection_name, embedding_function=embedding_functions.OpenAIEmbeddingFunction(api_key=key,  model_name="text-embedding-ada-002"))
    

@eel.expose
def delete_document(collection_name, id):
    current_collection = current_client.get_collection(collection_name, embedding_function=embedding_functions.OpenAIEmbeddingFunction(api_key=key,  model_name="text-embedding-ada-002"))
    current_collection.delete(ids=[id])


@eel.expose
def add_document(collection_name, document_name, document_source, document_contents):

    current_collection = current_client.get_or_create_collection(collection_name, embedding_function=embedding_functions.OpenAIEmbeddingFunction(api_key=key,  model_name="text-embedding-ada-002"))
    current_collection.add(     
            documents=[document_contents], # we embed for you, or bring your own
            metadatas=[{"source": document_source}], # filter on arbitrary metadata!
            ids=[document_name], # must be unique for each doc 
        )
    print("Added to collection ")
    print(current_collection.get())





eel.init("web")
eel.start("index.html")