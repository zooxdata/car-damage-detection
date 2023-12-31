# Set the project ID that we will be working with
import streamlit as st
import os
import vertexai
from vertexai.preview.vision_models import Image, ImageQnAModel
import time
import json
import requests
import base64
import tempfile

# Set the project_id
PROJECT_ID = "PROJECT_ID"

# Set the region that you will be working with
REGION = "us-central1"

# Set the image model name if its different
IMAGE_MODEL_NAME = "imagetext"

# Image Q&A
def image_check_simple(files):
    vertexai.init(project=PROJECT_ID, location=REGION)
    model = ImageQnAModel.from_pretrained(IMAGE_MODEL_NAME)
    image = Image.load_from_file(files)
    answers = model.ask_question(
    image=image,
    question="Is the vehicle damaged?",
    # Optional:
    number_of_results=1,
    )

    return answers


#####################################################################################################
#####################################################################################################
#####################################################################################################
#
#                        Let's Put a Nice UI Using Streamlit
#
#####################################################################################################
#####################################################################################################
#####################################################################################################

def main():
    # Streamlit app title and header
    st.write("<h2 style='text-align: center; color: red;'>Damage Detection App</h2>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>Please submit your car photos for processing</h3>", unsafe_allow_html=True)

    # Upload Files
    files = st.file_uploader("Upload car images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # Submit button
    submit_button = st.button("Submit photos to Google's GenAI")

    # Check if files are uploaded and the submit button is clicked
    if submit_button and files:
        for image_file in files:
            image_bytes = image_file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(image_bytes)
                temp_file_path = temp_file.name
            # Call the image_check function to get the answers
            with st.spinner("Google GenAI is reviewing submitted cars to detect damage..."):
                answers = image_check_simple(temp_file_path)

            # Create a layout with columns
            col1, col2 = st.columns([1, 2])  # Ratio: 1:2

            # Display the image on the left
            col1.image(image_bytes, caption=f"Uploaded Image: {image_file.name}", use_column_width=True)

            # Display damage assessment results in the middle column
            col2.markdown(f"**Damaged?**")
            for answer in answers:
                col2.write(answer)

            # Check if the vehicle is damaged and ask the second question
            if any("yes" in answer.lower() for answer in answers):
                # Display the second question about damage type
                with st.spinner("Asking about damage type..."):
                    model = ImageQnAModel.from_pretrained(IMAGE_MODEL_NAME)
                    image = Image.load_from_file(temp_file_path)
                    answers2 = model.ask_question(
                        image=image,
                        question="What is the vehicle damage type?",
                        number_of_results=1,
                    )
                    col2.markdown(f"**Damage Type:**")
                    for answer in answers2:
                        col2.write(answer)

if __name__ == '__main__':
    main()








