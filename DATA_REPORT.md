# Week 09 期中資料前處理報告

> **狀態：已完成真實資料測量。** 2026-11-04 以本機 `data/raw/` 內 9 份校規 PDF 完整執行 Notebook；原始 PDF、interim Markdown 與 processed JSON 依課程規定只留在本機，不上傳 GitHub。下列數據來自本次執行結果，不使用示範值。

## 1. 資料集概覽

本作業使用 `data/raw/<類別>/*.pdf` 分類掃描校規文件，透過 Docling 轉成 Markdown，再進行邊界修復與 chunk 切分。預期的資料夾包括 `data/raw/`、`data/interim/`、`data/processed/`。

| 資料項目 | 實測數據 | 證據或限制 |
|---|---|---|
| 各類別 PDF 數量 | Academic_Affairs 3、Library_Information 3、Student_Affairs 3 | 由 `data/raw/<類別>/*.pdf` 動態掃描 |
| PDF 總數 | 9 | Notebook 第 5 節：成功解析 9、錯誤 0 |
| 清洗前 chunk 數量 | 410 | 9 份 raw JSON 合計 |
| 清洗後 chunk 數量 | 345 | 9 份 cleaned JSON 合計 |
| Schema 驗證 | 755 筆通過 | 410 raw + 345 cleaned；文字與 metadata 欄位逐筆斷言 |

清洗後 chunk 數由 410 降為 345，符合雙語標題與條文合併後區塊數減少的預期；是否合併正確仍需搭配實際文字抽查判斷。

## 2. 清洗步驟（任務 1-A／1-B／1-C）

| 任務 | 規則與預期目的 | 已驗證情形 | 真實 PDF 前／後截圖 |
|---|---|---|---|
| 1-A 頁首頁尾溢出清除 | 從檔名動態擷取規章名稱，只移除完整符合規章名稱的孤立行 | Notebook 斷言 `[Success]`；已套用到 9 份真實 PDF | 尚未另存前／後截圖 |
| 1-B 雙語標題合併 | 合併相鄰中文／英文 `##` 標題，以 ` / ` 分隔；不得合併兩個中文標題 | Notebook 斷言 `[Success]`；cleaned JSON 標題可見 `中文 / English` | 尚未另存前／後截圖 |
| 1-C 雙語條文合併 | 將中文文字行與緊接的英文 `- ` 清單項合併，不誤併兩個中文條文 | Notebook 斷言 `[Success]`；raw／cleaned 總 chunk 數為 410／345 | 尚未另存前／後截圖 |

**證據界線：** 三個成功斷言只證明範例測試通過，不能證明對每份真實 PDF 的清洗都正確。

目前已保存四拼圖；三組前後對照截圖仍可在第 9 週正式報告時補入 `reports/figures/`。因此本報告只把斷言與真實批次結果列為現有證據，不把尚未建立的截圖寫成已完成。

## 3. 評估指標與 AI 解讀查證

`metrics.json` 位於專案根目錄，已由 9 份真實 PDF 的 755 筆 chunks 計算。

| 評估指標 | Raw | Cleaned | 說明 |
|---|---|---|---|
| Morphology Median Length（chunk 字元長度中位數） | 204.0 | 272.0 | 合併後 chunk 數下降且中位長度提高 |
| Topological Anchoring Ratio, TAR（標題錨定率） | 100.00% | 100.00% | raw 與 cleaned chunks 均以 `##` 標題起始 |
| Structural Depth Variance, SDV（標題深度變異量） | 0.00 | 0.00 | 本資料切塊標題層級皆為 `##`，因此沒有層級變異 |
| Shannon Median Entropy（chunk 文字資訊熵中位數） | 4.7149 | 5.0484 | cleaned 中位資訊熵較高 |

**四拼圖：** Notebook 第 6 節已實際產生四張圖：① chunk 長度箱型圖（對數刻度）；② TAR 長條圖；③ Markdown 標題深度分布比較；④ 資訊熵箱型圖。圖片保存在本機 `reports/figures/week08_dashboard.png`，同一張圖也已嵌入 notebook 輸出。

**AI 解讀查證：**

- 主張 1：清洗把相鄰雙語結構合併，因此 chunk 數會下降、典型 chunk 會變長。查證結果為 **成立**：raw／cleaned 數量為 410／345，中位長度為 204／272；同時 TAR 仍維持 100%，沒有因合併失去標題錨點。
- 主張 2：資訊熵中位數由 4.7149 提高至 5.0484，可解讀為典型 cleaned chunk 的字元資訊較豐富；但不能推論所有 chunk 都改善。查證時找到一個資訊熵僅 1.2101 的 14,350 字元表格 chunk，顯示整體中位數改善仍會掩蓋極端異常。

## 4. 清洗後仍未解決的一個問題

Notebook 第 6.1 節顯示，最長 chunk 與資訊熵最低 chunk 是同一筆真實資料：

| 查證欄位 | 實測結果 |
|---|---|
| 來源檔案／類別 | `Library_Information/A271010023_圖書館管理作業規範.pdf` |
| 問題 chunk 原文與標題 | `## Attachment 5 / Comparison Table of Unit Recommendation Points in Database`；14,350 字元，資訊熵 1.2101 |
| 錯誤特徵及原因 | 大型比較表被合併成單一 chunk；大量重複欄位文字造成超長且低熵，會稀釋主題並增加檢索雜訊 |
| 修正方法 | 對 Markdown 表格另設 table-aware 切分，依列群組或頁面分段，並增加最大字元門檻；每個子 chunk 保留附件標題與來源 metadata |
| 修正後再次驗證 | 尚未修改本週固定管線；第 9 週可重新執行後確認最大長度下降，並抽查表格列未遺失 |

## 5. AI 協作

完整紀錄請見 [AI_USAGE.md](AI_USAGE.md)。

**本週收穫：** 設計正規表示式時，必須同時列出正例與不能發生的反例；AI 的建議需要經過斷言及真實文件的人工查核，不能把示範成功視為批次處理全面成功。

### 實際繳交前檢查

- [x] 1-A／1-B／1-C 範例斷言及 Notebook 原始程式
- [x] 根目錄 `AI_USAGE.md`、`README.md`、`requirements.txt` 與 `.gitignore`
- [x] 根目錄 `metrics.json` 已由真實資料產生
- [x] 根據 9 份真實 PDF 計算並取代 `metrics.json` 的待測量架構
- [x] 在 Notebook 內保存真正的四拼圖輸出，並保存圖片至 `reports/figures/`
- [ ] 每項清洗的前後對照截圖（3 組）
- [x] 查證 AI 對圖表所做的兩項解讀
- [x] 紀錄一個來源可核對的問題 chunk
- [ ] 依第 9 週正式提供的報告範本檢查調整
- [ ] 建立課程規定的 Git Tag / Release `v0.5-midterm`

