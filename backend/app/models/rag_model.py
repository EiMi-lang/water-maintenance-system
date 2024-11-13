from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

openai_api_key = 'sk-5L8TC5pRmukw7xyE52C75f19961f4d49Aa6aA3Db26E9C1B4'
openai_api_base = 'https://api.aigc369.com/v1'


def generate_rag_response(question):

    # 选择模型
    model = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=openai_api_key,
        openai_api_base=openai_api_base
                       )
    # 加载文档
    raw_documents = TextLoader('scripts/data/files/device_report.txt', encoding='utf-8').load()
    # 文档切分实例
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
    )
    # 切分文档
    documents = text_splitter.split_documents(raw_documents)
    # 嵌入器
    underlying_embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base
    )
    # 向量存储
    db = FAISS.from_documents(documents, underlying_embeddings)
    # 构建检索器
    retriever = db.as_retriever()
    # 构建检索增强生成数据链
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
    )
    invoked = qa.invoke({"chat_history": [],"question": question})
    return invoked
