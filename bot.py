import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv, find_dotenv
import datetime
import json
from vision import image_input

_ = load_dotenv(find_dotenv())

current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)

if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"


from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

from langchain_community.tools import YouTubeSearchTool



llm = ChatOpenAI(temperature=0.0, model=llm_model)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)

with open('context.json', 'r') as f:
    context = json.load(f)
    for c in context:
        memory.save_context({"input": c['input']}, {"output": c['output']})

conversation = ConversationChain(
    llm=llm,
    memory = memory,
    verbose=False
)

tool = YouTubeSearchTool()


while True:
    input_text = input("Mentee: ")
    image_path = input("Image Path (relative to the bot script, leave blank if None): ")

    if input_text == 'x': break
    if image_path != '': 
        image_context = image_input(image_path=image_path)
        input_text = input_text + " We are also given an image here: " + image_context

    
    
    output = conversation.predict(input=input_text)
    print(output)

    yt_search_query = conversation.predict(input='For the following text, extract a 5 word title summary that represents the topic as a whole: '+output)

    youtube_results = tool.run(yt_search_query+', 2')
    print("For your references, here are some youtube videos: ")
    print(youtube_results)

