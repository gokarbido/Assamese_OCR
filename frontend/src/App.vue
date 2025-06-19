<script setup>
import TranslationDashboard from './components/TranslationDashboard.vue'
import ThemeToggle from './components/ThemeToggle.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
    <header class="w-full bg-white dark:bg-gray-800 shadow-sm py-4 px-6 flex items-center justify-between mb-8">
      <div class="flex items-center gap-3">
        <img src="/src/assets/ocr-icon.svg" alt="OCR Icon" class="h-8 w-8" />
        <span class="text-2xl font-bold text-blue-700 tracking-tight">Assamese OCR & Translation</span>
      </div>
    <ThemeToggle />
    </header>
    <main>
      <TranslationDashboard />
    </main>
  </div>
</template>

<style>
body {
  @apply bg-gray-100 dark:bg-gray-900;
}

:root {
  --primary-color: #3b82f6;
  --primary-hover: #2563eb;
  --success-color: #10b981;
  --error-color: #ef4444;
}

.dark {
  --primary-color: #3b82f6;
  --primary-hover: #2563eb;
  --success-color: #10b981;
  --error-color: #ef4444;
}

/* Tailwind CSS is already included */
</style>
