from fastapi import FastAPI, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List
from datetime import datetime
from pydantic import BaseModel
from HandleCenter import handleCenter
import os
import requests
from fastapi.responses import Response
import vg
from fastapi import Body
from urllib.parse import urlparse
import os

from models import Material, Project
import base64

app = FastAPI()
hc = handleCenter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

video_gen = vg.VideoGenerator(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="1e2a6dd2-cbfa-4f33-8f5d-953a7d584bbc"
)

DATABASE_URL = "mysql+pymysql://root:040601@localhost:3306/media_platform?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)


# 静态资源配置
UPLOAD_ROOT = "uploads"
os.makedirs(UPLOAD_ROOT, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")



def image_to_base64(file_path: str) -> str:
    """将本地图片转换为base64编码"""
    with open(file_path, "rb") as f:
        img_data = f.read()
        b64 = base64.b64encode(img_data).decode('utf-8')
        # 获取文件扩展名判断MIME类型
        ext = file_path.lower().split('.')[-1]
        mime_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp',
            'gif': 'image/gif'
        }
        mime = mime_map.get(ext, 'image/jpeg')
        return f"data:{mime};base64,{b64}"


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


@app.post("/generate_image/")
def generate_image(prompts: str = Form(...)):
    try:
        urls = hc.generateImageT2I(prompts)
        return {
            "status": "success",
            "urls": urls
        }
    except Exception as e:
        return {
            "status": "error",
            "msg": str(e)
        }

@app.post("/download_image/")
def download_image(url: str = Body(..., embed=True)):
    try:
        # 后端请求图片（不会被 CORS 拦截）
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        # 获取格式
        content_type = resp.headers.get("Content-Type", "image/jpeg")

        # 返回图片二进制
        return Response(content=resp.content, media_type=content_type)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "msg": f"下载失败: {str(e)}"},
        )


@app.post("/video/generate/")
async def video_generate(
        text: str = Body(..., embed=True),
        first_imgurl: str = Body(..., embed=True),
        last_imgurl: str = Body(..., embed=True),
):
    try:

        def url_to_local_path(url: str) -> str:
            parsed = urlparse(url)
            # parsed.path 是 '/uploads/user_1/xxx.jpg'
            local_path = parsed.path.lstrip('/')  # 去掉开头的 '/'
            # 拼上项目根目录
            local_path = os.path.join(os.getcwd(), local_path)
            return local_path

        first_local_path = url_to_local_path(first_imgurl)
        last_local_path = url_to_local_path(last_imgurl)

        first_processed = image_to_base64(first_local_path)
        last_processed = image_to_base64(last_local_path)



        print(f"🎬 视频生成请求:")
        print(f"  文本提示: {text}")
        print(f"  首帧: {'base64编码' if first_processed.startswith('data:') else first_processed}")
        print(f"  尾帧: {'base64编码' if last_processed.startswith('data:') else last_processed}")

        video_url = video_gen.D_vedio(text, first_processed, last_processed)

        if not video_url:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "msg": "视频生成失败"}
            )

        print(f"✅ 视频生成成功: {video_url}")

        return {
            "status": "success",
            "video_url": video_url
        }

    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {str(e)}")
        return JSONResponse(
            status_code=404,
            content={"status": "error", "msg": str(e)}
        )
    except Exception as e:
        print(f"❌ 视频生成异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "msg": str(e)}
        )

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
