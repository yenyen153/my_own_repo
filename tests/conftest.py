import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.user import app, get_db  # 確保正確導入你的 FastAPI 應用
from app.models import Base  # 確保導入你的 SQLAlchemy 模型

# 連接 MariaDB，請修改為你的連線資訊
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/ptt_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """ 讓測試用資料庫連線，並使用 Transaction 回滾機制 """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session  # 測試時使用這個 session

    session.close()
    transaction.rollback()  # 測試結束時回滾，避免影響 MariaDB 內容
    connection.close()

# 覆蓋 FastAPI 的 `get_db()`，讓它使用測試 Transaction
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
