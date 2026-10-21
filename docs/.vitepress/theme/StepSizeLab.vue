<script setup>
import { ref, computed } from 'vue'
import { stepSequence } from './step-model.mjs'
const eta = ref(0.25)
const points = computed(() => stepSequence(Number(eta.value)))
const limit = computed(() => Math.max(2, ...points.value.map(p => p.error)) * 1.08)
const path = computed(() => points.value.map(p => (45+p.k*47.5)+','+(200-165*p.error/limit.value)).join(' '))
const factor = computed(() => 1-2*Number(eta.value))
const status = computed(() => Math.abs(factor.value)<1 ? '误差幅度收敛到零' : Math.abs(factor.value)===1 ? '误差幅度不缩小' : '误差幅度不断扩大')
</script>
<template>
  <section class="step-lab" aria-label="梯度下降步长实验">
    <div class="controls">
      <label for="step-size">步长 η = {{ Number(eta).toFixed(2) }}</label>
      <input id="step-size" type="range" min="0.05" max="1.20" step="0.05" v-model="eta" aria-describedby="step-help" />
      <button type="button" @click="eta=0.25">重置</button>
    </div>
    <p id="step-help">使用方向键调整步长；每次从 x = 0 重新计算 8 步。</p>
    <p aria-live="polite">误差乘数 {{ factor.toFixed(2) }}：{{ status }}。</p>
    <svg viewBox="0 0 460 245" role="img" aria-label="误差绝对值随迭代次数变化">
      <path d="M45 25V200H430" fill="none" stroke="currentColor"/>
      <polyline :points="path" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="3"/>
      <circle v-for="p in points" :key="p.k" :cx="45+p.k*47.5" :cy="200-165*p.error/limit" r="3.5" fill="var(--vp-c-brand-1)"/>
      <text x="5" y="16" fill="currentColor">|误差|</text>
      <text x="20" y="205" fill="currentColor">0</text>
      <text x="45" y="224" fill="currentColor">0</text>
      <text x="420" y="224" fill="currentColor">8</text>
      <text x="190" y="242" fill="currentColor">迭代次数 k</text>
      <text x="2" y="40" font-size="12" fill="currentColor">{{ limit.toFixed(2) }}</text>
    </svg>
    <p>第 8 步：x = {{ points[8].x.toFixed(6) }}，目标值 = {{ points[8].value.toFixed(6) }}。</p>
  </section>
</template>
<style scoped>
.step-lab{margin:24px 0;padding:20px;border:1px solid var(--vp-c-divider);border-radius:12px;background:var(--vp-c-bg-soft)}
.controls{display:flex;align-items:center;flex-wrap:wrap;gap:16px}
label{font-weight:600;min-width:135px}input{flex:1;min-width:130px;accent-color:var(--vp-c-brand-1)}
button{padding:5px 14px;border:1px solid var(--vp-c-divider);border-radius:6px;background:var(--vp-c-bg)}
button:focus-visible,input:focus-visible{outline:3px solid var(--vp-c-brand-1);outline-offset:3px}
svg{display:block;width:100%;max-width:580px;margin:14px auto}
p{font-size:14px;line-height:1.8;margin:12px 0!important}
</style>
