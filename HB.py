import streamlit as st
import google.generativeai as genai
import tempfile
import os
import base64

API_KEY = "Your-API-KEY"
genai.configure(api_key=API_KEY)


def generate_response(prompt, image_file_path=None):
    if image_file_path:
        with open(image_file_path, "rb") as f:
            image_bytes = f.read()

        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
    else:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

    return response.text


def set_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Heisenberg AI", layout="wide")
    st.title("Heisenberg AI")

    set_bg_from_local("logo1.png")

    img = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg", "webp"])

    st.header(":violet[Question]")
    question = st.text_area(label="Enter your question")

    submit = st.button("Submit")

    if submit and question:
        path = None
        if img:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, img.name)
            with open(path, "wb") as f:
                f.write(img.getvalue())

        with st.spinner("Generating answer... 🧙‍♂️"):
            response = generate_response(question, path)

        if img:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Your Image")
                st.image(img, use_container_width=True)
            with col2:
                st.subheader("Answer")
                st.write(response)
        else:
            st.subheader("Answer")
            st.write(response)

if __name__ == "__main__":
    main()
