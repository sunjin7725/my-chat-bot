# 나만의 챗봇 앱

## 프로젝트 설명
OpenAI API를 활용한 대화형 AI 챗봇 애플리케이션입니다.

## 주요 기능
- AI와의 실시간 대화
- 이메일 작성 지원(API만 붙이면 가능)

## 시작하기

### 필수 요구사항
- Python 3.8 이상
- OpenAI API 키

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

3. secret.yaml 파일 설정
- secret.yaml.example을 참고하여 secret.yaml 파일을 생성하고 OpenAI API 키를 설정

4. 프로젝트 실행
```bash
streamlit run run.py
```

#### 도커
1. Docker와 Docker Compose가 설치되어 있는지 확인

2. secret.yaml 파일 설정
- secret.yaml.example을 참고하여 secret.yaml 파일을 생성하고 OpenAI API 키를 설정

3. Docker 컨테이너 빌드 및 실행
```bash
docker-compose up -d
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
- `app/chat.py`: 챗봇 대화 로직 구현
- `app/client.py`: OpenAI API 클라이언트
- `requirements.txt`: 필요한 패키지 목록