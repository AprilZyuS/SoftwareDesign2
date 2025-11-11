<script setup>
import { ref } from 'vue';

const VideoLink = ref();
const API_BASE = "http://127.0.0.1:8000";

</script>

<template>
  <el-button class="action-btn" @click="BeginSyn">点击复制下载链接</el-button>
</template>

<style scoped>
.action-btn {
  padding: 8px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

</style>