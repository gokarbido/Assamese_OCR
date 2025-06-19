<template>
  <div class="uploader" :class="{ dragging }" @dragover.prevent="dragging = true" @dragleave.prevent="dragging = false" @drop.prevent="onDrop">
    <input type="file" accept="image/png, image/jpeg" @change="onFileChange" ref="fileInput" style="display:none" />
    <div v-if="imageUrl" class="preview">
      <img :src="imageUrl" alt="Preview" />
      <button @click="removeImage">Remove</button>
    </div>
    <div v-else class="upload-area" @click="triggerFileInput">
      <p>Drag & drop an image here, or <span class="browse">browse</span></p>
      <p class="hint">(JPG/PNG, max 5MB)</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useOcrStore } from '../../stores/ocr'

const fileInput = ref(null)
const dragging = ref(false)
const ocrStore = useOcrStore()
const imageUrl = computed(() => ocrStore.imageUrl)

function triggerFileInput() {
  fileInput.value.click()
}

function onFileChange(e) {
  const file = e.target.files[0]
  handleFile(file)
}

function onDrop(e) {
  dragging.value = false
  const file = e.dataTransfer.files[0]
  handleFile(file)
}

function handleFile(file) {
  if (!file) return
  if (!['image/jpeg', 'image/png'].includes(file.type)) {
    ocrStore.error = 'Only JPG/PNG images are allowed.'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    ocrStore.error = 'File size exceeds 5MB.'
    return
  }
  const reader = new FileReader()
  reader.onload = (e) => {
    ocrStore.setImageUrl(e.target.result)
  }
  reader.readAsDataURL(file)
  ocrStore.uploadImage(file)
}

function removeImage() {
  ocrStore.clear()
  fileInput.value.value = ''
}
</script>

<style scoped>
.uploader {
  border: 2px dashed #aaa;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}
.uploader.dragging {
  border-color: #42b983;
  background: #f0f9f5;
}
.upload-area {
  color: #888;
}
.browse {
  color: #42b983;
  text-decoration: underline;
  cursor: pointer;
}
.preview {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.preview img {
  max-width: 300px;
  max-height: 200px;
  margin-bottom: 1rem;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.preview button {
  background: #ff4d4f;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.hint {
  font-size: 0.9em;
  color: #aaa;
}
</style> 