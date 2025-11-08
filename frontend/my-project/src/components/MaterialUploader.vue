<script setup>
import { ref } from "vue";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";
const file = ref(null);
const userId = 1;

function onFileChange(e) {
  file.value = e.target.files[0];
}

async function upload() {
  if (!file.value) return alert("请选择文件");
  const formData = new FormData();
  formData.append("file", file.value);
  formData.append("user_id", userId);

  const res = await axios.post(`${API_BASE}/upload/`, formData, {
    headers: {"Content-Type": "multipart/form-data"},
  });

  alert(`上传成功：${res.data.filename}`);
}
</script>

<template>
  <div>
    <input type="file" @change="onFileChange"/>
    <button @click="upload">上传素材</button>
  </div>
</template>
