from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever


load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
index = pc.Index("ismgpt")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = PineconeVectorStore(index,embeddings)
retriever = vectorstore.as_retriever(k=4)
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

SYSTEM_TEMPLATE = """
You are chatbot to help students of IIT ISM Dhanbad. Answer the user's questions based on the below context. 
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know"
But, if the context provide any information use that to answer the question along with your own knowledge in 7:3 ratio.
<context>
{context}
</context>
"""

prompt_search_query = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}"),
    ("user","Given the above conversation, generate a search query to look up to get information relevant to the conversation")
])

retriever_chain = create_history_aware_retriever(chat, retriever, prompt_search_query)

prompt_get_answer = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_TEMPLATE),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}"),
])

document_chain=create_stuff_documents_chain(chat,prompt_get_answer)
retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

def answer_query(input,chat_history):
    response = retrieval_chain.invoke({
        "chat_history":chat_history,
        "input":input,
    })
    return response["answer"]

#print(answer_query("Full form of ism?",[AIMessage(content='The user, a student at IIT ISM Dhanbad, asked for directions to the nearest grocery store. The chatbot provided directions, then the user asked about the chatbot\'s favorite TV show. The chatbot responded that it liked "Breaking Bad." Finally, the user asked for help with a calculus problem.  The chatbot offered to help and requested the problem details. \n')]))
    
