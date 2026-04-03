from pydantic import BaseModel
from typing import Dict
from typing import List

class CategorySummary(BaseModel):
    category:str
    total:float

class DashboardSummary(BaseModel):
    total_income:float
    total_expenses:float
    net_balance:float
    total_records:int
    category_totals:List[CategorySummary]