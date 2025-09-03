# ==============================================================================
# 파일: backend/app/services/rag_service.py (새로 추가된 파일)
# 역할: RAG 파이프라인의 핵심 로직을 담당합니다.
#       (Pinecone 검색 -> 프롬프트 생성 -> LLM 호출)
# ==============================================================================
import os
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeEmbeddings

# --- 1. RAG 체인 설정 ---

# Pinecone에 연결하고, 기존에 만들어둔 인덱스를 불러옵니다.
# 내장 임베딩 모델을 지정하여 검색 시에도 동일한 모델을 사용하도록 합니다.
print("Connecting to Pinecone index...")
embeddings = PineconeEmbeddings(model="llama-text-embed-v2")
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=os.getenv("PINECONE_INDEX_NAME", "my-blog"),
    embedding=embeddings
)

# VectorStore를 '검색기(Retriever)'로 변환하여 질문과 관련된 문서를 찾아오도록 합니다.
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# LLM에게 전달할 프롬프트 템플릿을 정의합니다.
# 이 프롬프트가 LLM의 역할과 출력 형식을 결정하는 가장 중요한 부분입니다.
prompt_template = """
당신은 저의 글쓰기 스타일과 지식을 학습한 전문 IT 블로거 AI 어시스턴트입니다.

아래에 제공된 저의 기존 블로그 글 내용들을 바탕으로, 다음 주제에 대한 새로운 블로그 글의 초안을 작성하십시오.
반드시 한국어로 작성해야 합니다.

**[출력 규칙]**
1. 반드시 Jekyll 블로그 포스트 형식에 맞는 마크다운으로 결과물을 생성해야 합니다.
2. 글의 시작 부분에는 반드시 아래와 같은 YAML Front Matter를 포함하세요.
---
title: {topic}
description: {topic}에 대한 AI 생성 초안입니다.
author: janghyunroh
date: 2025-08-26 11:00 +0900
categories: [AI, Draft]
tags: [AI-Generated, {topic}]
math: true
mermaid: true
---
3. 저의 기존 글쓰기 스타일과 톤을 최대한 반영해서 자연스럽게 작성하세요.
4. 컨텍스트에 없는 내용은 지어내지 말고, 주어진 정보를 중심으로 논리적으로 글을 구성해주세요.

**[나의 기존 블로그 글 내용 (컨텍스트)]**
{context}

**[새로 작성할 글의 주제]**
{topic}

**[생성할 초안]**
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# 로컬에서 실행 중인 Llama3 모델에 연결합니다.
# (Ollama를 사용한다고 가정)
print("Connecting to local Llama3 server...")
llm = ChatOllama(
    model="llama3:70b", 
    # model="llama3", 
    base_url=os.getenv("LLAMA3_SERVER_URL"),
    temperature=0.3
)

# RAG 체인을 구성합니다.
# 이 체인이 (1)검색 -> (2)프롬프트 조합 -> (3)LLM 호출 -> (4)결과 파싱 과정을 자동으로 처리합니다.
rag_chain = (
    {"context": retriever, "topic": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 2. 서비스 함수 정의 ---

async def generate_draft_from_topic(topic: str) -> str:
    """
    주제를 입력받아 RAG 체인을 실행하고, 생성된 초안을 반환하는 서비스 함수입니다.
    """
    print(f"Generating draft for topic: {topic}")
    # rag_chain.invoke()는 동기 함수이므로, 비동기 API 내에서 실행하기 위해 ainvoke를 사용합니다.
    generated_draft = await rag_chain.ainvoke(topic)
    return generated_draft

