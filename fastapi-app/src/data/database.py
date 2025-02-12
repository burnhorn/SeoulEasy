from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from starlette.config import Config
import os
from dotenv import load_dotenv

# azure 환경에서 사용하려면 False, False로 변경
# local 환경에서 sqlite 안 쓰려면 False, True로 변경
sqlite_test = True
env_activate = True

# 비동기 연결 문자열 생성 (asyncmy 드라이버 사용)
if sqlite_test:
    # SQLite 비동기 연결 설정 (check_same_thread=False 추가)
    engine = create_async_engine(
        "sqlite+aiosqlite:///./myapi.db", 
        echo=True, 
        connect_args={"check_same_thread": False}
    )

    # 비동기 세션 설정
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Base 클래스 정의
    Base = declarative_base()

    # MetaData에 naming convention 추가
    naming_convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    Base.metadata = MetaData(naming_convention=naming_convention)

    # 비동기 세션 의존성
    async def get_db():
        async with AsyncSessionLocal() as db:
            yield db

else:
    if env_activate:
        ## local 환경 설정
        # .env 파일의 절대 경로를 지정합니다.
        # .env 파일의 절대 경로를 생성합니다.
        dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))

        # .env 파일을 로드합니다.
        load_dotenv(dotenv_path)
        print(dotenv_path)
        # 환경 변수를 가져옵니다.
        SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
    
    else:
        # Azure 환경 설정
        SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

    # 비동기 엔진 및 세션 설정
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Base 클래스 정의
    Base = declarative_base()

    # 비동기 세션 의존성
    async def get_db():
        async with AsyncSessionLocal() as db:
            yield db
