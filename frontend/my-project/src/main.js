import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')

const API_BASE = 'http://127.0.0.1:8000'

const handleUpload = async (file) => {
    if (!file) return
    const form = new FormData()
    form.append('user_id', userId)
    form.append('file', file)
    await axios.post(`${API_BASE}/upload/`, form)


    try {
        const res = await axios.get(`${API_BASE}/materials/`, { params: { user_id: userId } })


        const { url, filename } = res.data
        // 拼接完整访问地址
        const fullUrl = `${API_BASE}${url}`

        materials.value.push({
            id: Date.now(),
            name: filename,
            thumbnail: fullUrl
        })
    } catch (err) {
        console.error('上传失败:', err)
    }
}