<script setup>
import { ref } from "vue";

const emit = defineEmits(['upload']);

const file = ref(null);
const fileInputRef = ref(null);

function onFileChange(e) {
  const selectedFile = e.target.files[0];
  if (selectedFile) {
    file.value = selectedFile;
    // 发射事件给父组件，传递文件对象
    emit('upload', selectedFile);
    console.log('📤 文件已选择:', selectedFile.name);

    // 清空 input，允许重复选择同一文件
    e.target.value = '';
  }
}

function triggerFileSelect() {
  fileInputRef.value?.click();
}
</script>

<template>
  <div class="uploader-container">
    <input
        ref="fileInputRef"
        type="file"
        @change="onFileChange"
        accept="image/*"
        style="display: none;"
    />
    <button class="upload-btn" @click="triggerFileSelect">
      <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
      </svg>
      选择图片
    </button>
  </div>
</template>

<style scoped>
.uploader-container {
  margin: 20px;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.upload-btn:active {
  transform: translateY(0);
}

.upload-icon {
  width: 18px;
  height: 18px;
}
</style>