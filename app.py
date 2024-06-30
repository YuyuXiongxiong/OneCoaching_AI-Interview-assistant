import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import chainlit as cl
import random

model_name = "ft:mistral-small-latest:93b81e3f:20240630:0d04725b"

api_key=os.environ.get("MISTRAL_API_KEY")
client = MistralClient(api_key=api_key)

def lire_questions(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        questions = f.readlines()
    # Supprimer les caractères de fin de ligne
    questions = [question.strip() for question in questions]
    return questions

Questions_Data = lire_questions('Questions_Data.txt')
Questions_Consulting = lire_questions('Questions_Consulting.txt')
Questions_Marketing = lire_questions('Questions_Marketing.txt')
Questions_Finance = lire_questions('Questions_Finance.txt')

prompt = """Vous êtes un coach de carrière. Votre tâche consiste à fournir des retours sur des réponses d'entretien.
Vos commentaires doivent être structurés en trois parties :

Pourquoi la réponse actuelle est inadéquate : Expliquez les lacunes de la réponse actuelle.
Actions et considérations pour l'amélioration : Proposez des actions spécifiques et des points de réflexion que le candidat devrait considérer pour améliorer sa réponse.
Exemple d'une réponse améliorée : Fournissez un exemple concret d'une meilleure réponse.

Une fois que vous avez terminé les retours, poser directement une question suivante de la liste des questions, et attendre la réponse de l'utilisateur pour évaluer."""

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Data",
            markdown_description="Data professionals specialize in collecting, analyzing, and interpreting large datasets to help organizations make informed decisions. They often work with tools and techniques such as data mining, machine learning, and statistical analysis.\n\n数据专业人员专门收集、分析和解释大型数据集, 以帮助组织做出明智的决策。他们通常使用数据挖掘、机器学习和统计分析等工具和技术。"
            #,
            #icon="/public/avion-alt.svg"       
        ),

        cl.ChatProfile(
            name="Strategy and Management Consulting",
            markdown_description="Strategy and management consultants assist organizations in developing and implementing strategies to achieve their long-term objectives. They analyze business practices, market conditions, and operational processes to recommend improvements and guide decision-making.\n\n战略和管理顾问帮助组织制定和实施策略, 以实现其长期目标。他们分析商业实践、市场状况和运营流程，提出改进建议并指导决策。"
            #,
            #icon="/public/avion-alt.svg"
        ),

        cl.ChatProfile(
            name="Marketing",
            markdown_description="Marketing professionals create and execute strategies to promote products or services, increase brand awareness, and engage customers. They utilize various channels such as digital marketing, social media, content marketing, and advertising to reach target audiences.\n\n营销专业人员创建和执行策略来推广产品或服务、提高品牌知名度并吸引客户。他们利用数字营销、社交媒体、内容营销和广告等多种渠道来接触目标受众。"
            #,
            #icon="/public/photo-film-musique.svg"
        ),


        cl.ChatProfile(
            name="Corporate Finance",
            markdown_description="Corporate finance professionals manage a company’s financial activities, including capital raising, investment decisions, and financial planning. They aim to optimize the firm’s financial performance and ensure sustainable growth.\n\n公司财务专业人员管理公司的财务活动，包括筹集资本、投资决策和财务规划。他们旨在优化公司的财务表现并确保可持续增长。"
            #,
            #icon="/public/coins.png"
        )
    ]

@cl.on_chat_start
async def on_chat_start():
    chat_profile = cl.user_session.get("chat_profile")
    if chat_profile == 'Data':
        random_question = random.choice(Questions_Data)
    
    elif chat_profile == 'Strategy and Management Consulting':
        random_question = random.choice(Questions_Consulting)

    elif chat_profile == 'Marketing':
        random_question = random.choice(Questions_Marketing)

    elif chat_profile == 'Corporate Finance':
        random_question = random.choice(Questions_Finance)
    
    cl.user_session.set("chat_history", [ChatMessage(role="assistant", content=prompt)])
    await cl.Message(content=random_question, disable_feedback=True).send()


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
