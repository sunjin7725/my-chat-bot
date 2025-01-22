# 나만의 챗봇 앱

## 프로젝트 설명
OpenAI API를 활용한 대화형 AI 챗봇 애플리케이션입니다. 사용자가 질문을 하면, 네이버 및 카카오 API를 통해 검색 결과를 기반으로 답변을 제공합니다. 또한, 유튜브 비디오에 대한 질문도 처리할 수 있습니다.

## 주요 기능
- AI와의 실시간 대화
- 네이버 및 카카오 검색 결과 기반 답변
- 유튜브 비디오에 대한 질문 및 요약 제공
- 이메일 작성 지원 (API만 붙이면 가능)

## 시작하기

### 필수 요구사항
- Python 3.9 이상
- OpenAI API 키
- 네이버 API 클라이언트 ID 및 비밀
- 카카오 API 키

### 설치 방법
#### 로컬
1. 저장소 클론
```bash
git clone https://github.com/sunjin7725/my-chat-bot.git
cd my-chat-bot
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. `secret.yaml` 파일 설정
- `secret.yaml.example`을 참고하여 `secret.yaml` 파일을 생성하고 OpenAI API 키, 네이버 API 클라이언트 ID 및 비밀, 카카오 API 키를 설정합니다.

4. 프로젝트 실행
```bash
streamlit run run.py
```

#### 도커
1. Docker와 Docker Compose가 설치되어 있는지 확인

2. `secret.yaml` 파일 설정
- `secret.yaml.example`을 참고하여 `secret.yaml` 파일을 생성하고 OpenAI API 키, 네이버 API 클라이언트 ID 및 비밀, 카카오 API 키를 설정합니다.

3. Docker 컨테이너 빌드 및 실행
```bash
docker-compose up --build -d
```

4. 컨테이너 정지
```bash
docker-compose down
```

5. 로그 확인
```bash
docker-compose logs -f
```

## 프로젝트 구조
- `app/run.py`: 메인 애플리케이션 실행 파일
- `app/common/chat.py`: 챗봇 대화 로직 구현
- `app/common/client.py`: OpenAI API 클라이언트
- `app/common/ask_for_youtube.py`: 유튜브 비디오 관련 기능
- `app/common/ask_with_search.py`: 검색 결과 기반 질문 처리
- `requirements.txt`: 필요한 패키지 목록