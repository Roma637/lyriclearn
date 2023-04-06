import openai

def ask_gpt(rhyme, topic, keywords):

    openai.api_key= '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'

    rhymes_instructions = {
        'london':"each verse has four lines. the first line has 7 syllables, the second line has 6 syllables, the third line has 7 syllables, and the fourth line has 6 syllables.", 
        'twinkle':"each verse has six lines, and each line has 7 syllables.", 
        # 'ants':"each verse has four lines. the first and second line have 12 syllables, the third line has 16 syllables, and the fourth line has 13 syllables.", 
        'frere':"each verse has four lines. the first line has 8 syllables, the second line has 6 syllables, the third line has 12 syllables, and the fourth line has 6 syllables.", 
        'weasel':"each verse has four lines. the first line has 9 syllables, the second line has 7 syllables, the third line has 9 syllables, the fourth line has 5 syllables."
        }

    gpt_prompt = "write lyrics about " + topic + " where " + rhymes_instructions[rhyme] + "use as many verses as necessary."
    # gpt_prompt = "write a poem about elasticity in economics where there are 18 lines, and each line is 7 syllables. make sure it is only 5 verses maximum with no chorus, and that it mentions the types of elasticity like price elasticity of demand or supply, cross price elasticity of demand and income elasticity of demand"

    if len(keywords)>0:
        gpt_prompt.append(". ensure it includes these keywords: ")
        for kw in keywords:
            gpt_prompt.append(kw+", ")
        gpt_prompt = gpt_prompt[-2:]

    # print("====================")
    print(gpt_prompt)

    gpt_prompts = 5 * [gpt_prompt]

    final_responses = []

    for gpt_prompt_opt in gpt_prompts:
        response = openai.Completion.create(
            engine="text-davinci-002", #the most capable variation of GPT-3
            prompt=gpt_prompt_opt,
            temperature=0.7, #randomness
            max_tokens=300,
        )

        gpt_response = response['choices'][0]['text']
        print(gpt_response)

        final_responses.append(gpt_response.strip())

    return final_responses

#todo

#keywords not keywording