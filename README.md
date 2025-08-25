# P.A.G.E. (Personalized Article Generation Engine)

**나의 글쓰기 과정을 자동화하기 위해 시작한 개인 AI 프로젝트, P.A.G.E.를 소개합니다.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flutter](https://img.shields.io/badge/Frontend-Flutter-blue)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com/)

---

## 📖 프로젝트 소개

글을 쓸 때마다 제 기존 글들의 스타일과 톤을 일관되게 유지하고, 과거에 썼던 글의 내용을 다시 참고하는 것은 번거로운 일이었습니다. **P.A.G.E.**는 바로 이 문제를 저 스스로 해결하기 위해 시작한 개인 프로젝트입니다.

제가 작성한 Jekyll 블로그 포스트들을 지식 기반으로 삼아, 저만의 고유한 스타일과 톤을 반영한 새로운 글의 초안을 생성해주는 개인 맞춤형 글쓰기 보조 도구입니다. P.A.G.E.는 저의 글쓰기 효율을 극대화하는 데 초점을 맞추고 있지만, 향후에는 다른 작가와 개발자들도 자신만의 AI 글쓰기 어시스턴트를 가질 수 있도록 서비스로 확장할 계획을 가지고 있습니다.

### ✨ 핵심 기능

- **✍️ 개인화된 초안 생성**: 저의 기존 블로그 글들을 RAG(검색 증강 생성) 기술로 분석하여, 새로운 주제에 대한 글을 저의 스타일로 작성합니다.
- **📋 Jekyll 완벽 지원**: YAML Front Matter(`title`, `description`, `tags` 등)가 포함된, Jekyll 블로그에 바로 게시할 수 있는 완벽한 형식의 마크다운을 생성합니다.
- **🖥️ 실시간 미리보기**: Flutter 기반의 깔끔한 UI를 통해 생성된 마크다운 초안이 실제 블로그에서 어떻게 보일지 실시간으로 렌더링하여 보여줍니다.
- **🔒 안전한 비공개 환경**: 로컬 LLM 서버와 API 키로 보호되는 개인 백엔드를 사용하여, 저의 모든 데이터와 글은 외부에 노출되지 않고 안전하게 관리됩니다.

---

## 📂 프로젝트 구조 (Monorepo)

이 프로젝트는 프런트엔드와 백엔드 코드를 하나의 Git 저장소에서 관리하는 모노레포(Monorepo) 방식으로 구성되어 있습니다.

```
/PAGE_Project/
├── 📁 backend/
│   ├── app/
│   ├── .env
│   └── requirements.txt
├── 📁 frontend/
│   ├── lib/
│   └── pubspec.yaml
└── 📄 README.md
```

- **`backend/`**: FastAPI로 구현된 백엔드 서버입니다. RAG 파이프라인 실행, LLM 호출 등 핵심 로직을 담당합니다.
- **`frontend/`**: Flutter로 구현된 프런트엔드 애플리케이션입니다. 사용자가 상호작용하는 UI를 담당합니다.

--

## ⚙️ 작동 원리 (How It Works)

P.A.G.E.는 최신 AI 기술 스택을 기반으로 유기적으로 작동하는 시스템입니다.

**[데이터 파이프라인]**

```
1. GitHub Repository (블로그 글 Push)
   |
   V
2. GitHub Actions (자동 실행)
   |
   V
3. Pinecone Vector DB (지식 베이스 자동 업데이트)
```

**[초안 생성 파이프라인]**

```
1. Flutter App (사용자 주제 입력)
   |
   V
2. FastAPI Backend (API 요청 수신)
   |
   V
3. RAG (Pinecone에서 관련 지식 검색)
   |
   V
4. Local Llama3 (나의 스타일로 초안 생성)
   |
   V
5. Flutter App (생성된 초안 및 미리보기 표시)
```

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분           | 기술                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **프런트엔드** | ![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)                      |
| **백엔드**     | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)                      |
| **AI / LLM**   | ![LangChain](https://img.shields.io/badge/LangChain-005571?style=for-the-badge) `Llama3 (Local)`                              |
| **벡터 DB**    | ![Pinecone](https://img.shields.io/badge/Pinecone-3B5998?style=for-the-badge&logo=pinecone&logoColor=white)                   |
| **CI/CD**      | ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) |

---

## 🚀 시작하기 (Getting Started)

이 섹션은 P.A.G.E. 프로젝트를 여러분의 로컬 환경에서 직접 실행하고 테스트해보기 위한 가이드입니다.

### 사전 준비

- Jekyll 블로그 GitHub 저장소
- Pinecone 계정 및 API 키
- 로컬 환경에 Llama3 모델 서버 실행 (e.g., Ollama)
- Flutter SDK 및 Python 3.10+ 설치

### 1. 백엔드 설정

```bash
# 1. 저장소 클론
git clone https://github.com/janghyunroh/PAGE_Project.git
# 1-1. 백엔드 디렉토리로 이동
cd backend

# 1-2. 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 1-3. 의존성 패키지 설치
pip install -r requirements.txt

# 1-4. .env 파일 생성 및 환경 변수 설정
# PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
# LLAMA3_SERVER_URL="http://localhost:11434"
# MY_SECRET_API_KEY="YOUR_OWN_SECRET_KEY"

# 1-5. FastAPI 서버 실행
uvicorn app.main:app --reload
```

### 2. 프런트엔드 설정

```bash
# 2-1. 프런트엔드 디렉토리로 이동 (프로젝트 루트에서 시작)
cd frontend

# 2-2. 의존성 패키지 설치
flutter pub get

# 2-3. API 엔드포인트 및 키 설정
# lib/api/api_service.dart 파일 내의 API 주소와 키를 설정합니다.

# 2-4. Flutter 앱 실행
flutter run
```

## 향후 로드맵 (Roadmap)

- [ ] GitHub 자동 Push: 앱 내에서 버튼 하나로 GitHub 저장소에 포스트를 자동으로 발행하는 기능

- [ ] 인앱 초안 편집기: 생성된 초안을 앱 내에서 바로 수정하고 저장하는 기능

- [ ] 다중 LLM 지원: 로컬 Llama3 외 OpenAI API 등 다른 언어 모델 선택 기능

- [ ] 초안 이력 관리: 과거에 생성했던 초안들을 확인하고 이어 쓰는 기능

## 📄 라이선스 (License)
