# app.py
import streamlit as st
from music_recommendation import detect_emotion, recommend_music
from chatbot_therapy import chatbot_therapy


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
    st.title("EmoCompanion App")

    # Add the Streamlit button for emotion detection or therapy
    option = st.radio("Choose an option:", ["Detect Emotion"])

    if option == "Detect Emotion":
        emotion_button_clicked = st.button("Detect Emotion")
        st.write("Launching Emotion Detection...")
        emotion_result = detect_emotion(emotion_button_clicked)

        # Ask user for music or therapy
        option = st.radio("Choose an option:", ["Therapy", "Recommend playlist basing on detected emotion"])

        if option == "Recommend playlist basing on detected emotion":
            # Recommend music based on the detected emotion
            music_links = recommend_music(emotion_result.get("Detected Emotion:"))
            st.subheader(f'''{emotion_result["emotion"]}, Recommended Music Playlist:''')
            for link in music_links:
                st.write(link)
        else:
            # Redirect to the chatbot therapy section
            st.write("Redirecting to Chatbot Therapy!!!")
            user_input = st.text_area("You:", key="therapy_input")
            if st.button("Chat"):
                st.write("Welcome to Chatbot Therapy!")
                assistant_response = chatbot_therapy(user_input, context=context)

                # Display the Assistant's response
                st.write(f'User: {user_input}')
                st.write(f'Assistant: {assistant_response}')

                # Check if the user wants to end the conversation
                if "exit" in user_input.lower():
                    st.write("Thank you! It was nice talking with you. Feel free to ask me anything.")

    elif option == "Therapy":
        st.write("Launching Chatbot Therapy!!!")
        user_input = st.text_area("You:", key="therapy_input")
        if st.button("Chat"):
            assistant_response = chatbot_therapy(user_input, context=context)

            # Display the Assistant's response
            st.write(f'User: {user_input}')
            st.write(f'Assistant: {assistant_response}')

            # Check if the user wants to end the conversation
            if "exit" in user_input.lower():
                st.write("Thank you! It was nice talking with you. Feel free to ask me anything.")

if __name__ == "__main__":
    main()
