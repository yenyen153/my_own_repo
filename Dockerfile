# 使用 Python 3.10 作為基礎映像
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 複製專案檔案到容器內
COPY . /app

# 安裝系統相依性與 Python 依賴
RUN apt-get update && apt-get install -y \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 指定預設啟動命令（可用於 Celery Worker）
#CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
