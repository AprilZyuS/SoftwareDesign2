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

onMounted(loadMaterials);
</script>

<template>
  <div class="material-list">
    <div class="grid">
      <div v-for="m in materials" :key="m.id" class="item">
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
}

.item img {
  width: 100%;
  height: 80px;
  object-fit: cover;
}
</style>
