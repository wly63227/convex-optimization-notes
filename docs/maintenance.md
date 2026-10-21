# 维护与更新

## 正文只改一处

所有正文维护在 docs/ 的 Markdown 中。根目录的“凸优化系统学习笔记.md”、网站下载版与构建产物由脚本生成，不能分开改写。原始入门稿保留为历史交付，不作为新版网站的另一套正文。

知识条目在 sources/topics.tsv，来源元数据在 sources/manifest.json，逐页提取与覆盖在 sources/pages.json。后者包含大量原始提取文本，不随公开构建自动发布；可由本地原始 PDF 重建。

## 新课件到来时

1. 把新文件保存在工作目录，先记录文件名、版本、SHA-256 和页数。
2. 运行内容检查发现新增、缺失或修改；不要立即覆盖旧来源基线。
3. 对照旧页与新页，检查公式、图示、案例、代码和补充内容。哈希只能识别文件变化，不能自动判断知识变化。
4. 更新来源调查脚本和主题页码映射；已有知识 ID 不重排，新增内容分配新 ID。
5. 改写受影响的正文、例题、图表模型与实验。知识点合并时保留旧链接或注明迁移。
6. 重新运行索引、计算、图形与构建，实际浏览器检查相关页面。
7. 如果数学内容确实改变，记录原因，人工审查基线差异后显式重建内容基线。

## 质量命令

~~~bash
python scripts/inventory.py
python scripts/generate_indexes.py
python examples/run_experiments.py
python scripts/check_math.py
python scripts/generate_figures.py
python scripts/prepare_download.py
python scripts/check_content.py
pnpm run build
node scripts/check_site.mjs
~~~

PDF 调查脚本只负责提取、分章与指纹，不能代替作者阅读。重新调查后，必须完成逐页核对，才允许更新对应的审阅状态。

sources/baseline.json 保护章节、锚点、知识 ID 和已有公式。数学公式的合法更正也会触发检查，需要先解释原因，再显式运行：

~~~bash
python scripts/check_content.py --write-baseline
~~~

不要在失败后自动刷新基线。首次建立基线与后续有意更新，是需要审查的维护行为。

## 网站与发布

本地预览使用 pnpm run dev；构建输出为 docs/.vitepress/dist。GitHub Pages 工作流在受信任的仓库中构建并发布，SITE_BASE 根据仓库路径生成。

原 PDF 不随公开站点打包。持续集成可使用已审查的索引与指纹清单，构建时无法重新核查未上传 PDF 的哈希；本地完整检查必须持有原文件。不要在 CI 报告里伪称重新检查了缺失的原始文件。

release.json 记录构建可获取的 Git commit；当前目录没有 Git 仓库时为 null。上线后应访问这个文件，确认线上版本与预期提交一致。

本项目的正式公开托管使用 GitHub Pages。源码仓库为 wly63227/convex-optimization-notes；推送 main 后由 .github/workflows/deploy-pages.yml 运行检查、构建并发布。仓库 Settings → Pages 的来源设为 GitHub Actions，SITE_BASE 由仓库名自动生成。构建产物不提交，发布凭据由 GitHub Actions 的 pages 与 id-token 权限提供。
