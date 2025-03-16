from src.data.database import Base
from src.model import model, population

# 모든 모델이 임포트되었으므로 Base.metadata에 모두 등록됨
target_metadata = Base.metadata
