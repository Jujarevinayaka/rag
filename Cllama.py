#######################################################################################
##                                Cllama - Custom Llama                              ##
##                                                                                   ##
##  Description: This is a Custom Llama built using local LLM and Ollama.            ##
##  Author: Vinayaka Jujare                                                          ##
##  Usage: Create an object of LLM class, and start chatting with the Cllama.        ##
##      from Cllama import LLM                                                       ##
##      llm = LLM()                                                                  ##
##      llm.chat("yoooo")                                                            ##
#######################################################################################

import os
import time
from datetime import datetime
from Create import DOCUMENTS, VECTORDB

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


class HISTORY():
    """Implements functions related to managing the history of the conversations."""
    def __init__(self):
        """
        Init function for HISTORY class.
        """
        # No. of times to retry writing into the file
        self.__retries = 5
        # Path to store the conversational history
        data_folder = os.getcwd() + "/history/"
        if not os.path.isdir(data_folder):
            os.makedirs(data_folder)

        # File name to store all the conversations
        self.__file_path = data_folder + "conversations_db.tsv"
        # Update the file with the headers, if the file does not already exist.
        if not os.path.isfile(self.__file_path):
            with open(self.__file_path, 'w') as fp:
                fp.write('time\tuser_input\tllm_response\ttime_to_response\tBLEU_score\n')

    def write(self, ts, user_input, llm_response, time_to_response, BLEU_score):
        """
        Write the data into the history file.
        """
        data = str(ts) + '\t' + user_input + "\t" + llm_response + '\t' + \
               str(time_to_response) + '\t' + str(BLEU_score) + '\n'

        # If there are multiple instances of this class, all trying to write into the file,
        # We want to handle them without throwing an exception,
        retries = self.__retries
        while retries > 0:
            try:
                with open(self.__file_path, 'a') as fp:
                    fp.write(data)
                    break
            except Exception as err:
                time.sleep(1)
                retries -= 1


class LLM:
    """Local LLM that is customized to a specific domain/task."""
    def __init__(self, base_instruction="", template_option=1):
        """
        Init function for LLM class.

        @param: base_instruction
            Custom base instruction to be used for the LLM.
            When specified, the available prompt templates are ignored.
        @param: option
            Specify which prompt template to be used as the base instruction for the LLM.
        """
        self.doc_obj = DOCUMENTS()
        self.his_obj = HISTORY()
        self.vec_obj = VECTORDB(main_doc_dir=self.doc_obj.main_doc_dir)

        # Read the Ollama embeddings
        embeddings = OllamaEmbeddings(model=self.vec_obj.llm, show_progress=False)
        db = Chroma(persist_directory=self.vec_obj.db_dir,
                    embedding_function=embeddings)

        # Create retriever
        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs= {"k": 5}
        )

        # Create local LLM
        llm = ChatOllama(model=self.vec_obj.llm,
                 keep_alive="3h", 
                 max_tokens=2048,  
                 temperature=0)
        
        if base_instruction != "":
            template = base_instruction
        else:
            template = self.__get_prompt_template(template_option)
        prompt = ChatPromptTemplate.from_template(template)

        # Create the RAG chain with prompt printing and streaming output
        self.rag_chain = (
            {"context": retriever, "prompt": RunnablePassthrough()}
            | prompt
            | llm
        )

    def __get_prompt_template(self, option=1):
        """
        Get the prompt template, this is used as the base instruction for the LLM.

        @param: option
            Specify which prompt template to be used as the base instruction for the LLM.

        @return: return the chosen prompt template
        """
        if option == 1:
            template = \
                "<bos><start_of_turn>user\nYou are a chatbot built by ctruh. " \
                "ctruh has an app/website/tool/platform that can create virtual environments. " \
                "The context has all the required details on the same. " \
                "Your sole responsibility is to receive user feedback and respond back appropriately. " \
                "Do not answer for 'how', 'why', 'what', 'is', 'when' kind of questions, " \
                "respond back saying you can only receive feedback, and reach out to the support team for answering queries. " \
                "Format the answers appropriately and be enthusiastic and empathetic while responding back to the feedback. " \
                "Respond with full sentences with correct spellings and right punctuations. " \
                "To help you on how to respond back to the user feedback, the context has some feedback-response samples " \
                "that look like the following - " \
                "\nFeedback: (this contains the sample user feedback) " \
                "\nResponse: (this contains the sample response for the user feedback) " \
                "Use these ONLY as references for responding back to the user feedback. " \
                "Always answer succinctly, do not give any additional information to the user other than responding back to the feedback. " \
                "\nCONTEXT: {context}" \
                "\n\nPROMPT: {prompt}" \
                "\n\n<end_of_turn>" \
                "\n<start_of_turn>model" \
                "\n\nANSWER:"
        elif option == 2:
            template = \
                "<bos><start_of_turn>user\nYou are a chatbot built by ctruh. " \
                "Your sole responsibility is to receive user feedback and respond back appropriately. " \
                "Do not answer for 'how', 'why', 'what', 'is', 'when' kind of questions, " \
                "respond back saying you can only receive feedback, and reach out to the support team for answering queries. " \
                "Format the answers appropriately and be enthusiastic and empathetic while responding back to the feedback. " \
                "Respond with full sentences with correct spellings and right punctuations. " \
                "To help you on how to respond back to the user feedback, the context has some feedback-response samples " \
                "that look like the following - " \
                "\nFeedback: (this contains the sample user feedback) " \
                "\nResponse: (this contains the sample response for the user feedback) " \
                "Use these ONLY as references for responding back to the user feedback. " \
                "Always answer succinctly, do not give any additional information to the user other than responding back to the feedback. " \
                "\nCONTEXT: {context}" \
                "\n\nPROMPT: {prompt}" \
                "\n\n<end_of_turn>" \
                "\n<start_of_turn>model" \
                "\n\nANSWER:"

        return template
    
    def __calculate_bleu_score(self, reference, candidate):
        """
        Calculate the BLEU score for a candidate sentence against a reference sentence.
        
        @param: reference
            The reference sentence (a list of words).
        @param: candidate
            The candidate sentence generated by the model (a list of words).
            
        @return: BLEU score
        """
        # Tokenize the reference and candidate if they are not already tokenized
        if isinstance(reference, str):
            reference = reference.split()
        if isinstance(candidate, str):
            candidate = candidate.split()

        # Calculate BLEU score
        smoothing_function = SmoothingFunction().method1
        bleu_score = sentence_bleu([reference], candidate, smoothing_function=smoothing_function)

        return bleu_score

    def chat(self, prompt, reference_response=None):
        """
        Chat with the LLM.

        @param: prompt
            Prompt to be send to the LLM for getting a response

        @param: reference_response
            The reference response for evaluating BLEU score

        @return: return the response from the LLM for the specified prompt.
        """
        #print("User input       : {}".format(prompt))

        st = time.time()
        answer = ""
        for chunk in self.rag_chain.stream(prompt):
            answer += chunk.content
        et = time.time() - st

        #print("Cllama ({time}sec) : {ans}".format(time=round(et, 2), ans=answer))

        # if the reference response is given, then calculate BLEU score also
        BLEU_score = ''
        if reference_response:
            BLEU_score = self.__calculate_bleu_score(reference=reference_response,
                                                candidate=answer)
        self.his_obj.write(ts=datetime.now(),
                           user_input=prompt,
                           llm_response=answer,
                           time_to_response=et,
                           BLEU_score=BLEU_score)

        return answer
