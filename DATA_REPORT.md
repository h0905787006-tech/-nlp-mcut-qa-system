# Week 09 期中資料前處理報告（資料待驗證版）

> **狀態：尚未完成實際 PDF 測量。** 本文件以 2026-11-04 可取得的課程 Notebook、`AI_USAGE.md`、繳交要求與 GitHub 檔案為依據。未取得原始校規 PDF、`data/interim` 清洗輸出或 `data/processed` chunk JSON。**不使用示範數值代替實測**；請勿將本版作為完整實證報告。

## 1. 資料集概覽

本作業使用 `data/raw/<類別>/*.pdf` 分類掃描校規文件，透過 Docling 轉成 Markdown，再進行邊界修復與 chunk 切分。預期的資料夾包括 `data/raw/`、`data/interim/`、`data/processed/`。

| 資料項目 | 已取得之可驗證數據 | 證據或限制 |
|---|---|---|
| 各類別 PDF 數量 | 待統計 | 未提供原始 PDF |
| PDF 總數 | 待統計 | 不能將「附件沒有 PDF」冒充「本地資料集有 0 份」 |
| 清洗前 chunk 數量 | 待統計 | 未產生原始 chunk JSON |
| 清洗後 chunk 數量 | 待統計 | 未產生清洗後 chunk JSON |
| 各類別分布 | 待統計 | 需實際 `data/raw` |

**待完成操作：** 放入原始 PDF 後，執行 `notebooks/01_Data_Ingestion.ipynb` 第 2、5 節；保留執行時印出的每類 PDF 與清洗前後 chunk 計數，再填入上表。

## 2. 清洗步驟（任務 1-A／1-B／1-C）

| 任務 | 規則與預期目的 | 已驗證情形 | 真實 PDF 前／後截圖 |
|---|---|---|---|
| 1-A 頁首頁尾溢出清除 | 從檔名動態擷取規章名稱，只移除完整符合規章名稱的孤立行 | Notebook 範例斷言 `[Success]` | **缺少，待擷取** |
| 1-B 雙語標題合併 | 合併相鄰中文／英文 `##` 標題，以 ` / ` 分隔；不得合併兩個中文標題 | Notebook 範例斷言 `[Success]` | **缺少，待擷取** |
| 1-C 雙語條文合併 | 將中文文字行與緊接的英文 `- ` 清單項合併，不誤併兩個中文條文 | Notebook 範例斷言 `[Success]` | **缺少，待擷取** |

**證據界線：** 三個成功斷言只證明範例測試通過，不能證明對每份真實 PDF 的清洗都正確。

截圖預計存放 `reports/figures/`，建議使用 `1A_before_after.png`、`1B_before_after.png`、`1C_before_after.png`。這些檔案目前未產生，不能引用為已完成證據。

## 3. 評估指標與 AI 解讀查證

`metrics.json` 位於專案根目錄；目前是**待計算結構標記**，其 `null` 表示沒有可用測量，不是零。

| 評估指標 | Raw | Cleaned | 說明 |
|---|---|---|---|
| Morphology Median Length（chunk 字元長度中位數） | 待計算 | 待計算 | 需真實 chunks |
| Topological Anchoring Ratio, TAR（標題錨定率） | 待計算 | 待計算 | 需真實 chunks |
| Structural Depth Variance, SDV（標題深度變異量） | 待計算 | 待計算 | 需真實 chunks |
| Shannon Median Entropy（chunk 文字資訊熵中位數） | 待計算 | 待計算 | 需真實 chunks |

**四拼圖：** Notebook 第 6 節已配置四張圖：① chunk 長度箱型圖（對數刻度）；② TAR 長條圖；③ Markdown 標題深度分布比較；④ 資訊熵箱型圖。已修改為僅在真的有 raw/clean chunks 時才產生 `reports/figures/week08_dashboard.png`。若沒有原始 PDF，會提示待處理，不輸出任何假圖。

**AI 解讀查證（必須在產生真實圖後填寫）：**

- 主張 1：**尚未提出**。待根據實際圖表寫出一個可檢驗的觀察，指出相應的來源檔案與 chunk，引用片段核對，不接受只憑圖形的推測。
- 主張 2：**尚未提出**。待檢查另一項指標，找出可核對的原始及清洗後 chunk，確認說法是否成立。

## 4. 清洗後仍未解決的一個問題

**目前無法指認真實的問題 chunk**，因為沒有可用的清洗後 JSON。這一節必須以自己的資料為證據，而不是編造異常紀錄。

取得資料後，執行 Notebook 第 6.1 節，查看最長 chunk 和資訊熵最低的 chunk，選取一個確實存在的異常；記錄其 `cluster`、`source_file`、標題、字元長度與原文片段，說明異常原因和可行修正方式。

| 查證欄位 | 待填 |
|---|---|
| 來源檔案／類別 | 待取得真實 chunk |
| 問題 chunk 原文與標題 | 待取得真實 chunk |
| 錯誤特徵及原因 | 待人工確認 |
| 修正方法 | 待人工確認 |
| 修正後再次驗證 | 待執行 |

## 5. AI 協作

完整紀錄請見 [AI_USAGE.md](AI_USAGE.md)。

**本週收穫：** 設計正規表示式時，必須同時列出正例與不能發生的反例；AI 的建議需要經過斷言及真實文件的人工查核，不能把示範成功視為批次處理全面成功。

### 實際繳交前檢查

- [x] 1-A／1-B／1-C 範例斷言及 Notebook 原始程式
- [x] 根目錄 `AI_USAGE.md`、`README.md`、`requirements.txt` 與 `.gitignore`
- [x] 根目錄 `metrics.json` 待測量架構，明確以 `null` 標註缺少數據
- [ ] 根據真實 PDF 計算並取代 `metrics.json` 的待測量架構
- [ ] 在 Notebook 內保存真正的四拼圖輸出，並保存圖片至 `reports/figures/`
- [ ] 每項清洗的前後對照截圖（3 組）
- [ ] 查證 AI 對圖表所做的兩項解讀
- [ ] 紀錄一個來源可核對的問題 chunk
- [ ] 依第 9 週正式提供的報告範本檢查調整
- [ ] 建立課程規定的 Git Tag / Release `v0.5-midterm`
