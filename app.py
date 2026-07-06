import os
import requests
import streamlit as st
from openai import AzureOpenAI

st.set_page_config(
    page_title="V3 Enterprise AI Advisor",
    layout="wide"
)

st.title("🚀 V3 Enterprise AI Advisor")
st.caption("Powered by Azure OpenAI + Azure ML")


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-12-01-preview"
)


menu = st.sidebar.radio(
    "AI Modules",
    [
        "Safety Intelligence AI",
        "Enterprise AI Advisor"
    ]
)


if menu == "Safety Intelligence AI":

    st.header("🛡 Safety Risk Prediction")

    temperature = st.number_input(
        "Machine Temperature",
        value=80
    )

    vibration = st.number_input(
        "Vibration Level",
        value=5
    )


    if st.button("Analyze Risk"):

        payload = {
            "input_data":{
                "data":[
                    {
                        "temperature":temperature,
                        "vibration":vibration
                    }
                ]
            }
        }

        result = requests.post(
            os.getenv("AZURE_ML_ENDPOINT"),
            headers={
                "Authorization":
                "Bearer "+os.getenv("AZURE_ML_KEY"),
                "Content-Type":"application/json"
            },
            json=payload
        )

        st.subheader("ML Result")
        st.json(result.json())


if menu == "Enterprise AI Advisor":

    st.header("🤖 Ask V3 AI Advisor")

    question = st.text_area(
        "Ask business question"
    )


    if st.button("Ask AI"):

        response = client.chat.completions.create(

            model=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT"
            ),

            messages=[
                {
                    "role":"system",
                    "content":
                    "You are V3 Enterprise AI Advisor. Give enterprise recommendations."
                },
                {
                    "role":"user",
                    "content":question
                }
            ]
        )


        st.success(
            response.choices[0]
            .message.content
        )
