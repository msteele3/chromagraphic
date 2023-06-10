import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import openai
import os
import random


key = os.environ.get('OPENAI_API_KEY')

def add_document_to_collection(chroma_collection, document_name, document_contents, document_source = "blank",id=-1) -> bool:
    """
    Adds a document to the collection

    Args:
        chroma_collection(collection): The chroma collection to be added to
        text_to_add(str): the string of text to add
        source(str): The source of the information

    Returns:
        bool: The success of the operation.
    """
    if id == -1:
        new_id = document_source + str(random.randint(0,9999))
    else:
        new_id = id
    try:
        chroma_collection.add(     
            documents=[document_contents], # we embed for you, or bring your own
            metadatas=[{"source": document_source}, {"name": document_name}], # filter on arbitrary metadata!
            ids=[new_id], # must be unique for each doc 
        )
    except:
        return False
    return True

    
#You can filter by the metadata tag
#Check return type
def get_query_result(chroma_collection, query_text, num_results, use_filter = "no") -> object:
    """
    Returns a query result from a chroma collection

    Args:
        chroma_collection(collection): The chroma collection to be added to
        query_text(str): the string of text to search
        num_results(int): The number of results to return
        use_filter(str): filter by metadata, so you can use a filter by a source, etc. Will need to update later to contain more meta

    Returns:
        object: The query results in object format.
    """
    if use_filter.__eq__("no"):
        query_results = chroma_collection.query(
            query_texts=[query_text],
            n_results=num_results
            )
        return query_results
    else:
        query_results = chroma_collection.query(
            query_texts=[query_text],
            n_results=num_results,
            where={"metadata_field": "is_equal_to_this"}
        )
        return query_results



#TODO. Make this unwrap the JSONs of the query into a string with \ns inbetween relevant text entries
def unwrap_query_results(query_data) -> list[str]:
    """
    Unwraps a query result for debugging purposes

    Args:
        query_data(object): filter by metadata, so you can use a filter by a source, etc. Will need to update later to contain more meta

    Returns:
        List[str]: The query results in list format.
    """
    documents = []
    for i in range(len(query_data['ids'][0])):
        new_document = "Document id: " + query_data['ids'][0][i] + "\n"
        new_document += "Document data: " + query_data['documents'][0][i] + "\n"
        new_document += "Document source: " + query_data['metadatas'][0][i]['source'] + "\n"
        new_document += "Query difference: " + str(query_data['distances'][0][i])
        documents.append(new_document)

    return documents


def unwrap_query_text(query_data) -> list[str]:
    """
    Unwraps a query result for debugging purposes

    Args:
        query_data(object): filter by metadata, so you can use a filter by a source, etc. Will need to update later to contain more meta

    Returns:
        List[str]: The query results in list format.
    """
    documents = []
    for i in range(len(query_data['ids'][0])):
        new_document = query_data['documents'][0][i] + "\n"
        documents.append(new_document)
    return documents


def split_file_into_sections(document_text, source_name, section_length, overlap) -> list[str]:
    """
    Takes file text and makes it into a split list to be put into the db

    Args:
        document_text(object): the text of an entire txt file
        source_name(str): name of the source(normally just the txt file)
        section_length(int): the length, in characters, that each segment should be
        overlap(int): the length, in characters, that the overlap between segments should be

    Returns:
        tuple(List[str],List[str)]: A tuple with the entire txt file data broken up into chunks for inde 0 and their source in index 1
    """
    sections = []
    section_source = []
    start = 0
    while start + section_length < len(document_text):
        sections.append(document_text[start:start+section_length])
        start += section_length - overlap
        section_source.append(source_name)
    # Add the last section, including any remaining characters
    sections.append(document_text[start:])
    section_source.append(source_name)

    return [sections,section_source]


def initialize_collection_from_documents(collection_name, document_tuple, persist_path = "testerdb") -> chromadb.Client:
    """
    Creates a collection from a document tuple on a specific path.

    Args:
        collection_name(str): The name of the collection
        document_tuple(tuple(List[str],List[str)]): The tuple with the documents and their sources
        persist_path(str): the path to the database for persisting

    Returns:
        object: The collection from the documents
    """    
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=persist_path # Optional, defaults to .chromadb/ in the current directory
    ))
    documents = document_tuple[0]
    sources = document_tuple[1]
    iterator = 0

    collection = client.create_collection(collection_name, embedding_function=get_openai_embedding_function())
    for document in documents:
            success = add_document_to_collection(collection,document,sources[iterator])
            iterator += 1
            if iterator % 10 == 0:
                print("Number of iterations: {} out of {}".format(iterator,len(sources)))
    print("done")
    client.persist()
    return client


def get_openai_embedding_function() -> embedding_functions.OpenAIEmbeddingFunction:
    """
        Gets the embedding function for openAI embeddings
    Returns:
        object: The openai embedding function
    """    
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=key,
    model_name="text-embedding-ada-002")
    return openai_ef


def retrieve_collection(collection_name, persist_path):
    """
        Gets the collection stored at a name and certain path
    Returns:
        object: the chromadb collection
    """
    try:
            
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_path # Optional, defaults to .chromadb/ in the current directory
        ))
        collection = client.get_collection(name=collection_name, embedding_function=get_openai_embedding_function())
        return collection
    except:
        return None



def createCollection(client, name, embdf = None):
    collection = client.create_collection(name, embedding_function= embedding_functions.OpenAIEmbeddingFunction(api_key=key,  model_name="text-embedding-ada-002"))
    return collection

#Use this with loaded documents to return a List of 

def create_message(message_list,role, content) -> list[object]:
    new_message = {"role": role, "content": content}
    message_list.append(new_message)
    return message_list

#TODO clean algobook and write this into a gpt-3.5 lib test. Then create prompt injection, and build prompt, and test performance against v 1.0
def complete_text(message, inputTemp=0):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens= 1000,
        temperature=inputTemp,
        messages=message)
    return response
    
#For the documents, create a splitter that takes text and puts it into a list of 150 characters per list. Langchain does this well copy their code

#From there make a function that builds a new document list by taking the two most similar and then removing them both from the database
def generate_prompt(collection, user_question):
    results = get_query_result(collection, user_question, 1)
    unwrapped = unwrap_query_text(results)
    examples = ""
    for strung in unwrapped:
        examples+= strung

    prompt = """
    Pretend to be an AI language model trying to answer algorithm questions. Use primarily the following data in this prompt, but if it is not sufficient use your outside resources to answer. Make sure to indicate whether or not external resources were used. Answer by notating steps rather than writing paragraphs
    Context:
    {}

    Now, answer the following question: "{}"
    """.format(examples, user_question)
    return prompt


def store_qa_in_collection(collection, query, answer):
    storable = query + "\n\n ANSWER: " + answer
    added = add_document_to_collection(collection, storable, "prompted_answer")
    print(added)
    


def __main__():
    print("Hello")
    with open("final_txt.txt", 'r') as file:
        file_contents = file.read()
    splitted = split_file_into_sections(file_contents, "Algorithms textbook", 1000, 0)
    collection_name = "algo_collection"
    persist_path = "algo path"

def testLister():
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="tester2" # Optional, defaults to .chromadb/ in the current directory
    ))
    functios = get_openai_embedding_function()

    client.create_collection("N2amed", embedding_function=functios)
    #print(client.list_collections())


#def listCollections(client):


#     query = """
# Your current location is represented by a coordinate pair (x, y). You are given an
# array, A, with N coordinate points labeled (xi
# , yi) for i = 1 to N. Find the k farthest spots from
# (x, y) in terms of Euclidean distance. Assume that k < N.
# (a) (15 points) Use a divide and conquer approach to find the k farthest spots from (x, y). We
# expect the average-case runtime to be better than O(n log n).

# Use a quick select algorithm and explain the runtime
# """
#     collection = retrieve_collection(collection_name, persist_path)
#     #collection = initialize_collection_from_documents(collection_name, splitted, persist_path)
#     prompt = generate_prompt(collection, query)
#     messages = []
#     message = create_message(messages, "user", prompt)
#     response = complete_text(message)
#     print(response.choices[0].message.content)

    # collection = retrieve_collection(collection_name, persist_path)
    # q_result = get_query_result(collection, "This is a test", 2)
    # unwarpped = unwrap_query_results(q_result)
    # for wrapped in unwarpped:
    #     print(wrapped + "\n\n ====================END==================== \n\n\n")


# test_splitter()

#TODO. Create a new databse of questions ans aswers, run query testing to see what comes up. Redesign prompt to make it so the prompt is beter with Concept combination.

#TEST PASSED, new DB Stuture good

#TODO
"""

create a rename function







REDO THE ID system so you can delete documents


Create a getcollections function

create a getdocuments function from a collection

Create a deleteDocument from collection function

"""