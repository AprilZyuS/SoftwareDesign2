from sqlmodel import create_engine

DB_USER = "root"
DB_PASSWORD = "040601"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "media_platform"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 打印 SQL，开发时方便调试
    pool_size=10,         # 连接池大小
    max_overflow=20,      # 最大溢出连接
    pool_recycle=1800,    # 30分钟自动回收
)
