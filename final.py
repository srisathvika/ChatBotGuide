import openai

with open('./hiddden.txt') as file:
    openai.api_key = file.read().strip()

messages=[{"role":"system","content":"You are a helpful assistant"}]    
def get_api_response(prompt:str) -> str|None:
    text: str | None = None
    
    
    try:
        response: dict= openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # message=prompt,
            messages=messages,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.7,
            stop=[' user:',' assistant:']
            
        )
        
        choices: dict = response.get('choices')[0]
        text = choices.message.get('content')

        
    except Exception as e:
        print('ERROR: ',e)
        
    return text

def is_health_related(query:str)-> bool:
    health_keywords=['health','medical','doctor','hospital','weight','headache','hi','diet']
    return any(keyword in query.lower() for keyword in health_keywords)


def get_bot_response(message:str, pl:list[str]) -> str:
    if is_health_related(message):
        bot_response: str = get_api_response(message)
    else:
        bot_response="I'm sorry, I can assist with health related quries only."
    
    if bot_response:
        messages.append({"role":"user","content":message})
        messages.append({"role":"assistant","content":bot_response})
        return bot_response
    else:
        return 'Something went wrong...'
        


def main():    
    while True:
        # print("Hello, how can I assist you today")
        user_input = input('You: ')
        response: str = get_bot_response(user_input,[])
        print(f'Bot: {response}')
        # print(messages)
        
        
        
if __name__=='__main__':
    main()
