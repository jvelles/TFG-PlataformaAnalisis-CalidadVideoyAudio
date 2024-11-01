import openai
import os

openai.api_key = "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"

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Hola, ¿puedes confirmarme que tengo acceso a gpt-4?"}
        ]
    )
    print("Respuesta de gpt-4:", response['choices'][0]['message']['content'])
except openai.error.InvalidRequestError as e:
    print("Error:", e)
except openai.error.OpenAIError as e:
    print("Otro error:", e)
