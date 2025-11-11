import axios from "axios";
const API_BASE = "http://127.0.0.1:8000";

// 获取素材列表
export async function getMaterials(userId = 1) {
    return (await axios.get(`${API_BASE}/materials/`, { params: { user_id: userId } })).data;
}

// 上传文件到服务器（使用后端的 /upload/ 接口）
export async function uploadMaterial(file, userId = 1) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    return (await axios.post(`${API_BASE}/upload/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })).data;
}

// 删除素材
export async function deleteMaterial(id) {
    return (await axios.delete(`${API_BASE}/materials/${id}`)).data;
}

// 获取项目列表
export async function getProjects(userId = 1) {
    return (await axios.get(`${API_BASE}/projects/`, { params: { user_id: userId } })).data;
}

// 添加项目
export async function addProject(title, description, userId = 1) {
    return (
        await axios.post(`${API_BASE}/projects/`, {
            title,
            description,
            user_id: userId,
        })
    ).data;
}

// 删除项目
export async function deleteProject(id) {
    return (await axios.delete(`${API_BASE}/projects/${id}`)).data;
}