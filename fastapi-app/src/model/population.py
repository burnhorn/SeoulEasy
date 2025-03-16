from sqlalchemy import Column, Integer, Float, String, DateTime
from src.data.database import Base

from sqlalchemy import Column, Integer, Float, String, DateTime

class PopulationStation(Base):
    __tablename__ = 'population'
    
    datetime = Column(DateTime(timezone=True), primary_key=True, nullable=False, index=True)  
    region_id = Column(String(255), primary_key=True, nullable=False)              
    male_rate = Column(Float, nullable=True)                 
    female_rate = Column(Float, nullable=True)               
    area_congest = Column(String(255), nullable=True)      
    congestion_message = Column(String(255), nullable=True)
    gen_10 = Column(Float, nullable=True)
    gen_20 = Column(Float, nullable=True) 
    gen_30 = Column(Float, nullable=True) 
    gen_40 = Column(Float, nullable=True) 
    gen_50 = Column(Float, nullable=True)  
    gen_60 = Column(Float, nullable=True)       
    gen_70 = Column(Float, nullable=True) 
    min_population = Column(Integer, nullable=True)           
    max_population = Column(Integer, nullable=True)           

    def __repr__(self):
        return (
            f"<PopulationStation(datetime={self.datetime}, region_id={self.region_id}, "
            f"male_rate={self.male_rate}, female_rate={self.female_rate}, "
            f"min_population={self.min_population}, max_population={self.max_population})>"
        )
          
