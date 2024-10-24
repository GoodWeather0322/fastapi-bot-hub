FROM python:3.12-slim

# 安裝 tzdata
RUN apt-get update && apt-get install -y tzdata

# 設置時區
ENV TZ=Asia/Taipei

# 清理
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt