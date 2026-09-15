# Product Requirements Document (PRD)

## AI Data Analyst Web

**Version:** 1.0  
**Status:** Draft  
**Product Type:** AI-Powered Data Analytics Web Application

---

# 1. Overview

## 1.1 Product Name

**AI Data Analyst**

## 1.2 Product Summary

AI Data Analyst adalah aplikasi web yang memungkinkan pengguna mengunggah dataset dan melakukan analisis data menggunakan bahasa natural.

Pengguna tidak perlu menulis kode Python atau SQL untuk melakukan analisis dasar. Pengguna cukup memberikan pertanyaan seperti:

> "Produk mana yang memiliki penjualan tertinggi?"

atau

> "Buatkan grafik revenue per bulan."

Sistem akan menggunakan **LLM + LangChain + Python/Pandas** untuk memahami permintaan, melakukan analisis terhadap dataset asli, dan mengembalikan hasil dalam bentuk teks, tabel, atau visualisasi.

---

# 2. Problem Statement

Analisis dataset biasanya membutuhkan kemampuan menggunakan Python, Pandas, SQL, dan tools visualisasi.

Bagi pengguna non-teknis, proses tersebut dapat menjadi cukup sulit.

AI Data Analyst bertujuan membuat proses analisis data menjadi lebih mudah dengan menyediakan antarmuka berbasis percakapan.

Pengguna dapat:

- Upload dataset
- Melihat struktur dataset
- Bertanya menggunakan bahasa natural
- Meminta analisis
- Meminta visualisasi
- Mendapatkan insight
- Mendapatkan rekomendasi berdasarkan data

---

# 3. Goals

## Primary Goals

1. Memungkinkan pengguna mengupload dataset.
2. Melakukan exploratory data analysis secara otomatis.
3. Memungkinkan pengguna bertanya kepada dataset menggunakan bahasa natural.
4. Menggunakan LLM untuk memahami intent pengguna.
5. Menggunakan Pandas/Python sebagai tool untuk melakukan perhitungan terhadap data asli.
6. Menghasilkan visualisasi berdasarkan permintaan pengguna.
7. Menampilkan insight dan hasil analisis dalam UI yang mudah dipahami.

## Secondary Goals

1. Menampilkan kualitas dataset.
2. Mendeteksi missing values.
3. Mendeteksi duplikasi.
4. Mendeteksi outlier sederhana.
5. Menghasilkan automated data summary.
6. Menyediakan export hasil analisis.

---

# 4. Non-Goals

Versi awal tidak ditujukan untuk:

- Training machine learning secara otomatis.
- Deep learning.
- Big Data dengan ukuran dataset sangat besar.
- Real-time streaming analytics.
- Penggantian penuh terhadap data analyst profesional.
- Menjamin keputusan bisnis secara otomatis.

---

# 5. Target Users

## Primary User

Mahasiswa, data analyst pemula, developer, researcher, dan pengguna umum yang ingin memahami dataset tanpa menulis banyak kode.

## Example Users

### Student

Mengupload dataset untuk tugas kuliah dan meminta:

> "Berikan statistik deskriptif dataset ini."

### Junior Data Analyst

Meminta:

> "Cari tren revenue selama periode terakhir."

### Researcher

Meminta:

> "Apakah terdapat korelasi antara variabel X dan Y?"

---

# 6. Core User Flow

```text
User membuka website
        ↓
Upload dataset
        ↓
Dataset validation
        ↓
Dataset preview
        ↓
Automatic EDA
        ↓
Dashboard
        ↓
User mengajukan pertanyaan
        ↓
LangChain Agent
        ↓
LLM memahami pertanyaan
        ↓
Memilih tool yang diperlukan
        ↓
Pandas / Python
        ↓
Hasil analisis
        ↓
LLM menyusun jawaban
        ↓
Frontend menampilkan hasil
```

---

# 7. Example Interaction

## User

> Produk mana yang paling banyak terjual?

## System Process

```text
User Question
      ↓
LLM
      ↓
Intent Detection
      ↓
Pandas Tool
      ↓
Group By Product
      ↓
Sum Quantity
      ↓
Sort Descending
      ↓
Result
      ↓
LLM
      ↓
Natural Language Response
```

## Output

```text
Produk dengan jumlah penjualan tertinggi adalah Mouse
dengan total 1.245 unit.
```

---

# 8. Features

# 8.1 Dataset Upload

User dapat mengupload dataset.

### Supported Format — MVP

- CSV

### Future

- XLSX
- JSON
- Parquet

### Requirements

- File size validation
- File type validation
- Dataset schema detection
- Error handling

---

# 8.2 Dataset Preview

Setelah upload, sistem menampilkan:

- Nama file
- Jumlah rows
- Jumlah columns
- Column names
- Data types
- Sample rows
- Missing values
- Duplicate rows

Example:

```text
Dataset: supermarket_sales.csv

Rows       : 9,994
Columns    : 11
Missing    : 0
Duplicates : 3
```

---

# 8.3 Automatic EDA

Sistem secara otomatis menghasilkan analisis awal.

### Statistics

- Mean
- Median
- Minimum
- Maximum
- Standard deviation
- Quantiles

### Data Quality

- Missing values
- Duplicate rows
- Unique values
- Data types

### Analysis

- Distribution
- Correlation
- Categorical frequency
- Numerical summary

---

# 8.4 AI Chat

User dapat bertanya menggunakan bahasa natural.

Example:

```text
"Berapa rata-rata revenue?"
```

```text
"Kategori mana yang paling menguntungkan?"
```

```text
"Apakah ada data yang aneh?"
```

```text
"Bandingkan revenue tahun 2025 dan 2026."
```

---

# 8.5 AI Data Analyst Agent

Agent merupakan komponen utama aplikasi.

Agent menggunakan LLM untuk memahami pertanyaan dan menentukan tool yang diperlukan.

Example:

```text
Question
   ↓
Agent
   ├── Pandas Tool
   ├── Statistics Tool
   ├── Visualization Tool
   └── Dataset Information Tool
```

---

# 8.6 Python/Pandas Tool

Tool digunakan untuk melakukan operasi langsung terhadap dataset.

Contoh operasi:

- Filtering
- Grouping
- Aggregation
- Sorting
- Statistical calculation
- Correlation
- Date analysis

LLM tidak boleh mengarang hasil numerik.

Perhitungan harus dilakukan terhadap dataset menggunakan tool.

---

# 8.7 Visualization

Sistem dapat menghasilkan visualisasi berdasarkan pertanyaan pengguna.

Supported charts:

- Bar chart
- Line chart
- Pie chart
- Scatter plot
- Histogram
- Box plot
- Correlation heatmap

Example:

> "Buatkan grafik revenue per bulan."

System:

```text
User
 ↓
LLM
 ↓
Pandas
 ↓
Aggregation
 ↓
Plotly
 ↓
Chart
```

---

# 8.8 AI Insight

Sistem dapat menghasilkan insight otomatis.

Example:

```text
KEY INSIGHTS

1. Revenue meningkat 12.4% dibanding periode sebelumnya.

2. Electronics merupakan kategori dengan revenue
   terbesar.

3. Penjualan mengalami penurunan pada bulan Juli.

4. Produk X memiliki quantity tinggi tetapi revenue
   relatif rendah.

5. Region Y memiliki pertumbuhan paling tinggi.
```

---

# 8.9 AI Recommendation

Sistem dapat memberikan rekomendasi berdasarkan hasil analisis.

Example:

```text
RECOMMENDATIONS

→ Evaluasi performa kategori Electronics.

→ Fokus pada region dengan pertumbuhan tinggi.

→ Investigasi penurunan revenue pada bulan Juli.
```

Recommendation harus diberi konteks bahwa AI menghasilkan rekomendasi berdasarkan pola dataset dan bukan keputusan bisnis yang pasti.

---

# 9. Architecture

```text
┌─────────────────────────────┐
│           USER              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        NEXT.JS FRONTEND     │
│                             │
│ Upload / Dashboard / Chat   │
└──────────────┬──────────────┘
               │ HTTP API
               ▼
┌─────────────────────────────┐
│        FASTAPI BACKEND      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          LANGCHAIN          │
│                             │
│ Agent / Tools / Prompts     │
└───────┬───────────┬─────────┘
        │           │
        ▼           ▼
┌────────────┐  ┌─────────────┐
│ GEMINI API  │  │ PYTHON      │
│    LLM      │  │ PANDAS      │
└────────────┘  └──────┬──────┘
                       │
                       ▼
                 ┌───────────┐
                 │ DATASET   │
                 └───────────┘

                 Visualization
                       │
                       ▼
                    Plotly
```

---

# 10. Technology Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

## Backend

- Python
- FastAPI

## AI

- LangChain
- LangGraph
- Gemini API

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly

## Database

MVP:

- Local/session storage

Future:

- PostgreSQL

## Deployment

Frontend:

- Vercel

Backend:

- Railway / Render / similar Python hosting

---

# 11. LangChain Responsibilities

LangChain digunakan sebagai orchestration layer.

Responsibilities:

- Prompt management
- Model integration
- Tool calling
- Agent workflow
- Output handling
- Context management

LangChain bukan model AI.

Architecture:

```text
LangChain
    ↓
Gemini
    +
Python/Pandas
    +
Visualization Tools
    +
Dataset
```

---

# 12. LLM Responsibilities

LLM digunakan untuk:

1. Memahami pertanyaan user.
2. Menentukan operasi yang diperlukan.
3. Memilih tool.
4. Menjelaskan hasil analisis.
5. Menghasilkan insight.
6. Menghasilkan rekomendasi berbasis hasil analisis.

LLM tidak menjadi sumber kebenaran numerik.

---

# 13. Tool Architecture

Example:

```text
tools/
│
├── dataset_tool.py
├── pandas_tool.py
├── statistics_tool.py
└── visualization_tool.py
```

Example workflow:

```text
User:
"Berapa rata-rata revenue per kategori?"

        ↓

Agent

        ↓

Pandas Tool

        ↓

groupby(category)
mean(revenue)

        ↓

Result

        ↓

LLM

        ↓

Natural Language Answer
```

---

# 14. API Design

## POST /upload

Upload dataset.

### Response

```json
{
  "dataset_id": "abc123",
  "filename": "sales.csv",
  "rows": 9994,
  "columns": 11
}
```

---

## GET /dataset/{id}

Mengambil metadata dataset.

---

## GET /dataset/{id}/preview

Mengambil sample dataset.

---

## GET /dataset/{id}/eda

Mengambil hasil automatic EDA.

---

## POST /chat

Mengirim pertanyaan ke AI Analyst.

### Request

```json
{
  "dataset_id": "abc123",
  "message": "Produk mana yang paling banyak terjual?"
}
```

### Response

```json
{
  "answer": "Mouse merupakan produk dengan...",
  "type": "text"
}
```

---

# 15. Visualization Response

Example:

```json
{
  "type": "chart",
  "chart_type": "bar",
  "title": "Revenue by Category",
  "data": []
}
```

Frontend kemudian melakukan rendering chart.

---

# 16. Frontend Pages

## Landing Page

```text
AI Data Analyst

Upload your dataset.
Ask questions.
Get insights.

[Upload Dataset]
```

## Dashboard

```text
┌───────────────────────────────────────┐
│ Dataset Overview                      │
├───────────────────────────────────────┤
│ Rows │ Columns │ Missing │ Duplicates │
└───────────────────────────────────────┘

Charts

AI Insights

Ask AI
```

## AI Chat

```text
┌──────────────────────────────────────┐
│ AI Data Analyst                      │
├──────────────────────────────────────┤
│ User: What product sells the most?   │
│                                      │
│ AI: Mouse with 1,245 units.          │
│                                      │
├──────────────────────────────────────┤
│ Ask your dataset...             [→]  │
└──────────────────────────────────────┘
```

---

# 17. Project Structure

```text
ai-data-analyst/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   ├── dataset.py
│   │   │   └── chat.py
│   │   │
│   │   ├── services/
│   │   │   ├── dataset_service.py
│   │   │   └── eda_service.py
│   │   │
│   │   ├── agents/
│   │   │   └── analyst_agent.py
│   │   │
│   │   ├── tools/
│   │   │   ├── pandas_tool.py
│   │   │   ├── statistics_tool.py
│   │   │   └── visualization_tool.py
│   │   │
│   │   └── prompts/
│   │       └── analyst_prompt.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── data/
│
├── README.md
└── .gitignore
```

---

# 18. Environment Variables

```env
GEMINI_API_KEY=your_api_key
```

API key hanya berada di backend dan tidak boleh dikirim ke frontend.

---

# 19. Security

System harus:

- Validasi file upload.
- Membatasi ukuran file.
- Membatasi tipe file.
- Tidak mengekspos API key.
- Mengisolasi eksekusi kode jika menggunakan dynamic Python execution.
- Membersihkan temporary files.
- Membatasi operasi yang dapat dilakukan agent.

---

# 20. Error Handling

System harus menangani:

### Invalid File

```text
Unsupported file format.
Please upload a CSV file.
```

### Dataset Empty

```text
The uploaded dataset is empty.
```

### Missing Column

```text
The requested column does not exist.
```

### AI Error

```text
Unable to analyze the dataset right now.
Please try again.
```

### Unsupported Question

```text
I can't answer that using the available dataset.
```

---

# 21. MVP Scope

MVP hanya mencakup:

- CSV upload
- Dataset preview
- Dataset statistics
- Automatic EDA dasar
- AI chat
- Gemini API
- LangChain
- Pandas tool
- Basic chart generation
- Insight generation

Tidak termasuk:

- Authentication
- Multi-user database
- XLSX
- Advanced ML
- Complex agent workflows

---

# 22. Development Phases

## Phase 1 — Foundation

```text
Python
FastAPI
CSV upload
Pandas
```

Goal:

Dataset berhasil masuk dan dibaca backend.

---

## Phase 2 — EDA

Implement:

- Dataset summary
- Missing values
- Data types
- Descriptive statistics
- Basic charts

---

## Phase 3 — LLM

Integrate:

```text
FastAPI
 ↓
Gemini API
```

Test basic AI responses.

---

## Phase 4 — LangChain

Integrate:

```text
FastAPI
 ↓
LangChain
 ↓
Gemini
```

Implement:

- Prompt
- Tool
- Agent

---

## Phase 5 — Data Analyst Agent

Implement tools:

```text
Pandas Tool
Statistics Tool
Dataset Tool
Visualization Tool
```

---

## Phase 6 — Frontend

Build:

- Landing page
- Upload interface
- Dashboard
- Chat interface
- Charts
- Insight cards

---

## Phase 7 — Deployment

```text
Frontend → Vercel

Backend → Python Hosting

LLM → Gemini API
```

---

# 23. Success Metrics

MVP dianggap berhasil apabila:

1. User dapat mengupload dataset CSV.
2. Dataset dapat dibaca tanpa error.
3. Automatic EDA berhasil ditampilkan.
4. User dapat mengajukan pertanyaan menggunakan bahasa natural.
5. AI dapat menggunakan dataset untuk menjawab pertanyaan.
6. Perhitungan numerik berasal dari data asli.
7. AI dapat menghasilkan minimal beberapa tipe chart.
8. Aplikasi dapat digunakan melalui internet setelah deployment.

---

# 24. Future Development

Future versions dapat menambahkan:

## Multi-format Dataset

```text
CSV
XLSX
JSON
Parquet
SQL Database
```

## Advanced Analytics

```text
Regression
Forecasting
Clustering
Anomaly Detection
```

## Machine Learning

User dapat meminta:

> "Coba prediksi sales bulan depan."

System kemudian:

```text
EDA
 ↓
Feature Engineering
 ↓
Model Selection
 ↓
Training
 ↓
Evaluation
 ↓
Prediction
```

## Automated Report

Generate:

```text
Executive Summary
EDA
Key Findings
Charts
Recommendations
```

dan export menjadi PDF/HTML.

---

# 25. Portfolio Positioning

Project dapat diposisikan sebagai:

> **AI-powered Data Analytics Platform that combines LLMs, LangChain, Python data analysis, and interactive visualization to allow users to explore datasets using natural language.**

### Skills Demonstrated

- Full-stack development
- Python
- FastAPI
- Next.js
- LLM integration
- LangChain
- AI Agents
- Tool Calling
- Data Analysis
- Pandas
- Data Visualization
- API development
- Deployment

---

# 26. Final Product Vision

```text
                 AI DATA ANALYST
                       │
                       ▼
                 Upload Dataset
                       │
                       ▼
                Automatic EDA
                       │
                       ▼
                 Ask Your Data
                       │
                       ▼
                AI Analyst Agent
                 /     |      \
                /      |       \
           Pandas   Statistics  Charts
                \      |       /
                 \     |      /
                       ▼
                  AI Insights
                       │
                       ▼
                Recommendations
                       │
                       ▼
                 Export Report
```

**Core principle:**

> LLM memahami pertanyaan, tools melakukan pekerjaan terhadap data, dan LLM menjelaskan hasilnya kepada pengguna.