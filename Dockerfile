FROM python:3.11-slim

RUN mkdir -p /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 애플리케이션 코드 복사
COPY app/ /app/

# Streamlit 실행
EXPOSE 8501

# 실행 권한 설정
RUN chmod +x /app/run.py

CMD ["streamlit", "run", "/app/run.py", "--server.address", "0.0.0.0", "--server.port", "8501"]