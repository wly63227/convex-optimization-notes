---
layout: home
hero:
  name: 凸优化
  text: 从几何直觉，到可核查的答案
  tagline: 一份以问题、推导、例题和计算贯穿的中文自学教材
  actions:
    - theme: brand
      text: 从阅读指南开始
      link: /guide
    - theme: alt
      text: 查看知识地图
      link: /syllabus
features:
  - title: 先补基础，再学主线
    details: 向量与导数、凸集与凸函数、标准模型、对偶与算法，按知识依赖阅读。
  - title: 公式有条件，答案能验证
    details: 区分存在性、唯一性、最优性与数值精度，保留关键推导与反例。
  - title: 回得到原始资料
    details: 以 402 页讲义为主要覆盖对象，保留主题与物理页码映射，教材用于解释与补充。
---

<script setup>
import { withBase } from 'vitepress'
</script>

## 选一条适合自己的入口

第一次学习，请从[阅读指南](./guide.md)开始。如果只想查某个概念，用[知识点清单](./knowledge.md)或顶部搜索。如果正在对照课件，用[逐页覆盖索引](./coverage.md)。

正文是唯一维护来源，网站与下载版都由同一组 Markdown 生成。<a :href="withBase('/downloads/凸优化系统学习笔记.md')" download>下载整合版 Markdown</a>，或<a :href="withBase('/downloads/凸优化笔记与图表.zip')" download>下载笔记与配套图表</a>。离线查看图片时，请把压缩包完整解压。

本项目依据本地 Boyd 与 Vandenberghe 教材、修订讲义整理。自编例题与参考解不代表教师官方答案；没有据此推定任何考试范围。
