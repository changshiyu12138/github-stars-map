# 🗂️ 我的 GitHub Star 地图

> 收录 **180** 个 Star 过的项目，按主题分类并逐个补上中文说明。  
> 数据来源：GitHub API（`changshiyu12138` 的公开 Star 列表）· 最后更新 2026-10-10  
> 🤖 由 GitHub Actions 每 6 小时自动刷新，新项目会出现在文末「🆕 待归类」。

这个仓库的用途只有一个：**过三个月再想起来某个项目是干嘛的时候，这里能查到。**

## 概览

- **总收藏**：180 个项目
- **时间跨度**：2019-05-03 → 2026-10-09
- **收藏高峰**：2026 年 74 个、2025 年 59 个（占总量 73%）
- **主力语言**：Python 46、TypeScript 27、JavaScript 14、C++ 10、HTML 8
- **分类数量**：15 个主题

### 收藏节奏

```
2019  ████ 8
2020  ████████ 15
2021  ██ 3
2022  ███ 6
2023  █████ 9
2024  ███ 6
2025  ████████████████████████████████ 59
2026  ████████████████████████████████████████ 74
```

### 主题目录

| | 主题 | 数量 | 一句话概括 |
|---|---|---:|---|
| 🤖 | [AI Agent 与智能体应用](#cat-ai-agent) | 32 | 真正在做事的东西 —— 工作流、Agent 循环、Skills 生态 |
| 🧠 | [大模型训练、推理与基础设施](#cat-ai-infra) | 10 | 模型本身的训练、推理与 API 接入层 |
| 📈 | [金融量化与投资研究](#cat-finance) | 19 | A股、加密货币与量化投研的全部工具箱 |
| 📖 | [电子书与阅读器](#cat-reading) | 10 | 电子书阅读器、书库管理与本地化 |
| 📰 | [RSS、资讯与舆情监控](#cat-rss-news) | 6 | 信息获取：订阅源、热点聚合与舆情监控 |
| 🕷️ | [爬虫与浏览器自动化](#cat-crawl-browser) | 4 | 给 Agent 喂数据的抓取与浏览器自动化 |
| 🛠️ | [实用工具与效率软件](#cat-tools) | 21 | 日常真正会打开的小工具 |
| 📱 | [Android / 移动端开发](#cat-mobile) | 12 | 安卓与移动端开发，含 Smartisan 情怀项目 |
| 🎬 | [影音媒体与家庭娱乐](#cat-media) | 12 | Jellyfin 家庭媒体、字幕与电视盒子 |
| ⚙️ | [硬件、系统与嵌入式](#cat-system) | 18 | 硬件、系统与嵌入式，含大量 Smartisan OS 遗产 |
| 🌐 | [前端与网页开发](#cat-frontend) | 2 | 网页与前端 |
| 📚 | [学习资料与教程](#cat-learning) | 22 | 教程、书籍与 Awesome Lists |
| 🎮 | [游戏与模拟器](#cat-games) | 2 | 游戏与模拟器 |
| 🔒 | [隐私、安全与逆向](#cat-security) | 4 | 隐私、安全与逆向工程 |
| 🌱 | [生活、健康与个人成长](#cat-life) | 6 | 健身、做饭、副业与人生指南 |

---

## 📚 项目清单

> 排序：各分类内按 Star 时间倒序，最新的在最前面。⭐ 为该项目当前的总 Star 数。

<a id="cat-ai-agent"></a>

### 🤖 AI Agent 与智能体应用 · 32

> 真正在做事的东西 —— 工作流、Agent 循环、Skills 生态

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`chengyi-ai/native-subtitle-quote-image`](https://github.com/chengyi-ai/native-subtitle-quote-image) | 保留视频内嵌字幕、精确取帧并生成 3:4 社交长图的 Agent Skill | Python | 2,580 | 2026-10-07 |
| [`mcncarl/yichen-skills`](https://github.com/mcncarl/yichen-skills) | 个人整理的 Skills 合集（仓库暂无官方简介） | Python | 4,362 | 2026-08-31 |
| [`esengine/DeepSeek-Reasonix`](https://github.com/esengine/DeepSeek-Reasonix) | Go 写的可靠编码 Agent，面向复杂软件工程任务 | Go | 35,749 | 2026-08-09 |
| [`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 给 Agent 用的 UI/UX 设计智能 Skill，跨平台产出专业级界面 | Python | 134,287 | 2026-06-21 |
| [`yan-labs/serenity-aleabitoreddit`](https://github.com/yan-labs/serenity-aleabitoreddit) | 可安装的推文归档 + AI 语义供应链 Skill，一条命令 npx 装到本地 | Python | 481 | 2026-05-31 |
| [`fathah/hermes-desktop`](https://github.com/fathah/hermes-desktop) | Hermes Agent 的桌面伴侣客户端 | TypeScript | 14,381 | 2026-05-25 |
| [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) | 一整套「AI 数字 Agency」角色库：前端专家、社区运营、创意注入、现实检验等 | Shell | 158,572 | 2026-05-16 |
| [`farion1231/cc-switch`](https://github.com/farion1231/cc-switch) | 跨平台桌面端 AI 助手，一键切换 Claude Code、Codex、OpenCode、OpenClaw 等 | Rust | 142,082 | 2026-05-03 |
| [`drona23/claude-token-efficient`](https://github.com/drona23/claude-token-efficient) | 单个 CLAUDE.md 配置，让 Claude 输出更简洁，显著降低 token 消耗 | Python | 6,080 | 2026-03-31 |
| [`linuxhsj/openclaw-zero-token`](https://github.com/linuxhsj/openclaw-zero-token) | 让 OpenClaw 复用主流模型而无需自备 API Token 的方案 | TypeScript | 5,199 | 2026-03-30 |
| [`6551Team/opennews-mcp`](https://github.com/6551Team/opennews-mcp) | 新闻聚合 + AI 评分 + 交易信号 + 实时更新的 MCP 服务 | Python | 2,426 | 2026-03-19 |
| [`Lawliet-ai/openclaw-skills-Lawliet`](https://github.com/Lawliet-ai/openclaw-skills-Lawliet) | 高质量 OpenClaw Skills 合集，专门收集「高主动性」工作流 | Python | 11 | 2026-03-17 |
| [`bytedance/deer-flow`](https://github.com/bytedance/deer-flow) | 字节开源长周期 SuperAgent 框架：研究、编码、创作，沙箱 + 记忆 + 工具 + 子 Agent | Python | 83,602 | 2026-03-04 |
| [`openclaw/clawhub`](https://github.com/openclaw/clawhub) | OpenClaw 生态的 Skill 与插件注册中心 | TypeScript | 9,499 | 2026-03-04 |
| [`puzhen-ryan/xhs-toolkit`](https://github.com/puzhen-ryan/xhs-toolkit) | 面向 Agent 的小红书发帖与运营工具，同时提供配套 Skills | JavaScript | 25 | 2026-02-26 |
| [`HKUDS/ClawWork`](https://github.com/HKUDS/ClawWork) | 把 OpenClaw 当 AI 同事用的实战项目（作者称 11 小时赚到 15K 美元） | Python | 8,551 | 2026-02-25 |
| [`ZekerTop/ai-cli-complete-notify`](https://github.com/ZekerTop/ai-cli-complete-notify) | Claude Code / Codex / Gemini CLI 任务完成提醒，支持飞书、钉钉、Telegram 等多通道推送 | JavaScript | 422 | 2026-02-04 |
| [`hellangleZ/Raffaello`](https://github.com/hellangleZ/Raffaello) | PRD 并行执行引擎，Ralph 的「更冷静更快」的孪生兄弟 | Shell | 68 | 2026-02-04 |
| [`snarktank/ralph`](https://github.com/snarktank/ralph) | 自治循环 Agent：反复读取 PRD 清单，直到所有条目被逐项完成 | TypeScript | 21,932 | 2026-01-28 |
| [`openclaw/openclaw`](https://github.com/openclaw/openclaw) | 主打「真干活」的个人 AI 助手，跨系统跨平台的自托管 Agent | TypeScript | 391,554 | 2026-01-26 |
| [`666ghj/MiroFish`](https://github.com/666ghj/MiroFish) | 简洁通用的群体智能引擎，用多 Agent 模拟推演做任何预测，含金融预测应用 | Python | 77,517 | 2025-12-25 |
| [`xiamuceer-j/MuMuAINovel`](https://github.com/xiamuceer-j/MuMuAINovel) | AI 智能小说创作助手，帮你把故事点子写成完整稿件 | Python | 3,148 | 2025-11-27 |
| [`Ido-Levi/Hephaestus`](https://github.com/Ido-Levi/Hephaestus) | 半结构化 Agent 框架，工作流随Agent 发现的任务自动生长，而非预先编排 | Python | 1,186 | 2025-10-31 |
| [`MoonshotAI/kimi-cli`](https://github.com/MoonshotAI/kimi-cli) | 月之暗面官方 Kimi 命令行客户端（已归档，请改用 kimi-code） | Python | 11,424 | 2025-10-27 |
| [`lobehub/lobehub`](https://github.com/lobehub/lobehub) | AI 团队的「调度台」：管理、定时、汇报你的多个 Agent | TypeScript | 83,091 | 2025-10-14 |
| [`Zie619/n8n-workflows`](https://github.com/Zie619/n8n-workflows) | n8n 全网工作流收集合集，含从官网与社区搜集的可导入 JSON | Python | 56,933 | 2025-10-12 |
| [`FlowiseAI/Flowise`](https://github.com/FlowiseAI/Flowise) | 拖拽式搭建 AI Agent 与对话机器人，可视化编排 LLM 流程 | TypeScript | 55,495 | 2025-10-12 |
| [`google-gemini/computer-use-preview`](https://github.com/google-gemini/computer-use-preview) | Google 官方 Computer Use 预览版，让模型像人一样操作电脑界面 | Python | 3,216 | 2025-10-12 |
| [`wassupjay/n8n-free-templates`](https://github.com/wassupjay/n8n-free-templates) | 200+ 开箱即用的 n8n 工作流模板，含向量库、Embedding、LLM 组合 | 未标注 | 6,223 | 2025-07-26 |
| [`firecrawl/fireplexity`](https://github.com/firecrawl/fireplexity) | 开源版 Perplexity，带实时引用与流式回答，数据由 Firecrawl 供给 | TypeScript | 1,972 | 2025-06-29 |
| [`minhalvp/android-mcp-server`](https://github.com/minhalvp/android-mcp-server) | 通过 adb 控制安卓设备的 MCP Server，让 Agent 直接操作手机 | Python | 809 | 2025-04-12 |
| [`n8n-io/n8n`](https://github.com/n8n-io/n8n) | 可视化搭建 AI 工作流的自托管平台，400+ 集成，可写自定义代码节点 | TypeScript | 206,853 | 2025-04-07 |

<a id="cat-ai-infra"></a>

### 🧠 大模型训练、推理与基础设施 · 10

> 模型本身的训练、推理与 API 接入层

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`jingyaogong/minimind`](https://github.com/jingyaogong/minimind) | 2 小时从零训练一个 6400 万参数 LLM 的极简教学项目 | Python | 63,471 | 2026-09-06 |
| [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | DeepSeek 官方 Agent Harness，核心设计是「一切皆插件」 | TypeScript | 246,536 | 2026-08-19 |
| [`QuantumNous/new-api`](https://github.com/QuantumNous/new-api) | 统一大模型网关：把各家 LLM 转成 OpenAI / Claude / Gemini 兼容接口 | Go | 49,574 | 2026-02-04 |
| [`songquanpeng/one-api`](https://github.com/songquanpeng/one-api) | 老牌 LLM API 管理分发系统，支持十几家国内主流模型统一适配 | JavaScript | 37,108 | 2026-02-04 |
| [`knownsec/aipyapp`](https://github.com/knownsec/aipyapp) | Python 与 AI 双向互操作的应用合集，涵盖「AI 用 Python」与「Python 驱动 AI」 | HTML | 4,026 | 2025-07-28 |
| [`datawhalechina/self-llm`](https://github.com/datawhalechina/self-llm) | 《开源大模型食用指南》：Linux 下微调与部署国内外 LLM / 多模态模型 | Jupyter Notebook | 32,420 | 2025-07-02 |
| [`Xtra-Computing/ThunderGP`](https://github.com/Xtra-Computing/ThunderGP) | 面向 FPGA 的 HLS 图计算框架，做超大规模图算法硬件加速 | C++ | 152 | 2024-03-25 |
| [`PaddlePaddle/PaddleGAN`](https://github.com/PaddlePaddle/PaddleGAN) | 百度飞桨 GAN 库，含老照片修复、Wav2Lip 换口型、超分、人脸编辑等大量应用 | Python | 8,044 | 2023-11-01 |
| [`XianrenYty/OldVideoRepair_PaddleGAN`](https://github.com/XianrenYty/OldVideoRepair_PaddleGAN) | 用插帧 DAIN + 上色 DeOldify + 超分 EDVR 三个模型修复老视频的实践 Notebook | Jupyter Notebook | 51 | 2023-11-01 |
| [`yahoo/open_nsfw`](https://github.com/yahoo/open_nsfw) | 基于 Caffe 深度神经网络的 NSFW 图像分类模型，Yahoo 开源 | Python | 6,014 | 2020-01-21 |

<a id="cat-finance"></a>

### 📈 金融量化与投资研究 · 19

> A股、加密货币与量化投研的全部工具箱

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`sngyai/Sequoia-X`](https://github.com/sngyai/Sequoia-X) | A 股自动选股系统，多种技术形态扫描，收盘后自动跑并推送飞书 | Python | 8,007 | 2026-09-01 |
| [`jcdreamjc/wudao-ashare`](https://github.com/jcdreamjc/wudao-ashare) | 悟道 A 股数据套件：26 个实时 API，专为 AI Agent 设计 | 未标注 | 6 | 2026-08-27 |
| [`Benboerba620/Benboerba620`](https://github.com/Benboerba620/Benboerba620) | 零代码 × AI 投研 × 个人知识库的一体化投资研究工具包 | 未标注 | 37 | 2026-08-25 |
| [`ccxt/ccxt`](https://github.com/ccxt/ccxt) | 统一加密货币交易 API，100+ 交易所与预测市场，多语言支持 | Python | 44,302 | 2026-08-15 |
| [`ranaroussi/yfinance`](https://github.com/ranaroussi/yfinance) | 从雅虎财经抓取行情数据的事实标准库 | Python | 25,478 | 2026-08-15 |
| [`Micro-sheep/efinance`](https://github.com/Micro-sheep/efinance) | 快速获取基金、股票、债券、期货数据的 Python 库，附回测与量化工具 | Python | 4,080 | 2026-08-15 |
| [`simonlin1212/a-stock-data`](https://github.com/simonlin1212/a-stock-data) | A 股全栈数据工具包：行情、研报、信号、资金面、财务，15 层 87 端点免 Key | Python | 10,741 | 2026-07-26 |
| [`pythonstock/stock`](https://github.com/pythonstock/stock) | Python 开发的股票系统，完整业务流实践项目 | Python | 7,878 | 2026-07-19 |
| [`Fincept-Corporation/FinceptTerminal`](https://github.com/Fincept-Corporation/FinceptTerminal) | 对标彭博终端的金融终端，集成行情分析、投资研究与经济数据 | C++ | 32,344 | 2026-07-05 |
| [`xbtlin/ai-berkshire`](https://github.com/xbtlin/ai-berkshire) | AI 时代的伯克希尔：巴菲特、芒格、段永平、李录四大师方法论 + 多 Agent 并行研究 | HTML | 16,675 | 2026-07-05 |
| [`wbh604/UZI-Skill`](https://github.com/wbh604/UZI-Skill) | 游资「UZI」Skills：22 维数据 × 180 条量化规则 × 17 种机构分析法，A/H/美股通吃 | Python | 7,135 | 2026-06-12 |
| [`virattt/ai-hedge-fund`](https://github.com/virattt/ai-hedge-fund) | 多 Agent 模拟一支 AI 对冲基金：基本面、技术面、风险、看多看空各自成角色 | Python | 63,918 | 2026-05-28 |
| [`24mlight/A_Share_investment_Agent`](https://github.com/24mlight/A_Share_investment_Agent) | A 股投资 Agent 项目（仓库暂无官方简介） | Python | 2,484 | 2026-05-28 |
| [`wensongz/stock-portfolio-manager`](https://github.com/wensongz/stock-portfolio-manager) | 个人自用的股票投资组合管理器，Rust 编写 | Rust | 73 | 2026-03-29 |
| [`waditu/tushare`](https://github.com/waditu/tushare) | A股历史行情与财务数据爬取工具，国内量化数据基建常用 | Python | 15,444 | 2026-03-15 |
| [`waditu/czsc`](https://github.com/waditu/czsc) | 缠中说禅（缠论）技术分析工具，Rust 编写，覆盖股票与期货 | Rust | 6,390 | 2026-03-15 |
| [`ZhuLinsen/daily_stock_analysis`](https://github.com/ZhuLinsen/daily_stock_analysis) | LLM 驱动的多市场股票分析：多源行情 + 实时新闻 + 决策看板 + 自动推送 | Python | 66,118 | 2026-01-23 |
| [`mementum/backtrader`](https://github.com/mementum/backtrader) | Python 回测库的事实标准，交易策略的历史表现验证用它 | Python | 23,446 | 2025-09-02 |
| [`jrothschild33/learn_backtrader`](https://github.com/jrothschild33/learn_backtrader) | Backtrader 中文教程笔记，系统讲清策略构建、数据结构、回测与可视化 | Python | 2,275 | 2025-09-02 |

<a id="cat-reading"></a>

### 📖 电子书与阅读器 · 10

> 电子书阅读器、书库管理与本地化

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`santinic/audiblez`](https://github.com/santinic/audiblez) | 用本地 TTS（Kokoro）把 EPUB 电子书一键生成有声书 | Python | 8,715 | 2026-08-07 |
| [`xincmm/sageread`](https://github.com/xincmm/sageread) | AI 辅助阅读器，三栏布局让笔记、阅读、AI 对话同屏，适合深度阅读 | TypeScript | 779 | 2025-11-28 |
| [`Kareadita/Kavita`](https://github.com/Kareadita/Kavita) | 高性能跨平台阅读服务器，一站式管理小说与漫画书库（含 CBZ） | C# | 11,823 | 2025-07-22 |
| [`baturyilmaz/wordpecker-app`](https://github.com/baturyilmaz/wordpecker-app) | 把 Duolingo 式课程与自己的生词表结合，支持从书籍里直接摘词加入 | TypeScript | 2,275 | 2025-07-20 |
| [`Dujltqzv/Some-Many-Books`](https://github.com/Dujltqzv/Some-Many-Books) | 个人收藏书单仓库（作者以大量空白字符排版，纯清单项目） | 未标注 | 24,519 | 2025-07-05 |
| [`koodo-reader/koodo-reader`](https://github.com/koodo-reader/koodo-reader) | 现代电子书管理与阅读器，支持 Win/Mac/Linux/Android/iOS/Web 多端同步备份 | JavaScript | 28,460 | 2025-05-16 |
| [`MeowSalty/LocalizeEpub_For_Windows`](https://github.com/MeowSalty/LocalizeEpub_For_Windows) | C# 重写的 EPUB 本地化客户端，借繁化姬等第三方服务做繁简转换与翻译 | C# | 28 | 2025-05-16 |
| [`oomol-lab/pdf-craft`](https://github.com/oomol-lab/pdf-craft) | PDF 转其他格式的工具包，专注扫描书籍的结构化处理 | Python | 6,349 | 2025-04-19 |
| [`readest/readest`](https://github.com/readest/readest) | 跨平台现代电子书阅读器，接Calibre 库，支持插件与书库同步 | TypeScript | 24,999 | 2025-03-19 |
| [`Anxcye/anx-reader`](https://github.com/Anxcye/anx-reader) | AI 能力突出的电子书阅读器，支持多种格式，主打更聪明的沉浸阅读 | Dart | 8,932 | 2024-08-17 |

<a id="cat-rss-news"></a>

### 📰 RSS、资讯与舆情监控 · 6

> 信息获取：订阅源、热点聚合与舆情监控

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`newsnext/newsnow`](https://github.com/newsnext/newsnow) | 极简风格的实时热点聚合阅读器，一屏看完今日要闻 | TypeScript | 21,991 | 2026-05-18 |
| [`zarazhangrui/follow-builders`](https://github.com/zarazhangrui/follow-builders) | AI 创作者速报：监控 X 与 YouTube 播客上的顶级 AI builder 并二次创作摘要 | JavaScript | 6,856 | 2026-03-22 |
| [`cooderl/wewe-rss`](https://github.com/cooderl/wewe-rss) | 更优雅的公众号订阅方案：私有化部署，基于微信读书生成公众号 RSS | TypeScript | 9,654 | 2025-10-03 |
| [`DIYgod/RSSHub`](https://github.com/DIYgod/RSSHub) | 万物皆可 RSS，把微博、B站、豆瓣、Instagram 等全网内容变成订阅源 | TypeScript | 46,477 | 2025-09-29 |
| [`sansan0/TrendRadar`](https://github.com/sansan0/TrendRadar) | AI 舆情与热点监控，多平台聚合 + RSS 订阅 + 关键词智能推送 | Python | 62,770 | 2025-09-01 |
| [`RSSNext/Folo`](https://github.com/RSSNext/Folo) | AI 驱动的 RSS 阅读器，界面干净，支持 RSSHub 生态 | TypeScript | 39,077 | 2024-11-23 |

<a id="cat-crawl-browser"></a>

### 🕷️ 爬虫与浏览器自动化 · 4

> 给 Agent 喂数据的抓取与浏览器自动化

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`h4ckf0r0day/obscura`](https://github.com/h4ckf0r0day/obscura) | 面向 AI Agent 的无头浏览器，带反检测能力，兼顾网页抓取 | Rust | 28,734 | 2026-05-16 |
| [`unclecode/crawl4ai`](https://github.com/unclecode/crawl4ai) | 开源爬虫，把任意网站转成干净的 LLM 友好 Markdown | Python | 85,112 | 2025-12-03 |
| [`apify/crawlee`](https://github.com/apify/crawlee) | Apify 出品的 Node.js 爬虫与浏览器自动化库，专为 AI/LLM 数据管道设计 | TypeScript | 26,094 | 2025-11-30 |
| [`browserbase/stagehand`](https://github.com/browserbase/stagehand) | 浏览器数据提取与交互 SDK，官方推荐与 Claude Code、Codex 搭配使用 | TypeScript | 25,599 | 2025-10-12 |

<a id="cat-tools"></a>

### 🛠️ 实用工具与效率软件 · 21

> 日常真正会打开的小工具

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`iawia002/lux`](https://github.com/iawia002/lux) | Go 编写的高效视频下载库与命令行工具 | Go | 31,756 | 2026-10-08 |
| [`tobi/disktree`](https://github.com/tobi/disktree) | 用树图空间找方式清理磁盘占用，Rust + GPUI 实现 | Rust | 2,533 | 2026-10-03 |
| [`sumimakito/Mac-Duo`](https://github.com/sumimakito/Mac-Duo) | 在 MacBook 上复刻 iPhone「灵动岛」Duo 效果的小工具 | Swift | 1,184 | 2026-09-11 |
| [`galaxy-s10/billd-desk`](https://github.com/galaxy-s10/billd-desk) | 基于 Vue3 + WebRTC 的远程桌面与游戏串流，自建可控 | TypeScript | 8,392 | 2026-09-07 |
| [`reactive-resume/reactive-resume`](https://github.com/reactive-resume/reactive-resume) | 隐私优先的开源简历生成器，可定制、可移植、免费 | TypeScript | 44,056 | 2026-08-19 |
| [`AnInsomniacy/rayburst`](https://github.com/AnInsomniacy/rayburst) | 重新定义开源下载体验的下载管理器 | TypeScript | 10,875 | 2026-04-16 |
| [`Devolutions/UniGetUI`](https://github.com/Devolutions/UniGetUI) | 包管理器的图形前端，统一管理 winget、choco、scoop 等各家包管理器 | C# | 26,455 | 2026-02-10 |
| [`eythaann/Seelen-UI`](https://github.com/eythaann/Seelen-UI) | 高度可定制的 Windows 10/11 桌面环境：启动器、Dock、Finder 一体化 | Rust | 17,973 | 2026-02-03 |
| [`x1ao4/douban-api`](https://github.com/x1ao4/douban-api) | 基于豆瓣移动端 API 的影视榜单接口服务 | JavaScript | 28 | 2026-01-13 |
| [`microsoft/markitdown`](https://github.com/microsoft/markitdown) | 微软官方工具：把各类文件与 Office 文档统一转成 Markdown | Python | 189,257 | 2025-11-24 |
| [`ImranR98/Obtainium`](https://github.com/ImranR98/Obtainium) | 直接从项目源站拉取 APK 更新，绕开应用商店版本滞后 | Dart | 20,309 | 2025-09-27 |
| [`zhongyang219/TrafficMonitor`](https://github.com/zhongyang219/TrafficMonitor) | Windows 桌面悬浮窗，显示网速、CPU、内存，支持任务栏显示与换肤 | C++ | 46,484 | 2025-09-17 |
| [`Xinrea/JPet`](https://github.com/Xinrea/JPet) | C++ + WebView2 的 Live2D 桌面宠物 | C++ | 105 | 2025-09-11 |
| [`chen08209/FlClash`](https://github.com/chen08209/FlClash) | 基于 ClashMeta 的多平台代理客户端，Flutter 编写，简洁无广告 | Dart | 55,035 | 2025-09-07 |
| [`Cp0204/quark-auto-save`](https://github.com/Cp0204/quark-auto-save) | 夸克网盘自动化：签到、自动转存、命名整理、推送提醒、刷新媒体库 | Python | 3,063 | 2025-08-11 |
| [`Usagi-org/ai-goofish-monitor`](https://github.com/Usagi-org/ai-goofish-monitor) | 基于 Playwright + AI 的闲鱼多任务实时监控与筛选系统，带后台管理 UI | Python | 14,734 | 2025-07-23 |
| [`xiaobaigroup/ClashBox`](https://github.com/xiaobaigroup/ClashBox) | HarmonyOS NEXT 上的代理客户端，ArkTS + ArkUI 实现 | 未标注 | 4,504 | 2025-07-05 |
| [`blinkospace/blinko`](https://github.com/blinkospace/blinko) | 开源自托管的个人 AI 笔记，强调隐私，数据留在本地 | TypeScript | 11,072 | 2025-07-04 |
| [`wanglin2/mind-map`](https://github.com/wanglin2/mind-map) | SimpleMindMap 思维导图，交互简洁、功能扎实的开源导图工具 | JavaScript | 12,804 | 2025-03-23 |
| [`easychen/LazyBoardExt`](https://github.com/easychen/LazyBoardExt) | Chrome 扩展机器人：定时采集数据并推送到指定接口 | JavaScript | 54 | 2022-01-28 |
| [`xinyueyongliang/FileRcovery`](https://github.com/xinyueyongliang/FileRcovery) | 实现了三种文件系统的数据恢复工具，偏底层实践 | 未标注 | 19 | 2020-11-30 |

<a id="cat-mobile"></a>

### 📱 Android / 移动端开发 · 12

> 安卓与移动端开发，含 Smartisan 情怀项目

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`SangLuoCN/OneStep4`](https://github.com/SangLuoCN/OneStep4) | 小项目，仓库信息仅标注 Designed By SangLuo | Java | 382 | 2026-07-28 |
| [`RANH-F/Smartisan-original-launcher`](https://github.com/RANH-F/Smartisan-original-launcher) | 让原版 Smartisan Launcher 在当代安卓上重新跑起来，还原简洁克制的美学 | Smali | 263 | 2026-07-16 |
| [`CashewTeam/BigBang_NovaText`](https://github.com/CashewTeam/BigBang_NovaText) | 老罗 Smartisan BigBang 输入法的社区重制版 | Kotlin | 220 | 2026-07-07 |
| [`elyesmansour/compose-floating-tab-bar`](https://github.com/elyesmansour/compose-floating-tab-bar) | Jetpack Compose 悬浮标签栏，仿 iOS 26 Liquid Glass 效果 | Kotlin | 160 | 2026-01-17 |
| [`DrKLO/Telegram`](https://github.com/DrKLO/Telegram) | Telegram 安卓客户端官方源码 | Java | 30,041 | 2026-01-12 |
| [`ChaoMixian/vFlow`](https://github.com/ChaoMixian/vFlow) | Android 图形化自动化工具，把动作模块拼成工作流完成重复点击操作 | Kotlin | 1,282 | 2026-01-10 |
| [`gkd-kit/gkd`](https://github.com/gkd-kit/gkd) | 基于无障碍能力的 Android 自动点击应用，支持高级选择器与订阅规则 | Kotlin | 42,646 | 2025-09-07 |
| [`barry-ran/QtScrcpy`](https://github.com/barry-ran/QtScrcpy) | 基于 Qt 的 Android 实时投屏与控制软件，跨平台 | C++ | 32,328 | 2021-03-04 |
| [`Soulghost/InfiniteSpringBoard`](https://github.com/Soulghost/InfiniteSpringBoard) | 锤子科技「无限屏」的 iOS 实现复刻 | Objective-C++ | 77 | 2020-11-28 |
| [`the1812/Bilibili-Evolved`](https://github.com/the1812/Bilibili-Evolved) | 功能强大的哔哩哔哩油猴增强脚本（按移动端增强归类） | TypeScript | 30,726 | 2020-08-04 |
| [`CarGuo/GSYVideoPlayer`](https://github.com/CarGuo/GSYVideoPlayer) | Android 通用视频播放器框架，集成 IJKPlayer、ExoPlayer，支持 16K 分页与弹幕 | Java | 21,509 | 2019-06-07 |
| [`CarGuo/gsy_github_app_flutter`](https://github.com/CarGuo/gsy_github_app_flutter) | Flutter 版 GitHub App，功能完整，适合作为 Flutter 学习工程 | Dart | 15,499 | 2019-06-07 |

<a id="cat-media"></a>

### 🎬 影音媒体与家庭娱乐 · 12

> Jellyfin 家庭媒体、字幕与电视盒子

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`bggRGjQaUbCoE/PiliPlus`](https://github.com/bggRGjQaUbCoE/PiliPlus) | Flutter 写的第三方 B 站客户端，支持 iOS / 桌面多端 | Dart | 19,266 | 2026-02-03 |
| [`youhunwl/TVAPP`](https://github.com/youhunwl/TVAPP) | 全网安卓电视盒子应用与影视仓接口配置源合集，分类整理并支持自动更新 | JavaScript | 24,703 | 2026-01-29 |
| [`LibreSpark/LibreTV`](https://github.com/LibreSpark/LibreTV) | 一分钟搭建的影视站，支持 Docker 部署 | TypeScript | 14,089 | 2025-07-04 |
| [`Richasy/Bili.Copilot`](https://github.com/Richasy/Bili.Copilot) | B 站第三方 Windows 桌面客户端，WinUI 3 + Windows App SDK 原生实现 | GLSL | 5,228 | 2024-11-26 |
| [`lizongying/my-tv`](https://github.com/lizongying/my-tv) | 开源电视直播软件，安装即用 | C | 31,963 | 2024-02-16 |
| [`Eanya-Tonic/CCTV_Viewer`](https://github.com/Eanya-Tonic/CCTV_Viewer) | 简易电视浏览器，方便在机顶盒上收看网页视频 | Java | 2,960 | 2024-02-16 |
| [`awesome-jellyfin/awesome-jellyfin`](https://github.com/awesome-jellyfin/awesome-jellyfin) | Jellyfin 插件、主题与教程的精选合集 | Shell | 9,538 | 2023-10-27 |
| [`metatube-community/jellyfin-plugin-metatube`](https://github.com/metatube-community/jellyfin-plugin-metatube) | MetaTube 的 Jellyfin/Emby 插件，含自动翻译与人脸识别 | C# | 4,520 | 2023-10-27 |
| [`ChineseSubFinder/ChineseSubFinder`](https://github.com/ChineseSubFinder/ChineseSubFinder) | 自动中文字幕下载，支持 Emby / Jellyfin / Plex / Sonarr / Radarr 等媒体库 | Go | 3,929 | 2023-10-27 |
| [`CTalvio/Ultrachromic`](https://github.com/CTalvio/Ultrachromic) | Jellyfin 主题插件：色相动态取色，明暗主题随封面变化 | CSS | 999 | 2023-10-27 |
| [`DirtyRacer1337/Jellyfin.Plugin.PhoenixAdult`](https://github.com/DirtyRacer1337/Jellyfin.Plugin.PhoenixAdult) | Jellyfin/Emby 元数据插件，抓取多个成人站点的信息 | C# | 445 | 2023-10-27 |
| [`jellyfin/jellyfin-plugin-template`](https://github.com/jellyfin/jellyfin-plugin-template) | Jellyfin 插件开发官方模板 | HTML | 441 | 2023-10-27 |

<a id="cat-system"></a>

### ⚙️ 硬件、系统与嵌入式 · 18

> 硬件、系统与嵌入式，含大量 Smartisan OS 遗产

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`mx3353672833-debug/moto-gps-waveshare`](https://github.com/mx3353672833-debug/moto-gps-waveshare) | 装在车把上的圆屏导航终端：ESP32-S3 1.75C AMOLED + iPhone App，手机算路线、圆屏显示路口与速度 | C++ | 321 | 2026-10-09 |
| [`KingKongRobotics/jumper`](https://github.com/KingKongRobotics/jumper) | 开源螃蟹机器人硬件项目 | Python | 2,239 | 2026-10-07 |
| [`CashewTeam/awesome-smartisanOS`](https://github.com/CashewTeam/awesome-smartisanOS) | SmartisanOS 相关优质项目、工具、资源与文章汇总 | 未标注 | 40 | 2026-07-16 |
| [`CentyLab/PocketPD`](https://github.com/CentyLab/PocketPD) | PocketPD 开源固件项目 | C++ | 534 | 2025-11-24 |
| [`medisoft/pcb-coil-generator`](https://github.com/medisoft/pcb-coil-generator) | EasyEDA Pro 的 PCB 线圈生成器 | HTML | 4 | 2025-07-29 |
| [`thunder439/QNASMINI`](https://github.com/thunder439/QNASMINI) | 6 盘位 2.5 寸 NAS 硬件项目 | 未标注 | 1,207 | 2025-07-23 |
| [`joanbono/awesome-kicad`](https://github.com/joanbono/awesome-kicad) | KiCad 插件与资源精选合集 | Python | 628 | 2025-06-13 |
| [`dsa-t/jlc-kicad-lib-loader`](https://github.com/dsa-t/jlc-kicad-lib-loader) | 在 KiCad 里批量浏览下载立创商城 / LCSC 元件库 | Python | 112 | 2025-06-13 |
| [`Robotips/uConfig`](https://github.com/Robotips/uConfig) | 从 PDF 数据手册提取引脚定义并生成 KiCad 符号与库文件 | C++ | 587 | 2025-03-19 |
| [`Forairaaaaa/Monica`](https://github.com/Forairaaaaa/Monica) | DIY AMOLED 屏智能手表，硬件加固件全自制 | C | 976 | 2023-06-04 |
| [`LeiWang1999/FPGA`](https://github.com/LeiWang1999/FPGA) | FPGA 入门与优质项目文章合集，含 Vivado / Xilinx 相关资料 | 未标注 | 5,778 | 2022-05-19 |
| [`FASTSHIFT/X-TRACK`](https://github.com/FASTSHIFT/X-TRACK) | 支持离线地图与轨迹记录的 GPS 自行车码表，C + LVGL | C | 6,300 | 2021-07-23 |
| [`FuchsiaOS/FuchsiaOS-docs-zh_CN`](https://github.com/FuchsiaOS/FuchsiaOS-docs-zh_CN) | Fuchsia OS 官方文档简体中文版 | Rust | 926 | 2020-12-09 |
| [`FuchsiaOS/Fuchsia-OS-tutorial`](https://github.com/FuchsiaOS/Fuchsia-OS-tutorial) | Fuchsia OS 学习资料与教程汇总 | 未标注 | 350 | 2020-12-09 |
| [`SmartisanTech/android`](https://github.com/SmartisanTech/android) | Smartisan OS 完整源码与构建清单 | 未标注 | 2,718 | 2020-11-28 |
| [`Sunbelife/get_smartisan_icon_pack`](https://github.com/Sunbelife/get_smartisan_icon_pack) | 从 Smartisan OS 提取 1400+ 图标的脚本 | Python | 38 | 2020-11-28 |
| [`LiteOS/LiteOS`](https://github.com/LiteOS/LiteOS) | 华为 LiteOS 轻量级物联网操作系统源码与开发手册 | C | 4,905 | 2020-11-27 |
| [`Sunbelife/Snowboard-IconPack-for-Smartisan-OS`](https://github.com/Sunbelife/Snowboard-IconPack-for-Smartisan-OS) | Smartisan OS 的雪地主题图标包 | Python | 96 | 2020-08-04 |

<a id="cat-frontend"></a>

### 🌐 前端与网页开发 · 2

> 网页与前端

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`joshajohnson/Hub16`](https://github.com/joshajohnson/Hub16) | 自制 16 键宏键盘，带两个旋钮编码器与四口 USB Hub，主打灯光效果 | HTML | 388 | 2022-01-06 |
| [`kkuchta/css-only-chat`](https://github.com/kkuchta/css-only-chat) | 前端零 JavaScript 的异步聊天界面，纯 CSS 实现的怪物级实验 | Ruby | 6,582 | 2019-05-10 |

<a id="cat-learning"></a>

### 📚 学习资料与教程 · 22

> 教程、书籍与 Awesome Lists

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`bobeff/open-source-games`](https://github.com/bobeff/open-source-games) | 开源游戏清单索引 | Python | 15,774 | 2026-10-07 |
| [`luongnv89/claude-howto`](https://github.com/luongnv89/claude-howto) | 图解式 Claude Code 指南，从基础概念到高级 Agent，附可直接复制的模板 | Python | 41,781 | 2026-03-31 |
| [`hesamsheikh/awesome-openclaw-usecases`](https://github.com/hesamsheikh/awesome-openclaw-usecases) | OpenClaw 社区用例合集，看别人怎么用 Agent 省事 | 未标注 | 31,668 | 2026-03-01 |
| [`leereilly/games`](https://github.com/leereilly/games) | GitHub 上架游戏的归档清单，覆盖各平台与引擎 | 未标注 | 24,967 | 2026-02-03 |
| [`ZuodaoTech/everyone-can-use-english`](https://github.com/ZuodaoTech/everyone-can-use-english) | 《人人都能用英语》开源教材与配套资源 | TypeScript | 38,665 | 2025-09-13 |
| [`beihaili/Get-Started-with-Web3`](https://github.com/beihaili/Get-Started-with-Web3) | 双语 AI-native Web3 课程：钱包、比特币、以太坊、DeFi、DAO、llms.txt 与 MCP | JavaScript | 614 | 2025-09-02 |
| [`ProbiusOfficial/Hello-CTF`](https://github.com/ProbiusOfficial/Hello-CTF) | 面向零基础新手的 CTF 入门开源教程，同时补信息差 | HTML | 4,242 | 2025-08-13 |
| [`sindresorhus/awesome`](https://github.com/sindresorhus/awesome) | 覆盖各行各业的 Awesome Lists 总目录 | 未标注 | 516,886 | 2025-07-02 |
| [`xiaolai/bitcoin-whitepaper-chinese-translation`](https://github.com/xiaolai/bitcoin-whitepaper-chinese-translation) | 比特币白皮书中文全译（仓库暂无官方简介） | HTML | 1,221 | 2025-05-28 |
| [`justjavac/free-programming-books-zh_CN`](https://github.com/justjavac/free-programming-books-zh_CN) | 免费的中文计算机编程书籍汇总 | 未标注 | 119,102 | 2022-05-13 |
| [`ruanyf/free-books`](https://github.com/ruanyf/free-books) | 互联网上的免费书籍索引 | 未标注 | 16,028 | 2022-05-13 |
| [`fireinthehole2019/awesome-reverse-engineering`](https://github.com/fireinthehole2019/awesome-reverse-engineering) | 全平台逆向工程资源：3500+ 开源工具与2300 篇文章 | 未标注 | 1 | 2022-02-07 |
| [`xiaobaiTech/golangFamily`](https://github.com/xiaobaiTech/golangFamily) | 超全 Golang 面试题、学习指南与知识图谱 | Go | 6,981 | 2021-09-19 |
| [`SwiftGGTeam/the-swift-programming-language-in-chinese`](https://github.com/SwiftGGTeam/the-swift-programming-language-in-chinese) | Apple 官方《Swift 编程语言》中文版 | Markdown | 21,171 | 2020-11-28 |
| [`Snailclimb/JavaGuide`](https://github.com/Snailclimb/JavaGuide) | Java 面试与后端通用面试指南，已扩展到 AI 应用开发 | JavaScript | 158,915 | 2020-11-27 |
| [`AobingJava/JavaFamily`](https://github.com/AobingJava/JavaFamily) | Java 面试与学习指南，覆盖 Java 程序员需掌握的核心知识 | 未标注 | 36,988 | 2020-11-27 |
| [`DuGuQiuBai/Java`](https://github.com/DuGuQiuBai/Java) | 「27 天成为 Java 大神」系列教程 | Java | 14,589 | 2020-11-27 |
| [`HelloWorld521/Java`](https://github.com/HelloWorld521/Java) | Java 项目实战练习集 | Java | 3,824 | 2020-11-27 |
| [`CyC2018/CS-Notes`](https://github.com/CyC2018/CS-Notes) | 技术面试必备：算法、操作系统、计算机网络、系统设计笔记 | 未标注 | 186,191 | 2019-05-10 |
| [`nndl/nndl`](https://github.com/nndl/nndl) | 邱锡鹏《神经网络与深度学习》第二版电子书与配套学习资源 | 未标注 | 19,311 | 2019-05-08 |
| [`jaywcjlove/linux-command`](https://github.com/jaywcjlove/linux-command) | Linux 命令大全搜索工具：手册、详解、学习资料全收录 | Markdown | 37,091 | 2019-05-04 |
| [`jackfrued/Python-100-Days`](https://github.com/jackfrued/Python-100-Days) | Python 从新手到大师的 100 天学习路线，含 Jupyter Notebook | Jupyter Notebook | 186,976 | 2019-05-03 |

<a id="cat-games"></a>

### 🎮 游戏与模拟器 · 2

> 游戏与模拟器

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`KsanaDock/Microverse`](https://github.com/KsanaDock/Microverse) | 基于 Godot 4 的 AI 社会沙盒：虚拟世界里的角色各有性格与关系，模拟群体智能 | GDScript | 2,495 | 2025-10-12 |
| [`shadps4-emu/shadPS4`](https://github.com/shadps4-emu/shadPS4) | C++ 编写的 PlayStation 4 模拟器，支持 Win/Linux/macOS/FreeBSD | C++ | 33,321 | 2025-04-16 |

<a id="cat-security"></a>

### 🔒 隐私、安全与逆向 · 4

> 隐私、安全与逆向工程

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`assafdori/bypass-mdm`](https://github.com/assafdori/bypass-mdm) | 绕过 macOS 的 MDM 设备管理限制（至 Golden Gate 版本） | Shell | 2,431 | 2026-09-09 |
| [`DimensionDev/Flare`](https://github.com/DimensionDev/Flare) | 一个客户端聚合浏览 Mastodon、Bluesky、X、Misskey、Nostr、Pixiv、RSS | Kotlin | 1,586 | 2026-07-25 |
| [`LadybirdBrowser/ladybird`](https://github.com/LadybirdBrowser/ladybird) | 真正独立的浏览器，从零自研引擎，不依赖 Chromium | C++ | 66,465 | 2026-03-04 |
| [`minbrowser/min`](https://github.com/minbrowser/min) | 快速、极简、注重隐私的浏览器 | JavaScript | 9,202 | 2025-06-25 |

<a id="cat-life"></a>

### 🌱 生活、健康与个人成长 · 6

> 健身、做饭、副业与人生指南

| 项目 | 说明 | 语言 | ⭐ | 收藏于 |
|---|---|---|---:|---|
| [`eternity4719/HowToLiveBetter`](https://github.com/eternity4719/HowToLiveBetter) | 高性价比人生指南：长寿防病、急救、理财、法律红线，每条标注成本与证据等级 | HTML | 57,604 | 2026-09-16 |
| [`Gar-b-age/CookLikeHOC`](https://github.com/Gar-b-age/CookLikeHOC) | 像老乡鸡那样做饭：按《老乡鸡菜品溯源报告》整理的菜谱 | JavaScript | 24,764 | 2026-02-03 |
| [`easychen/opc-methodology`](https://github.com/easychen/opc-methodology) | 《一人企业方法论》第二版，非技术人群做副业的通用框架 | PHP | 16,890 | 2025-11-12 |
| [`easychen/lean-side-bussiness`](https://github.com/easychen/lean-side-bussiness) | 《精益副业》：程序员如何优雅地做副业 | 未标注 | 12,152 | 2025-11-12 |
| [`Snouzy/workout-cool`](https://github.com/Snouzy/workout-cool) | 开源健身教练平台：制定训练计划、追踪进度、内置动作数据库 | TypeScript | 8,581 | 2025-06-23 |
| [`evil-huawei/evil-huawei`](https://github.com/evil-huawei/evil-huawei) | 记录华为历次争议事件的档案库 | JavaScript | 9,296 | 2019-12-03 |

---

## ⭐ 万星以上的项目

这些是Star 列表里体量最大的 10 个，Star 数远高于其他项目。

| 项目 | 说明 | ⭐ |
|---|---|---:|
| [`sindresorhus/awesome`](https://github.com/sindresorhus/awesome) | 覆盖各行各业的 Awesome Lists 总目录 | 516,886 |
| [`openclaw/openclaw`](https://github.com/openclaw/openclaw) | 主打「真干活」的个人 AI 助手，跨系统跨平台的自托管 Agent | 391,554 |
| [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | DeepSeek 官方 Agent Harness，核心设计是「一切皆插件」 | 246,536 |
| [`n8n-io/n8n`](https://github.com/n8n-io/n8n) | 可视化搭建 AI 工作流的自托管平台，400+ 集成，可写自定义代码节点 | 206,853 |
| [`microsoft/markitdown`](https://github.com/microsoft/markitdown) | 微软官方工具：把各类文件与 Office 文档统一转成 Markdown | 189,257 |
| [`jackfrued/Python-100-Days`](https://github.com/jackfrued/Python-100-Days) | Python 从新手到大师的 100 天学习路线，含 Jupyter Notebook | 186,976 |
| [`CyC2018/CS-Notes`](https://github.com/CyC2018/CS-Notes) | 技术面试必备：算法、操作系统、计算机网络、系统设计笔记 | 186,191 |
| [`Snailclimb/JavaGuide`](https://github.com/Snailclimb/JavaGuide) | Java 面试与后端通用面试指南，已扩展到 AI 应用开发 | 158,915 |
| [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) | 一整套「AI 数字 Agency」角色库：前端专家、社区运营、创意注入、现实检验等 | 158,572 |
| [`farion1231/cc-switch`](https://github.com/farion1231/cc-switch) | 跨平台桌面端 AI 助手，一键切换 Claude Code、Codex、OpenCode、OpenClaw 等 | 142,082 |

---

## 🏷️ 标签索引

按 GitHub 官方 Topic 检索（点击即搜索）：

[`python`](https://github.com/topics/python) · [`ai`](https://github.com/topics/ai) · [`android`](https://github.com/topics/android) · [`typescript`](https://github.com/topics/typescript) · [`llm`](https://github.com/topics/llm) · [`mcp`](https://github.com/topics/mcp) · [`openai`](https://github.com/topics/openai) · [`pdf`](https://github.com/topics/pdf) · [`react`](https://github.com/topics/react) · [`jellyfin`](https://github.com/topics/jellyfin) · [`automation`](https://github.com/topics/automation) · [`ai-agents`](https://github.com/topics/ai-agents) · [`claude-code`](https://github.com/topics/claude-code) · [`flutter`](https://github.com/topics/flutter) · [`awesome-list`](https://github.com/topics/awesome-list) · [`epub`](https://github.com/topics/epub) · [`windows`](https://github.com/topics/windows) · [`markdown`](https://github.com/topics/markdown) · [`open-source`](https://github.com/topics/open-source) · [`playwright`](https://github.com/topics/playwright) · [`trading`](https://github.com/topics/trading) · [`claude`](https://github.com/topics/claude) · [`ai-agent`](https://github.com/topics/ai-agent) · [`cpp`](https://github.com/topics/cpp) · [`java`](https://github.com/topics/java) · [`ios`](https://github.com/topics/ios) · [`bilibili`](https://github.com/topics/bilibili) · [`agent`](https://github.com/topics/agent) · [`deepseek`](https://github.com/topics/deepseek) · [`javascript`](https://github.com/topics/javascript) · [`rss`](https://github.com/topics/rss) · [`nextjs`](https://github.com/topics/nextjs) · [`self-hosted`](https://github.com/topics/self-hosted) · [`gemini`](https://github.com/topics/gemini) · [`quant`](https://github.com/topics/quant) · [`quantitative-finance`](https://github.com/topics/quantitative-finance) · [`fintech`](https://github.com/topics/fintech) · [`stock-market`](https://github.com/topics/stock-market) · [`linux`](https://github.com/topics/linux) · [`interview`](https://github.com/topics/interview)

---

## 📊 语言分布

| 语言 | 数量 | 占比 |
|---|---:|---:|
| Python | 46 | 26% |
| TypeScript | 27 | 15% |
| JavaScript | 14 | 8% |
| C++ | 10 | 6% |
| HTML | 8 | 4% |
| Rust | 7 | 4% |
| Java | 6 | 3% |
| Dart | 5 | 3% |
| Go | 5 | 3% |
| C# | 5 | 3% |
| Kotlin | 5 | 3% |
| C | 4 | 2% |
| Shell | 4 | 2% |
| Jupyter Notebook | 3 | 2% |
| Markdown | 2 | 1% |
| Ruby | 1 | 1% |
| Objective-C++ | 1 | 1% |
| CSS | 1 | 1% |
| GLSL | 1 | 1% |
| GDScript | 1 | 1% |
| PHP | 1 | 1% |
| Smali | 1 | 1% |
| Swift | 1 | 1% |

---

## 📌 关于这个仓库

- 数据来自 GitHub 官方 REST API 的 `/user/starred` 接口，`starred_at` 为真实收藏时间。
- 所有中文说明为人工撰写，非机器翻译；少数仓库官方无简介，已按项目内容补写并标注。
- 分类依据项目实际功能而非仓库作者，个别归类带主观判断。
- **每 6 小时自动刷新**：GitHub Actions 定时拉取 Star 列表，重新生成 README 并提交。
  新项目会先落进「🆕 待归类」，等补写中文说明后归入对应分类。

### 本地重新生成

```bash
# 1. 拉取全部 Star（需要 gh 已登录）
gh api -H "Accept: application/vnd.github.star+json" --paginate "user/starred?per_page=100" > stars_raw.json

# 2. 生成 stars.json（退出码 2 表示有新项目待归类）
python build_stars.py

# 3. 重新渲染 README（分类与说明维护在 map.py）
python gen_readme.py
```
