# Discord Weekly Reminder

每週三晚上 22:00 (台灣時間) 自動在 Discord 頻道發送提醒訊息，並自動加上 ✅ Reaction。

## 專案結構

```
.
├── .github/workflows/discord-reminder.yml   # GitHub Actions 排程設定
├── src/main.py                                # Discord Bot 主程式
├── requirements.txt                           # Python 依賴
├── .gitignore                                 # Git 忽略規則
└── README.md                                  # 本文件
```

## 建立 Discord Bot

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 點擊 **New Application**，輸入名稱後建立
3. 左側選單點擊 **Bot**
4. 點擊 **Reset Token**（或 View Token）取得 Bot Token
5. 開啟以下 Privileged Gateway Intents（在 Bot 頁面下方）：
   - **Message Content Intent**

## 邀請 Bot 進伺服器

1. 左側選單點擊 **OAuth2 > URL Generator**
2. 勾選 **bot** (Scopes)
3. 在 Bot Permissions 勾選以下權限：
   - `View Channels`
   - `Send Messages`
   - `Add Reactions`
   - `Read Message History`
4. 複製產生的 URL，在瀏覽器中開啟
5. 選取目標伺服器，點擊 **授權**

## 取得頻道 ID

1. 在 Discord 中開啟 **使用者設定 > 進階**
2. 開啟 **開發者模式**
3. 在目標頻道上按右鍵 > **複製頻道 ID**

## GitHub Secrets 設定

在 GitHub Repository 中前往 **Settings > Secrets and variables > Actions**

新增以下 Repository Secrets：

| Secret Name | 說明 |
|---|---|
| `DISCORD_TOKEN` | Discord Bot 的 Token |
| `DISCORD_CHANNEL_ID` | 要發送訊息的頻道 ID |

## GitHub Actions 自動排程

Workflow 位於 `.github/workflows/discord-reminder.yml`

- **自動觸發**：每週三 UTC 14:00（台灣時間 22:00）
- **手動觸發**：在 GitHub Actions 頁面點擊 **Run workflow**

## 手動測試

設定環境變數後直接執行：

```bash
export DISCORD_TOKEN=你的BotToken
export DISCORD_CHANNEL_ID=你的頻道ID
python src/main.py
```
