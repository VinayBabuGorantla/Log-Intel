from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.memory import ConversationBufferMemory
from src.config.logger import setup_logger
from src.exception.custom_exception import QAFailure

logger = setup_logger(__name__)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
MODEL_NAME = "google/flan-t5-small"

def get_llm_pipeline():
    try:
        llm_pipe = pipeline("text2text-generation", model=MODEL_NAME, max_length=512)
        logger.info("LLM loaded successfully.")
        return HuggingFacePipeline(pipeline=llm_pipe)
    except Exception as e:
        logger.error(f"LLM load failed: {e}")
        raise QAFailure(str(e))

def ask_question(vector_store, question: str):
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        qa = ConversationalRetrievalChain.from_llm(
            llm=get_llm_pipeline(), retriever=retriever, memory=memory
        )
        return qa.run(question)
    except Exception as e:
        logger.error(f"QA failed: {e}")
        raise QAFailure(str(e))
