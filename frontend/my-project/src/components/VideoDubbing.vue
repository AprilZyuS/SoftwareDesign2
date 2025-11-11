<script setup>
import {ref} from "vue";
import MaterialUploader from "./MaterialUploader.vue";

const activeTab = ref('素材生成')
const loading = ref(false)
const audioUrl = ref('')
const materials = ref([])

const handleUpload = (file) => {
  if (!file) return

  const imageURL = URL.createObjectURL(file)

  materials.value.push({
    id: Date.now(),
    name: file.name,
    thumbnail: imageURL,
    file
  })

  console.log("已添加素材",file.name)
}

const startDubbing = () => {
  loading.value = true
  setTimeout(() => {
    audioUrl.value = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
    loading.value = false
  }, 1000)
}

const downloadFile = () => alert('下载中...')

</script>

<template>
  <MaterialUploader @upload="handleUpload" />
  <el-button type="primary" :loading="loading" @click="startDubbing">开始配音</el-button>

  <div v-if="audioUrl" class="preview-box">
    <audio :src="audioUrl" controls></audio>
  </div>

  <el-button type="success" @click="downloadFile">下载文件</el-button>
</template>

<style scoped>

</style>