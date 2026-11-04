# NLP 自然語言處理 (115 S1) - 課程專案

本專案為 NLP 課程開發環境與實作練習區。

---

## 開發者資訊 (Developer Info)
* **學號**：[U12627020]
* **姓名**：[張峻毓]

## 硬體與環境狀態 (Environment Setup)
* **PyTorch 執行環境**：[ Windows CPU]

---

## 課程任務清單 (Task Checklist)

### Week 2：開發環境與專案架構初始化
請在完成下列任務後，將 `[ ]` 改為 `[x]`：
- [X] 成功建立 GitHub 帳號並 Clone 本專案至本機端。
- [X] 成功建立 `.venv` 虛擬環境，並透過 `.gitignore` 隱藏底層檔案。
- [X] 成功於虛擬環境內安裝通用套件清單 (`requirements.txt`) 與專屬硬體版本的 PyTorch。
- [X] 更新本 README 文件，填寫學號、姓名與 PyTorch 環境狀態。
- [X] 成功使用 Git 完成 `commit` 並 `push` 同步至 GitHub 雲端。

---

本專案以 Docling 解析 PDF，將校規轉換為 Markdown，再使用 Regex 清理、切塊並輸出 JSON。

## Week 4 / 8: Data Ingestion & Topology-Aware Chunking
- [x] **環境建置與版控防護**：已設定 `.gitignore` 和 `.keep`。
- [x] **資料擷取與合併**：已完成 1-A / 1-B / 1-C 正則與範例斷言。
  - [x] 1-A
  - [x] 1-B
  - [x] 1-C
- [ ] **結構健全度**：待原始 PDF 到位後計算 TAR、中位數長度。
- [ ] **語意品質（選修）**：待真實 PDF 後計算熵。
- [ ] **觀測儀表板與報告**：待真實 PDF 後產生 4 拼圖及 `metrics.json`。

## 執行方式
1. 在專案資料夾安裝：`pip install -r requirements.txt`。
2. 放置原始 PDF 至 `data/raw/Academic_Affairs/` 等類別子資料夾。
3. 用 VS Code / Jupyter 開啟 `notebooks/01_Data_Ingestion.ipynb` 從頭執行並儲存，保留 3 項斷言輸出與 4 拼圖儀表板。
4. 執行時檔案撞名會詢問 `O` 覆蓋、`A` 追加或 `S` 略過；若無法輸入則安全略過。
5. 根目錄自動產出 `metrics.json`，並將數據填入 `DATA_REPORT.md`（第 9 週課堂報告）。

注意：此交付包不包含課程原始校規 PDF，因此目前不包含真實儀表板及指標數值。請勿以模擬值作為測量結果。

## GitHub 提交
`git add .` → `git commit -m "feat: 完成 Week 08 資料前處理 (任務 1-A, 1-B, 1-C)"` → `git push`。
請確認 GitHub 上**沒有**原始 PDF、大量 interim Markdown 或 processed JSON。
