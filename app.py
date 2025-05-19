import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# Load color data
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

def get_color_name(R, G, B, csv_data):
    min_dist = float('inf')
    closest_color = None
    for i in range(len(csv_data)):
        d = abs(R - csv_data.loc[i, "R"]) + abs(G - csv_data.loc[i, "G"]) + abs(B - csv_data.loc[i, "B"])
        if d < min_dist:
            min_dist = d
            closest_color = csv_data.loc[i, "color_name"]
    return closest_color

# Streamlit UI
st.title("🎨 Color Detection from Image")
csv_data = load_colors()

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_cv = np.array(image)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.write("Select coordinates to detect color (x = horizontal, y = vertical):")

    height, width = img_cv.shape[:2]
    x = st.slider("X (Width)", 0, width - 1, int(width / 2))
    y = st.slider("Y (Height)", 0, height - 1, int(height / 2))

    # Extract RGB
    b, g, r = img_cv[y, x]
    color_name = get_color_name(r, g, b, csv_data)

    st.markdown(f"**Detected Color:** {color_name}")
    st.markdown(f"**RGB:** ({r}, {g}, {b})")

    # Show color box
    st.markdown(
        f"""
        <div style='width:100px;height:100px;background-color:rgb({r},{g},{b});border:1px solid #000;'></div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("Made with ❤️ using OpenCV + Streamlit")
