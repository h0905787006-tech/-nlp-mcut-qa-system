# Week 09 期中資料前處理報告

> **狀態：已完成真實資料測量。** 2026-11-04 以本機 `data/raw/` 內 9 份校規 PDF 完整執行 Notebook；2026-11-06 以學號 `U12627020` 與 SEED `1106` 執行 `09_midterm_chunks.ipynb`。原始 PDF、interim Markdown 與 processed JSON 依課程規定只留在本機，不上傳 GitHub。下列數據來自本次執行結果，不使用示範值。

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
| 1-A 頁首頁尾溢出清除 | 從檔名動態擷取規章名稱，只移除完整符合規章名稱的孤立行 | Notebook 斷言 `[Success]`；raw 第 373 行的頁首溢出在 cleaned 版本中已移除 | [1-A 前／後對照](reports/figures/1A_before_after.png) |
| 1-B 雙語標題合併 | 合併相鄰中文／英文 `##` 標題，以 ` / ` 分隔；不得合併兩個中文標題 | Notebook 斷言 `[Success]`；cleaned JSON 標題可見 `中文 / English` | [1-B 前／後對照](reports/figures/1B_before_after.png) |
| 1-C 雙語條文合併 | 將中文文字行與緊接的英文 `- ` 清單項合併，不誤併兩個中文條文 | Notebook 斷言 `[Success]`；raw／cleaned 總 chunk 數為 410／345 | [1-C 前／後對照](reports/figures/1C_before_after.png) |

**證據界線：** 三個成功斷言只證明範例測試通過，不能證明對每份真實 PDF 的清洗都正確。

四拼圖與三組真實前後對照截圖皆已保存於 `reports/figures/`。1-A 截圖經人工核對後使用 `A232020018_大學部學則` raw 第 373 行的實際頁首溢出，而非同檔案較前方的同名標題。

## 3. 評估指標與 AI 解讀查證

`metrics.json` 位於專案根目錄，已由 9 份真實 PDF 的 755 筆 chunks 計算。

| 評估指標 | Raw | Cleaned | 說明 |
|---|---|---|---|
| Morphology Median Length（chunk 字元長度中位數） | 204.0 | 272.0 | 合併後 chunk 數下降且中位長度提高 |
| Topological Anchoring Ratio, TAR（標題錨定率） | 100.00% | 100.00% | raw 與 cleaned chunks 均以 `##` 標題起始 |
| Structural Depth Variance, SDV（標題深度變異量） | 0.00 | 0.00 | 本資料切塊標題層級皆為 `##`，因此沒有層級變異 |
| Shannon Median Entropy（chunk 文字資訊熵中位數） | 4.7149 | 5.0484 | cleaned 中位資訊熵較高 |

**四拼圖：** Notebook 第 6 節已實際產生四張圖：① chunk 長度箱型圖（對數刻度）；② TAR 長條圖；③ Markdown 標題深度分布比較；④ 資訊熵箱型圖。圖片已保存為 [week08_dashboard.png](reports/figures/week08_dashboard.png)，同一張圖也已嵌入 Notebook 輸出。

**AI 解讀查證：**

- 主張 1：清洗把相鄰雙語結構合併，因此 chunk 數會下降、典型 chunk 會變長。查證結果為 **成立**：raw／cleaned 數量為 410／345，中位長度為 204／272；同時 TAR 仍維持 100%，沒有因合併失去標題錨點。
- 主張 2：資訊熵中位數由 4.7149 提高至 5.0484，可解讀為典型 cleaned chunk 的字元資訊較豐富；但不能推論所有 chunk 都改善。查證時找到指定的學分抵免申請表 chunk，長 4,367 字元、資訊熵僅 3.06，顯示整體中位數改善仍會掩蓋表單異常。

**個人指定 chunks（報告 3.4）：**

- 很長的 chunk：`cleaned_A232020018_大學部學則.md` 第 501 行，JSON 第 10 個物件（position 9），7,304 字元、資訊熵 5.46、最長候選第 11 名，驗證碼 **`b5e1784a`**。內容涵蓋第四十三條至第五十二條；因現行程式只用 `\n(?=##\s)` 切分，章內條文沒有再分段，造成請假、休學、復學、退學等多個主題集中於同一 chunk。建議辨識 `第…條`／`Article n` 的雙語配對，並繼承章節標題作為 metadata。
- 低資訊熵 chunk：`cleaned_A232060013_學生抵免學分辦法.md` 第 277 行，JSON 第 26 個物件（position 25），4,367 字元、資訊熵 3.06、低熵候選第 18 名，驗證碼 **`f2c4c2f8`**。內容為學分抵免申請表；`□准予抵免` 出現 8 次、`核簽流程` 出現 10 次，大量空白欄位與重複模板拉低資訊熵。建議標記為 `content_type=form`，保留原始表格供稽核，另建立去除重複空白列的正規化版本。

## 4. 清洗後仍未解決的一個問題

`09_midterm_chunks.ipynb` 顯示，個人指定的低資訊熵 chunk 是一張仍被當作一般長文本處理的表單：

| 查證欄位 | 實測結果 |
|---|---|
| 來源檔案／類別 | `Academic_Affairs/A232060013_學生抵免學分辦法.pdf` |
| 問題 chunk 原文與標題 | 學分抵免申請書；4,367 字元，資訊熵 3.06，驗證碼 `f2c4c2f8` |
| 錯誤特徵及原因 | 大量空白儲存格、核取方塊、重複審查選項與核簽流程被合併成單一 chunk；重複模板稀釋真正的欄位語意 |
| 修正方法 | 辨識 `content_type=table/form`，保留原始 Markdown，另將欄位、審查選項與簽核角色正規化；依邏輯區段或 1,200–1,500 字元上限切分並繼承來源 metadata |
| 修正後再次驗證 | 尚未修改本週固定管線；後續應確認欄位未遺失、重複模板只保留一次、最大 chunk 明顯低於 4,367 字元，並以「抵免申請欄位」及「審查結果」進行人工檢索測試 |

## 5. AI 協作

完整紀錄請見 [AI_USAGE.md](AI_USAGE.md)。

**本週收穫：** 設計正規表示式時，必須同時列出正例與不能發生的反例；AI 的建議需要經過斷言及真實文件的人工查核，不能把示範成功視為批次處理全面成功。相同文字在文件中可能出現多次，因此截圖與 chunk 分析還要再用來源檔、行號及驗證碼核對。

### 實際繳交前檢查

- [x] 1-A／1-B／1-C 範例斷言及 Notebook 原始程式
- [x] 根目錄 `AI_USAGE.md`、`README.md`、`requirements.txt` 與 `.gitignore`
- [x] 根目錄 `metrics.json` 已由真實資料產生
- [x] 根據 9 份真實 PDF 計算並取代 `metrics.json` 的待測量架構
- [x] 在 Notebook 內保存真正的四拼圖輸出，並保存圖片至 `reports/figures/`
- [x] 每項清洗的前後對照截圖（3 組）
- [x] 查證 AI 對圖表所做的兩項解讀
- [x] 紀錄一個來源可核對的問題 chunk
- [x] 依第 9 週正式提供的報告規格檢查調整
- [x] 依第 9 週最新規則，不建立 Git Tag／Release
