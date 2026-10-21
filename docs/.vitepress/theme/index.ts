import DefaultTheme from 'vitepress/theme'
import './style.css'
import StepSizeLab from './StepSizeLab.vue'
export default {
  extends: DefaultTheme,
  enhanceApp({app}) { app.component('StepSizeLab', StepSizeLab) }
}
