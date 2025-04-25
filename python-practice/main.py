## Chat bot using google gemini api key

# ***----Import required libraries and modules----*** #

import langchian.google_generativeai as genai

# ***---- Replace with your GOOGLE_GEMINI_API_KEY----*** #

api_key = ('')

# ***----Intialize the llm you are using----*** #

llm = genai.ChatGenerativeai(
    model= 'gemini-1.5-flash',
    tempreture = 0.4
)

response = llm.generate_content('what is the usecases of LangGraph?')
print(f"Response" : {response.content})
