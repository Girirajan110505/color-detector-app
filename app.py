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

    st.image(image, caption="Click anywhere on the image", use_column_width=True)

    st.write("Click on the image to detect color (only works in local run due to OpenCV).")

    # Only works in local environment
    if st.button("Open image for click detection (local only)"):
        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                b, g, r = img_cv[y, x]
                color_name = get_color_name(r, g, b, csv_data)
                color_box = np.zeros((100, 300, 3), np.uint8)
                color_box[:] = [b, g, r]

                cv2.imshow("Detected Color", color_box)
                print(f"Color Name: {color_name}, RGB: ({r}, {g}, {b})")

        cv2.imshow("Click on Image", img_cv)
        cv2.setMouseCallback("Click on Image", click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

st.markdown("---")
st.markdown("Made with ❤️ using OpenCV + Streamlit")
