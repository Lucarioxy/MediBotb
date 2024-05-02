from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv
from langchain import PromptTemplate

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def query_output(query,docsearch):
    retriever = docsearch.as_retriever()
    llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages= True)
    chain = ConversationalRetrievalChain.from_llm(llm, retriever= retriever, memory= memory)
    return chain.invoke({'question': query})

def context_summary(docsearch):
    llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")
    retriever = docsearch.as_retriever()
    map_prompt = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
    combine_prompt = """
    Write a concise summary of the following text delimited by triple backquotes.
    Return your response in bullet points which covers the key points of the text.
    ```{text}```
    BULLET POINT SUMMARY:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])
    summary_chain = load_summarize_chain(llm=llm,
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,
                                     retriever=retriever
                                    )
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    summary = chain.run()
    print(summary)
