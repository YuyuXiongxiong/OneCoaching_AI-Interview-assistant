from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import chainlit as cl

model_name = "ft:open-mistral-7b:93b81e3f:20240628:3888e2fb"

client = MistralClient(api_key="8BXU9qP4ba24JS0OY7vS1kdRpRWFNvfT")

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [ChatMessage(role="assistant", content="Parlez-moi de vous.")])
    await cl.Message(content="Parlez-moi de vous.", disable_feedback=True).send()

@cl.on_message
async def on_message(message: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    chat_history.append(ChatMessage(role="user", content=message.content))
    
    chat_response = client.chat_stream(
        model=model_name,
        messages=chat_history,
    )
    
    answer = cl.Message(content="")
    
    for token in chat_response:
        await answer.stream_token(token.choices[0].delta.content)
    
    chat_history.append(ChatMessage(role="assistant", content=answer.content))
    
    await answer.send()
