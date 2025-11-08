from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)

class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    filename: str
    filepath: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    name: str
    description: Optional[str] = None
    material_ids: Optional[str] = None  # JSON 字符串或 CSV
    output_url: Optional[str] = None
