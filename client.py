from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="<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>",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)
#28ba6dfafb114cd2b46dddfc5af8378f
#AIzaSyDHNMsx1l0ZQTj3bsZU7w6-HpvtX3cffpE