from langchain_groq import ChatGroq

print(ChatGroq(
    model='openai/gpt-oss-20b',
    temperature=0.5,
    api_key='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',
).invoke('oi'))

