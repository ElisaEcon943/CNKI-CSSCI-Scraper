CNKI-CSSCI-Scraper: 知网高质量文献自动化爬取工具
📌 项目简介
本项目是一个基于 Python + Selenium 开发的自动化脚本，专门用于从中国知网（CNKI）高级检索界面批量获取文献元数据。

核心特色：

学术导向：预设了对 CSSCI（南大核心） 期刊的选择逻辑，适合商科及社会科学研究者获取高质量参考文献。

高级逻辑支持：支持知网特有的布尔逻辑运算符（如 *、+、-）以及引号保护规则。

深度数据采集：抓取信息包括但不限于：标题、第一作者、所属单位、来源期刊以及关键词。

鲁棒性设计：内置多种 XPath 匹配模式以应对知网前端页面的动态更新，并包含自动切换“详细模式”及“每页50条”展示的逻辑。

🛠️ 环境要求
Python: 3.8 或更高版本

浏览器: Microsoft Edge (推荐)

WebDriver: 需安装与 Edge 版本匹配的 msedgedriver。

🚀 快速开始
1. 克隆仓库
Bash
git clone https://github.com/ElisaEcon943/CNKI-CSSCI-Scraper.git
cd CNKI-CSSCI-Scraper
2. 安装依赖
Bash
pip install selenium
3. 配置路径
在 scratchzhiwang.py 中修改工作目录为你本地的存储路径：

Python
os.chdir(r'C:\你的路径\CODE_Field\...')
4. 运行脚本
Bash
python scratchzhiwang.py
⚙️ 自定义配置
你可以根据研究需求在脚本中直接修改检索条件：

关键词检索式：

Python
input_field.send_keys("(区域创新 + 创新中心) * 现代化产业体系")
目标期刊范围：

Python
journal_name = '经济研究 + 管理世界 + 中国工业经济 + ...'
📊 爬取字段说明
脚本会自动生成一个名为 区域生态1.csv 的文件（UTF-8-BOM 编码，Excel 可直接打开），包含以下字段：

标题：文章全名。

第一作者：默认抓取排名第一的研究者。

单位：作者所属的高校或研究机构。

期刊：刊载该文献的期刊名称。

关键词：文献的核心关键词标签。

⚠️ 注意事项
反爬机制：知网具有较严的反爬策略。脚本内已设置随机等待时间（time.sleep），请勿过快、高频次运行。

校园网限制：建议在连接校园网（VPN）环境下使用，以便自动获取下载/查看权限。

验证码：如遇到滑块验证，脚本会触发 TimeoutException，请在浏览器中手动完成验证后再重启或继续。

📜 许可证
本项目采用 MIT 许可证，仅供学术交流使用，请勿用于商业用途。

Author: [Elisa]
