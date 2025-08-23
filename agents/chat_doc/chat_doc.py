import os
import dotenv
from langchain.retrievers import MultiQueryRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_chroma import Chroma
from langchain_community.document_compressors import LLMLinguaCompressor

from langchain_community.document_loaders import UnstructuredExcelLoader, Docx2txtLoader, PyPDFLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter

dotenv.load_dotenv()

embedding_model = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("BL_API_KEY"),
)

llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=os.getenv("OR_API_KEY"),
    base_url=os.getenv("OR_BASE"),
    temperature=0
)


class ChatDoc():
    def __init__(self):
        self.doc = None
        self.split_text = []  # 存储分割后的文本

    def get_file(self):
        """
        加载文件内容
        """
        doc = self.doc
        loaders = {
            "docx": Docx2txtLoader,
            "pdf": PyPDFLoader,
            "xlsx": UnstructuredExcelLoader,
        }

        file_extension = doc.split('.')[-1]
        loader_class = loaders.get(file_extension)
        if loader_class:
            try:
                loader = loader_class(doc)
                text = loader.load()
                return text
            except Exception as e:
                print(f"Error loading {file_extension} files: {e}")
        else:
            print(f"Unsupported file extension: {file_extension}")
        return None

    def split_sentences(self):
        """
        处理文档
        """
        full_text = self.get_file()
        if full_text:
            # 对文档进行分割
            text_split = CharacterTextSplitter(
                chunk_size=50,
                chunk_overlap=20,
            )
            texts = text_split.split_documents(full_text)
            self.split_text = texts

    def embedding_doc(self):
        """
        向量化
        """
        db = Chroma.from_documents(
            documents=self.split_text,
            embedding=embedding_model,
        )
        return db

    def ask_chat_bot(self, question: str):
        """
        进行提问
        Args:
            question: 问题

        Returns:
            LLM的回答
        """
        db = self.embedding_doc()
        retriever = db.as_retriever()

        # 相似度搜索
        # retriever = db.as_retriever(search_type="mmr")

        # 1 原生的retriever
        # retriever_from_llm = MultiQueryRetriever.from_llm(
        #     retriever=retriever,
        #     llm=llm,
        # )

        # 2 使用上下文压缩器
        # 2.1 从llm中提取压缩器
        compressor = LLMChainExtractor.from_llm(
            llm=llm
        )
        # 2.2 创建上下文压缩检索器
        compressor_retriever = ContextualCompressionRetriever(
            base_retriever=retriever,
            base_compressor=compressor,
        )

        # return retriever_from_llm.invoke(question)
        return compressor_retriever.invoke(question)


if __name__ == '__main__':
    chat_doc = ChatDoc()
    chat_doc.doc = "doc.pdf"
    chat_doc.split_sentences()
    # print(chat_doc.split_text)
    unique_doc = chat_doc.ask_chat_bot("高速公路上逆行扣多少分?")
    print(unique_doc)
