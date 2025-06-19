import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useOcrStore = defineStore('ocr', () => {
  const loading = ref(false)
  const error = ref('')
  const result = ref(null)

  async function uploadImage(file) {
    loading.value = true
    error.value = ''
    result.value = null
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await fetch('/api/upload-image', {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        throw new Error('Upload failed')
      }
      const data = await res.json()
      result.value = data
    } catch (e) {
      error.value = e.message || 'Unknown error'
    } finally {
      loading.value = false
    }
  }

  return { loading, error, result, uploadImage }
}) 