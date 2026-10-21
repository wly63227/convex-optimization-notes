# 凸优化中文自学教材

依据 knowledge-prompt(1).md 建设。主要覆盖本地 402 页 Boyd–Vandenberghe 修订讲义，714 页教材用于解释、推导与核正。

## 从这里开始

- [新版整合 Markdown](./凸优化系统学习笔记.md)
- [阅读指南与统一符号](./docs/guide.md)
- [学习大纲](./docs/syllabus.md)
- [知识点清单](./docs/knowledge.md)
- [逐页来源覆盖](./docs/coverage.md)
- [来源版本与勘误](./docs/sources.md)
- [练习与参考解](./docs/exercises.md)
- [程序实验](./docs/experiments.md)
- [建设与验收报告](./docs/report.md)

已有的“凸优化从零开始学习笔记.md”完整保留；新版正文只在 docs/ 中维护，整合版与网站由同一份内容生成。

## 本地环境

网站需要 Node.js 22 或以上与 pnpm 11。Python 复现建议 3.12；先建立自己的虚拟环境：

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pnpm install --frozen-lockfile
pnpm run dev
~~~

安装仅允许 esbuild 的构建脚本，配置位于 pnpm-workspace.yaml。首次依赖安装与后续构建分开进行，不需要全局安装 VitePress。

## 完整验证与构建

~~~powershell
python scripts/inventory.py
python scripts/generate_indexes.py
python examples/run_experiments.py
python scripts/check_math.py
python scripts/generate_figures.py
python scripts/prepare_download.py
python scripts/check_content.py
pnpm run build
node scripts/check_site.mjs
pnpm run preview
~~~

保持源 PDF 在根目录，才可以运行完整来源哈希检查。它们不自动随公开站点发布；教材、讲义原作者权利不因本项目改变。

## 项目结构

| 路径 | 用途 |
|---|---|
| docs/ | 唯一 Markdown 正文、图表与网站配置 |
| sources/topics.tsv | 稳定知识 ID 与页码映射 |
| sources/manifest.json | 来源指纹与版本 |
| sources/baseline.json | 内容、锚点、公式保留基线 |
| examples/ | 固定小数据与可复现模型 |
| results/ | 实际执行的结果与检查记录 |
| scripts/ | 调查、索引、图表、下载版与质量检查 |
| .github/workflows/ | GitHub Pages 构建与部署 |
| PROGRESS.md | 任务状态与剩余事项 |

## GitHub Pages 发布

正式站点使用 GitHub Pages，入口为 https://wly63227.github.io/convex-optimization-notes/ 。源码仓库为 https://github.com/wly63227/convex-optimization-notes 。发布结果与版本记录保存在 results/deployment.json；线上 release.json 标明构建对应的源码提交。原始 PDF、依赖、缓存与临时截图不随站点发布。

推送到 main 后，“教材检查与 Pages 发布”工作流会先运行来源、内容、数学与静态站点检查，再部署构建产物。仓库 Settings → Pages → Build and deployment 的来源必须设置为 GitHub Actions。

工作流根据仓库名自动选择子路径。用户名首页仓库使用根路径；普通项目使用 /仓库名/。发布后检查 /release.json 的 commit，并抽查公式、图片、搜索与手机页面。

CI 只使用已审查的来源元数据；没有上传原 PDF 时，不会声称重新验证其二进制哈希。新增课件与修改数学内容时，必须先在本地完成[维护流程](./docs/maintenance.md)。

## 材料与许可

自编讲解、例题和程序参考解不代表教师答案。没有据此推定考试范围，没有为原始 PDF 擅自授予开源许可。大型讲义案例缺少原始数据时，保留方法解释，以明确标注的小数据实验补充。
