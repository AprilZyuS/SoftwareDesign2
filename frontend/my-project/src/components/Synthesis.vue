<script setup>
import {ref} from 'vue';
import Synthesis from "./Synthesis.vue";

const firstFile = ref(null)
const lastFile = ref(null)

const firstFileUrl = ref(null);
const lastFileUrl = ref(null);


// 图片源（默认使用网络图片,可替换为本地路径）
const image1 = ref('https://picsum.photos/600/400?random=1');
const image2 = ref('https://picsum.photos/600/400?random=2');

// 上传输入框引用
const uploadInput1 = ref(null);
const uploadInput2 = ref(null);

// 预览相关
const previewSrc = ref('');

// 拖拽状态(用于显示拖拽提示)
const dragOver1 = ref(false);
const dragOver2 = ref(false);

// 触发上传（点击按钮打开文件选择）
const triggerUpload = (index) => {
  if (index === 1) uploadInput1.value.click();
  else uploadInput2.value.click();
};

// 处理图片上传
const handleUpload = (index, e) => {
  const file = e.target.files[0];
  if (file) {
    const url = URL.createObjectURL(file);

    if (index === 1) {
      image1.value = url;
      firstFile.value = file;
    } else {
      image2.value = url;
      lastFile.value = file;
    }

    e.target.value = '';
  }
};


// 预览图片
const previewImage = (index) => {
  previewSrc.value = index === 1 ? image1.value : image2.value;
};

// 关闭预览
const closePreview = () => {
  previewSrc.value = '';
};

// 拖拽进入
const handleDragEnter = (index, e) => {
  e.preventDefault();
  index === 1 ? dragOver1.value = true : dragOver2.value = true;
};

// 拖拽离开
const handleDragLeave = (index) => {
  index === 1 ? dragOver1.value = false : dragOver2.value = false;
};

// 拖拽悬停
const handleDragOver = (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'copy';
};

// 处理放置
const handleDrop = (index, e) => {
  e.preventDefault();
  index === 1 ? dragOver1.value = false : dragOver2.value = false;

  const source = e.dataTransfer.getData("source");

  if (source === "library") {
    const materialStr = e.dataTransfer.getData("material");
    if (!materialStr) return;

    const material = JSON.parse(materialStr);

    // 直接使用 URL 显示图片
    if (index === 1) {
      image1.value = material.url;

      // 注意：生成视频时后端需要文件，这里你没有 File，只能传 URL
      // 所以后端 first_frame 应改为接收 URL
      firstFile.value = material.url;
    } else {
      image2.value = material.url;
      lastFile.value = material.url;
    }

    console.log("📥 从素材库拖入图片框:", material.filename);
    return;
  }


  const file = e.dataTransfer.files[0];
  if (!file) return;

  const url = e.dataTransfer.getData("material-url");
  if (url) {
    if (index === 1) {
      image1.value = BASE_URL + url;  // 关键：完整 URL
    } else {
      image2.value = BASE_URL + url;
    }
    return;
  }

};


const BeginSyn = async () => {
  try {
    // 检查是否有图片
    if (!firstFile.value && !firstFileUrl.value) {
      alert("请先上传或选择首帧图片");
      return;
    }
    if (!lastFile.value && !lastFileUrl.value) {
      alert("请先上传或选择尾帧图片");
      return;
    }

    let firstImgUrl, lastImgUrl;

    // 处理首帧
    if (firstFile.value instanceof File) {
      console.log("⬆️ 上传首帧图片...");
      const formData = new FormData();
      formData.append("file", firstFile.value);
      formData.append("user_id", 1);

      const uploadRes = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!uploadRes.ok) {
        throw new Error(`首帧上传失败: ${uploadRes.status}`);
      }

      const uploadData = await uploadRes.json();
      firstImgUrl = uploadData.url;
      console.log("✅ 首帧上传成功:", firstImgUrl);
    } else {
      // URL 素材
      firstImgUrl = firstFile.value || firstFileUrl.value;
      console.log("✅ 使用素材库首帧:", firstImgUrl);
    }

    // 处理尾帧
    if (lastFile.value instanceof File) {
      console.log("⬆️ 上传尾帧图片...");
      const formData = new FormData();
      formData.append("file", lastFile.value);
      formData.append("user_id", 1);

      const uploadRes = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!uploadRes.ok) {
        throw new Error(`尾帧上传失败: ${uploadRes.status}`);
      }

      const uploadData = await uploadRes.json();
      lastImgUrl = uploadData.url;
      console.log("✅ 尾帧上传成功:", lastImgUrl);
    } else {
      lastImgUrl = lastFile.value || lastFileUrl.value;
      console.log("✅ 使用素材库尾帧:", lastImgUrl);
    }

    // 发送视频生成请求
    const body = {
      text: "360度环绕运镜",
      first_imgurl: firstImgUrl,
      last_imgurl: lastImgUrl,
    };

    console.log("🎬 发送视频生成请求:", body);

    const res = await fetch("http://127.0.0.1:8000/video/generate/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`请求失败 ${res.status}: ${errorText}`);
    }

    const data = await res.json();
    console.log("✅ 后端返回:", data);

    if (data.status === "success") {
      alert(`视频生成成功!\n\n视频URL:\n${data.video_url}`);
    } else {
      alert(`生成失败: ${data.msg}`);
    }
  } catch (err) {
    console.error("❌ 错误:", err);
    //alert(`操作失败: ${err.message}`);
  }
};


</script>

<template>
  <div class="image-display-container">
    <!-- 第一个图片展示框 -->
    <div class="image-box">
      <div
          class="image-preview"
          :class="{ 'drag-over': dragOver1 }"
          @dragenter="handleDragEnter(1, $event)"
          @dragleave="handleDragLeave(1)"
          @dragover="handleDragOver"
          @drop="handleDrop(1, $event)"
      >
        <img :src="image1" alt="图片1" class="display-image" @click="previewImage(1)">
        <div v-if="dragOver1" class="drag-hint">松开以替换图片</div>
      </div>
      <div class="image-actions">
        <label>首帧</label>
        <input
            type="file"
            accept="image/*"
            @change="handleUpload(1, $event)"
            class="upload-input"
            ref="uploadInput1"
        >
      </div>
    </div>

    <!-- 第二个图片展示框 -->
    <div class="image-box">
      <div
          class="image-preview"
          :class="{ 'drag-over': dragOver2 }"
          @dragenter="handleDragEnter(2, $event)"
          @dragleave="handleDragLeave(2)"
          @dragover="handleDragOver"
          @drop="handleDrop(2, $event)"
      >
        <img :src="image2" alt="图片2" class="display-image" @click="previewImage(2)">
        <div v-if="dragOver2" class="drag-hint">松开以替换图片</div>
      </div>
      <div class="image-actions">
        <label>尾帧</label>
        <input
            type="file"
            accept="image/*"
            @change="handleUpload(2, $event)"
            class="upload-input"
            ref="uploadInput2"
        >
      </div>
    </div>

    <!-- 预览模态框 -->
    <div v-if="previewSrc" class="preview-modal" @click="closePreview">
      <img :src="previewSrc" class="preview-img">
    </div>
  </div>
  <el-button class="action-btn" @click="BeginSyn">开始合成</el-button>

</template>

<style scoped>
.image-display-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: flex-start;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.image-box {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.image-preview {
  width: 100%;
  height: 400px;
  border-radius: 8px;
  background: #f9f9f9;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

/* 拖拽悬停效果 */
.image-preview.drag-over {
  border: 2px dashed #4096ff;
  background: rgba(64, 150, 255, 0.05);
}

/* 拖拽提示 */
.drag-hint {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(64, 150, 255, 0.9);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  pointer-events: none;
  z-index: 10;
}

.display-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-preview:empty::after {
  content: '点击上传图片或拖拽图片到此';
  color: #999;
  font-size: 14px;
}

.display-image:hover {
  transform: scale(1.01);
}

.image-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
  justify-content: center;
}

.action-btn {
  padding: 8px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.action-btn:not(.clear-btn) {
  background: #4096ff;
  color: white;
}

.action-btn:not(.clear-btn):hover {
  background: #69b1ff;
}

.clear-btn {
  background: #f5f5f5;
  color: #666;
}

.clear-btn:hover {
  background: #e8e8e8;
}

.upload-input {
  display: none;
}

.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  cursor: zoom-out;
}

.preview-img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

@media (max-width: 768px) {
  .image-display-container {
    flex-direction: column;
    padding: 15px;
  }

  .image-box {
    max-width: 100%;
  }

  .image-preview {
    height: 300px;
  }
}

</style>