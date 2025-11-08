<script setup>
import {ref} from "vue";
import MaterialUploader from "./MaterialUploader.vue";
import axios from 'axios'

const activeTab = ref('素材生成')
const loading = ref(false)
const audioUrl = ref('')
const materials = ref([])
const description = ref('')
const API_BASE = "http://127.0.0.1:8000";


const handleUpload = (file) => {
  if (!file) return

  const imageURL = URL.createObjectURL(file)

  materials.value.push({
    id: Date.now(),
    name: file.name,
    thumbnail: imageURL,
    file
  })

  console.log("已添加素材",file.name)
}

const Generate = () => {
  const data = {
    prompts: description.value
  }
  //生成图像，传输字符串
  axios.post(`${API_BASE}/api/submit/`,data)
      .then(res => console.log('响应：', res.data))
      .catch(err => console.error('错误：', err))
}


</script>

<template>
  <MaterialUploader @upload="handleUpload" />

  <div v-if="audioUrl" class="preview-box">
    <audio :src="audioUrl" controls></audio>
  </div>

  <div class="textarea-container">
    <label class="textarea-label">请描述你想生成的画面</label>
    <textarea
        v-model="description"
        class="custom-textarea"
        placeholder="请输入内容..."
        :disabled="isDisabled"

    ></textarea>
  </div>

  <div class="buttom-panel">
    <h3>备选素材</h3>
  </div>

  <el-button type="primary" @click="Generate">生成</el-button>
</template>

<style scoped>
:root {
  --textarea-bg: #f8f9fa;
  --textarea-border: #ddd;
  --textarea-border-focus: #42b983; /* 聚焦时边框色 */
  --textarea-text: #333;
  --textarea-placeholder: #999;
  --textarea-radius: 8px;
  --textarea-shadow: 0 2px 4px rgba(0,0,0,0.05);
  --transition-speed: 0.3s; /* 过渡动画速度 */
  --textarea-width: 100%; /* 固定宽度（可改为具体像素，如 500px） */
  --textarea-height: 150px; /* 固定高度 */
}

.textarea-container {
  margin: 20px;
  padding: 20px;
  border: 1px solid #f0f0f0;
  border-radius: var(--textarea-radius);
  width: var(--textarea-width);
  min-width: var(--textarea-width); /* 最小宽度 = 固定宽度 */
  max-width: var(--textarea-width); /* 最大宽度 = 固定宽度 */

  /* 2. 固定高度（禁止缩放高度） */
  height: var(--textarea-height);
  min-height: var(--textarea-height); /* 最小高度 = 固定高度 */
  max-height: var(--textarea-height); /* 最大高度 = 固定高度 */

  /* 3. 禁用用户拖拽调整大小 */
  resize: none; /* 关键：取消默认的拖拽调整功能 */

  /* 4. 内容溢出时显示滚动条 */
  overflow: auto; /* 文本超出高度时，显示垂直滚动条 */
}
.textarea-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: var(--textarea-text);
}
.preview-box {
  background: #2a2a2a;
  padding: 16px;
  border-radius: 12px;
  width: 400px;
  text-align: center;
}


.buttom-panel {
  width: 800px;
  background: #1e1e1e;
  padding: 50px;
  border-radius: 12px;
  overflow-y: auto;
}

/* 占位符样式（嵌套在内部，结构更清晰） */
&::placeholder {
  color: var(--textarea-placeholder);
  opacity: 1; /* 修复部分浏览器占位符透明度问题 */
}

/* 聚焦状态（嵌套） */
&:focus {
  border-color: var(--textarea-border-focus);
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.2); /* 聚焦发光效果 */
}

/* 禁用状态（嵌套） */
&:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
  border-color: #eee;
  color: #999;
}

/* 滚动条美化（仅 WebKit 浏览器，通过 autoprefixer 自动加前缀） */
&::-webkit-scrollbar {
  width: 6px;
}
&::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}
&::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}
&::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}


</style>