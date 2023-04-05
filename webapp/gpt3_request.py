import os
import openai
import wandb

os.environ['OPENAI_API_KEY'] = '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'

openai.api_key= os.getenv('OPENAI_API_KEY')

run = wandb.init(project='GPT-3 in Python')
prediction_table = wandb.Table(columns=["prompt", "completion"])

rhymes_instructions = {
    'london':"london bridge is falling down", 
    'twinkle':"twinkle twinkle littne star", 
    'ants':"the ants go marching one by one", 
    'frere':"frere jacques", 
    'weasel':"pop goes the weasel"
    }

def ask_gpt(rhyme, topic, keywords):

    print("HI.")

    gpt_prompt = "write lyrics about " + topic + " that can be set to the nursery rhyme " + rhyme 

    if len(keywords)>0:
        gpt_prompt.append(". ensure it includes these keywords: ")
        for kw in keywords:
            gpt_prompt.append(kw+", ")
        gpt_prompt = gpt_prompt[-2:]

    print("====================")
    print(gpt_prompt)

    response = openai.Completion.create(
        engine="text-davinci-002", #the most capable variation of GPT-3
        prompt=gpt_prompt,
        temperature=0.5, #randomness
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    gpt_response = response['choices'][0]['text']
    print(gpt_response)
    prediction_table.add_data(gpt_prompt, gpt_response)

    wandb.log({'predictions':prediction_table})
    wandb.finish()

    return gpt_response