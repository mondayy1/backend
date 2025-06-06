## FastAPI 기반 백엔드의 Poetry 패키지 관리 이관 프로젝트
### Goal
- 기존 requirements.txt 기반의 Python 프로젝트를 Poetry 패키지 매니저를 활용한 구조로 이관.
- 해당 프로젝트를 Docker 환경 내에서 효율적으로 실행할 수 있도록 컨테이너화하는 것입니다.

- Poetry를 도입함으로써 의존성 관리를 명확히 하고, 개발 및 배포 환경에서의 일관성을 확보하며,
- Docker 기반의 실행 환경을 통해 독립적인 실행을 가능하게 합니다.

### Requirements
- 다음은 Docker 이미지 내에 설치되는 주요 라이브러리 및 그 버전입니다:
  - Python: 3.11 (python:3.11-slim)
  - Poetry: 최신 버전(2.1.1)(pip install --no-cache-dir poetry)
  - poetry-plugin-shell: Poetry 명령어 확장을 위한 플러그인, poetry 버전에 따라 맞춰짐
  
- 기타 패키지들은 pyproject.toml 및 poetry.lock에 정의되어 있습니다.

### How to Install & Run
0. 프로젝트 클론
깃헙에서 본 프로젝트를 클론하고, 디렉토리로 진입합니다.
```
$ git clone git@github.com:mondayy1/backend.git
```
```
$ cd backend
```

1. Docker 이미지 빌드
```
$ docker build -t final_2020038040:v1 .
```

2. Docker 컨테이너 생성 및 실행
```
$ docker compose up -d
```

3. 컨테이너 진입
```
$ docker exec -it backend-fastapi-1 /bin/bash
```

4. api 엔드포인트 테스트
```
$ curl localhost:8000
```
- "stocknear api"가 response된다면 성공!

5. 디렉토리 구조
```
/app
├── main.py           # fastapi main 스크립트
├── pyproject.toml    # Poetry 설정 파일
├── poetry.lock       # 의존성 버전 고정 파일
├── .env              # 환경 변수 파일
└── 기타 소스 및 깃 설정 파일들
```

6. 컨테이너 종료
```
$ docker compose down
```
