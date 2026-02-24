param (
    [Alias("i")]
    [string]$Issue = "",
    [switch]$Strict
)

# ================== 1. 物理层对齐：编码修正 ==================
# 强制当前会话使用 UTF-8，防止中文和 Emoji 乱码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ================== 2. 基础配置 ==================
$Model = "deepseek-ai/DeepSeek-V3"
$ApiUrl = "https://api.siliconflow.cn/v1/chat/completions"

# ================== 3. 环境检查 ==================
$null = git rev-parse --is-inside-work-tree 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 当前目录不是 git 仓库" -ForegroundColor Red
    exit 1
}

$ApiKey = $env:SILICONFLOW_API_KEY
if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    Write-Host "❌ 未设置 SILICONFLOW_API_KEY 环境变量" -ForegroundColor Red
    exit 1
}

# 获取暂存区改动
$Diff = git diff --cached
if ([string]::IsNullOrWhiteSpace($Diff)) {
    Write-Host "⚠️ 没有 staged 的改动，请先执行 git add" -ForegroundColor Yellow
    exit 1
}

# ================== 4. 逻辑处理：提取 ERP ID ==================
$ErpId = $Issue
if ([string]::IsNullOrWhiteSpace($ErpId)) {
    $BranchName = git branch --show-current
    if ($BranchName -match "erp#(\d+)") {
        $ErpId = $matches[1]
    }
}

if ($Strict -and [string]::IsNullOrWhiteSpace($ErpId)) {
    Write-Host "❌ strict 模式下未找到 erp#ID" -ForegroundColor Red
    exit 1
}

$Prefix = if (-not [string]::IsNullOrWhiteSpace($ErpId)) { "erp#$ErpId " } else { "" }

# ================== 5. 提示词工程（基于结构化约束） ==================
# 这里利用了 # 标签加速 Encoder 对特征的提取，并强制 Softmax 排除解释性文字
$Prompt = @"
# ROLE: 资深后端工程师
# TASK: 根据 git diff 生成高质量的 Git 提交信息。
# CONSTRAINTS:
- 语言：中文
- 规范：符合 Conventional Commits (feat/fix/refactor/chore/docs/style/test)
- 强制要求：仅输出最终的 commit message 文本，严禁包含解释、分析或 Markdown 代码块。
- 前缀要求：如果提供前缀，必须将其置于最前方。

# INPUT DATA:
## PREFIX: 
$Prefix

## GIT DIFF:
$Diff
"@

Write-Host "🤖 AI 正在生成 commit message..." -ForegroundColor Cyan

# ================== 6. API 请求（高保真传输） ==================
$Headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Content-Type"  = "application/json; charset=utf-8"
}

$Body = @{
    model = $Model
    messages = @(
        @{ role = "user"; content = $Prompt }
    )
    stream = $false
    temperature = 0.3  # 降低随机性，使输出更符合规范
    top_p = 0.7
} | ConvertTo-Json -Depth 10

try {
    # 显式使用 UTF8 字节流发送，确保中文 Context 准确进入 AI 的 Embedding 层
    $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body))
    $Result = $Response.choices[0].message.content.Trim()
    
    # 二次过滤：防止 AI 仍然返回了 ```commit 这种 Markdown 格式
    $Result = $Result -replace '^```\w*\s*', '' -replace '\s*```$', ''
} catch {
    Write-Host "❌ 调用 API 失败: $_" -ForegroundColor Red
    exit 1
}

Write-Host "----------------------------------" -ForegroundColor DarkGray
Write-Host $Result -ForegroundColor Green
Write-Host "----------------------------------" -ForegroundColor DarkGray

if ([string]::IsNullOrWhiteSpace($Result)) {
    Write-Host "❌ AI 未生成有效的消息" -ForegroundColor Red
    exit 1
}

# ================== 7. 交互提交 ==================
$Confirm = Read-Host "💡 使用这个 commit message？ [Y/n]"
if ([string]::IsNullOrWhiteSpace($Confirm) -or $Confirm -match "^[Yy]$") {
    git commit -m "$Result"
    Write-Host "✅ Commit 完成" -ForegroundColor Green
} else {
    Write-Host "🚫 已取消 commit" -ForegroundColor Yellow
}