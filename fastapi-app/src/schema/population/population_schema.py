from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PopulationBase(BaseModel):
    datetime: datetime
    region_id: Optional[str] = None
    male_rate: Optional[float] = None
    female_rate: Optional[float] = None
    area_congest: Optional[str] = None
    congestion_message: Optional[str] = None
    gen_10: Optional[float] = Field(None) 
    gen_20: Optional[float] = Field(None)
    gen_30: Optional[float] = Field(None)
    gen_40: Optional[float] = Field(None)
    gen_50: Optional[float] = Field(None)
    gen_60: Optional[float] = Field(None)
    gen_70: Optional[float] = Field(None)
    min_population: Optional[int] = None
    max_population: Optional[int] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class PopulationRequest(PopulationBase):
    pass


class PopulationResponse(PopulationBase):
    pass

class GenderPopulationResponse(BaseModel):
    datetime: datetime
    region_id: Optional[str] = None
    male_min_population: Optional[float] = None
    male_max_population: Optional[float] = None
    female_min_population: Optional[float] = None
    female_max_population: Optional[float] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True
        
class AgeGroupPopulationResponse(BaseModel):
    datetime: datetime
    region_id: Optional[str] = None
    gen_10: Optional[float] = None
    gen_20: Optional[float] = None
    gen_30: Optional[float] = None
    gen_40: Optional[float] = None
    gen_50: Optional[float] = None
    gen_60: Optional[float] = None
    gen_70: Optional[float] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True