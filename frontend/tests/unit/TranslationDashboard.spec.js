import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import TranslationDashboard from '@/components/TranslationDashboard.vue'
import { createPinia, setActivePinia } from 'pinia'
import { useTranslationStore } from '@/stores/translation'

// Mock the translation store
vi.mock('@/stores/translation', () => ({
  useTranslationStore: vi.fn(() => ({
    uploadAndTranslate: vi.fn()
  }))
}))

describe('TranslationDashboard', () => {
  let wrapper
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useTranslationStore()
    wrapper = mount(TranslationDashboard)
  })

  it('renders upload interface', () => {
    expect(wrapper.find('button').text()).toContain('Upload Image')
    expect(wrapper.text()).toContain('or drag and drop image here')
  })

  it('handles file selection', async () => {
    const file = new File([''], 'test.jpg', { type: 'image/jpeg' })
    const input = wrapper.find('input[type="file"]')
    
    await input.setValue(file)
    expect(store.uploadAndTranslate).toHaveBeenCalled()
  })

  it('handles drag and drop', async () => {
    const file = new File([''], 'test.jpg', { type: 'image/jpeg' })
    const dataTransfer = new DataTransfer()
    dataTransfer.items.add(file)
    
    await wrapper.trigger('drop', {
      dataTransfer
    })
    expect(store.uploadAndTranslate).toHaveBeenCalled()
  })

  it('displays translation results', async () => {
    const result = {
      assamese_text: 'Test Assamese text',
      translation: 'Test English translation'
    }
    
    store.uploadAndTranslate.mockResolvedValue(result)
    
    const file = new File([''], 'test.jpg', { type: 'image/jpeg' })
    const input = wrapper.find('input[type="file"]')
    
    await input.setValue(file)
    await wrapper.vm.$nextTick()
    
    expect(wrapper.text()).toContain('Assamese Text')
    expect(wrapper.text()).toContain('English Translation')
    expect(wrapper.text()).toContain(result.assamese_text)
    expect(wrapper.text()).toContain(result.translation)
  })

  it('handles copy to clipboard', async () => {
    const copySpy = vi.spyOn(navigator.clipboard, 'writeText')
    
    const result = {
      assamese_text: 'Test Assamese text',
      translation: 'Test English translation'
    }
    
    store.uploadAndTranslate.mockResolvedValue(result)
    
    const file = new File([''], 'test.jpg', { type: 'image/jpeg' })
    const input = wrapper.find('input[type="file"]')
    
    await input.setValue(file)
    await wrapper.vm.$nextTick()
    
    // Click copy buttons
    const copyButtons = wrapper.findAll('button:has(svg)')
    await copyButtons[0].trigger('click')
    await copyButtons[1].trigger('click')
    
    expect(copySpy).toHaveBeenCalledTimes(2)
    expect(copySpy).toHaveBeenCalledWith(result.assamese_text)
    expect(copySpy).toHaveBeenCalledWith(result.translation)
  })

  it('handles invalid files', async () => {
    // Invalid file type
    const file = new File([''], 'test.txt', { type: 'text/plain' })
    const input = wrapper.find('input[type="file"]')
    
    await input.setValue(file)
    expect(wrapper.text()).toContain('Invalid file type')
    
    // Clear error
    await wrapper.vm.$nextTick()
    expect(wrapper.text()).not.toContain('Invalid file type')
    
    // Large file
    const largeFile = new File([''.repeat(6 * 1024 * 1024)], 'test.jpg', { type: 'image/jpeg' })
    await input.setValue(largeFile)
    expect(wrapper.text()).toContain('File too large')
  })
})
