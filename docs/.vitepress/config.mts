import { defineConfig } from 'vitepress'

const chapters = [
 ['00-foundations','预备章 · 数学基础'], ['01-modeling','1 · 优化建模'],
 ['02-sets','2 · 凸集'], ['03-functions','3 · 凸函数'],
 ['04-problems','4 · 凸问题与建模'], ['05-duality','5 · 对偶与 KKT'],
 ['06-approximation','6 · 逼近与拟合'], ['07-statistics','7 · 统计估计'],
 ['08-geometry','8 · 几何应用'], ['appendix-numerics','附录 · 数值线性代数'],
 ['09-unconstrained','9 · 无约束算法'], ['10-equality','10 · 等式约束算法'],
 ['11-interior','11 · 内点法'], ['12-practice','12 · 综合实践']
]
export default defineConfig({
  lang: 'zh-CN',
  title: '凸优化 · 从直觉到求解',
  description: '依据 Boyd 与 Vandenberghe 教材和讲义整理的中文自学教材',
  base: process.env.SITE_BASE || '/',
  cleanUrls: false,
  srcExclude: ['public/**'],
  lastUpdated: false,
  markdown: { math: true },
  head: [['meta', { name: 'theme-color', content: '#176b62' }]],
  themeConfig: {
    siteTitle: '凸优化自学教材',
    nav: [
      { text:'开始学习', link:'/guide' },
      { text:'知识地图', link:'/syllabus' },
      { text:'查知识点', link:'/knowledge' },
      { text:'资料与覆盖', link:'/sources' }
    ],
    sidebar: [
      { text:'阅读入口', items:[
        {text:'阅读指南与统一符号',link:'/guide'},
        {text:'学习大纲与知识地图',link:'/syllabus'}
      ]},
      { text:'系统教材', items: chapters.map(([p,t])=>({text:t,link:'/'+p})) },
      { text:'练习与追溯', items:[
        {text:'练习与参考解',link:'/exercises'},
        {text:'程序实验',link:'/experiments'},
        {text:'全课程知识点',link:'/knowledge'},
        {text:'来源与版本',link:'/sources'},
        {text:'逐页覆盖索引',link:'/coverage'},
        {text:'图表设计说明',link:'/visualizations'},
        {text:'维护与更新',link:'/maintenance'},
        {text:'建设与验收报告',link:'/report'}
      ]}
    ],
    outline: { level: [2,3], label:'本页内容' },
    search: { provider:'local', options:{ locales:{ root:{
      translations:{button:{buttonText:'搜索笔记',buttonAriaLabel:'搜索笔记'},
      modal:{noResultsText:'没有找到相关内容',resetButtonTitle:'清除搜索',
      footer:{selectText:'选择',navigateText:'切换',closeText:'关闭'}}}
    }}}},
    docFooter:{prev:'上一节',next:'下一节'},
    darkModeSwitchLabel:'外观',
    sidebarMenuLabel:'章节导航',
    returnToTopLabel:'回到顶部',
    footer:{message:'核心内容依据本地讲义；例题、参考解与复现代码不代表教师官方答案。'}
  }
})
