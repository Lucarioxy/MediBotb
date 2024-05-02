from llama_parse import LlamaParse
import os
from dotenv import load_dotenv

load_dotenv()

LLAMA_PARSE_KEY = os.getenv('LLAMA_PARSE_KEY')
LLAMA_PARSE_KEY_ALT = os.getenv('LLAMA_PARSE_KEY_ALT')

def process_pdf(file_path):
        parsingInstruction = """The provided document contains medical documents of various types.
        It contains papers, precriptions, medical data of a patient, and other such details integral to
        understanding the medical information of a patient
        """
        parser = LlamaParse(api_key=LLAMA_PARSE_KEY,
                            result_type="markdown",
                            parsing_instruction=parsingInstruction,
                            max_timeout=10000,)
        loaded_documents = parser.load_data(file_path)[0].text
        return loaded_documents
