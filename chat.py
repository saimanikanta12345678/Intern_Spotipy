import openai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("API_KEY")

# Rest of your code using the OpenAI library

context = [
  {
    'role': "system",
    'content': 'You are a bot, start every response with "BOT :". Ask  different \
    questions how did the day went to analyze the mood of the user, \
    and every response ends with " amigo"',
  },
];
 # accumulate messages

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#   print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def collect_messages_text(msg):
    prompt = msg
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    return response
