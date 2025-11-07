# 🐞Issue & Fix Report

## 📋 Overview

This document summarizes identified bugs and their fixes in the **BERT Sentiment Analysis and Recommendation Service**. All issues were resolved and verified through testing, ensuring stable model training, inference, and API operation.

---

## 🧩 Fixed Issues Summary

### Bug 1 — Incorrect Label Tensor Type
- File: `ml/data.py` (L46)
- Issue: Labels were cast to `torch.float`, causing CrossEntropyLoss to raise CUDA dtype errors during training.
- Fix:
```python
# ml/data.py
'label': torch.tensor(label, dtype=torch.long)
```
- Verification: Training completes without the "nll_loss_forward_reduce_cuda_kernel_2d_index" runtime error.

### Bug 2 — Typographical Errors in Asset Paths
- File: `app/main.py` (L49–L50)
- Issue: Asset paths used `"accets/"` instead of `"assets/"`, preventing model/tokenizer loading at startup.
- Fix:
```python
# app/main.py
model_path = "assets/model.pth"
tokenizer_path = "assets/tokenizer/"
```
- Verification: Model and tokenizer load successfully on service start.

### Bug 3 — Missing Model Prediction Call
- File: `app/endpoints.py` (L105)
- Issue: `/predict` endpoint returned `(None, None)` because the classifier's predict method was not invoked.
- Fix:
```python
# app/endpoints.py
label, confidence = clf.predict(request.text)
return {"label": label, "confidence": float(confidence)}
```
- Verification: Endpoint returns valid label and confidence for sample requests.

### Bug 4 — Missing Gradient Context During Inference
- File: `ml/model.py` (L117)
- Issue: Inference ran with gradient tracking enabled, increasing GPU memory and reducing throughput.
- Fix:
```python
# ml/model.py
with torch.no_grad():
    outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
    probabilities = F.softmax(outputs.logits, dim=1)
```
- Verification: Inference memory usage reduced; predictions unchanged.

### Bug 5 — Inverted Label Mapping
- File: `ml/model.py` (L80)
- Issue: Label map was inverted, causing positive reviews to be labeled negative and vice versa.
- Fix:
```python
# ml/model.py
self.label_map = {0: 'negative', 1: 'positive'}
```
- Verification: Sample inputs map to expected sentiment labels.

### Bug 6 — Extra Dimension in Embedding Vectors
- File: `db/vector_store.py` (L156)
- Issue: Embeddings were 769D due to an unnecessary appended element, breaking vector-store assumptions.
- Fix:
```python
# db/vector_store.py
return embedding.flatten()
```
- Verification: Embeddings are 768-dimensional and accepted by Qdrant.

### Bug 7 — Incorrect Metadata Field in Vector Store
- File: `db/vector_store.py` (L320)
- Issue: Collection info returned vector size instead of the collection name.
- Fix:
```python
# db/vector_store.py
return {
    "name": self.collection_name,
    "vector_size": info.config.params.vectors.size,
    "distance": info.config.params.vectors.distance,
    "points_count": info.points_count
}
```
- Verification: API returns correct collection name and metadata.

### Bug 8 — Training Script Help Fails on Windows
- **File:** `tests/test_api.py` (L129)
- **Issue:** The test used `"python3"` directly, which caused `exit code 9009` on Windows because the command was not recognized.
- **Fix:**
```python
# tests/test_api.py
import sys

result = subprocess.run(
    [sys.executable, "-m", "ml.train", "--help"],
    capture_output=True,
    text=True,
    timeout=10
)
```
- Verification: Test now passes on both Linux/macOS and Windows environments, confirming that the training script help message displays successfully.

### Bug 9 — Incorrect API Root Message Assertion
- **File:** `tests/test_api.py` (L44)
- **Issue:** The test expected a different or outdated root message, causing an assertion failure when checking the API’s `/` endpoint response.
- **Fix:**
```python
# tests/test_api.py
assert data["message"] == "Sentiment Analysis & Product Recommendation API"
```
- Verification: Test passes with the correct root message from the API.

---

## 🧠 Additional Improvements

| Area | Enhancement | Result |
|------|-------------|--------|
| Performance | Added `torch.no_grad()` during inference | Reduced GPU load |
| Accuracy | Corrected label mapping | Proper sentiment classification |
| Compatibility | Fixed label dtype for `CrossEntropyLoss` | Stable model training |
| Robustness | Fixed vector dimension mismatch | Reliable Qdrant integration |
| Maintainability | Cleaned asset paths & metadata fields | Simplified deployment |
| Infrastructure | Added `Dockerfile`, `docker-compose.yml`, and `.dockerignore`| Containerized training & deployment; reproducible environments |
| Security & Configuration | Added `.gitignore`, `.env`, and `.env.example` files | Prevented sensitive data (API keys, credentials, etc.) from being committed; simplified environment setup for collaborators |
| Dependencies | Added `python-dotenv` to `requirements.txt` | Enabled automatic loading of environment variables from `.env` files for seamless configuration management |

## ✅ Verification Summary

| Component | Test Status | Notes |
|-----------|-------------|-------|
| Model Training | ✅ Pass | No CUDA or dtype errors |
| Single Prediction | ✅ Pass | Accurate sentiment results |
| Batch Prediction | ✅ Pass | Consistent results across samples |
| Health Check | ✅ Pass | API returns healthy |
| Model Info | ✅ Pass | Correct metadata |
| Vector Store | ✅ Pass | Correct 768D embeddings |
| Unit Tests | ✅ All Passed | Coverage for endpoints and core logic |

---

## 🏁 Final Status

- All 7 issues identified and fixed.
- Training and inference pipelines operational.
- API endpoints functioning correctly.
- Vector store ready for Qdrant integration.
- All unit tests passing successfully.
- Dockerized ML service included (`Dockerfile`, `docker-compose.yml`, `.dockerignore`).
- Added environment and security configuration files (`.gitignore`, `.env`, `.env.example`) for safe and consistent setup.

Compiled by: Ashish Panara  
Date: November 7, 2025  
Status: ✅ Stable — Production Ready