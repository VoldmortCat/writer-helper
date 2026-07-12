# AI 写作搭子 — Hermes Agent Skill

选题 #21 — **AI 写作搭子**（来自 AI 实践场景清单）

## 项目简介

AI 写作搭子是一个**编辑伙伴 + 灵感催化剂**，封装为 Hermes Agent Skill。
你写一段，AI 给反馈；你卡壳了，AI 帮你梳理思路；你写长篇了，AI 帮你检查前后矛盾；
你写久了，AI 学会你的风格。

**AI 核心价值：** 不是套个 AI 壳做传统功能——AI 本身就是分析引擎。

## 运行环境

| 项目 | 说明 |
|------|------|
| 运行平台 | Hermes Agent（CLI / 桌面应用 / 网关） |
| 依赖模型 | 任意具备 tool-calling 能力的 LLM（推荐 DeepSeek） |
| Python 版本 | 3.11.5（仅辅助脚本需要，核心功能无需 Python） |
| 额外依赖 | 无（无需 pip install、无需额外 API Key 配置） |

## 核心流程

| 流程 | 触发短语 | 说明 |
|------|---------|------|
| 快速审稿 | 帮我看看这段 / 直接贴文字 | 5 维度分析 + 标出最需要改的一个问题 |
| 打磨跟单 | 帮我改改 | review - 你改 - 对比 - 再改，直到你说停 |
| 卡壳疏导 | 写不下去了 / 没思路 | 给 3 个发展方向 + 示例开头 |
| 长篇体检 | 帮我检查整篇 | 多章一致性检查：人物矛盾/情节漏洞/伏笔回收/细节照应 |

## 上下文管理

长文本（超过 1500 字）自动写入临时文件 output/tmp/，反馈结论留在上下文，原文不保留。
流程结束时自动清理，也可手动清理：python scripts/clean_tmp.py

## 项目结构

skill/
  SKILL.md              # 技能定义（Agent 指令）
  README.md             # 本文件
  scripts/
    stats.py            # 文章统计数据
    clean_tmp.py        # 临时文件清理
    gen_report.py       # 使用流程 HTML 报告生成
  references/
    使用指南.md         # 各流程使用说明
    写作技巧参考.md     # 分析框架参考
  style/
    风格记录_用户.md    # 用户写作风格存档
  data/                 # 测试数据
  tests/                # 测试记录
  output/
    tmp/                # 长文本临时文件
  iteration/            # 迭代升级日志

## 辅助工具

| 脚本 | 用途 | 用法 |
|------|------|------|
| scripts/stats.py | 文章统计数据 | python stats.py < 文章.txt |
| scripts/clean_tmp.py | 清理临时文件 | python clean_tmp.py [--dry-run] [--days N] |
| scripts/gen_report.py | 生成使用流程 HTML 报告 | cat data.json \| python gen_report.py |

## 迭代历程

| 迭代 | 方向 | 来源 | 核心变化 |
|------|------|------|---------|
| 1 | 文本类型自动检测 | 自发现 | review 适配不同文体 |
| 2 | 一致性检查 | xlsx 迭代1 | 长篇体检 |
| 3 | 风格学习 | xlsx 迭代2 | 风格存档 + 一致性检查 |
| 4 | 个性化灵感 | xlsx 迭代3 | 基于历史给方向 |
| 5 | 流程化跟单 | 自发现 | 4 个跟单流程 + 自动切换 |
| 6 | 上下文管理 | 自发现 | 长文本文件化 + 临时文件清理 + 轮次感知 |

详见 iteration/iteration_log.md。
