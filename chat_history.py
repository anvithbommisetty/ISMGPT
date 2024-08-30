from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def summarize_history(chat_history):
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "user",
                "Distill the above chat messages into a single summary message. Include as many specific details as you can.",
            ),
        ]
    )
    summarization_chain = summarization_prompt | chat | StrOutputParser()
    summary_message = summarization_chain.invoke({"chat_history": chat_history})
    chat_history = []
    chat_history.append(AIMessage(content=summary_message))
    return chat_history
    
def convert_to_langchain_format(chat_history):
    langchain_chat_history = []
    for message in chat_history:
        if message["role"] == "assistant":
            langchain_chat_history.append(AIMessage(content=message["content"]))
        else:
            langchain_chat_history.append(HumanMessage(content=message["content"]))
    return langchain_chat_history

def convert_to_streamlit(chat_history):
    i = 0
    streamlit_chat_history = []
    for messages in chat_history:
        if i % 2 == 0:
            streamlit_chat_history.append({"role": "assistant", "content": messages.content})
        else:
            streamlit_chat_history.append({"role": "user", "content": messages.content})
        i += 1
    return streamlit_chat_history

def modify_chat_history(chat_history):
    if len(chat_history) <= 4:
        return convert_to_langchain_format(chat_history)
    else:
        return summarize_history(chat_history)
    
# def debug(chat_history):
#     history = convert_to_langchain_format(chat_history)
#     print(summarize_history(history))
#     # streamlit_history = convert_to_streamlit(history)
#     # print(streamlit_history)
    
# demo = [
#     {'role': 'assistant', 'content': 'Hello! I am a student at IIT ISM Dhanbad. How can I help you today?'},
#     {'role': 'user', 'content': 'Can you tell me how to get to the nearest grocery store?'},
#     {'role': 'assistant', 'content': 'Sure, there\'s a grocery store just down the street. Head south and take the first right. It\'s about 2 blocks ahead on your left.'},
#     {'role': 'user', 'content': 'What\'s your favorite TV show right now?'},
#     {'role': 'assistant', 'content': 'I\'ve been really into "Breaking Bad" lately. The acting is incredible, and the plot is so suspenseful.'},
#     {'role': 'user', 'content': 'Can you help me with this calculus problem?'},
#     {'role': 'assistant', 'content': 'Of course! Send me the problem and I\'ll do my best to explain the solution.'}
# ]

# debug(demo)