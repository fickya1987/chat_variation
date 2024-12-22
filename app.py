import os
import openai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Pastikan set_page_config adalah yang pertama
st.set_page_config(page_title="Chat Assistant", layout="wide")

# Muat variabel lingkungan
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Tentukan ID model Anda
MODEL_ID = "ft:gpt-4o-2024-08-06:personal:fic-lestari-bahasa-01:ANtvR3xr"

def main():
    st.title("LESTARI BAHASA - Chat Assistant")

    # Inisialisasi riwayat pesan
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Anda adalah Penerjemah dan Ahli Bahasa yang membantu pengguna."},
            {"role": "assistant", "content": "Halo! Selamat datang di asisten chat pribadi Anda. Apa yang ingin Anda diskusikan hari ini? Berikut beberapa saran untuk memulai:\n1. Tips belajar bahasa\n2. Bantuan penerjemahan\n3. Eksplorasi frasa budaya\n4. Topik atau pertanyaan khusus lainnya\nSilakan pilih salah satu atau ceritakan apa yang ada di pikiran Anda!"}
        ]

    # Tampilkan riwayat obrolan
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"**Pengguna**: {message['content']}")
        else:
            st.write(f"**Asisten**: {message['content']}")

    # Input pengguna
    user_input = st.text_input("Respon atau pertanyaan Anda:")

    # Fungsi untuk mengunggah gambar
    uploaded_file = st.file_uploader("Unggah gambar untuk diskusi (opsional):", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar yang diunggah", use_column_width=True)
            st.session_state.messages.append({"role": "user", "content": "Saya telah mengunggah sebuah gambar."})
        except Exception as e:
            st.error(f"Gagal memproses gambar: {e}")

    # Fungsi tombol kirim
    if st.button("Kirim"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            try:
                response = openai.ChatCompletion.create(
                    model=MODEL_ID,
                    messages=st.session_state.messages,
                    temperature=1,
                    max_tokens=2048,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                assistant_response = response.choices[0].message['content'].strip()
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

                # Buat asisten menyesuaikan arahan berdasarkan jawaban user
                st.write(f"**Asisten**: {assistant_response}")
                st.session_state.messages.append({"role": "assistant", "content": "Apakah ada hal lain yang ingin Anda eksplorasi terkait ini?"})
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()








