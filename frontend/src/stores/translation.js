import { defineStore } from 'pinia'
import axios from 'axios'

export const useTranslationStore = defineStore('translation', {
  state: () => ({
    isLoading: false,
    error: null,
  }),

  actions: {
    async uploadAndTranslate(formData) {
      try {
        this.isLoading = true
        this.error = null

        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await axios.post(`${apiUrl}/upload-image`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'An error occurred while processing the image'
        throw error
      } finally {
        this.isLoading = false
      }
    },
  },
})
