"""
Chatbot Rekomendasi Manhwa (Streamlit Version)
======================================================
Jalankan dengan:
    streamlit run streamlit_app.py
"""

from collections import Counter
from datetime import datetime
import glob
import json
import os
import re

from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# Mengimpor SYSTEM_PROMPT dari chatbot_console.py
from chatbot_console import SYSTEM_PROMPT

load_dotenv()

# Model GPT-OSS 120B
MODEL_NAME = "openai/gpt-oss-120b"

GENRE_KEYWORDS = [
    "action",
    "aksi",
    "romance",
    "romantis",
    "fantasy",
    "fantasi",
    "comedy",
    "komedi",
    "drama",
    "thriller",
    "horror",
    "horor",
    "school",
    "sekolah",
    "martial arts",
    "bela diri",
    "isekai",
    "regression",
    "reinkarnasi",
    "revenge",
    "balas dendam",
    "slice of life",
    "supernatural",
    "tragedy",
    "tragedi",
    "sport",
    "olahraga",
    "mystery",
    "misteri",
    "villainess",
    "system",
    "murim",
]


def trim_history(messages, max_chat_history=10):
    """Memotong riwayat obrolan agar tidak membengkak,
    tetapi SELALU mempertahankan system prompt di posisi pertama.
    """
    system_msgs = [m for m in messages if m["role"] == "system"]
    chat_msgs = [m for m in messages if m["role"] != "system"]
    return system_msgs + chat_msgs[-max_chat_history:]


st.set_page_config(page_title="Rekomendasi Manhwa", page_icon="🌙")

# ==========================================
# SIDEBAR: API KEY, RIWAYAT & PENGATURAN
# ==========================================
st.sidebar.title("⚙️ Pengaturan & Riwayat")

env_api_key = os.environ.get("GROQ_API_KEY")
if env_api_key:
    api_key = env_api_key
    st.sidebar.success("API key dimuat dari .env ✅")
else:
    api_key = st.sidebar.text_input("Masukkan GROQ_API_KEY", type="password")
    st.sidebar.caption(
        "Atau isi file .env (lihat README.md) supaya tidak perlu ketik ulang."
    )

if not api_key:
    st.sidebar.warning("API key belum diisi.")
    st.title("Chatbot Rekomendasi Manhwa")
    st.info("Masukkan GROQ_API_KEY di sidebar kiri untuk mulai chat.")
    st.stop()

client = Groq(api_key=api_key)

# ------------------------------------------
# PARAMETER RESPONS (TEMPERATURE & NUMBER INPUT)
# ------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Parameter Respons")

temperature = st.sidebar.slider(
    "Kreativitas (Temperature)",
    min_value=0.0,
    max_value=2.0,
    value=0.3,
    step=0.05,
    help="0.0 = Jawaban selalu sama/pasti. 1.0 = Lebih variatif dan kreatif.",
)

# Input angka biasa untuk batas panjang jawaban (bukan slider)
max_tokens = st.sidebar.number_input(
    "Maksimal Panjang Jawaban (Tokens)",
    min_value=100,
    max_value=5000,
    value=100,
    step=1,
    help="Ketik atau tekan tombol +/- untuk menentukan batas panjang kata yang dihasilkan.",
)

# Inisialisasi riwayat obrolan aktif
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

col1, col2 = st.sidebar.columns(2)

if col1.button("➕ Chat Baru", use_container_width=True):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.rerun()

if col2.button("💾 Simpan", use_container_width=True):
    if len(st.session_state.messages) > 1:
        filename = f"riwayat_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
        st.sidebar.success("Tersimpan!")
        st.rerun()
    else:
        st.sidebar.warning("Belum ada obrolan.")

# ------------------------------------------
# DAFTAR RIWAYAT CHAT DI SIDEBAR
# ------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Riwayat Chat Tersimpan")

saved_files = sorted(glob.glob("riwayat_chat_*.json"), reverse=True)

if saved_files:
    for file_path in saved_files:
        time_str = file_path.replace("riwayat_chat_", "").replace(".json", "")
        try:
            display_name = datetime.strptime(
                time_str, "%Y%m%d_%H%M%S"
            ).strftime("%d %b %Y, %H:%M")
        except ValueError:
            display_name = file_path

        col_btn, col_del = st.sidebar.columns([4, 1])

        if col_btn.button(
            f"💬 {display_name}",
            key=f"load_{file_path}",
            use_container_width=True,
        ):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    st.session_state.messages = json.load(f)
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Gagal memuat: {e}")

        if col_del.button("🗑️", key=f"del_{file_path}", help="Hapus riwayat ini"):
            if os.path.exists(file_path):
                os.remove(file_path)
                st.rerun()

    st.sidebar.markdown("")
    if st.sidebar.button("🧹 Hapus Semua Riwayat", use_container_width=True):
        for file_path in saved_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        st.rerun()
else:
    st.sidebar.caption("Belum ada riwayat tersimpan.")

st.sidebar.markdown("---")

# ---------- Statistik ----------
user_msgs = [
    m["content"] for m in st.session_state.messages if m["role"] == "user"
]
assistant_msgs = [
    m["content"] for m in st.session_state.messages if m["role"] == "assistant"
]
all_text = " ".join(user_msgs + assistant_msgs).lower()
found = [
    g for g in GENRE_KEYWORDS if re.search(rf"\b{re.escape(g)}\b", all_text)
]
genre_count = Counter(found)

with st.sidebar.expander("📊 Statistik Percakapan"):
    st.write(f"Pesan kamu: **{len(user_msgs)}**")
    st.write(f"Balasan ChatBot: **{len(assistant_msgs)}**")
    if genre_count:
        st.write("Genre yang sering muncul:")
        for g, c in genre_count.most_common(5):
            st.write(f"- {g}: {c}x")
    else:
        st.caption("Belum ada genre spesifik yang terdeteksi.")

# ==========================================
# TAMPILAN CHAT
# ==========================================
st.title("Chatbot Rekomendasi Manhwa")
st.caption("Ngobrol soal manhwa, dapatkan rekomendasi sesuai preferensi kamu!")

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Tanya ChatBot soal manhwa... (misal: 'aku suka fantasy overpowered MC')"
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages = trim_history(st.session_state.messages)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_answer = ""
        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=temperature,
                max_completion_tokens=int(max_tokens),
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_answer += delta
                placeholder.markdown(full_answer + "▌")
            placeholder.markdown(full_answer)
        except Exception as e:
            full_answer = None
            st.error(f"⚠️ Terjadi error saat memanggil API: {e}")

    if full_answer:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_answer}
        )
    else:
        st.session_state.messages.pop()