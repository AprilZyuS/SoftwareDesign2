<script setup>
import { ref } from "vue";
import axios from "axios";
import { addMaterial } from "../api";

const API_BASE = "http://127.0.0.1:8000";
const materialsRef = defineProps(["onUploaded"]);

const file = ref(null);

function onFileChange(e) {
  file.value = e.target.files[0];
}

async function upload() {
  if (!file.value) return alert("请选择文件");
  const formData = new FormData();
  formData.append("file", file.value);

  // 上传图片文件
  const res = await axios.post(`${API_BASE}/upload/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  const { url, filename } = res.data;
  const fullUrl = `${API_BASE}${url}`;

  // 保存元数据到数据库
  await addMaterial(filename, fullUrl);

  if (materialsRef.onUploaded) materialsRef.onUploaded();
}
</script>

<template>
  <div class="uploader">
    <input type="file" @change="onFileChange" />
    <button @click="upload">上传素材</button>
  </div>
</template>
