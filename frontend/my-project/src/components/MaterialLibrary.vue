<script setup>
import {ref, onMounted} from "vue";
import {getMaterials, deleteMaterial} from "../api";

const materials = ref([]);
const API_BASE = "http://127.0.0.1:8000";

async function loadMaterials() {
  materials.value = await getMaterials();
}

async function removeMaterial(id) {
  await deleteMaterial(id);
  await loadMaterials();
}

// 拖拽开始
function handleDragStart(event, material) {
  // 传递图片URL
  event.dataTransfer.setData('imageUrl', API_BASE + material.filepath);
  event.dataTransfer.effectAllowed = 'copy';
}

onMounted(loadMaterials);
</script>

<template>
  <div class="material-list">
    <div class="grid">
      <div
          v-for="m in materials"
          :key="m.id"
          class="item"
          draggable="true"
          @dragstart="handleDragStart($event, m)"
      >
        <img :src="API_BASE + m.filepath" :alt="m.filename"/>
        <p>{{ m.filename }}</p>
        <button @click="removeMaterial(m.id)">删除</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.item {
  width: 120px;
  text-align: center;
  cursor: move; /* 添加拖拽光标 */
  transition: opacity 0.2s;
}

.item:active {
  opacity: 0.5; /* 拖拽时半透明 */
}

.item img {
  width: 100%;
  height: 80px;
  object-fit: cover;
  pointer-events: none; /* 防止图片干扰拖拽 */
}
</style>