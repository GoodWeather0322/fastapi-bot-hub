# fastapi-bot-hub

## 預計新增

- [ ] 新增 LINE 機器人
- [ ] 新增 Email 機器人
- [ ] 新增 Discord 機器人

## 專案介紹

`fastapi-bot-hub` 是一個基於 FastAPI 的聊天機器人集線器，旨在整合多個聊天平台的機器人功能。目前支持的聊天平台包括 LINE 和 Telegram。該專案的架構設計使得未來可以輕鬆擴展以支持更多平台。

## 專案結構

```
fastapi-bot-hub/
│
├── app/
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── line_adapter.py
│   │   └── telegram_adapter.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── common_models.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── line_router.py
│   │   │   └── telegram_router.py
│   │   └── router.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── business_logic.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── helpers.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

- `app/adapters/`: 包含不同平台的適配器，用於將平台特定的訊息/指令轉換為統一的格式做後續處理。
  - `line_adapter.py`: LINE 平台的適配器。
  - `telegram_adapter.py`: Telegram 平台的適配器。

- `app/models/`: 定義了統一的數據模型。
  - `common_models.py`: 包含 `UnifiedInput` 和 `UnifiedOutput` 模型。

- `app/routers/`: 定義了各個平台的路由。
  - `endpoints/`: 包含各平台的具體路由實現。
    - `line_router.py`: LINE 平台的路由。
    - `telegram_router.py`: Telegram 平台的路由。
  - `router.py`: 主路由文件，註冊所有平台的路由。

- `app/services/`: 包含業務邏輯的實現。
  - `business_logic.py`: 處理統一格式的輸入數據，並返回統一格式的輸出數據。

- `app/utils/`: 包含配置和輔助工具。
  - `config.py`: 配置文件，使用 Pydantic 來管理環境變量。

- `app/main.py`: FastAPI 應用的入口文件，配置中間件和路由。

## 安裝與運行

1. 安裝依賴：

   ```bash
   pip install -r requirements.txt
   ```

2. 運行應用：

   ```bash
   uvicorn app.main:app --reload
   ```