import os
import openai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Streamlit configuration
st.set_page_config(page_title="Deskripsi Image", layout="wide")

def main():
    st.title("Deskripsi dan Terjemahan Gambar dengan Lestari Bahasa")
    st.write("Unggah gambar dan berikan konteksnya untuk mendapatkan deskripsi AI dalam bahasa Sunda dan terjemahannya dalam bahasa Indonesia.")

    # Check if the OpenAI API key is set
    if not openai.api_key:
        st.error("Kunci API OpenAI tidak ditemukan. Silakan periksa file .env atau variabel lingkungan.")
        return

    # Upload image
    uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

    # Prompt for image context
    image_context = st.text_input(
        "Masukkan konteks atau deskripsi singkat tentang gambar ini (contoh: 'pantai dengan ombak besar dan langit mendung')",
        "Gambarkan gambar ini secara mendetail."
    )

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Gambar yang diunggah", use_column_width=True)

        # Generate detailed description using OpenAI
        try:
            # Prepare the prompt with user input as context for AI
            description_prompt = (
                f"Berdasarkan konteks gambar: '{image_context}', deskripsikan gambar ini secara detail dalam 10 kalimat berbahasa Sunda. "
                "Tambahkan juga terjemahan dalam bahasa Indonesia."
            )

            response = openai.ChatCompletion.create(
                model="ft:gpt-4o-2024-08-06:personal:fic-lestari-bahasa-01:ANtvR3xr",  # Replace with your model ID
                messages=[
                    {"role": "system", "content": "Anda adalah model AI yang dapat memberikan deskripsi mendetail dalam bahasa Sunda dengan terjemahan bahasa Indonesia."},
                    {"role": "user", "content": description_prompt}
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Display the generated description and translation
            detailed_description = response['choices'][0]['message']['content']
            st.subheader("Deskripsi AI dalam Bahasa Sunda dan Terjemahan Bahasa Indonesia")
            st.write(detailed_description)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()







