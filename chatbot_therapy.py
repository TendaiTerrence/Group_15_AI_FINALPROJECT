import streamlit as st
import openai
import panel as pn


def collect_messages(prompt, context, panels):
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = chatbot_therapy(prompt, context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    panels.append(pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))

    return pn.Column(*panels)


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


def chatbot_therapy(user_input, context):
    api_key = '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'
    openai.api_key = api_key
    job_id = "ftjob-PKtepiET4iw3aa169lZ7itJ5"
    response = openai.FineTuningJob.retrieve(job_id)
    fine_tuned_model_id = response["fine_tuned_model"]

    # Add the context to the thread
    thread = context + [{"role": "user", "content": user_input}]

    # Assistant responds using the fine-tuned model
    assistant_response = openai.ChatCompletion.create(
        model=fine_tuned_model_id,
        messages=thread,
        temperature=0,
        max_tokens=250,
    )

    # Check if the user wants to end the conversation
    if "exit" in user_input.lower():
        return "Thank you! It was nice talking with you. Feel free to ask me anything."

    # Check if the assistant is asking for the user's name
    if "What can I do for you today?" in assistant_response['choices'][0]['message']['content']:
        response_text = f"Hello, {context[-1]['content']}"
    else:
        response_text = assistant_response["choices"][0]["message"]["content"]

    return response_text


def main():
    st.title("Chatbot Therapy")

    # Create Streamlit app layout
    st.sidebar.title("Chatbot Therapy")
    inp = st.sidebar.text_input("You:")
    if st.sidebar.button("Start Therapy"):
        # Create Streamlit app panels
        panels = []
        # Collect and display messages
        collect_messages(inp, context, panels)
        st.sidebar.write(pn.Column(*panels))


if __name__ == "__main__":
    main()
