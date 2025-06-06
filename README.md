## FastAPI 기반 백엔드의 Poetry 패키지 관리 이관 프로젝트
### Goal
이 프로젝트의 목표는 기존 requirements.txt 기반의 Python 프로젝트를 Poetry 패키지 매니저를 활용한 구조로 이관하고, 해당 프로젝트를 Docker 환경 내에서 효율적으로 실행할 수 있도록 컨테이너화하는 것입니다.

Poetry를 도입함으로써 의존성 관리를 명확히 하고, 개발 및 배포 환경에서의 일관성을 확보하며, Docker 기반의 실행 환경을 통해 플랫폼 독립적인 실행을 가능하게 합니다.

### Requirements
다음은 Docker 이미지 내에 설치되는 주요 라이브러리 및 그 버전입니다:

Python: 3.11 (python:3.11-slim)

Poetry: 최신 버전(2.1.1)(pip install --no-cache-dir poetry)

poetry-plugin-shell: Poetry 명령어 확장을 위한 플러그인, poetry 버전에 따라 맞춰짐

기타 패키지들은 pyproject.toml 및 poetry.lock에 정의되어 있으며, 이는 기존 requirements.txt 파일을 Poetry로 이관하여 구성된 것입니다.

How to Install & Run
1. Docker 이미지 빌드
다음 명령어를 터미널에서 실행하여 Docker 이미지를 생성합니다 (Dockerfile이 있는 디렉토리 기준):

docker build -t final_studentID:v1 .
2. Docker 컨테이너 실행
이미지로부터 컨테이너를 생성하고 실행하려면 아래 명령어를 입력하세요:

arduino
Copy
Edit
docker run -it --rm final_studentID:v1
옵션 설명:

-it: 터미널 상호작용 모드

--rm: 종료 시 컨테이너 자동 삭제

final_studentID:v1: 사용 이미지 이름 및 태그

3. 디렉토리 구조
Docker 컨테이너 내 프로젝트 디렉토리 구조는 다음과 같습니다:

bash
Copy
Edit
/app
├── main.py           # (예시) 실행 스크립트
├── pyproject.toml    # Poetry 설정 파일
├── poetry.lock       # 의존성 버전 고정 파일
├── .env              # 환경 변수 파일
└── 기타 소스 코드 파일들
프로젝트 파일들은 모두 /app 디렉토리 아래로 복사됩니다.

4. 컨테이너 종료 방법
컨테이너 실행 중 다음 방법 중 하나로 종료할 수 있습니다:

CTRL + C 입력

exit 명령어 입력

--rm 옵션 덕분에 컨테이너는 종료와 동시에 자동으로 삭제됩니다.

참고
본 프로젝트는 7주차 과제로서, requirements.txt 기반 레포를 Poetry 환경으로 이관하고 Docker 컨테이너로 구성하는 과정을 포함합니다.

pyproject.toml은 poetry init, poetry add 등을 활용하여 생성 및 설정하였습니다.