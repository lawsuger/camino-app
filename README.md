# 朝聖之路 · 法國之路規劃手冊（Camino Francés）

為自媒體朝聖之旅打造的單頁 Web App，**電腦／手機通用、可加到主畫面當離線 App**。整合裝備、品牌、逐日路線、庇護所、拍照座標、宗教儀式與在地美食。

## 功能

| 分頁 | 內容 |
|---|---|
| 🏠 總覽 | 四大區順序、最辛苦 5 段、最後 100km 規定、第一天翻山兩條路線比較、App 清單 |
| 🎒 裝備清單 | 9 大類可勾選清單，自動存進度（localStorage）、即時估算背包總重、體重 10% 目標線、只看必備／列印 PDF |
| 🏷️ 品牌推薦 | 11 類裝備品牌與型號比較表（背包、鞋、襪、雨披、保暖、底層、睡袋、登山杖、頭燈、足部護理、小物）＋ 10 款手機 App |
| 🥾 路線庇護所 | SJPP→Santiago 35 天 ＋ 世界盡頭 5 天，逐段距離/難度/注意事項，每站 2–3 間庇護所，可依難度篩選 |
| 📸 打卡地圖 | 11 個必拍點，附 GPS 座標、一鍵開 Google Maps、複製座標，標註最佳拍攝時間 |
| ⛪ 儀式聖餐 | 朝聖者彌撒時間、Botafumeiro 大香爐擺盪日、朝聖證書規則、非天主教徒領聖體禮儀 |
| 🍷 美食人文 | 四大區代表美食、必吃店家、朝聖者套餐 Menú del Peregrino |

## 使用方式

### 直接看（最快）
用瀏覽器開 `index.html` 即可，所有資料離線內建，勾選進度會記在瀏覽器。

### 當手機 App 用（推薦帶著走）
需用 http(s) 開啟才能安裝為 PWA／離線快取：

```powershell
# 在本資料夾起一個本機伺服器（任選其一）
python -m http.server 8080
# 或 npx serve .
```

開 `http://localhost:8080`，瀏覽器選單 →「加到主畫面 / 安裝應用程式」。
要在手機上裝，把整個資料夾部署到 Zeabur / Cloudflare Pages / GitHub Pages（純靜態，無需後端），用手機開網址後加到主畫面，即可離線使用。

## 檔案結構

```
camino-app/
├── index.html      # 主程式（HTML + CSS + JS + 全部資料，單檔自足）
├── manifest.json   # PWA 設定
├── sw.js           # Service Worker（離線快取）
├── icon.svg        # 扇貝圖示
└── README.md
```

## 資料來源

整合自 buencaminoinfo、gotokm0、prosabrina、cherstravel 等中文實走遊記，以及 Gronze、CaminoWays、American Pilgrims 等英文權威站與官方禮儀頁。

> ⚠️ 庇護所價格與彌撒時間逐年微調，出發前請再次確認；公立庇護所多為先到先得、不可預訂。

---
Buen Camino！🐚
