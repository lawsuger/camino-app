# 朝聖之路 · 法國之路規劃手冊（Camino Francés）

為自媒體朝聖之旅打造的單頁 Web App，**電腦／手機通用、可加到主畫面當離線 App**。整合裝備、品牌、逐日路線、庇護所、拍照座標、宗教儀式與在地美食。

## 功能

| 分頁 | 內容 |
|---|---|
| 📅 我的 40 天 | **實際拍板行程（2026/6/18–7/27）**：逐日路段／靈修主題／拍攝重點／住宿／交通，出發後自動跳「今天」並置頂高亮；內含「訂房／車票作戰板」（可勾選＋填訂單編號，倒數期預設展開）|
| 🏠 總覽 | 四大區順序、最辛苦 5 段、最後 100km 規定、第一天翻山兩條路線比較、App 清單 |
| 🎒 裝備清單 | 9 大類可勾選清單，自動存進度（localStorage）、即時估算背包總重、體重 10% 目標線、只看必備／列印 PDF |
| 🏷️ 品牌推薦 | 11 類裝備品牌與型號比較表（背包、鞋、襪、雨披、保暖、底層、睡袋、登山杖、頭燈、足部護理、小物）＋ 10 款手機 App |
| 🥾 路線庇護所 | SJPP→Santiago 35 天 ＋ 世界盡頭 5 天，逐段距離/難度/注意事項，每站 2–3 間庇護所，可依難度篩選；**每段標示實走日期或跳接略過**（對照我的 40 天），並有「✅ 我們的預訂」自填欄（最終住所＋訂房代碼，localStorage，填了在標題列亮綠色已訂徽章） |
| 📸 打卡地圖 | **33 個必拍點**（含奔牛節、火之夜、大香爐、波多、環法巴黎），照行程時間排序＋⭐1–3 星推薦＋對應日期；可「標記已拍」記進度、依星級/未拍篩選；座標確定者給 GPS＋複製座標，其餘用地名開 Google Maps（不亂給座標） |
| ⛪ 儀式聖餐 | 朝聖者彌撒時間、Botafumeiro 大香爐擺盪日、朝聖證書規則、非天主教徒領聖體禮儀 |
| 🍷 美食人文 | 四大區代表美食、必吃店家、朝聖者套餐 Menú del Peregrino |
| 🆘 SOS·西語 | 緊急電話一鍵撥打（112＋駐西／法／葡代表處急難專線，2026-06-11 查證自外交部官網）、自填緊急資料卡（僅存 localStorage）、救命＋常用西語 29 句 |
| 💶 記帳 | € 快速記帳：分類加總、日均、台幣換算（匯率可調）、一鍵複製 CSV 當出書附錄 |

另有 header「🙏 靈修／📔 日誌／🌐 總站」三站互連，串起 camino-prayer 與 camino-2026 生態系。旅途期間（6/18–7/27）App 一律開在「我的 40 天」。

### 資料匯出（給 camino-2026 等外站整合）

`data/myplan-camino40.json` ＝ 我的 40 天行程＋7 區塊＋33 打卡點的機器可讀版，部署後可直接跨站 fetch（GitHub Pages 已開 CORS）：

```
https://lawsuger.github.io/camino-app/data/myplan-camino40.json
```

唯一事實來源是 `index.html` 內的 `MYPLAN / PBLOCKS / SPOTS` 常數；改了行程後重跑匯出腳本再 push（腳本見 repo 歷史或請 Claude 重匯）。

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

分享卡（`qr/` 資料夾）：
- `qr-card-photo*`：底圖為 Alto del Perdón 寬恕之峰鐵雕朝聖者；`qr-card-mist*`：晨霧中的朝聖者；`qr-card-cruz*`：Cruz de Ferro 鐵十字日落。三者照片皆來自 [Unsplash](https://unsplash.com/)（免費授權 Unsplash License）。
- `qr-card-illust*`：程式繪製插畫（`make-qr.py`），版權自有。
- QR 皆指向本站、ECC-H 容錯、已用 zxing-cpp 解碼驗證可掃。

> ⚠️ 庇護所價格與彌撒時間逐年微調，出發前請再次確認；公立庇護所多為先到先得、不可預訂。

---
Buen Camino！🐚
