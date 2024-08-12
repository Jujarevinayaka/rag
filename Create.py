#######################################################################################
##                                        Create                                     ##
##                                                                                   ##
##  Description: This is used to create the documents and the vector DB used for     ##
##               customizing the LLM.                                                ##
##  Author: Vinayaka Jujare                                                          ##
##  Usage: Just execute the file with the appropriate options                        ##
##      python Create.py --create_doc True --create_db True                          ##                                              ##
#######################################################################################

import os
import time
import logging
import argparse

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

logger = logging.getLogger('run.log')
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename='run.log',
    encoding='utf-8', level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',)


class DOCUMENTS:
    """Handle all the document creation functions."""
    def __init__(self):
        """
        Init function for the DOCUMENTS class.
        """
        # Path where all the documents are stored
        self.main_doc_dir = os.getcwd() + "/documents/"
        if not os.path.isdir(self.main_doc_dir):
            logger.debug("Creating folder <{}> to store documents".format(self.main_doc_dir))
            os.makedirs(self.main_doc_dir)

        # Path where all the context based documents are stored.
        self.ctx_doc_dir = self.main_doc_dir + "/domain_context/"
        if not os.path.isdir(self.ctx_doc_dir):
            logger.debug("Creating folder <{}> to store context specific documents".format(self.ctx_doc_dir))
            os.makedirs(self.ctx_doc_dir)

        # Path where all the sample feedback-response documents are stored.
        self.fbr_doc_dir = self.main_doc_dir + "/sample_feedback/"
        if not os.path.isdir(self.fbr_doc_dir):
            logger.debug("Creating folder <{}> to store feedback-response specific documents".format(self.fbr_doc_dir))
            os.makedirs(self.fbr_doc_dir)

        # Path where custom feedback-responses document is stored
        self.custom_feedback_doc = self.fbr_doc_dir + "custom_feedback.txt"

        logger.debug("Main Documents dir - {}".format(self.main_doc_dir))
        logger.debug("Domain context documents dir - {}".format(self.ctx_doc_dir))
        logger.debug("Feedback-response documents dir - {}".format(self.fbr_doc_dir))
        logger.debug("Custom Feedback-response document file - {}".format(self.custom_feedback_doc))

    def __get_docs_from_web(self, url):
        """
        Parse the web and return the content for the documents.

        @return: return the content of the web page parsed.
        """
        # Set up Edge options
        options = Options()
        options.use_chromium = True

        # Initialize the Edge driver
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

        # Open the URL
        logger.debug("Opening the URL - {}".format(url))
        driver.get(url)

        # Give the page some time to load
        sleep_for = 5
        logger.debug("Waiting for {}sec for the URL to load".format(sleep_for))
        time.sleep(sleep_for)

        # Extract the textual content
        text = driver.find_element(By.TAG_NAME, 'body').text

        # Remove repeated header
        text = "\n".join(text.split("\n")[4:])

        # Close the driver
        driver.quit()

        logger.debug("Done parsing the URL - {}".format(url))
        return text
    
    def _url_docs(self):
        """
        Process the URLs and create documents out of them.
        """
        # These URLs contain all the relevant information on ctruh, which can be used to give domain_context for the LLM.
        urls = ["https://ctruhtech.notion.site/Scheduling-a-Demo-9e1166c8d24246eb80ef3efcdaaf07b6?pvs=25",
                "https://ctruhtech.notion.site/Dashboard-Overview-8f3bc3ac26cd4a0096d53931945155dd?pvs=25",
                "https://ctruhtech.notion.site/How-to-Sign-in-to-Ctruh-6b1a546dda96499ba6f2ff95d4ef4ab1?pvs=25",
                "https://ctruhtech.notion.site/Sign-up-using-your-Email-ID-and-Phone-number-bcbad713817f4ed2bd186483a6c08474?pvs=25",
                "https://ctruhtech.notion.site/Sign-up-using-Social-accounts-da9040ac7a2342ff98b7488857e8cb98?pvs=25",
                "https://ctruhtech.notion.site/How-to-Create-a-New-Scene-b99d01067d704beaaaee7bd3776fdb5e?pvs=25",
                "https://ctruhtech.notion.site/Customising-Ctruh-Editor-1ea5824d93f24e4dbae90cb846b5a8e8?pvs=25",
                "https://ctruhtech.notion.site/Previewing-the-Scene-9759d53b4fe44963a6c0c5271f35ee90?pvs=25",
                "https://ctruhtech.notion.site/Syncing-your-Project-8896d739b37f48fc823bf4bc63860b5d?pvs=25",
                "https://ctruhtech.notion.site/How-to-Rename-Delete-and-Edit-the-Project-67fdbe20e7a1484abe69ddd7fb74f060?pvs=25",
                "https://ctruhtech.notion.site/Understanding-the-Assets-Panel-38e0b6653eb34e9d97160a1a07a2da66?pvs=25",
                "https://ctruhtech.notion.site/Undo-Redo-0528b54224dc4e1b8a8f9126f39d8d34?pvs=25",
                "https://ctruhtech.notion.site/3D-Shapes-a4007f2e592a4303a7fb22b454793287?pvs=25",
                "https://ctruhtech.notion.site/Hotspots-Camera-b3da172c57e34d3badc513352e64b178?pvs=25",
                "https://ctruhtech.notion.site/Point-Light-45ebe22b91e84719934c255e84cef918?pvs=25",
                "https://ctruhtech.notion.site/Spatial-Audio-1a4221fea7e44c67bb86fb1ae241d84e?pvs=25",
                "https://ctruhtech.notion.site/3D-Text-0c74ee07e8fd4c91803d6fd2d8a5df5c?pvs=25",
                "https://ctruhtech.notion.site/Spotlight-5ab3d86f089845bab88812546ac094b6?pvs=25",
                "https://ctruhtech.notion.site/Directional-Light-91a40e71f9a34cd9a2b8e0ad80f9829b?pvs=25",
                "https://ctruhtech.notion.site/Screens-c38dc92b1ac64eff9178da5d5890a8c8?pvs=25",
                "https://ctruhtech.notion.site/Uploading-a-GLB-0a16f9ec3cab49d58ede08fe9e06d874?pvs=25",
                "https://ctruhtech.notion.site/Uploading-a-Spatial-Audio-1b9f8e1aeaae46679a72903d1d04fb8a?pvs=25",
                "https://ctruhtech.notion.site/Uploading-a-video-as-a-Screen-3c171dd3e5064038b55bc98644fdf17f?pvs=25",
                "https://ctruhtech.notion.site/Uploading-a-360-degree-Background-Image-ca0f1c68b357449dbcf0f87f454faf4b?pvs=25",
                "https://ctruhtech.notion.site/Uploading-Image-as-a-Screen-10b6cab888e141dfa81c233f1a940995?pvs=25",
                "https://ctruhtech.notion.site/Adding-Object-Templates-2f29fd8bf5934cbd87cc52de8a355471?pvs=25",
                "https://ctruhtech.notion.site/Adding-Audio-from-Asset-Library-e3e23f0cd3874536a06629c94e10c6b0?pvs=25",
                "https://ctruhtech.notion.site/Connecting-Sketchfab-Account-5e77934372f345199bf5a0ad36c63f2b?pvs=25",
                "https://ctruhtech.notion.site/Adding-a-Scene-Template-85c76cee04574f9baf63b7de8255311b?pvs=25",
                "https://ctruhtech.notion.site/Adding-uploaded-Assets-to-the-Scene-61e816c1f0454a4ebe711bf14eb25450?pvs=25",
                "https://ctruhtech.notion.site/Sketchfab-Integration-Features-28fde93fa98e49ac862b454015564f5e?pvs=25",
                "https://ctruhtech.notion.site/Publishing-a-Project-1ebf6d38a1e649c1b39b4134adde86c4?pvs=25",
                "https://ctruhtech.notion.site/Downloading-Scene-as-Image-94f5b29c684c4da8bf1ff2e629a5f6fe?pvs=25",
                "https://ctruhtech.notion.site/Publishing-an-XR-Experience-0cc1af628936456b9b46cf08fa50250c?pvs=25",
                "https://ctruhtech.notion.site/Downloading-the-Project-as-GLB-440db156def44d6db1f1191a52a6cc5e?pvs=25"]

        for url in urls:
            # For each URL, get the text content
            logger.info("Picked up URL - {}".format(url))
            text = self.__get_docs_from_web(url)
            # Get the name of the file to store the doc content
            file_name = text.split("\n")[0] + ".txt"
            # Dump the textual content into a doc file
            with open(self.ctx_doc_dir + "/" + file_name, 'w') as fp:
                fp.write(text)

            logger.info("Done creating document - {}".format(file_name))

    def _feedback_doc(self):
        """
        Create doc with custom user feedback and the responses from the LLM to refer
        """
        data = [
            (
                "Feedback: I loved creating my first 3D scene using Ctruh! The dashboard was so easy to navigate.",
                "Response: That's fantastic to hear! We're glad you enjoyed the process.",
            ),
            (
                "Feedback: I love the new color picker feature in Ctruh! It makes choosing colors so much easier.",
                "Response: We're thrilled you like it! Our team worked hard to make it user-friendly and fun to use. If you have any suggestions on how we can improve it, please let us know!",
            ),
            (
                "Feedback: I love how customizable Ctruh is! I was able to change the screen orientation and aspect ratio to fit my needs.",
                "Response: That's one of our favorite features too! We're glad you found it helpful.",
            ),
            (
                "Feedback: I love using Ctruh for my projects! The community support is amazing.",
                "Response: We're so glad to hear that! Our community is a big part of what makes Ctruh special. We're always here to help and support each other in our creative endeavors.",
            ),
            (
                "Feedback: The dashboard is very intuitive!",
                "Response: We're glad you found the dashboard easy to use! Our team worked hard to make it user-friendly.",
            ),
            (
                "Feedback: I love the new scene creation feature!",
                "Response: Thank you for trying out our new scene creation feature! We're happy to hear that it's working well for you.",
            ),
            (
                "Feedback: The 3D text properties panel is really helpful!",
                "Response: We're glad you found the 3D text properties panel useful! It was designed to make it easy to customize your text.",
            ),
            (
                "Feedback: I had trouble finding the reset button.",
                "Response: Sorry to hear that you had trouble finding the reset button. Can you tell us more about what happened? We'll do our best to help you out.",
            ),
            (
                "Feedback: The documentation is not clear",
                "Response: Sorry to hear that. We are constantly working on improvements in our documentation, can you tell us more about what was not clear? We'll do our best to help you out.",
            ),
            (
                "Feedback: The website is slow to load.",
                "Response: We apologize for the slow website performance. Our team is constantly working to improving load times. Can you check your internet connectivity is reliable?",
            ),
        ]

        # Dump the feedback data into a doc file
        logger.info("Started writing custom feedback data")
        with open(self.custom_feedback_doc, 'w') as fp:
            for i in data:
                for j in i:
                    fp.write(j + '\n')
                fp.write('\n')

        logger.info("Done creating document - {}".format(self.custom_feedback_doc))

    def create_documents(self):
        """
        Create documents for the LLM to be fine-tuned.
        """
        self._url_docs()
        self._feedback_doc()


class VECTORDB():
    """handle all Vector DB creation functionalities."""
    def __init__(self, main_doc_dir):
        """
        Init function of VECTORDB class.
        """
        # Path where the VectorDB is created
        self.db_dir = os.getcwd() + "/vectordb/"
        if not os.path.isdir(self.db_dir):
            logger.debug("Creating folder <{}> to store vector DB".format(self.db_dir))
            os.makedirs(self.db_dir)

        # path where the documents are present
        self.main_doc_dir = main_doc_dir
        # vectorstore object returned
        self.vectorstore = None
        # LLM to be used
        self.llm = "llama3.1"

    def create_vector_db(self):
        """
        Create vector DB by updating the LLM with the relevant documents.
        """
        # Load documents from a directory
        loader = DirectoryLoader(self.main_doc_dir, glob="**/*.txt")
        documents = loader.load()
        logger.debug("Loaded all the files under {}".format(self.main_doc_dir))

        # Create embeddings
        embeddings = OllamaEmbeddings(model=self.llm, show_progress=True)
        logger.debug("Created embeddings for {}".format(self.llm))

        # Split texts recursively
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            add_start_index=True,
        )

        # Split documents into chunks
        texts = text_splitter.split_documents(documents)
        logger.debug("Split documents: \n{}".format(texts))

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=texts, 
            embedding= embeddings,
            persist_directory=self.db_dir
        )

        logger.info("Done creating vectorDB - {}".format(self.db_dir))


if __name__ == "__main__":
    # Parse the arguments passed
    parser = argparse.ArgumentParser(description='Create document corpus and vectorDB used to update a local LLM.')
    parser.add_argument('--create_doc', default=False,
                        help='Create document corpus (default: false)',
                        type=bool)
    parser.add_argument('--create_db', default=False,
                        help='Create vectorDB (default: false)',
                        type=bool)
    args = parser.parse_args()

    # Create the class objects
    doc_obj = DOCUMENTS()
    vec_obj = VECTORDB(main_doc_dir=doc_obj.main_doc_dir)
    if args.create_doc is True:
        doc_obj.create_documents()
    if args.create_db is True:
        vec_obj.create_vector_db()
