# Rei — Chatbot Rekomendasi Manhwa

Chatbot AI berbasis LLM (via **Groq API**) yang berperan sebagai teman ngobrol yang merekomendasikan manhwa (komik Korea) sesuai genre, mood, dan preferensi pengguna.

---

## 1. Tema & Konsep

**Tema:** Chatbot rekomendasi manhwa.

Rei bertindak sebagai teman ngobrol yang:

- Menanyakan preferensi (genre, mood, status cerita ongoing/completed, gaya art) kalau belum jelas.
- Memberi rekomendasi judul manhwa lengkap dengan genre, status, dan sinopsis singkat tanpa spoiler.
- Mengingat konteks percakapan sepanjang sesi (misal kalau kamu bilang sudah baca satu judul, Rei tidak akan merekomendasikannya lagi di obrolan yang sama).

Chatbot ini tersedia dalam dua bentuk:

| File | Deskripsi |
|---|---|
| `chatbot_console.py` | Versi terminal/console, lengkap dengan streaming |
| `streamlit_app.py` | Versi web sederhana pakai Streamlit |

---

## 2. Cara Mendapatkan GROQ_API_KEY

1. Buka [console.groq.com](https://console.groq.com) dan login (bisa pakai akun Google).
2. Di sidebar, buka menu **API Keys**.
3. Klik **Create API Key**, beri nama bebas (misal `tugas-1`), lalu buat.
4. **Copy key-nya**. Key (diawali `gsk_...`) hanya ditampilkan sekali.
5. Simpan key tersebut dan jangan dibagikan ke publik.

---

## 3. Cara Menjalankan Program

### Langkah 1 — Clone / download project ini

```bash
git clone https://github.com/ririthm/manhwa-recommend.git
cd manhwa-recommend
```

### Langkah 2 — Install dependencies

Proyek ini dikembangkan dengan Python 3.10.

```bash
pip install -r requirements.txt
```

### Langkah 3 — Setup API key

Buat file baru bernama `.env` di folder proyek (file ini sengaja tidak ikut diunggah ke GitHub karena masuk `.gitignore`), lalu isi dengan:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

> Alternatif: kalau memakai versi web, API key juga bisa dimasukkan manual lewat sidebar tanpa file `.env`.

### Langkah 4 — Jalankan versi Streamlit (web)

```bash
streamlit run streamlit_app.py
```

Browser akan otomatis terbuka di `http://localhost:8501`.

### Langkah 5 — (Opsional) Jalankan versi console

```bash
python chatbot_console.py
```

Perintah yang tersedia di versi console:

| Perintah | Fungsi |
|---|---|
| `exit` | Keluar dari aplikasi |
| `clear` | Mereset percakapan |
| `save` | Mengekspor riwayat percakapan ke berkas JSON |
| `stats` | Menampilkan ringkasan genre yang dibahas |
| `set` | Mengubah parameter Temperature dan Max Tokens |

---

## 4. Pengaturan & Fitur Sidebar

Semua kontrol, pengaturan parameter, dan manajemen riwayat obrolan dapat diakses langsung oleh user melalui **sidebar di sebelah kiri layar**:

| Fitur / Kontrol | Bentuk Interaksi | Fungsi |
| --- | --- | --- |
| **API Key** | Kolom input | Memasukkan API Key secara manual, atau dibaca otomatis dari file `.env`. |
| **Chat Baru** | Tombol (*Button*) | Menghapus riwayat percakapan saat ini dan memulai obrolan baru dari awal. |
| **Simpan** | Tombol (*Button*) | Menyimpan riwayat obrolan aktif ke dalam berkas JSON (`riwayat_chat_YYYYMMDD_HHMMSS.json`). |
| **Buka Chat Lama** | Daftar Tombol | Memuat kembali riwayat percakapan dari berkas JSON yang pernah disimpan sebelumnya. |
| **Hapus Riwayat** | Tombol (*Button*) | Menghapus berkas riwayat tersimpan tertentu atau membersihkan seluruh riwayat sekaligus. |
| **Kreativitas (Temperature)** | Slider (0.0–1.0) | Mengatur kebebasan/kreativitas AI. Nilai `0.0` menghasilkan jawaban konsisten/pasti, sedangkan `1.0` lebih bervariasi. |
| **Maksimal Panjang Jawaban** | Input angka (`st.number_input`) | Menentukan batas jumlah *Max Tokens* (128–4096) yang dapat dihasilkan oleh AI dalam satu balasan. |
| **Statistik Percakapan** | Panel ekspander | Menampilkan rangkuman statistik obrolan aktif (jumlah pesan kamu, balasan AI, dan genre populer yang terdeteksi). |

---

## 5. Contoh Cuplikan Percakapan

![Contoh percakapan dengan Rei, chatbot rekomendasi manhwa](image.png)

---

## 6. Struktur Kode

```
manhwa-recommend/
├── .env
├── .gitignore
├── chatbot_console.py
├── image.png
├── README.md
├── requirements.txt
├── riwayat_chat_YYYYMMDD_HHMMSS.json
├── streamlit_app.py
└── __pycache__/
    └── chatbot_console.cpython-310.pyc
```

| Berkas / Folder | Deskripsi |
|---|---|
| `chatbot_console.py` | Inti logika sekaligus versi terminal. Menyimpan `SYSTEM_PROMPT` terpusat, koneksi ke Groq API (`openai/gpt-oss-120b`) dengan streaming, perintah interaktif, dan fungsi `trim_history()` untuk menjaga riwayat tidak melebihi batas token. |
| `streamlit_app.py` | Antarmuka web berbasis Streamlit. Mengimpor `SYSTEM_PROMPT` dari `chatbot_console.py` dan menyediakan sidebar kontrol serta tampilan chat dengan efek ketikan *streaming*. |
| `.env` | Tempat menyimpan kunci rahasia `GROQ_API_KEY` dalam format *key-value*. File ini dibaca oleh library `python-dotenv` agar API Key tidak ditulis langsung (*hardcode*) di dalam kode Python. |
| `.gitignore` | Panduan untuk Git agar mengabaikan berkas sensitif atau berkas sampah (misalnya `.env`, `riwayat_chat_*.json`, dan `__pycache__/`) sehingga tidak ikut diunggah ke GitHub. |
| `requirements.txt` | Daftar dependensi pustaka luar yang dibutuhkan agar aplikasi bisa berjalan: `groq`, `streamlit`, dan `python-dotenv`. |
| `README.md` | Dokumentasi lengkap berisi latar belakang proyek, petunjuk instalasi *step-by-step*, penjelasan fitur, panduan perintah, serta tautan aset pendukung. |
| `riwayat_chat_YYYYMMDD_HHMMSS.json` | Berkas rekaman obrolan yang diekspor oleh sistem. Berisi *array of objects* dengan struktur `{"role": "...", "content": "..."}` yang mencatat interaksi antara pengguna dan AI. |
| `image.png` | Tangkapan layar (*screenshot*) tampilan aplikasi yang disematkan ke dalam `README.md` sebagai pratinjau visual. |
| `__pycache__/` | Folder internal Python yang dibuat otomatis saat `streamlit_app.py` menjalankan `from chatbot_console import SYSTEM_PROMPT`, berisi *bytecode* terkompilasi (`.pyc`) agar pemanggilan berikutnya lebih cepat. |

---

## 7. Catatan Penggunaan AI

Dalam proses pengembangan chatbot rekomendasi manhwa ini, Generative AI dimanfaatkan sebagai asisten virtual interaktif untuk mengoptimalkan berbagai tahapan proyek.

Pada tahap konseptualisasi dan perancangan, Generative AI membantu melakukan *brainstorming* ide untuk membentuk persona "Rei", merumuskan batasan instruksi (*System Prompt* terpusat), serta merancang logika pengelolaan riwayat percakapan.

Pada tahap pengembangan antarmuka (UI/UX) dan *debugging*, Generative AI membantu menyusun struktur komponen antarmuka Streamlit.
