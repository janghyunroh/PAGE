# ==============================================================================
# 파일: backend/tests/conftest.py (새로 추가된 파일)
# 역할: pytest를 위한 중앙 설정 파일입니다.
#       테스트 실행 전에 프로젝트 루트 경로를 sys.path에 추가하여
#       'app' 모듈을 찾을 수 있도록 합니다.
# ==============================================================================
import sys
import os

# 현재 파일(conftest.py)의 위치를 기준으로 프로젝트 루트 디렉토리의 절대 경로를 계산합니다.
# (backend/tests/ -> backend/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 파이썬이 모듈을 찾는 경로 목록(sys.path)의 맨 앞에 프로젝트 루트를 추가합니다.
sys.path.insert(0, project_root)
