<script setup>
import {ref} from "vue";
import MaterialUploader from "./MaterialUploader.vue";
import axios from 'axios'

const activeTab = ref('素材生成')
const loading = ref(false)
const audioUrl = ref('')
const candidateMaterials = ref([]) // 备选素材（本地暂存）
const description = ref('')
const API_BASE = "http://127.0.0.1:8000";

// 处理上传 - 添加到备选素材
const handleUpload = (file) => {
  console.log('📥 接收到文件:', file);

  if (!file) {
    console.error('❌ 文件为空');
    return;
  }

  // 创建本地预览 URL
  const imageURL = URL.createObjectURL(file);

  // 添加到备选素材列表
  const newMaterial = {
    id: Date.now(), // 临时ID
    name: file.name,
    thumbnail: imageURL,
    file: file // 保存原始文件对象
  };

  candidateMaterials.value.push(newMaterial);

  console.log('✅ 已添加到备选素材:', file.name);
  console.log('📊 当前备选素材数量:', candidateMaterials.value.length);
}

// 生成图像
const Generate = () => {
  if (!description.value.trim()) {
    alert('请输入描述内容');
    return;
  }

  const data = {
    prompts: description.value
  }

  console.log('🚀 发送生成请求:', data);

  axios.post(`${API_BASE}/api/submit`, data)
      .then(res => {
        console.log('✅ 响应：', res.data);
        alert('提交成功！');
      })
      .catch(err => {
        console.error('❌ 错误：', err);
        alert('提交失败，请检查网络连接');
      })
}

// 拖拽开始
function handleDragStart(event, material) {
  console.log('🎯 开始拖拽:', material.name);

  event.dataTransfer.setData('source', 'candidate');
  event.dataTransfer.setData('materialId', String(material.id));

  // 使用全局变量存储文件对象
  window.__draggedMaterial = material;

  event.dataTransfer.effectAllowed = 'copy';
}

// 拖拽结束
function handleDragEnd() {
  console.log('🏁 拖拽结束');
}

// 从备选素材删除
function removeCandidateMaterial(id) {
  const material = candidateMaterials.value.find(m => m.id === id);
  if (material) {
    // 释放 blob URL
    URL.revokeObjectURL(material.thumbnail);
  }

  candidateMaterials.value = candidateMaterials.value.filter(m => m.id !== id);
  console.log('🗑️ 已从备选素材删除, 剩余:', candidateMaterials.value.length);
}
</script>

<template>
  <div class="main-container">
    <!-- 上传组件 -->
    <MaterialUploader @upload="handleUpload"/>

    <!-- 音频预览 -->
    <div v-if="audioUrl" class="preview-box">
      <audio :src="audioUrl" controls></audio>
    </div>

    <!-- 描述输入框 -->
    <div class="textarea-container">
      <label class="textarea-label">请描述你想生成的画面</label>
      <textarea
          v-model="description"
          class="custom-textarea"
          placeholder="例如：一只可爱的小猫在花园里玩耍..."
      ></textarea>
    </div>

    <!-- 备选素材区域 -->
    <div class="bottom-panel">
      <div class="panel-header">
        <h3>备选素材 ({{ candidateMaterials.length }})</h3>
        <span class="hint-text">💡 拖拽到素材库以上传到服务器</span>
      </div>

      <div class="material-grid">
        <div
            v-for="m in candidateMaterials"
            :key="m.id"
            class="material-item"
            draggable="true"
            @dragstart="handleDragStart($event, m)"
            @dragend="handleDragEnd"
        >
          <img :src="m.thumbnail" :alt="m.name"/>
          <p class="material-name" :title="m.name">{{ m.name }}</p>
          <div class="item-badge">本地</div>
          <button class="remove-btn" @click="removeCandidateMaterial(m.id)">×</button>
        </div>

        <!-- 空状态提示 -->
        <div v-if="candidateMaterials.length === 0" class="empty-state">
          <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
          </svg>
          <p>暂无备选素材</p>
          <p class="empty-desc">点击上方按钮选择图片</p>
        </div>
      </div>
    </div>

    <!-- 生成按钮 -->
    <div class="action-bar">
      <el-button type="primary" size="large" @click="Generate">
        🎨 开始生成
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.textarea-container {
  margin: 20px 0;
  padding: 20px;
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.textarea-label {
  display: block;
  margin-bottom: 12px;
  font-weight: 600;
  color: #333;
  font-size: 15px;
}

.custom-textarea {
  width: 100%;
  min-height: 120px;
  padding: 14px;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  transition: all 0.3s;
  font-family: inherit;
}

.custom-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.custom-textarea::placeholder {
  color: #bbb;
}

.preview-box {
  background: #2a2a2a;
  padding: 20px;
  border-radius: 12px;
  margin: 20px 0;
  text-align: center;
}

/* 备选素材面板 */
.bottom-panel {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px;
  border-radius: 16px;
  margin: 20px 0;
  min-height: 240px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h3 {
  color: #fff;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.hint-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  background: rgba(255, 255, 255, 0.15);
  padding: 6px 14px;
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

/* 素材网格 */
.material-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 16px;
  min-height: 160px;
}

/* 单个素材项 */
.material-item {
  position: relative;
  background: rgba(255, 255, 255, 0.97);
  border-radius: 12px;
  padding: 10px;
  cursor: move;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
  overflow: hidden;
}

.material-item:hover {
  border-color: rgba(255, 255, 255, 0.8);
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25);
  background: #fff;
}

.material-item:active {
  opacity: 0.7;
  transform: scale(0.95);
}

.material-item img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  pointer-events: none;
  background: #f5f5f5;
}

.material-name {
  color: #333;
  font-size: 13px;
  margin: 10px 0 0;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

/* 本地标记 */
.item-badge {
  position: absolute;
  bottom: 12px;
  right: 10px;
  background: rgba(102, 126, 234, 0.95);
  color: white;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* 删除按钮 */
.remove-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 77, 79, 0.95);
  color: white;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  opacity: 0;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.material-item:hover .remove-btn {
  opacity: 1;
}

.remove-btn:hover {
  background: #ff4d4f;
  transform: scale(1.15) rotate(90deg);
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  padding: 50px 20px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  opacity: 0.7;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-state p {
  margin: 10px 0;
  font-size: 17px;
  font-weight: 500;
}

.empty-desc {
  font-size: 14px;
  opacity: 0.8;
}

/* 操作栏 */
.action-bar {
  text-align: center;
  margin-top: 30px;
}

/* 响应式 */
@media (max-width: 768px) {
  .material-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 12px;
  }

  .panel-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>