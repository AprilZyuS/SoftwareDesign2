<script setup>
import {ref, onMounted} from "vue";
import {getMaterials, deleteMaterial, uploadMaterial} from "../api";

const materials = ref([]);
const API_BASE = "http://127.0.0.1:8000";
const dragOver = ref(false);
const uploading = ref(false);

// 加载素材列表
async function loadMaterials() {
  try {
    materials.value = await getMaterials();
    console.log('📂 素材库加载完成，共', materials.value.length, '个素材');
  } catch (error) {
    console.error('❌ 加载素材失败:', error);
  }
}

// 删除素材
async function removeMaterial(id) {
  if (!confirm('确定要删除这个素材吗？')) return;

  try {
    await deleteMaterial(id);
    await loadMaterials();
    console.log('✅ 素材已删除');
  } catch (error) {
    console.error('❌ 删除素材失败:', error);
  }
}

// 拖拽开始 - 用于拖拽到双图片框
function handleDragStart(event, material) {
  event.dataTransfer.setData('source', 'library');
  event.dataTransfer.setData('material', JSON.stringify({
    id: material.id,
    filename: material.filename,
    url: API_BASE + material.filepath,
  }));
}


// 接收从备选素材拖拽过来的文件
function handleDragEnter(e) {
  e.preventDefault();
  dragOver.value = true;
}

function handleDragLeave(e) {
  if (e.currentTarget === e.target) {
    dragOver.value = false;
  }
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'copy';
}

async function handleDrop(e) {
  e.preventDefault();
  dragOver.value = false;

  const source = e.dataTransfer.getData('source');

  console.log('📥 接收到拖拽，来源:', source);

  if (source === 'candidate') {
    const material = window.__draggedMaterial;

    if (!material || !material.file) {
      console.error('❌ 未找到文件对象');
      alert('拖拽失败：未找到文件');
      return;
    }

    // 检查是否已存在
    const exists = materials.value.some(m => m.filename === material.name);
    if (exists) {
      alert('该素材已存在于素材库中！');
      console.log('⚠️ 素材已存在:', material.name);
      return;
    }

    try {
      uploading.value = true;
      console.log('⏫ 开始上传:', material.name);

      // 上传文件到服务器
      const result = await uploadMaterial(material.file);

      console.log('✅ 上传成功:', result);
      alert(`上传成功：${material.name}`);

      // 重新加载素材列表
      await loadMaterials();

      // 清理全局引用
      window.__draggedMaterial = null;

    } catch (error) {
      console.error('❌ 上传失败:', error);
      alert('上传失败，请检查网络连接');
    } finally {
      uploading.value = false;
    }
  }
}

onMounted(loadMaterials);
</script>

<template>
  <div
      class="material-list"
      :class="{ 'drag-over': dragOver }"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @dragover="handleDragOver"
      @drop="handleDrop"
  >
    <div class="header">
      <h3>素材库</h3>
      <div class="header-right">
        <span v-if="uploading" class="uploading-hint">
          <span class="loading-spinner"></span>
          上传中...
        </span>
        <span class="count-badge">{{ materials.length }} 个</span>
      </div>
    </div>

    <!-- 拖拽提示层 -->
    <transition name="fade">
      <div v-if="dragOver" class="drop-hint">
        <div class="hint-content">
          <svg class="hint-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
          </svg>
          <p class="hint-title">松开以上传到素材库</p>
          <p class="hint-subtitle">文件将保存到服务器</p>
        </div>
      </div>
    </transition>

    <div class="grid">
      <div
          v-for="m in materials"
          :key="m.id"
          class="item"
          draggable="true"
          @dragstart="handleDragStart($event, m)"
      >
        <img :src="API_BASE + m.filepath" :alt="m.filename"/>
        <p class="filename" :title="m.filename">{{ m.filename }}</p>
        <div class="item-badge server">服务器</div>
        <button class="delete-btn" @click="removeMaterial(m.id)">删除</button>
      </div>

      <!-- 空状态 -->
      <div v-if="materials.length === 0 && !uploading" class="empty-hint">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
          <polyline points="17 21 17 13 7 13 7 21"/>
          <polyline points="7 3 7 8 15 8"/>
        </svg>
        <p>素材库为空</p>
        <p class="empty-desc">从备选素材拖拽到此处上传</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.material-list {
  position: relative;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  border: 2px dashed #e0e0e0;
  transition: all 0.3s ease;
  min-height: 300px;
}

.material-list.drag-over {
  border-color: #52c41a;
  background: rgba(82, 196, 26, 0.03);
  box-shadow: 0 0 0 4px rgba(82, 196, 26, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.uploading-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #52c41a;
  font-size: 14px;
  font-weight: 500;
}

.loading-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #52c41a;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.count-badge {
  background: #f0f0f0;
  color: #666;
  font-size: 13px;
  padding: 5px 12px;
  border-radius: 14px;
  font-weight: 600;
}

/* 拖拽提示层 */
.drop-hint {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.97);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  border-radius: 12px;
  pointer-events: none;
}

.hint-content {
  text-align: center;
}

.hint-icon {
  width: 80px;
  height: 80px;
  color: #52c41a;
  margin: 0 auto 20px;
  animation: bounce 1s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.hint-title {
  font-size: 20px;
  color: #52c41a;
  font-weight: 700;
  margin: 0 0 10px;
}

.hint-subtitle {
  font-size: 15px;
  color: #666;
  margin: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 16px;
  min-height: 120px;
}

.item {
  position: relative;
  text-align: center;
  cursor: move;
  transition: all 0.25s;
  padding: 10px;
  border-radius: 12px;
  border: 2px solid transparent;
  background: #fafafa;
}

.item:hover {
  border-color: #52c41a;
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  background: #fff;
}

.item:active {
  opacity: 0.6;
  transform: scale(0.97);
}

.item img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  pointer-events: none;
  background: #f0f0f0;
}

.filename {
  margin: 10px 0 0;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #333;
  font-weight: 500;
}

.item-badge {
  position: absolute;
  bottom: 12px;
  right: 10px;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 600;
}

.item-badge.server {
  background: rgba(82, 196, 26, 0.95);
  color: white;
}

.delete-btn {
  padding: 6px 14px;
  background: #ff4d4f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
  width: 100%;
  margin-top: 8px;
  font-weight: 500;
}

.delete-btn:hover {
  background: #ff7875;
  transform: scale(1.03);
}

.empty-hint {
  grid-column: 1 / -1;
  text-align: center;
  color: #999;
  padding: 60px 20px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  opacity: 0.4;
}

.empty-hint p {
  margin: 10px 0;
  font-size: 17px;
  color: #666;
  font-weight: 500;
}

.empty-desc {
  font-size: 14px;
  color: #999;
}
</style>
