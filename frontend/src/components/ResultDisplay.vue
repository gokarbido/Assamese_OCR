<template>
  <div v-if="ocrStore.imageUrl" class="result-display">
    <div v-if="ocrStore.loading" class="loading">Processing image...</div>
    <div v-else>
      <div v-if="ocrStore.error" class="error">{{ ocrStore.error }}</div>
      <div v-else>
        <div class="text-block">
          <label>Assamese Text</label>
          <div class="text-content">{{ ocrStore.assameseText || '—' }}</div>
          <button @click="copy(ocrStore.assameseText)">Copy</button>
        </div>
        <div class="text-block">
          <label>English Translation</label>
          <div class="text-content">{{ ocrStore.translation || '—' }}</div>
          <button @click="copy(ocrStore.translation)">Copy</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOcrStore } from '../../stores/ocr'
const ocrStore = useOcrStore()

function copy(text) {
  if (!text) return
  navigator.clipboard.writeText(text)
}
</script>

<style scoped>
.result-display {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.text-block {
  background: #f8f8f8;
  border-radius: 6px;
  padding: 1rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
label {
  font-weight: bold;
  color: #42b983;
}
.text-content {
  font-family: inherit;
  font-size: 1.1em;
  margin-bottom: 0.5rem;
  word-break: break-word;
}
button {
  align-self: flex-start;
  background: #42b983;
  color: #fff;
  border: none;
  padding: 0.3rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.loading {
  color: #888;
  font-style: italic;
}
.error {
  color: #ff4d4f;
  font-weight: bold;
}
</style> 