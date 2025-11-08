<script setup>
import { ref, onMounted } from "vue";
import { getProjects, addProject, deleteProject } from "../api";

const projects = ref([]);
const newTitle = ref("");
const newDesc = ref("");

async function loadProjects() {
  projects.value = await getProjects();
}

async function saveProject() {
  if (!newTitle.value) return alert("请输入作品名称");
  await addProject(newTitle.value, newDesc.value);
  newTitle.value = "";
  newDesc.value = "";
  await loadProjects();
}

async function removeProject(id) {
  await deleteProject(id);
  await loadProjects();
}

onMounted(loadProjects);
</script>

<template>
  <div class="project-panel">
    <h3>作品管理</h3>
    <input v-model="newTitle" placeholder="作品标题" />
    <input v-model="newDesc" placeholder="描述（可选）" />
    <button @click="saveProject">保存作品</button>

    <div class="list">
      <div v-for="p in projects" :key="p.id">
        <p><strong>{{ p.title }}</strong></p>
        <p>{{ p.description }}</p>
        <button @click="removeProject(p.id)">删除</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.list {
  margin-top: 10px;
}
.list div {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 5px;
}
</style>
