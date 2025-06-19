<template>
  <div class="w-full mx-auto bg-gray-100 dark:bg-gray-800 rounded-2xl shadow-2xl p-6 md:p-10 my-10 flex flex-col min-h-[520px]">
    <!-- Mobile Header (for branding on small screens) -->
    <div class="md:hidden flex items-center gap-3 mb-6">
      <img src="/src/assets/ocr-icon.svg" alt="OCR Icon" class="h-7 w-7" />
      <span class="text-xl font-bold text-blue-700 tracking-tight">Assamese OCR & Translation</span>
    </div>
    <!-- Loading Overlay -->
    <div v-if="translationStore.isLoading" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div class="flex flex-col items-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
        </svg>
        <span class="text-white text-lg font-semibold">Recognizing text, please wait...</span>
      </div>
    </div>
    <!-- Copy Toast -->
    <div v-if="showCopyToast" class="fixed top-6 left-1/2 transform -translate-x-1/2 z-50 bg-green-500 text-white px-6 py-2 rounded shadow-lg transition-all">
      Text copied!
    </div>
    <div class="flex flex-col md:flex-row gap-10 w-full h-full">
      <!-- Left: Upload & Preview -->
      <div class="w-full md:w-1/2 flex-1 min-w-0 flex flex-col items-center gap-6 justify-center">
        <input
          type="file"
          ref="fileInput"
          accept="image/jpeg,image/png"
          @change="handleFileChange"
          class="hidden"
        />
        <button
          @click="selectFile"
          class="bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center w-full font-semibold text-lg text-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>Upload Image</span>
        </button>
        <p class="text-gray-600 dark:text-gray-400 text-sm text-center">or drag and drop image here</p>
        <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
          Supported formats: JPG, PNG (max 5MB)
        </p>
        <div 
          class="w-full border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center min-h-[180px] bg-gray-50 dark:bg-gray-700 cursor-pointer transition-all duration-300 hover:border-blue-500 mt-2"
          @dragover.prevent
          @dragenter.prevent
          @drop.prevent="handleDrop"
        >
          <div v-if="previewImage" class="w-full flex flex-col items-center">
            <img :src="previewImage" class="object-contain max-h-56 w-full rounded-lg shadow mb-2 bg-white" />
            <div class="text-xs text-gray-500 dark:text-gray-300 mb-2">Preview</div>
          </div>
          <div v-else class="text-gray-400 text-lg py-8">No image selected</div>
        </div>
        <!-- Recognize Button -->
        <div v-if="previewImage && !translationResult" class="w-full flex justify-center mt-2">
          <button
            @click="recognize"
            :disabled="!selectedFile || translationStore.isLoading"
            class="bg-green-600 text-white py-3 px-8 rounded-lg hover:bg-green-700 transition-colors text-lg font-semibold disabled:opacity-60 disabled:cursor-not-allowed shadow w-full text-center"
          >
            Recognize Text
          </button>
        </div>
        <!-- Upload Status -->
        <div v-if="uploadStatus" class="w-full mt-2">
          <div v-if="uploadStatus === 'success'" class="text-green-500 font-medium flex items-center gap-2">
            <svg class="inline-block w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            Upload successful!
          </div>
          <div v-if="uploadStatus === 'error'" class="text-red-500 font-medium flex items-center gap-2">
            <svg class="inline-block w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            {{ uploadError }}
          </div>
        </div>
      </div>
      <!-- Right: Results -->
      <div class="w-full md:w-1/2 flex-1 flex flex-col gap-8 justify-center min-h-[320px]">
        <!-- Alert if OCR fails -->
        <div v-if="translationResult && !translationResult.assamese_text" class="w-full mb-4">
          <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative text-center" role="alert">
            <strong class="font-bold">No text recognized!</strong>
            <span class="block sm:inline"> The OCR engine could not detect any text in the image.</span>
          </div>
        </div>
        <div v-if="translationResult" class="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 shadow w-full">
          <h3 class="text-xl font-bold mb-4 text-blue-700 dark:text-blue-300 flex items-center gap-2">
            <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
            </svg>
            Assamese Text
          </h3>
          <div class="text-gray-800 dark:text-gray-300 text-lg mb-4 whitespace-pre-line break-words">
            <p class="mb-4">{{ translationResult.assamese_text }}</p>
            <button
              @click="copyToClipboard(translationResult.assamese_text)"
              class="inline-flex items-center justify-center w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 dark:bg-blue-900 dark:text-blue-300 dark:border-blue-700 dark:hover:bg-blue-800 transition-colors text-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
              </svg>
              Copy to clipboard
            </button>
          </div>
        </div>
        <div v-if="translationResult" class="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 shadow w-full">
          <h3 class="text-xl font-bold mb-4 text-green-700 dark:text-green-300 flex items-center gap-2">
            <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
            </svg>
            English Translation
          </h3>
          <div class="text-gray-800 dark:text-gray-300 text-lg mb-4 whitespace-pre-line break-words">
            <p class="mb-4">{{ translationResult.translation }}</p>
            <button
              @click="copyToClipboard(translationResult.translation)"
              class="inline-flex items-center justify-center w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 dark:bg-green-900 dark:text-green-300 dark:border-green-700 dark:hover:bg-green-800 transition-colors text-center"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>
              </svg>
              Copy to clipboard
            </button>
          </div>
        </div>
        <div v-else class="flex flex-col items-center justify-center h-full min-h-[220px] w-full bg-gray-50 dark:bg-gray-900 rounded-xl p-6 shadow border-2 border-dashed border-gray-200 dark:border-gray-700">
          <svg class="w-16 h-16 text-gray-300 dark:text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2a4 4 0 014-4h3m4 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
          </svg>
          <div class="text-gray-400 dark:text-gray-500 text-lg text-center">Recognition results will appear here</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTranslationStore } from '../stores/translation'

const fileInput = ref(null)
const previewImage = ref(null)
const uploadStatus = ref(null)
const uploadError = ref('')
const translationResult = ref(null)
const selectedFile = ref(null)

const translationStore = useTranslationStore()

// Toast state for copy
const showCopyToast = ref(false)

const selectFile = () => {
  fileInput.value.click()
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    handleFileChange({ target: { files: [file] } })
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type and size
  if (!file.type.startsWith('image/')) {
    uploadStatus.value = 'error'
    uploadError.value = 'Please upload an image file (JPG/PNG)'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    uploadStatus.value = 'error'
    uploadError.value = 'File is too large (max 5MB)'
    return
  }

  // Create preview
  previewImage.value = URL.createObjectURL(file)
  uploadStatus.value = null
  uploadError.value = ''
  translationResult.value = null
  selectedFile.value = file
}

const recognize = async () => {
  if (!selectedFile.value) return
  uploadStatus.value = null
  uploadError.value = ''
  translationResult.value = null
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  try {
    const result = await translationStore.uploadAndTranslate(formData)
    translationResult.value = result
    uploadStatus.value = 'success'
  } catch (error) {
    uploadStatus.value = 'error'
    uploadError.value = error.message
  }
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => {
      showCopyToast.value = true
      setTimeout(() => {
        showCopyToast.value = false
      }, 1500)
    })
    .catch(err => {
      console.error('Failed to copy text: ', err)
    })
}
</script>

<style>
body {
  background: #f9fafb;
}
</style>
