# KiroGate 配置摘要

**生成时间：** 2026-01-27 14:07

---

## 🌐 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **主服务** | `http://localhost:9000` | API 网关主地址 |
| **API 文档** | `http://localhost:9000/docs` | Swagger UI 文档 |
| **Admin 面板** | `http://localhost:9000/admin` | 管理后台 |
| **健康检查** | `http://localhost:9000/health` | 服务健康状态 |

---

## 🔑 API 密钥配置

### 当前配置的 API Key
```bash
PROXY_API_KEY="my-super-secret-password-123"
```

### 客户端使用方式

#### 1️⃣ Anthropic SDK (Claude Code)
```bash
export ANTHROPIC_BASE_URL="http://localhost:9000"
export ANTHROPIC_API_KEY="my-super-secret-password-123"
```

#### 2️⃣ OpenAI SDK
```bash
export OPENAI_BASE_URL="http://localhost:9000/v1"
export OPENAI_API_KEY="my-super-secret-password-123"
```

#### 3️⃣ Factory 配置
```json
{
  "custom_models": [
    {
      "model_display_name": "KiroGate Claude",
      "model": "claude-sonnet-4-5",
      "base_url": "http://localhost:9000",
      "api_key": "my-super-secret-password-123",
      "provider": "anthropic"
    }
  ]
}
```

---

## ⚙️ 核心配置

| 配置项 | 当前值 | 说明 |
|--------|--------|------|
| **端口号** | `9000` | 服务监听端口 |
| **Token 分配策略** | `round_robin` | 轮询分配，多账号同时使用 |
| **强制模型** | `claude-sonnet-4-5` | 覆盖客户端请求的模型 |
| **调试模式** | `all` | 保存所有请求日志 |
| **Cookie 安全** | `false` | 本地开发模式 |

---

## 🔐 OAuth 配置

### GitHub OAuth
```bash
GITHUB_CLIENT_ID="Ov23liNwAKih364jkxh8"
GITHUB_CLIENT_SECRET="3830bf3a9b87a22db02d35a042d007026827f964"
GITHUB_REDIRECT_URI="http://localhost:9000/oauth2/github/callback"
```

⚠️ **注意：** 如果你修改了端口号，需要在 GitHub OAuth App 设置中更新回调地址。

---

## 📊 Token 分配策略详解

### 当前策略：round_robin（轮询分配）

**特点：**
- ✅ 多账号同时使用，均匀分配请求
- ✅ 避免单个 Token 过载
- ✅ 所有公共 Token 轮流使用

**其他可选策略：**
- `score_based`：评分优先（综合成功率、新鲜度、负载均衡）
- `sequential`：顺序使用（用完一个再用下一个）

**修改方式：**
```bash
# 在 .env 文件中修改
TOKEN_ALLOCATION_STRATEGY="round_robin"
```

---

## 🔧 今日完成的修复

### 1. ✅ 修复 IDC Token 验证问题
- **文件：** [kiro_gateway/health_checker.py:128-148](kiro_gateway/health_checker.py#L128-L148)
- **问题：** 健康检查器在验证 IDC 类型的 token 时缺少 `client_id` 和 `client_secret`
- **修复：** 使用 `get_token_credentials()` 获取完整凭证，支持 Social 和 IDC 两种认证模式

### 2. ✅ 更新端口号配置
- **修改：** 8000 → 9000
- **影响文件：**
  - [main.py](main.py)
  - [run.sh](run.sh)
  - [README.md](README.md)
  - [.env](.env)

### 3. ✅ 修改 Token 分配策略
- **配置：** [.env:172](.env#L172)
- **策略：** `round_robin`（多账号同时使用）

### 4. ✅ 动态显示 API Key
- **文件：** [kiro_gateway/pages.py:1023](kiro_gateway/pages.py#L1023)
- **功能：** API 文档页面自动显示当前配置的 `PROXY_API_KEY`

---

## 🚀 启动服务

```bash
./run.sh
```

服务启动后访问：
- 📖 API 文档：http://localhost:9000/docs
- 🎛️ Admin 面板：http://localhost:9000/admin

---

## 📝 注意事项

1. **重启服务以应用所有修改**
2. **IDC token 验证修复后，之前标记为 "invalid" 的有效 token 会自动恢复为 "active"**
3. **Token 分配策略修改后，请求将均匀分配到所有公共 token**
4. **API 文档中的配置示例会自动显示当前的 API Key 和服务地址**

---

**配置文件位置：** [.env](.env)
**文档生成时间：** 2026-01-27 14:07
