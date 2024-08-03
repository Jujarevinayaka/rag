import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


class VECTORDB():
    def __init__(self):
        self.db_dir = os.getcwd() + "/vectordb/"
        self.doc_dir = os.getcwd() + "/documents/"
        self.vectorstore = None

        if not os.path.isdir(self.db_dir):
            os.makedirs(self.db_dir)

    def create_vector_db(self):
        """
        Create vector DB which is fine tuned with the documents provided
        """
        # Load documents from a directory
        loader = DirectoryLoader(self.doc_dir, glob="**/*.txt")
        documents = loader.load()

        # Create embeddings
        embeddings = OllamaEmbeddings(model="llama3.1", show_progress=True)

        # Split texts recursively
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300,
            add_start_index=True,
        )

        # Split documents into chunks
        texts = text_splitter.split_documents(documents)

        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=texts, 
            embedding= embeddings,
            persist_directory=self.db_dir
        )

        print("vectorstore created")

if __name__ == "__main__":
    vec_obj = VECTORDB()
    vec_obj.create_vector_db()
