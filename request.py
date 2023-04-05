import os
import openai
import wandb

os.environ['OPENAI_API_KEY'] = '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'

openai.api_key= os.getenv('OPENAI_API_KEY')

run = wandb.init(project='GPT-3 in Python')
prediction_table = wandb.Table(columns=["prompt", "completion"])

gpt_prompts = ["here's a mnemonic to memorise the seven layers of the Open Systems Interconnection model, these are application, presentation, session, transport, network, data link, physical"]



for gpt_prompt in gpt_prompts:
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