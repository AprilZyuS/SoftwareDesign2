from fastapi import FastAPI, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List
from datetime import datetime
from pydantic import BaseModel
import os

from models import Material, Project

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "mysql+pymysql://root:040601@localhost:3306/media_platform?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)


# 静态资源配置
UPLOAD_ROOT = "uploads"
os.makedirs(UPLOAD_ROOT, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")

class Prompts(BaseModel):
    prompts: str
    #提示词

class VideoLink(BaseModel):
    VLink: str
    #视频链接
@app.post("/api/submit")
def receive_json(data: Prompts):
    print(f"接收 JSON 字符串：{data.prompts}")
    return {"status": "success", "msg": "字符串接收成功"}

@app.get("/api/VideoLink")
def get_video_link(data: VideoLink):
    return VideoLink.VLink


# 文件上传：每个用户单独文件夹
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), user_id: int = Form(1)):
    user_dir = os.path.join(UPLOAD_ROOT, f"user_{user_id}")
    os.makedirs(user_dir, exist_ok=True)

    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(user_dir, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    relative_url = f"/uploads/user_{user_id}/{filename}"
    content_type = file.content_type
    size = os.path.getsize(file_path)

    # 同步写入数据库
    material = Material(
        user_id=user_id,
        filename=file.filename,
        filepath=relative_url,
        content_type=content_type,
        size=size,
    )
    with Session(engine) as session:
        session.add(material)
        session.commit()
        session.refresh(material)

    return {
        "id": material.id,
        "filename": file.filename,
        "url": relative_url,
        "user_id": user_id,
        "content_type": content_type,
        "size": size,
    }


#素材接口
@app.get("/materials/", response_model=List[Material])
def get_materials(user_id: int = Query(1)):
    with Session(engine) as session:
        if user_id:
            materials = session.exec(select(Material).where(Material.user_id == user_id)).all()
        else:
            materials = session.exec(select(Material)).all()
        return materials


@app.post("/materials/")
def add_material(material: Material):
    with Session(engine) as session:
        session.add(material)
        session.commit()
        session.refresh(material)
        return material


@app.delete("/materials/{material_id}")
def delete_material(material_id: int):
    with Session(engine) as session:
        material = session.get(Material, material_id)
        if not material:
            return {"error": "not found"}
        session.delete(material)
        session.commit()
        return {"status": "deleted"}



# 作品相关接口
@app.get("/projects/", response_model=List[Project])
def get_projects(user_id: int = Query(1)):
    with Session(engine) as session:
        return session.exec(select(Project).where(Project.user_id == user_id)).all()


@app.post("/projects/")
def add_project(project: Project):
    with Session(engine) as session:
        session.add(project)
        session.commit()
        session.refresh(project)
        return project


@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project:
            return {"error": "not found"}
        session.delete(project)
        session.commit()
        return {"status": "deleted"}
