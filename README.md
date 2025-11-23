**项目概述**
- **用途**：该仓库包含用于自动化登录哈尔滨工业大学教务系统（jwts.hit.edu.cn）的脚本原型与调试页面，目标是通过浏览器（Selenium + Chrome）模拟登录并在需要时进行后续自动化操作。
- **注意**：教务系统使用 CAS 单点登录及客户端加密/滑块验证码等防护机制。频繁并行登录会触发短时冻结（例如“累计并行会话数≥10”），请参照下文的建议减少封禁风险。

**仓库结构（重要文件）**
- `login.py` : 主登录脚本（当前版本）。
- `main.py` : 项目入口 / 测试用脚本（如果存在，按需查看）。
- `base_login_debug.html` : 抓取的登录页面快照（用于离线调试与定位字段）。
- `.env` : (未提交) 存放 `JW_USERNAME` 与 `JW_PASSWORD`。请务必将此文件加入 `.gitignore` 并不要把真实密码提交到版本库。

**快速上手**
1. 准备 Python 环境（建议使用你的 `myenv` conda 环境）：

```bash
# 激活 conda 环境（示例）
conda activate myenv

# 安装运行时依赖
pip install selenium webdriver-manager python-dotenv
```

2. 在仓库根目录创建 `.env` 文件（示例）：

```
JW_USERNAME=你的学号
JW_PASSWORD=你的密码
```
（注意：不要为变量值加引号）

3. 运行主脚本（可见浏览器，以便手动处理验证码）：

```bash
python login.py
```

**常见问题与调试建议**
- Chrome 与 ChromeDriver 版本不匹配会导致 Session/启动错误。可通过 `webdriver-manager` 自动下载与本机 Chrome 匹配的 driver，或显式安装与你 Chrome 版本相配的 chromedriver。
- 如果遇到 `ERR_CONNECTION_RESET` 或浏览器启动失败：
  - 检查本机是否有网络代理或 VPN 干扰。
  - 尝试在 ChromeOptions 中加入或去除 `--no-sandbox`、`--disable-dev-shm-usage`、`--remote-debugging-port=9222` 以排查启动参数问题。
- CAS 页面使用客户端密码加密（js），若脚本只填入可见密码文本而不触发页面的加密逻辑，服务端可能拒绝登录。当前脚本尝试执行页面 JS 或提交表单以匹配真实页面行为。
- 若出现滑块验证码（Geetest / NC 等）：自动化破解不总是稳定，建议在首次登录时手动完成验证码并保存会话（见下面的“会话复用”）。

**会话复用（避免频繁登录） — 推荐做法**
- 原理：复用浏览器 profile 或保存/加载 cookies，可以避免每次都走登录流程，从而降低触发并行会话限制的概率。
- 两种常见方法：
  - **Chrome profile**：在 `ChromeOptions` 中加 `--user-data-dir=/path/to/profile`，首次手动登录后后续自动化会复用该已登录会话。
  - **Cookies**：登录后用 `driver.get_cookies()` 保存到 `cookies.json`，后续打开页面后注入这些 cookies 并刷新页面以恢复会话。
- 我可以按需为你添加 `session_save.py` / `session_use.py` 示例脚本（若你希望保持仓库不改变你的现有脚本，请告诉我，我会另建文件）。

**并行登录策略（如果你确实需要多次登录）**
- 服务端通常限制并行会话或并发 IP，直接大量并行会话会被短时冻结。可行策略：
  - 序列化登录（逐一登录，间隔随机短延迟）。
  - 受限并发（用线程池并将并发数限制在安全上限，如 `<=5`）。
  - 使用不同 IP（代理池）时依旧需小心：服务端可能同时计数会话与 IP。
  - 永远实现冻结检测并指数回退（避免循环立即重试）。

**安全与合规性提醒**
- 请确保你的自动化行为符合学校/服务的使用条款。绕过验证码或大量并发登录可能违反相关规定并带来账号风险。
- 保管好 `.env`、`cookies.json` 等敏感文件，不要将敏感数据提交到仓库。

**我可以为你做的下一步**
- 帮你在仓库中添加会话保存/复用脚本（`session_save.py` / `session_use.py`），并示范在 `myenv` 下如何运行。不会修改 `login.py` 本身，除非你明确允许。
- 如果你需要并发执行多次动作，我可以实现一个受限并发的 `login_manager.py`（内含冻结检测、回退与可配置的并发上限）。

如果你希望我现在把 `session_save.py` 和 `session_use.py` 加入仓库并示范一次登录并保存 cookies，请回复“请添加并示范”。如果你希望其它帮助（例如：将 `login.py` 改为支持 `--use-profile` 标志），也请告诉我具体偏好。