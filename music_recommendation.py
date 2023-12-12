from chatbot_therapy import chatbot_therapy
import streamlit as st
import cv2
import numpy as np
from tensorflow import keras
from googleapiclient.discovery import build
from keras.preprocessing.image import img_to_array
from keras.applications.resnet50 import preprocess_input, decode_predictions


API_KEY = 'AIzaSyA_Xt8VH6gEwWH9FoJzAEtnhyf1NovOHqM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search_youtube(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(
        q=query,
        part='id',
        type='video',
        maxResults=10
    ).execute()

    video_links = []
    for item in search_response['items']:
        video_links.append(f'https://www.youtube.com/watch?v={item["id"]["videoId"]}')

    return video_links

def recommend_music(emotion):
    search_query = f'{emotion} songs'
    video_links = search_youtube(search_query)
    return video_links

def detect_emotion(emotion_button_clicked):
    fine_model = keras.models.load_model("fine_model.h5")

    st.title("Emotion Detector")

    uploaded_file = st.file_uploader("Choose your face image or take one and save one...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file
        image_path = "./images/" + uploaded_file.name
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        # Load and preprocess the image
        image = cv2.imread(image_path)
        image = cv2.resize(image, (224, 224))
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)

        # Make predictions
        predictions = fine_model.predict(image)

        emotion_confidence = np.max(predictions)
        emotion_label = np.argmax(predictions)

        emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
        detected_emotion = emotion_labels[emotion_label]
        emotion_result = {
            "emotion": detected_emotion,
            "confidence": emotion_confidence
        }

        # Display the prediction
        st.write(f"Detected emotion is: {emotion_result['emotion']}")  
        # Display the prediction
        st.write(f"Level of Confidence is: {emotion_result['confidence']}") 

        # Return the emotion_result
        return emotion_result

    # Handle the case where no file is uploaded
    return {"emotion": "No face detected in the uploaded image.", "confidence": 0.0}

# Setting up initial context
context = [{'role': 'system', 'content': """
    You wait to collect the information on how your users are feeling and then offer therapy advice from there. \
    Your purpose is to help users navigate through their emotions and make them feel better. \
    Think of yourself as a virtual companion on the journey to emotional well-being. \
    Whether the users are feeling overwhelmed, anxious, or just need someone to talk to, \
    You are here for them.\
    You work together to explore users' emotions and help them find the path to a brighter day. \
    Another important thing even if referring the person to see another therapist would be the best option you should talk with them and give them general counseling. \
    The best way to do this is to be very clear about what you can and cannot do. \
    For example, you can say that you are not a therapist, but you can offer support and help people find resources. \
    You can also say that you are not a crisis hotline, but you can help people find the right number to call if they are in crisis. \
    Know that if you are clear about what you can and cannot do, people will be more likely to trust you and to feel that you are being honest with them. \
    Making your users feel better is your major priority. \
    Make sure to clarify all options. \
    You respond in a short, very conversational friendly and therapeutic style. \
    """}]

def main():
    st.title("Emotion-based Music Recommendation")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Call the function for emotion detection using the uploaded image
        emotion_result = detect_emotion(uploaded_file)

        # Create columns for options
        col1, col2 = st.columns(2)

        # Music Recommendation Section
        with col1:
            st.subheader("Choose an option:")
            option = st.radio("", ["Therapy", "Recommend playlist basing on detected emotion"])

            if option == "Recommend playlist basing on detected emotion" and emotion_result != "No face detected in the uploaded image.":
                # Recommend music based on the detected emotion
                music_links = recommend_music(emotion_result["emotion"])
                st.subheader(f'''{emotion_result["emotion"]}, Recommended Music Playlist:''')
                for link in music_links:
                    st.write(link)

        # Chatbot Therapy Section
        with col2:
            st.subheader("Chatbot Therapy:")
            # Add a unique key to the st.text_area widget
            user_input = st.text_area("You:")

            if st.button("Start Therapy"):
                st.write("Welcome to Chatbot Therapy!")

                # Chatbot response
                assistant_response = chatbot_therapy(user_input, context)

                # Display conversation
                st.write(f'User: {user_input}')
                st.write(f'Assistant: {assistant_response}')

                # Check if the user wants to end the conversation
                if "exit" in user_input.lower():
                    st.write("Thank you! It was nice talking with you. Feel free to ask me anything.")

if __name__ == "__main__":
    main()