# -*- coding: utf-8 -*-
"""自动分类器：给新 Star 项目自动判定分类。

设计原则（重要）：
  1. **只做辅助，不做替代**。自动分类的置信度不足时，项目仍然进入
     stars_pending.json 等人工确认，绝不猜。
  2. 规则基于 GitHub topics（作者自己打的标签，最可靠）+ 描述关键词，
     不依赖 star 数、语言等弱信号。
  3. 规则表可维护：新增关键词直接往RULES 里加。

置信度判定：
  - score >= STRONG :自动归类，直接进分类表
  - score >= WEAK   : 给出「最可能的分类」但仍标记为待确认
  - score <  WEAK   : 不猜，进待归类
"""

# 置信度阈值
STRONG = 8   # 强匹配：直接归类
WEAK = 4     # 弱匹配：给出建议但仍待确认

# 关键词 -> (分类, 权重)
# 权重设计：topics 命中通常比描述关键词更可信，故 topics 权重更高
RULES = {
    # ---------- AI Agent 与智能体 ----------
    'ai-agent': [
        ('openclaw', 10), ('clawdbot', 10), ('moltbot', 10),
        ('agent-skill', 10), ('agent-skills', 10), ('agent-harness', 10),
        ('ai-agents', 9), ('ai-agent', 9), ('agentic-ai', 9), ('agentic-workflow', 9),
        ('multi-agent', 9), ('autonomous-agents', 9), ('claude-code', 9),
        ('codex', 8), ('opencode', 8), ('cursor', 6), ('copilot', 5),
        ('mcp', 8), ('model-context-protocol', 8), ('skills', 7),
        ('workflow-automation', 8), ('n8n', 10), ('low-code', 6),
        ('langchain', 6), ('langgraph', 7), ('crewai', 8), ('autogen', 7),
        ('agent', 4), ('agents', 4), ('llm', 5), ('prompt', 5),
        ('harness-engineering', 10), ('computer-use', 9), ('browser-agent', 9),
        ('function-calling', 7), ('tool-use', 6), ('swarm', 7),
        ('chatbot', 7), ('ai-assistant', 7), ('ai-chatbot', 7),
        ('openclaw-plugin', 10), ('ai-coding', 8), ('coding-agent', 9),
    ],
    # ---------- 大模型训练、推理与基础设施 ----------
    'ai-infra': [
        ('llm', 4), ('llmops', 10), ('inference', 8), ('model-serving', 10),
        ('fine-tuning', 10), ('lora', 10), ('rlhf', 10), ('gguf', 10),
        ('ollama', 10), ('vllm', 10), ('llama', 7), ('gemma', 8), ('qwen', 8),
        ('deepseek', 7), ('mistral', 8), ('transformers', 8), ('huggingface', 7),
        ('pytorch', 6), ('tensorflow', 6), ('keras', 6), ('paddlepaddle', 9),
        ('gan', 6), ('diffusion', 6), ('stable-diffusion', 7), ('comfyui', 8),
        ('image-generation', 6), ('text-to-image', 7), ('text-to-video', 7),
        ('video-generation', 7), ('tts', 7), ('speech-to-text', 7),
        ('whisper', 8), ('embedding', 6), ('vector-database', 7),
        ('ai-gateway', 10), ('api-gateway', 7), ('model-hub', 9),
        ('rag', 7), ('knowledge-graph', 5), ('model-training', 10),
        ('neural-networks', 6), ('deep-learning', 6), ('machine-learning', 4),
    ],
    # ---------- 金融量化与投资研究 ----------
    'finance': [
        ('quant', 10), ('quantitative-finance', 10), ('trading', 8),
        ('a-stock', 10), ('a-shares', 10), ('ashare', 10), ('china-stocks', 10),
        ('backtrader', 10), ('tushare', 10), ('akshare', 10), ('czsc', 10),
        ('stock', 7), ('stocks', 7), ('finance', 8), ('fintech', 8),
        ('investment', 6), ('investing', 6), ('portfolio', 8),
        ('ccxt', 10), ('crypto', 8), ('cryptocurrency', 8), ('bitcoin', 6),
        ('algorithmic-trading', 10), ('market-data', 8), ('bloomberg', 8),
        ('fibonacci', 5), ('indicators', 6), ('trading-bot', 9),
        ('valuation', 6), ('dividend', 6), ('fund', 5), ('etf', 6),
    ],
    # ---------- 电子书与阅读器 ----------
    'reading': [
        ('ebook', 10), ('ebook-reader', 10), ('ebooks', 10), ('epub', 10),
        ('mobi', 9), ('azw3', 9), ('kindle', 8), ('calibre', 10),
        ('book', 7), ('books', 7), ('reader', 8), ('reading', 7),
        ('comics', 8), ('comic', 7), ('manga', 8), ('cbz', 9), ('cbr', 9),
        ('novel', 7), ('audiobook', 9), ('tts-reader', 8),
        ('library', 6), ('book-search', 8), ('text-to-speech', 6),
    ],
    # ---------- RSS、资讯与舆情 ----------
    'rss-news': [
        ('rss', 10), ('rss-reader', 10), ('rsshub', 10), ('feed-reader', 10),
        ('news', 7), ('news-aggregator', 9), ('aggregator', 7),
        ('hot-news', 9), ('public-opinion', 9), ('sentiment-analysis', 6),
        ('trend', 6), ('trending', 6), ('media-monitoring', 8),
        ('subscription', 6), ('feedly', 8), ('atom-feed', 8),
    ],
    # ---------- 爬虫与浏览器自动化 ----------
    'crawl-browser': [
        ('crawler', 10), ('crawling', 10), ('scraper', 10), ('scraping', 10),
        ('web-scraping', 10), ('headless', 9), ('playwright', 9),
        ('puppeteer', 9), ('selenium', 9), ('beautifulsoup', 9),
        ('browser-automation', 10), ('anti-detect', 9), ('antidetect', 9),
        ('spider', 7), ('html-to-markdown', 8), ('web-scraper', 10),
    ],
    # ---------- 实用工具与效率软件 ----------
    'tools': [
        ('cli', 6), ('command-line', 7), ('terminal', 6), ('tui', 7),
        ('download', 6), ('downloader', 7), ('automation', 5),
        ('productivity', 8), ('note-taking', 9), ('notes', 6), ('markdown', 5),
        ('file-manager', 9), ('disk-usage', 9), ('sysadmin', 7),
        ('self-hosted', 5), ('docker', 5), ('package-manager', 9),
        ('media-manager', 9), ('scraper', 4), ('image-viewer', 7),
        ('launcher', 7), ('desktop', 5), ('windows', 3), ('macos', 3),
        ('linux', 3), ('privacy', 5), ('remote-desktop', 9), ('screenshot', 6),
        ('converter', 7), ('ocr', 6), ('document', 4), ('spreadsheet', 5),
    ],
    # ---------- Android / 移动端 ----------
    'mobile': [
        ('android', 9), ('kotlin', 8), ('jetpack-compose', 10), ('compose', 5),
        ('flutter', 8), ('dart', 8), ('ios', 6), ('swiftui', 9), ('swift', 4),
        ('react-native', 9), ('flutter-app', 9), ('apk', 9),
        ('app-updater', 9), ('accessibility', 6), ('tasker', 8),
        ('harmonyos', 9), ('arkts', 9), ('applescript', 6),
        ('iphone', 6), ('ipad', 6), ('macos-app', 6), ('webview2', 7),
    ],
    # ---------- 影音媒体与家庭娱乐 ----------
    'media': [
        ('jellyfin', 10), ('emby', 10), ('plex', 9), ('media-server', 10),
        ('subtitle', 9), ('subtitles', 9), ('video', 4), ('movies', 7),
        ('tv', 4), ('iptv', 9), ('live-streaming', 8), ('video-player', 8),
        ('audiobook-server', 9), ('music-player', 8), ('podcast', 7),
        ('comic-server', 9), ('metadata-provider', 8), ('transcode', 7),
        ('remotion', 8), ('video-production', 9), ('ffmpeg', 7),
        ('danmaku', 8), ('bilibili', 5),
    ],
    # ---------- 硬件、系统与嵌入式 ----------
    'system': [
        ('embedded', 10), ('firmware', 10), ('esp32', 10), ('arduino', 10),
        ('raspberry-pi', 10), ('kicad', 10), ('pcb', 9), ('fpga', 10),
        ('hardware', 9), ('i2c', 8), ('spi', 7), ('lvgl', 9),
        ('rtos', 10), ('operating-system', 7), ('kernel', 8), ('linux-kernel', 9),
        ('zephyr', 9), ('nuttx', 9), ('robotics', 8), ('robot', 7),
        ('smartisan', 9), ('android-source', 9), ('amoled', 8),
        ('waveshare', 9), ('sensor', 6), ('motor', 6), ('gps', 6),
        ('nav', 5), ('navigation', 6), ('os', 2),
    ],
    # ---------- 前端与网页开发 ----------
    'frontend': [
        ('css', 7), ('css-only', 10), ('frontend', 9), ('react', 5),
        ('vue', 6), ('tailwind', 7), ('tailwindcss', 8), ('html', 3),
        ('web-components', 8), ('svelte', 8), ('nextjs', 6), ('vite', 7),
        ('webpack', 6), ('sass', 7), ('javascript', 3),
    ],
    # ---------- 学习资料与教程 ----------
    'learning': [
        ('awesome', 7), ('awesome-list', 9), ('tutorial', 9), ('tutorials', 9),
        ('learning', 7), ('course', 7), ('courses', 7), ('guide', 5),
        ('guides', 5), ('handbook', 8), ('cheatsheet', 9), ('interview', 8),
        ('books', 6), ('free-books', 9), ('notes', 5), ('roadmap', 8),
        ('curriculum', 9), ('study', 6), ('educational', 8), ('beginner', 6),
        ('example', 3), ('examples', 3), ('demo', 2), ('ctf', 9),
        ('writeup', 8), ('writeups', 8), ('reverse-engineering', 9),
        ('ebook-library', 8), ('chinese', 3), ('tips', 4),
    ],
    # ---------- 游戏与模拟器 ----------
    'games': [
        ('game', 9), ('games', 9), ('gamedev', 10), ('game-development', 10),
        ('game-engine', 10), ('godot', 10), ('unity', 9), ('unreal', 9),
        ('emulator', 10), ('emulation', 10), ('retro', 8), ('pixel-art', 8),
        ('rpg', 7), ('roguelike', 9), ('indie-game', 9), ('3d', 4),
        ('godot-game', 10), ('homebrew', 8), ('switch', 5),
    ],
    # ---------- 隐私、安全与逆向 ----------
    'security': [
        ('security', 9), ('privacy', 8), ('antidetect', 9), ('anti-detect', 9),
        ('vpn', 9), ('proxy', 8), ('firewall', 9), ('encryption', 8),
        ('cryptography', 8), ('mdm', 8), ('pentest', 10), ('exploit', 9),
        ('malware', 10), ('forensics', 9), ('osint', 8), ('reverse-engineering', 8),
        ('authentication', 6), ('oauth', 6), ('tls', 6), ('ssl', 6),
        ('browser-engine', 8), ('independent-browser', 9), ('password-manager', 9),
    ],
    # ---------- 生活、健康与个人成长 ----------
    'life': [
        ('health', 8), ('fitness', 9), ('workout', 9), ('exercise', 8),
        ('gym', 8), ('nutrition', 8), ('diet', 7), ('recipe', 8), ('recipes', 8),
        ('cooking', 8), ('meditation', 8), ('sleep', 6), ('productivity-tips', 8),
        ('self-improvement', 9), ('career', 7), ('side-hustle', 9),
        ('entrepreneurship', 7), ('personal-finance', 9), ('study-abroad', 9),
        ('scholarship', 8), ('how-to-live-better', 10), ('life-guide', 9),
        ('habit', 7), ('mindset', 7), ('longevity', 9),
    ],
}

# 描述关键词的补充规则（权重较低，因为描述文本噪声大）
DESC_RULES = [
    # (正则, 分类, 权重)
    (r'\bagent\b|\bagentic\b', 'ai-agent', 3),
    (r'\bskill\b', 'ai-agent', 3),
    (r'\bmcp\b', 'ai-agent', 4),
    (r'claude code|claude-code', 'ai-agent', 5),
    (r'\bllm\b|large language model', 'ai-infra', 4),
    (r'\bquant\b|backtest', 'finance', 5),
    (r'\bstocks?\b|trading', 'finance', 4),
    (r'\bebook|\bepub\b|kindle', 'reading', 5),
    (r'\brss\b', 'rss-news', 5),
    (r'\bnews\b|headlines|hot news', 'rss-news', 3),
    (r'scrap|crawl', 'crawl-browser', 5),
    (r'jellyfin|emby|plex', 'media', 5),
    (r'\bsubtitle', 'media', 4),
    (r'\bvideo player|video streaming', 'media', 3),
    (r'\bkicad\b|\bpcb\b|\bfpga\b', 'system', 5),
    (r'\bfirmware\b|\bembedded\b|\besp32\b', 'system', 5),
    (r'\bandroid\b|jetpack compose', 'mobile', 5),
    (r'\bflutter\b', 'mobile', 4),
    (r'\bgame\b|\bemulator\b', 'games', 4),
    (r'\btutorial\b|\bawesome\b|\bguide\b|\bhandbook\b', 'learning', 4),
    (r'\bcourse|\bcurriculum|\blearn', 'learning', 3),
    (r'\bfitness\b|\bworkout\b|\brecipe', 'life', 4),
    (r'\bcli\b|command-line|\bterminal', 'tools', 3),
    (r'\bsecurity\b|\bprivacy\b|\bvpn\b|\bproxy\b', 'security', 4),
    (r'\bcss\b|\bfrontend\b|\breact\b|\bvue\b', 'frontend', 4),
    (r'\bimage generation|text-to-image|stable diffusion', 'ai-infra', 4),
    (r'\bvideo generation|text-to-video', 'ai-infra', 4),
]

# 仓库名关键词规则（权重高：作者取名时通常已点明用途）
# 匹配对象是 repo 名（不含 owner），按分隔符切成词后匹配
NAME_RULES = [
    # ---------- AI Agent ----------
    (('skill', 'skills'), 'ai-agent', 7),
    (('agent', 'agents'), 'ai-agent', 6),
    (('mcp',), 'ai-agent', 8),
    (('claude',), 'ai-agent', 7),
    (('codex',), 'ai-agent', 6),
    (('openclaw', 'clawdbot', 'moltbot'), 'ai-agent', 10),
    (('harness',), 'ai-agent', 7),
    (('n8n',), 'ai-agent', 10),
    (('flowise',), 'ai-agent', 9),
    (('lobehub',), 'ai-agent', 9),
    (('coze',), 'ai-agent', 8),
    (('dify',), 'ai-agent', 8),
    (('prompt',), 'ai-agent', 6),
    (('rag',), 'ai-agent', 6),
    (('ragflow',), 'ai-agent', 8),
    # ---------- 大模型基础设施 ----------
    (('llm', 'vllm', 'ollama', 'lora', 'gguf'), 'ai-infra', 9),
    (('paddlegan', 'diffusion', 'comfyui', 'stable-diffusion'), 'ai-infra', 9),
    (('gemma', 'qwen', 'llama', 'mistral', 'deepseek'), 'ai-infra', 7),
    (('pytorch', 'tensorflow'), 'ai-infra', 7),
    (('whisper', 'tts', 'speech'), 'ai-infra', 8),
    (('model',), 'ai-infra', 4),
    (('neural',), 'ai-infra', 6),
    (('harness', 'deepseek-harness'), 'ai-infra', 6),
    # ---------- 金融量化 ----------
    (('quant', 'quantitative'), 'finance', 9),
    (('stock', 'stocks', 'ashare', 'a-share'), 'finance', 8),
    (('trade', 'trading', 'backtest', 'backtrader'), 'finance', 8),
    (('tushare', 'akshare', 'czsc'), 'finance', 10),
    (('hedgefund', 'hedge-fund'), 'finance', 9),
    (('portfolio', 'invest', 'investment'), 'finance', 7),
    (('ccxt', 'crypto', 'bitcoin'), 'finance', 7),
    (('finance', 'fincept'), 'finance', 8),
    (('fund', 'etf'), 'finance', 5),
    # ---------- 阅读器 ----------
    (('ebook', 'ebooks', 'epub', 'kindle', 'calibre'), 'reading', 10),
    (('reader', 'readest', 'koodo', 'kavita'), 'reading', 8),
    (('manga', 'comic', 'comics'), 'reading', 8),
    (('audiobook',), 'reading', 9),
    (('book', 'books'), 'reading', 6),
    (('novel',), 'reading', 7),
    (('read',), 'reading', 4),
    # ---------- RSS / 资讯 ----------
    (('rss', 'rsshub', 'folo', 'feed'), 'rss-news', 9),
    (('news',), 'rss-news', 7),
    (('trending', 'trendradar', 'newsnow'), 'rss-news', 8),
    (('opencost', 'monitor'), 'rss-news', 3),
    # ---------- 爬虫 ----------
    (('crawler', 'crawlee', 'crawl4ai', 'scrapy'), 'crawl-browser', 10),
    (('scraper', 'scrapling'), 'crawl-browser', 9),
    (('playwright', 'puppeteer', 'selenium'), 'crawl-browser', 8),
    (('stagehand', 'obscura'), 'crawl-browser', 9),
    (('firecrawl',), 'crawl-browser', 10),
    (('fireplexity',), 'ai-agent', 9),
    # ---------- 工具 ----------
    (('trafficmonitor', 'disktree', 'obtainium', 'unigetui'), 'tools', 9),
    (('seelen', 'uconfig'), 'tools', 8),
    (('cli', 'tui', 'terminal'), 'tools', 7),
    (('downloader', 'download'), 'tools', 6),
    (('markitdown',), 'tools', 9),
    (('note', 'notes', 'blinko', 'memos'), 'tools', 7),
    (('manager',), 'tools', 4),
    (('kit', 'toolkit', 'tools'), 'tools', 4),
    (('proxy', 'flclash', 'clashbox'), 'tools', 7),
    (('jpet', 'pet'), 'tools', 6),
    # ---------- 移动端 ----------
    (('android', 'compose'), 'mobile', 8),
    (('flutter', 'dart'), 'mobile', 7),
    (('harmony', 'arkts'), 'mobile', 9),
    (('kotlin',), 'mobile', 7),
    (('swift',), 'mobile', 6),
    (('apk',), 'mobile', 7),
    (('bigbang', 'launcher'), 'mobile', 7),
    (('jpet',), 'mobile', 5),
    (('moto-gps',), 'mobile', 6),
    # ---------- 影音 ----------
    (('jellyfin', 'emby', 'plex'), 'media', 10),
    (('subfinder', 'subtitle', 'subtitles'), 'media', 9),
    (('my-tv', 'tvapp', 'libretv', 'cctv'), 'media', 8),
    (('bilievolved',), 'mobile', 9),
    (('bili', 'pili'), 'media', 8),
    (('remotion', 'montage'), 'media', 8),
    (('peach',), 'media', 8),
    (('video', 'movie', 'movies', 'media'), 'media', 6),
    (('videoplayer', 'player'), 'media', 5),
    (('gsydouyin',), 'media', 6),
    # ---------- 硬件 / 嵌入式 ----------
    (('kicad', 'pcb', 'fpga'), 'system', 10),
    (('esp32', 'arduino', 'firmware', 'embedded'), 'system', 10),
    (('waveshare', 'amoled', 'smartisan', 'monica'), 'system', 9),
    (('nas', 'jumper', 'robot'), 'system', 8),
    (('fuchsia', 'liteos'), 'system', 9),
    (('qt', 'scrcpy'), 'system', 6),
    (('pocketpd',), 'system', 9),
    (('android-source', 'smartisanos'), 'system', 9),
    # ---------- 前端 ----------
    (('css', 'frontend', 'vue', 'react'), 'frontend', 7),
    (('hub16', 'macropad'), 'frontend', 7),
    (('mind-map', 'mindmap'), 'frontend', 7),
    # ---------- 学习资料 ----------
    (('awesome', 'tutorial', 'course', 'handbook'), 'learning', 9),
    (('guide', 'guides', 'roadmap', 'cheatsheet'), 'learning', 7),
    (('books', 'notes', 'learning'), 'learning', 6),
    (('interview', 'cs-notes', 'javaguide'), 'learning', 9),
    (('linux-command', 'free-programming', 'javafamily', 'golangfamily'), 'learning', 10),
    (('ctf', 'writeup'), 'learning', 8),
    (('100-days', 'nndl'), 'learning', 8),
    (('howto', 'how-to'), 'learning', 6),
    (('programming-books',), 'learning', 10),
    (('family',), 'learning', 7),
    # ---------- 游戏 ----------
    (('game', 'games', 'gamedev'), 'games', 8),
    (('emulator', 'emulation', 'shadps4'), 'games', 10),
    (('godot', 'unity', 'unreal'), 'games', 9),
    (('retro', 'nfs', 'dancingline'), 'games', 9),
    (('microverse',), 'games', 9),
    (('diablo', 'd2r'), 'games', 9),
    # ---------- 安全 ----------
    (('bypass', 'mdm', 'exploit'), 'security', 9),
    (('ladybird', 'minbrowser', 'flare'), 'security', 8),
    (('privacy', 'vpn', 'antidetect'), 'security', 9),
    (('reverse',), 'security', 7),
    # ---------- 生活 ----------
    (('howtolivebetter', 'paidtostudyabroad'), 'life', 10),
    (('fitness', 'workout', 'cooklikehoc'), 'life', 9),
    (('opc-methodology', 'side-bussiness', 'lean-side'), 'life', 9),
    # ---------- 工具（放在后面，用于覆盖前面的泛化匹配）----------
    (('reactive-resume', 'resume'), 'tools', 9),
    (('markitdown',), 'tools', 10),
    (('rayburst',), 'tools', 9),
    (('wordpecker',), 'reading', 9),
    (('pdf-craft', 'pdfcraft'), 'reading', 9),
    (('someread', 'sageread'), 'reading', 9),
    (('flashaim', 'ai-goofish'), 'tools', 9),
    (('kimi-cli', 'kimi'), 'ai-agent', 9),
    (('notify',), 'ai-agent', 6),
    (('xhs', 'xiaohongshu'), 'ai-agent', 9),
    (('mac-duo', 'macduo'), 'tools', 9),
    (('billd', 'billd-desk'), 'tools', 9),
    (('jpet',), 'tools', 9),
    (('mind-map', 'mindmap'), 'tools', 7),
    (('flclash', 'clashbox'), 'tools', 9),
    (('obtainium',), 'tools', 9),
    (('uzi', 'uzi-skill'), 'finance', 9),
    (('a_share', 'ashare', 'a-share', 'wudao'), 'finance', 9),
    (('investment', 'hedge'), 'finance', 8),
    (('bitcoin-whitepaper',), 'learning', 9),
    (('douban',), 'tools', 9),
    (('goofish',), 'tools', 9),
]

# 强制覆盖规则：命中即直接定案，不参与加权竞争。
# 用于修正关键词天然会误判的边界项目。
OVERRIDES = [
    (('markitdown',), 'tools'),
    (('mac-duo', 'macduo'), 'tools'),
    (('billd', 'billd-desk'), 'tools'),
    (('jpet',), 'tools'),
    (('mind-map', 'mindmap'), 'tools'),
    (('flclash', 'clashbox'), 'tools'),
    (('obtainium',), 'tools'),
    (('reactive-resume',), 'tools'),
    (('rayburst',), 'tools'),
    (('douban',), 'tools'),
    (('wordpecker',), 'reading'),
    (('pdf-craft', 'pdfcraft'), 'reading'),
    (('someread', 'sageread'), 'reading'),
    (('kimi-cli',), 'ai-agent'),
    (('xhs-toolkit',), 'ai-agent'),
    (('uzi-skill',), 'finance'),
    (('a_share', 'ashare', 'a-share', 'wudao-ashare'), 'finance'),
    (('ai-hedge-fund',), 'finance'),
    (('whitepaper',), 'learning'),
    (('ai-goofish',), 'tools'),
    (('d2r-mobile',), 'games'),
    (('nfsmostwanted',), 'games'),
    (('piliplus',), 'media'),
    (('tvapp',), 'media'),
    (('gsydouyin', 'gsyvideoplayer'), 'mobile'),
    (('bilibili-evolved',), 'mobile'),
    (('awesome-smartianos', 'awesome-smartisan'), 'system'),
    (('awesome-openclaw-usecases',), 'learning'),
    (('deepseek-harness',), 'ai-infra'),
    (('javaguide', 'linux-command', 'free-programming-books'), 'learning'),
    (('the-swift-programming-language',), 'learning'),
    (('some-many-books',), 'reading'),
    (('smartisan-tech',), 'system'),
    (('poseatlas', 'ruic'), 'tools'),
    (('nfsmostwanted2012',), 'games'),
    (('open-source-games',), 'learning'),
    (('fuchsiaos-docs-zh_cn',), 'system'),
    (('fuchsia-os-tutorial',), 'system'),
    (('smartisan-original-launcher',), 'mobile'),
    (('onestep4',), 'mobile'),
    (('smartisantech',), 'system'),
    (('chinesesubfinder',), 'media'),
    (('free-programming-books-zh_cn',), 'learning'),
    (('leereilly',), 'learning'),
    (('fireplexity',), 'ai-agent'),
    (('whitepaper',), 'learning'),
]

import re

# 预先编译
_DESC_COMPILED = [(re.compile(p, re.I), c, w) for p, c, w in DESC_RULES]

# 仓库名切词
_NAME_SPLIT = re.compile(r'[^a-z0-9+#.]+')

# 中文/本地化后缀：命中说明这是「中文学习资料」而非对应技术栈项目
# 收窄：只认明确的中文学习资料后缀，避免误伤 ChineseSubFinder 这类
# 名字里带 Chinese 但实为工具的项目
_ZH_SUFFIX = re.compile(r'(-zh[_-]?cn$|-chinese$|-in-chinese$|_zh_cn$|-zh_cn$)')
# awesome 列表：单独处理，避免被具体技术词带偏
_AWESOME = re.compile(r'^awesome')


def _name_tokens(full_name):
    """从 owner/repo 中提取分词结果（小写 + 连字符整体）。

    同时包含 repo 名与 owner 名：有些项目只有 owner 能提供线索
    （如 SmartisanTech/android，repo 名只有 android）。
    """
    owner, _, repo = full_name.partition('/')
    owner_l, repo_l = owner.lower(), repo.lower()
    toks = set(_NAME_SPLIT.split(repo_l))
    for part in re.split(r'[-_.]', repo_l):
        if part:
            toks.add(part)
    toks.add(repo_l)
    # owner 单独的分词
    toks.add(owner_l)
    for part in re.split(r'[-_.]', owner_l):
        if part:
            toks.add(part)
    return toks


def classify(repo, full_name=''):
    """判定一个仓库的分类。

    repo: dict，需包含 topics / description
    返回 (category, score, second_best_category, second_score)
      category 为 None 表示置信度不足，不猜。
    """
    topics = [t.lower() for t in (repo.get('topics') or [])]
    desc = repo.get('description') or ''
    desc_l = desc.lower()

    scores = {}

    def add(cat, w):
        scores[cat] = scores.get(cat, 0) + w

    # 0) 中文学习资料识别：优先级高于技术栈关键词
    #    这类项目名常含具体技术词（swift/java/...），但本质是学习资料
    is_zh_learning = bool(_ZH_SUFFIX.search(full_name.lower()))
    if is_zh_learning:
        add('learning', 12)

    # 1) topics 命中
    for t in topics:
        for cat, rules in RULES.items():
            for kw, weight in rules:
                if t == kw or (len(kw) > 4 and kw in t):
                    add(cat, weight)
                    break

    # 2) 描述关键词命中
    for pat, cat, weight in _DESC_COMPILED:
        if pat.search(desc_l):
            add(cat, weight)

    # 3) 仓库名命中
    toks = _name_tokens(full_name)
    repo_l = full_name.split('/', 1)[-1].lower()
    for keys, cat, weight in NAME_RULES:
        if any(k in toks for k in keys):
            add(cat, weight)

    # 4) awesome 列表：归入学习类（收集清单本质是索引资料）
    #    例外：awesome-<具体技术> 且带该技术 topics 时，仍按技术归类
    if _AWESOME.match(repo_l) and 'learning' not in scores:
        add('learning', 10)

    # 4b) 「某某列表/清单」型仓库（games list / book list 等）本质是索引资料
    if re.search(r'(list|collection|archive)$', repo_l) and not topics:
        add('learning', 8)

    # 5) 中文学习资料直接定案：名字带 -zh_CN / -chinese 的几乎都是中文学习资料
    #    优先级高于具体技术词（free-programming-books-zh_CN 里含 books/free/programming）
    if is_zh_learning:
        # 例外：FuchsiaOS-docs-zh_CN 这类系统文档属系统类
        if any(k in repo_l for k in ('fuchsiaos-docs', 'fuchsia-os')):
            return 'system', 99, None, 0
        return 'learning', 99, None, 0

    # 6) 高优先级覆盖：命中即直接定案，不参与加权竞争
    #    这些规则针对已知的边界/易错项目（如 markitdown 不是 Agent 而是工具）
    for keys, cat in OVERRIDES:
        if any(k in toks for k in keys):
            return cat, 99, None, 0

    if not scores:
        return None, 0, None, 0

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    best_cat, best_score = ranked[0]
    second_cat, second_score = (ranked[1] if len(ranked) > 1 else (None, 0))

    # 次选过于接近时弃权，避免在边界项目上乱猜
    if second_cat and second_score >= best_score * 0.85 and second_score > 0:
        return None, best_score, second_cat, second_score

    return best_cat, best_score, second_cat, second_score


def suggest_description(repo, category):
    """为自动归类的项目生成一句保守的中文说明。

    原则：宁可信息少，也不要瞎编。这里只做「事实搬运」：
    优先用官方简介（原文），没有则给出明确的待补充提示。

    repo 需包含 desc 或 description 字段（兼容两种来源）。
    """
    desc = (repo.get('desc') or repo.get('description') or '').strip()
    if not desc:
        return f'（{category} 类项目，官方无简介，待补充说明）'
    desc = desc.replace('\n', ' ').strip()
    if len(desc) > 60:
        desc = desc[:58].rstrip() + '…'
    return desc


# ---- 中文自动说明生成 ----
# 把 topics / 描述里的英文概念映射成中文短语，
# 再按分类组装成一句中文说明。只用词表里有的概念，不做翻译推测。

CONCEPT_CN = {
    # 通用形态
    'self-hosted': '自托管', 'open-source': '开源', 'cross-platform': '跨平台',
    'multi-platform': '多平台', 'local-first': '本地优先', 'free': '免费',
    'experimental': '实验性', 'unofficial': '非官方', 'archived': '已归档',
    'ad-free': '无广告', 'no-ads': '无广告', 'privacy': '注重隐私',
    'fast': '高性能', 'lightweight': '轻量', 'modern': '现代化',
    'powerful': '强大', 'simple': '简单', 'easy-to-use': '易用',
    'plugin': '插件', 'plugins': '插件', 'extension': '扩展',
    'server': '服务端', 'client': '客户端', 'app': '应用',
    'tool': '工具', 'library': '库', 'framework': '框架', 'engine': '引擎',
    'api': '接口', 'sdk': 'SDK', 'cli': '命令行', 'gui': '图形界面',
    'web': '网页版', 'desktop': '桌面端', 'mobile': '移动端',
    'video': '视频', 'audio': '音频', 'image': '图像', 'text': '文本',
    'markdown': 'Markdown', 'pdf': 'PDF', 'epub': 'EPUB', 'cbz': 'CBZ',
    'reader': '阅读器', 'server-side': '服务端', 'backend': '后端',
    'frontend': '前端', 'fullstack': '全栈', 'database': '数据库',
    'ai': 'AI', 'llm': '大模型', 'agent': '智能体', 'agents': '智能体',
    'multi-agent': '多智能体', 'agentic': '智能体化', 'autonomous': '自主',
    'skill': 'Skill', 'skills': 'Skills', 'mcp': 'MCP',
    'claude': 'Claude', 'gpt': 'GPT', 'gemini': 'Gemini', 'deepseek': 'DeepSeek',
    'ollama': 'Ollama', 'openai': 'OpenAI', 'anthropic': 'Anthropic',
    'rag': 'RAG', 'harness': 'Harness', 'workflow': '工作流',
    'automation': '自动化', 'scraper': '抓取', 'crawler': '爬虫',
    'proxy': '代理', 'vpn': 'VPN', 'mirror': '镜像',
    'quant': '量化', 'trading': '交易', 'stock': '股票', 'finance': '金融',
    'rss': 'RSS', 'news': '资讯', 'notification': '通知',
    'jellyfin': 'Jellyfin', 'emby': 'Emby', 'plex': 'Plex',
    'subtitle': '字幕', 'subtitles': '字幕', 'streaming': '流媒体',
    'comics': '漫画', 'manga': '漫画', 'novel': '小说', 'book': '书籍',
    'books': '书籍', 'library-server': '书库服务',
    'kicad': 'KiCad', 'pcb': 'PCB', 'fpga': 'FPGA', 'embedded': '嵌入式',
    'firmware': '固件', 'esp32': 'ESP32', 'arduino': 'Arduino',
    'raspberry-pi': '树莓派', 'hardware': '硬件', 'robot': '机器人',
    'android': 'Android', 'ios': 'iOS', 'flutter': 'Flutter',
    'kotlin': 'Kotlin', 'swift': 'Swift', 'dart': 'Dart',
    'react': 'React', 'vue': 'Vue', 'css': 'CSS', 'tailwind': 'Tailwind',
    'game': '游戏', 'games': '游戏', 'gamedev': '游戏开发',
    'emulator': '模拟器', 'emulation': '主机模拟', 'retro': '复古',
    'tutorial': '教程', 'course': '课程', 'guide': '指南',
    'handbook': '手册', 'awesome': '精选合集', 'notes': '笔记',
    'interview': '面试', 'roadmap': '路线图', 'cheatsheet': '速查表',
    'learning': '学习', 'book-library': '书库',
    'security': '安全', 'encryption': '加密', 'browser': '浏览器',
    'fitness': '健身', 'workout': '训练', 'recipe': '菜谱', 'health': '健康',
    'life': '生活', 'career': '职业', 'scholarship': '奖学金',
    'subtitle-generator': '字幕生成', 'image-generation': '图像生成',
    'text-to-image': '文生图', 'text-to-video': '文生视频',
    'video-generation': '视频生成', 'tts': '语音合成',
    'research': '研究', 'coding': '编程', 'developer': '开发',
    'note-taking': '笔记', 'notes-app': '笔记应用',
    'markdown-converter': 'Markdown 转换', 'converter': '转换工具',
    'proxy-client': '代理客户端', 'download': '下载', 'downloader': '下载器',
    'color-picker': '取色', 'theme': '主题', 'icon-pack': '图标包',
    'navigation': '导航', 'gps': 'GPS', 'dashboard': '仪表盘',
}

# 分类兜底短语（当 concepts 为空时用）
CAT_FALLBACK_CN = {
    'ai-agent': '智能体应用', 'ai-infra': '大模型工具',
    'finance': '金融量化工具', 'reading': '电子书阅读与书库',
    'rss-news': 'RSS 订阅与资讯聚合', 'crawl-browser': '网页抓取与浏览器自动化',
    'tools': '实用工具', 'mobile': '移动端应用',
    'media': '影音媒体工具', 'system': '硬件与嵌入式项目',
    'frontend': '前端项目', 'learning': '学习资料',
    'games': '游戏项目', 'security': '安全与隐私工具',
    'life': '生活与个人成长',
}


def auto_description(repo, category):
    """根据 topics 与官方简介自动拼一句中文说明。

    原则：只用词表中的概念做「事实重组」，不翻译整句、不臆测功能。
    产出形如「跨平台的电子书阅读服务器」——
    读起来是中文，信息来自官方 topics，可信度可控。
    """
    topics = [t.lower() for t in (repo.get('topics') or [])]
    desc = (repo.get('desc') or repo.get('description') or '').strip()

    # 1) 描述若已是中文，直接取第一个分句（中文项目简介本身信息最准）
    if desc:
        cn_chars = [c for c in desc if '\u4e00' <= c <= '\u9fff']
        if len(cn_chars) >= 6:
            first = re.split(r'[，。；,;]', desc)[0].strip()
            if len(first) >= 6:
                return first[:52]

    # 2) 收集可翻译的概念
    concepts = []
    for t in topics:
        if t in CONCEPT_CN:
            cn = CONCEPT_CN[t]
            # 同义概念去重（智能体/智能体化 只留一个）
            if cn not in concepts and not any(cn in c or c in cn for c in concepts):
                concepts.append(cn)

    # 3) 过滤掉信息量低的修饰词，避免出现「模拟的游戏项目」这种空话
    WEAK = {'模拟', '转换工具', '工具', '库', '应用', '扩展', '插件',
            '开发者', '编程', '研究', '文本', '图像', '音频', '视频', '前端', '后端'}
    strong = [c for c in concepts if c not in WEAK]
    if strong:
        concepts = strong

    tail = CAT_FALLBACK_CN.get(category, '')
    # 去掉与 concepts 重复的兜底词
    tail_core = tail
    for c in concepts:
        if c in tail_core:
            tail_core = tail_core.replace(c, '').strip('的 ·，,')
    tail_core = tail_core.lstrip('的 ')

    if concepts:
        head = concepts[0]
        rest = concepts[1:4]
        if rest:
            body = f'{head}、{"、".join(rest)}'
        else:
            body = head
        if tail_core:
            out = f'{body}的{tail_core}'
        else:
            out = body
        # 修掉中英文之间与重复的空格
        out = re.sub(r'\s+', ' ', out).replace(' 的', '的').strip()
        return out[:56]

    # 4) 实在没有信息
    return f'（{tail}，官方无简介，待补充说明）'


if __name__ == '__main__':
    import json, os, sys
    BASE = os.path.dirname(os.path.abspath(__file__))
    raw = json.load(open(os.path.join(BASE, 'stars_raw.json'), encoding='utf-8'))
    import map as M
    ok = wrong = 0
    misses = []
    for it in raw:
        r = it['repo']
        full = r['full_name']
        if full not in M.NOTES:
            continue
        truth = M.NOTES[full][0]
        pred, score, second, s2 = classify(r, full)
        if pred is None:
            misses.append((full, truth, score, second, s2))
            wrong += 1
        elif pred == truth:
            ok += 1
        else:
            wrong += 1
            misses.append((full, f'预测{pred} 但实际{truth}', score, second, s2))
    print(f'回测：{ok} 个正确，{wrong} 个不一致/未命中')
    print(f'准确率：{ok*100//max(1,ok+wrong)}%')
    print('\n不一致明细：')
    for full, note, score, second, s2 in misses:
        print(f'  {full}: {note} (score={score} 次选={second}:{s2})')
