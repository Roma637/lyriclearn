import openai

def ask_gpt(rhyme, topic, keywords):

    openai.api_key= '' #add in your own API key here!

    #each rhyme has a different rhyme scheme, meaning different instructions to give to gpt
    rhymes_instructions = {
        'london':"each verse has four lines. the first line has 7 syllables, the second line has 6 syllables, the third line has 7 syllables, and the fourth line has 6 syllables.", 
        'twinkle':"each verse has six lines, and each line has 7 syllables.", 
        'frere':"each verse has four lines. the first line has 8 syllables, the second line has 6 syllables, the third line has 12 syllables, and the fourth line has 6 syllables.", 
        'weasel':"each verse has four lines. the first line has 9 syllables, the second line has 7 syllables, the third line has 9 syllables, the fourth line has 5 syllables."
        }

    gpt_prompt = "write a poem about " + topic + " where " + rhymes_instructions[rhyme] + " use as many verses as necessary. " 

    #since keywords are optional, this only runs if they're there in the form
    if keywords != ['']:
        print("KEYWORDS IS")
        print(keywords)
        print(type(keywords))
        
        gpt_prompt = gpt_prompt + "ensure it includes the keywords: "
        gpt_prompt += ','.join(keywords) + '.'

    #debugging :D
    print("========PROMPT========")
    print(gpt_prompt)

    #because the quality of the responses varies greatly, we'll send 5 of the same prompt
    gpt_prompts = 5 * [gpt_prompt]

    final_responses = []
    
    #submit the same prompt 5 times
    for gpt_prompt_opt in gpt_prompts:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=gpt_prompt_opt,
            temperature=0.7,
            max_tokens=300,
        )

        gpt_response = response['choices'][0]['text']
        print(gpt_response)

        final_responses.append(gpt_response.strip())

    #final_responses is a list that contains the 5 responses
    return final_responses
