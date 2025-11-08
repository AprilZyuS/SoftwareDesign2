import os
import aiofiles
from typing import List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, select
from models import User, Material, Project
from config import engine

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Media Platform API (MySQL Version)")

# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态资源挂载
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    print("数据表初始化完成。")


# ========== 用户 ==========

@app.post("/user/create")
def create_user(user_id: str = Form(...)):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            user = User(id=user_id)
            session.add(user)
            session.commit()
    return {"user_id": user_id}


# ========== 素材 ==========

@app.post("/upload/")
async def upload_file(user_id: str = Form(...), file: UploadFile = File(...)):
    if not user_id:
        raise HTTPException(status_code=400, detail="缺少 user_id")

    user_dir = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)

    save_path = os.path.join(user_dir, file.filename)
    if os.path.exists(save_path):
        base, ext = os.path.splitext(file.filename)
        counter = 1
        while os.path.exists(os.path.join(user_dir, f"{base}_{counter}{ext}")):
            counter += 1
        save_path = os.path.join(user_dir, f"{base}_{counter}{ext}")

    async with aiofiles.open(save_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    rel_url = f"/uploads/{user_id}/{os.path.basename(save_path)}"

    with Session(engine) as session:
        mat = Material(
            user_id=user_id,
            filename=os.path.basename(save_path),
            filepath=rel_url,
            content_type=file.content_type,
            size=len(content)
        )
        session.add(mat)
        session.commit()
        session.refresh(mat)

    return {"id": mat.id, "filename": mat.filename, "url": rel_url}


@app.get("/materials/")
def list_materials(user_id: str):
    with Session(engine) as session:
        stmt = select(Material).where(Material.user_id == user_id)
        mats = session.exec(stmt).all()
        return [m.dict() for m in mats]


@app.delete("/materials/{material_id}")
def delete_material(material_id: int, user_id: str):
    with Session(engine) as session:
        mat = session.get(Material, material_id)
        if not mat or mat.user_id != user_id:
            raise HTTPException(status_code=404, detail="素材不存在")

        abs_path = os.path.join(os.getcwd(), mat.filepath.lstrip("/"))
        if os.path.exists(abs_path):
            os.remove(abs_path)

        session.delete(mat)
        session.commit()
    return {"ok": True}


# ========== 作品 ==========

@app.post("/projects/")
def create_project(
    user_id: str = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    material_ids: str = Form(None),
    output_url: str = Form(None)
):
    with Session(engine) as session:
        project = Project(
            user_id=user_id,
            name=name,
            description=description,
            material_ids=material_ids,
            output_url=output_url
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    return project


@app.get("/projects/")
def list_projects(user_id: str):
    with Session(engine) as session:
        stmt = select(Project).where(Project.user_id == user_id)
        projects = session.exec(stmt).all()
        return [p.dict() for p in projects]


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, user_id: str):
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project or project.user_id != user_id:
            raise HTTPException(status_code=404, detail="项目不存在")
        session.delete(project)
        session.commit()
    return {"ok": True}
