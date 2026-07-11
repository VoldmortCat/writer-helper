# API 配置示例

## DeepSeek（推荐）

```yaml
skills:
  config:
    ai_writing_buddy:
      api_key: sk-your-deepseek-key
      api_base: https://api.deepseek.com
      model: deepseek-chat
```

环境变量方式：
```bash
set WRITING_BUDDY_API_KEY=sk-your-deepseek-key
set WRITING_BUDDY_API_BASE=https://api.deepseek.com
set WRITING_BUDDY_MODEL=deepseek-chat
```

## 通义千问（阿里云）

```bash
set WRITING_BUDDY_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
set WRITING_BUDDY_MODEL=qwen-turbo
```

## 豆包（火山引擎）

```bash
set WRITING_BUDDY_API_BASE=https://ark.cn-beijing.volces.com/api/v3
set WRITING_BUDDY_MODEL=ep-2024xxxx-xxxxx
```

## OpenAI 兼容接口

任意兼容 OpenAI 的 API 都可以用：

```bash
set WRITING_BUDDY_API_BASE=你的接口地址
set WRITING_BUDDY_MODEL=模型名称
```
