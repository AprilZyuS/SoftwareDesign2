<template>
  <div class="app-container">
    <!-- 顶部导航 -->
    <div class="workflow-tabs">
      <div
          v-for="tab in tabs"
          :key="tab"
          class="tab"
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
      >
        {{ tab }}
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-area">
      <div class="center-content">
        <component :is="currentComponent" />

      </div>

      <!-- 右侧素材库 -->
      <div class="right-panel">
        <h3>素材库</h3>
        <MaterialLibrary :materials="materials" @select="selectMaterial" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MaterialUploader from './components/MaterialUploader.vue'
import MaterialLibrary from './components/MaterialLibrary.vue'
import MaterialGeneration from './components/MaterialGeneration.vue'
import Synthesis from './components/Synthesis.vue'
import VideoGeneration from './components/VideoGeneration.vue'
import VideoDubbing from './components/VideoDubbing.vue'

const tabs = ['素材生成', '合成', '视频生成', '视频配音']
const activeTab = ref('素材生成')
const loading = ref(false)
const audioUrl = ref('')
const materials = ref([])

const tabComponents = {
  '素材生成': MaterialGeneration,
  '合成': Synthesis,
  '视频生成': VideoGeneration,
  '视频配音': VideoDubbing
}

// 根据当前激活的标签，计算需要渲染的组件
const currentComponent = computed(() => {
  return tabComponents[activeTab.value]
})

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

const selectMaterial = (item) => console.log('选择素材：', item)
const downloadFile = () => alert('下载中...')
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* 顶部导航 */
.workflow-tabs {
  display: flex;
  background: linear-gradient(to right, #00b4ff, #ff4d94);
  padding: 8px;
}
.tab {
  padding: 10px 30px;
  cursor: pointer;
  border-radius: 8px;
  margin-right: 8px;
  font-weight: 600;
  transition: 0.2s;
}
.tab:hover {
  background: rgba(255, 255, 255, 0.2);
}
.tab.active {
  background: white;
  color: black;
}

/* 主区布局 */
.main-area {
  flex: 1;
  display: flex;
  justify-content: space-between;
  padding: 24px;
}

/* 中心内容区 */
.center-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

/* 右侧素材库 */
.right-panel {
  width: 280px;
  background: #1e1e1e;
  padding: 16px;
  border-radius: 12px;
  overflow-y: auto;
}
.right-panel h3 {
  margin-bottom: 12px;
}


</style>

