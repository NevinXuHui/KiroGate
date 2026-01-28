# 🔑 超级 API Key 功能使用指南

## 📖 目录

- [功能概述](#功能概述)
- [快速开始](#快速开始)
- [详细使用步骤](#详细使用步骤)
- [功能特性](#功能特性)
- [使用示例](#使用示例)
- [常见问题](#常见问题)
- [安全建议](#安全建议)

---

## 功能概述

**超级 API Key** 是 KiroGate 的高级功能，允许管理员为用户创建特殊的 API Key，这些 Key 具有以下特权：

### 🌟 核心特性

| 特性 | 说明 |
|------|------|
| 🌐 **访问所有公开 Token** | 可以使用所有用户捐献的公开 Token，不限于创建者自己的 Token |
| 🎯 **智能分配** | 自动选择最佳可用的公共 Token（基于成功率、使用次数和负载均衡） |
| 📊 **独立统计** | 使用记录独立追踪，不影响普通用户的统计数据 |
| 🔒 **管理员专属** | 只能由管理员通过后台创建，普通用户无法自行创建 |
| 🔑 **特殊格式** | 生成 `sk-super-xxx` 格式的 API Key，便于识别 |

### 📊 对比表格

| 特性 | 普通 API Key | 超级 API Key |
|------|-------------|-------------|
| Token 访问范围 | 仅自己的 Token | 所有公开 Token |
| 创建权限 | 用户自己创建 | 仅管理员创建 |
| Key 格式 | `sk-xxx` | `sk-super-xxx` |
| 使用限制 | 受自己 Token 数量限制 | 受公开 Token 池限制 |
| 适用场景 | 个人使用 | 团队共享、公共服务 |

---

## 快速开始

### 前置条件

1. ✅ KiroGate 服务已启动
2. ✅ 已有管理员账号
3. ✅ 至少有一个用户添加了公开 Token

### 3 步创建超级 API Key

```bash
# 步骤 1: 访问管理后台
浏览器打开: http://127.0.0.1:9000/admin
登录密码: admin123

# 步骤 2: 进入用户管理
点击顶部 "👥 用户" 标签页

# 步骤 3: 创建超级 Key
点击用户操作列的 "🔑超级Key" 按钮
```

---

## 详细使用步骤

### 步骤 1: 登录管理后台

1. 浏览器访问管理后台：
   ```
   http://127.0.0.1:9000/admin
   ```

2. 输入管理员密码：
   ```
   admin123  # 默认密码，建议修改
   ```

3. 成功登录后，你会看到管理后台首页

### 步骤 2: 进入用户管理

1. 点击顶部导航栏的 **"👥 用户"** 标签页

2. 你会看到所有注册用户的列表，包含以下信息：
   - ID
   - 用户名
   - 信任等级
   - Token 数量
   - API Key 数量
   - 状态（正常/已封禁）
   - 注册时间
   - 操作按钮

### 步骤 3: 创建超级 API Key

1. **找到目标用户**
   - 在用户列表中找到要创建超级 Key 的用户
   - 可以使用搜索框快速查找

2. **点击创建按钮**
   - 在用户操作列，点击 **"🔑超级Key"** 按钮（紫色）

3. **输入 Key 名称**
   - 弹出对话框，提示输入 Key 名称
   - 默认名称：`超级密钥`
   - 可以自定义，例如：`团队共享Key`、`测试专用Key` 等
   - 点击"确定"继续，或"取消"放弃

4. **查看生成的密钥**
   - 创建成功后，会弹出精美的密钥展示窗口
   - 窗口显示完整的密钥信息和使用说明
   - **重要**：密钥只显示一次，请立即保存！

5. **复制密钥**
   - 方式一：点击 **"📋 复制密钥"** 按钮，自动复制到剪贴板
   - 方式二：点击文本框，按 `Ctrl+A` 全选，然后 `Ctrl+C` 复制

6. **保存密钥**
   - 将密钥保存到安全的地方（密码管理器、加密文件等）
   - 点击"关闭"按钮关闭窗口

### 步骤 4: 使用超级 API Key

创建成功后，就可以像使用普通 API Key 一样使用超级 API Key 了！

---

## 功能特性

### 🎯 智能 Token 分配

超级 API Key 会根据配置的分配策略自动选择最佳 Token：

#### 1. **score_based（评分优先）** - 默认
```bash
# 在 .env 中配置
TOKEN_ALLOCATION_STRATEGY="score_based"
```
- 综合考虑成功率（70%）、新鲜度（15%）、负载均衡（15%）
- 适合生产环境，追求稳定性

#### 2. **round_robin（轮询分配）**
```bash
TOKEN_ALLOCATION_STRATEGY="round_robin"
```
- 循环使用所有 Token，均匀分配请求
- 适合高并发场景，最大化并发能力

#### 3. **sequential（顺序使用）**
```bash
TOKEN_ALLOCATION_STRATEGY="sequential"
```
- 按顺序使用，用完一个再用下一个
- 适合保守策略，保护备用账号

### 📊 独立统计追踪

超级 API Key 的使用会被独立追踪：

- ✅ 请求次数统计
- ✅ 成功率统计
- ✅ 最后使用时间
- ✅ 使用的 Token ID 记录

在管理后台可以查看详细的使用情况。

### 🔒 安全机制

1. **权限控制**
   - 只有管理员可以创建
   - 需要管理员 Session 验证
   - 支持 CSRF 保护

2. **密钥安全**
   - 密钥只显示一次
   - 使用 bcrypt 加密存储
   - 支持随时禁用/删除

3. **使用限制**
   - 依赖公开 Token 池的可用性
   - 如果没有可用的公开 Token，会返回 503 错误

---

## 使用示例

### 示例 1: OpenAI SDK (Python)

```python
from openai import OpenAI

# 使用超级 API Key
client = OpenAI(
    base_url="http://localhost:9000/v1",
    api_key="sk-super-abc123def456..."  # 你的超级 API Key
)

# 发送请求
response = client.chat.completions.create(
    model="claude-sonnet-4-5",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好！"}
    ]
)

print(response.choices[0].message.content)
```

### 示例 2: Anthropic SDK (Python)

```python
from anthropic import Anthropic

# 使用超级 API Key
client = Anthropic(
    base_url="http://localhost:9000",
    api_key="sk-super-abc123def456..."  # 你的超级 API Key
)

# 发送请求
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "你好，Claude！"}
    ]
)

print(message.content[0].text)
```

### 示例 3: curl 命令

```bash
# OpenAI 格式
curl http://localhost:9000/v1/chat/completions \
  -H "Authorization: Bearer sk-super-abc123def456..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'

# Anthropic 格式
curl http://localhost:9000/v1/messages \
  -H "x-api-key: sk-super-abc123def456..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "你好，Claude！"}
    ]
  }'
```

### 示例 4: Claude Code CLI

```bash
# 设置环境变量
export ANTHROPIC_BASE_URL="http://localhost:9000"
export ANTHROPIC_API_KEY="sk-super-abc123def456..."

# 使用 Claude Code
claude "帮我写一个 Python 函数"
```

### 示例 5: Node.js (OpenAI SDK)

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:9000/v1',
  apiKey: 'sk-super-abc123def456...'  // 你的超级 API Key
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'claude-sonnet-4-5',
    messages: [
      { role: 'user', content: '你好！' }
    ]
  });

  console.log(response.choices[0].message.content);
}

main();
```

---

## 常见问题

### Q1: 超级 API Key 和普通 API Key 有什么区别？

**A:** 主要区别在于 Token 访问范围：

| 特性 | 普通 API Key | 超级 API Key |
|------|-------------|-------------|
| Token 来源 | 仅自己添加的 Token | 所有用户的公开 Token |
| 创建权限 | 用户自己创建 | 仅管理员创建 |
| 使用限制 | 受自己 Token 数量限制 | 受公开 Token 池限制 |

### Q2: 如果没有公开 Token 会怎样？

**A:** 超级 API Key 会返回 `503 Service Unavailable` 错误：

```json
{
  "detail": "暂无可用的公共 Token"
}
```

**解决方法**：
1. 用户登录后添加 Token
2. 在 Token 管理页面将 Token 设置为"公开"
3. 超级 API Key 即可使用

### Q3: 如何查看已创建的超级 API Key？

**A:** 有两种方式：

1. **用户中心查看**
   - 登录对应用户的账号
   - 进入"API Key 管理"页面
   - 超级 Key 会有特殊标识（`sk-super-` 前缀）

2. **管理后台查看**
   - 在用户管理页面
   - 查看用户的"API Key"列数量

### Q4: 可以撤销超级 API Key 吗？

**A:** 可以！有两种方式：

1. **禁用 Key**
   - 在用户的 API Key 管理页面
   - 点击"禁用"按钮
   - Key 立即失效，但可以重新启用

2. **删除 Key**
   - 在用户的 API Key 管理页面
   - 点击"删除"按钮
   - Key 永久删除，无法恢复

### Q5: 超级 API Key 的使用会影响普通用户吗？

**A:** 不会！超级 API Key 的使用统计是独立的：

- ✅ 独立的请求计数
- ✅ 独立的成功率统计
- ✅ 不影响 Token 所有者的统计数据

### Q6: 一个用户可以有多个超级 API Key 吗？

**A:** 可以！管理员可以为同一个用户创建多个超级 API Key，每个 Key 都是独立的。

### Q7: 超级 API Key 可以访问私有 Token 吗？

**A:** 不可以！超级 API Key 只能访问：
- ✅ 所有用户的**公开** Token
- ❌ 不能访问**私有** Token

### Q8: 如何监控超级 API Key 的使用情况？

**A:** 在管理后台可以查看：

1. **Token 池管理**
   - 查看公开 Token 的使用次数
   - 查看成功率和健康状态

2. **用户管理**
   - 查看用户的 API Key 使用统计
   - 查看请求次数和最后使用时间

3. **日志系统**
   - 服务日志会记录超级 API Key 的使用
   - 包括使用的 Token ID 和请求结果

---

## 安全建议

### 🔒 创建时的安全建议

1. **谨慎分配**
   - 只为可信用户创建超级 API Key
   - 评估用户的信任等级
   - 记录创建原因和用途

2. **命名规范**
   - 使用有意义的名称，便于管理
   - 例如：`团队共享-2024`、`测试环境专用`
   - 避免使用敏感信息作为名称

3. **立即保存**
   - 密钥只显示一次，必须立即保存
   - 使用密码管理器或加密存储
   - 不要通过不安全的渠道传输

### 🛡️ 使用时的安全建议

1. **环境变量**
   ```bash
   # 推荐：使用环境变量
   export ANTHROPIC_API_KEY="sk-super-xxx"

   # 不推荐：硬编码在代码中
   api_key = "sk-super-xxx"  # ❌ 不安全
   ```

2. **权限最小化**
   - 只在需要访问公开 Token 池时使用超级 Key
   - 个人使用场景优先使用普通 API Key

3. **定期轮换**
   - 定期创建新的超级 API Key
   - 禁用或删除旧的 Key
   - 建议每 3-6 个月轮换一次

### 📊 监控和审计

1. **定期检查**
   - 每周检查超级 API Key 的使用情况
   - 关注异常的请求模式
   - 监控成功率和错误率

2. **日志审计**
   - 定期查看服务日志
   - 关注超级 API Key 的使用记录
   - 发现异常立即调查

3. **及时响应**
   - 发现泄露立即禁用 Key
   - 通知相关用户
   - 创建新的 Key 替换

### 🚨 应急响应

如果怀疑超级 API Key 泄露：

1. **立即禁用**
   ```bash
   # 在管理后台禁用 Key
   用户管理 → API Key 管理 → 禁用
   ```

2. **创建新 Key**
   - 为用户创建新的超级 API Key
   - 通知用户更新配置

3. **调查原因**
   - 检查日志，确定泄露来源
   - 评估影响范围
   - 采取预防措施

---

## 使用场景

### 场景 1: 团队共享

**需求**：团队成员需要共享使用 Claude API

**解决方案**：
1. 管理员为团队负责人创建超级 API Key
2. 团队成员使用同一个 Key
3. 自动负载均衡到所有公开 Token

**优势**：
- ✅ 统一管理，方便控制
- ✅ 自动负载均衡，提高并发能力
- ✅ 独立统计，便于追踪使用情况

### 场景 2: 测试和开发

**需求**：开发人员需要测试 API 集成

**解决方案**：
1. 管理员创建测试专用的超级 API Key
2. 开发人员使用该 Key 进行测试
3. 无需配置自己的 Token

**优势**：
- ✅ 快速开始，无需配置
- ✅ 隔离测试环境
- ✅ 便于管理和撤销

### 场景 3: 公共服务

**需求**：提供公共 API 服务，供用户免费使用

**解决方案**：
1. 管理员创建公共服务专用的超级 API Key
2. 在网站上提供该 Key 供用户使用
3. 自动使用 Token 池中的资源

**优势**：
- ✅ 资源共享，降低成本
- ✅ 自动负载均衡
- ✅ 便于监控和限流

### 场景 4: 高并发场景

**需求**：应用需要处理大量并发请求

**解决方案**：
1. 配置 Token 分配策略为 `round_robin`
2. 使用超级 API Key 访问所有公开 Token
3. 请求自动分散到多个 Token

**优势**：
- ✅ 最大化并发能力
- ✅ 避免单个 Token 限流
- ✅ 提高系统稳定性

---

## 技术细节

### 工作原理

```
┌─────────────┐
│  客户端请求  │
└──────┬──────┘
       │ 使用超级 API Key
       ▼
┌─────────────────┐
│  KiroGate 网关  │
│                 │
│  1. 验证 Key    │
│  2. 识别为超级  │
│  3. 选择 Token  │
└──────┬──────────┘
       │
       ▼
┌─────────────────────────┐
│    公开 Token 池         │
│                         │
│  Token 1 (用户A公开)    │
│  Token 2 (用户B公开)    │
│  Token 3 (用户C公开)    │
└──────┬──────────────────┘
       │ 根据策略选择最佳 Token
       ▼
┌─────────────┐
│  Kiro API   │
└─────────────┘
```

### 数据库结构

```sql
-- API Key 表
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    key_hash TEXT NOT NULL,
    key_encrypted TEXT NOT NULL,
    key_prefix TEXT NOT NULL,
    name TEXT,
    is_active INTEGER DEFAULT 1,
    is_super INTEGER DEFAULT 0,  -- 超级 API Key 标记
    request_count INTEGER DEFAULT 0,
    last_used INTEGER,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### API 端点

```bash
# 创建超级 API Key
POST /admin/api/super-api-keys
Content-Type: multipart/form-data

user_id: 1
name: "超级密钥"

# 响应
{
  "success": true,
  "key": "sk-super-abc123def456...",
  "key_prefix": "sk-super-abc1",
  "id": 5,
  "user_id": 1,
  "is_super": true
}
```

---

## 更新日志

### v2.1.0 (2026-01-28)

- ✅ 添加前端创建超级 API Key 功能
- ✅ 优化密钥展示界面
- ✅ 添加一键复制功能
- ✅ 完善安全提示

### v2.0.0 (2025-12-XX)

- ✅ 初始实现超级 API Key 功能
- ✅ 支持访问所有公开 Token
- ✅ 智能 Token 分配策略
- ✅ 独立使用统计

---

## 相关文档

- [KiroGate 主文档](README.md)
- [用户系统文档](docs/user-system.md)
- [Token 管理文档](docs/token-management.md)
- [API 文档](http://127.0.0.1:9000/docs)

---

## 支持和反馈

如果你在使用超级 API Key 功能时遇到问题：

1. 查看本文档的"常见问题"部分
2. 检查服务日志：`/tmp/claude/-mine-Code-ai-tools-KiroGate/tasks/*.output`
3. 提交 Issue：[GitHub Issues](https://github.com/your-repo/issues)

---

**祝你使用愉快！🎉**
