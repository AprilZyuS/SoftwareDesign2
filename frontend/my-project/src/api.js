import axios from "axios";
const API_BASE = "http://127.0.0.1:8000";

export async function getMaterials(userId = 1) {
    return (await axios.get(`${API_BASE}/materials/`, { params: { user_id: userId } })).data;
}

export async function addMaterial(name, thumbnail, userId = 1) {
    return (
        await axios.post(`${API_BASE}/materials/`, {
            name,
            thumbnail,
            user_id: userId,
        })
    ).data;
}

export async function deleteMaterial(id) {
    return (await axios.delete(`${API_BASE}/materials/${id}`)).data;
}

export async function getProjects(userId = 1) {
    return (await axios.get(`${API_BASE}/projects/`, { params: { user_id: userId } })).data;
}

export async function addProject(title, description, userId = 1) {
    return (
        await axios.post(`${API_BASE}/projects/`, {
            title,
            description,
            user_id: userId,
        })
    ).data;
}

export async function deleteProject(id) {
    return (await axios.delete(`${API_BASE}/projects/${id}`)).data;
}
