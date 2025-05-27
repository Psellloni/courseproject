import openai
from source.config import chatgpt_api_key

client = openai.Client(api_key=chatgpt_api_key)

def check_batch(text_batch, rules, model="gpt-4o-mini", temperature=0):

    condition="""Analyze each dictionary {'id':..., 'message':'...'} and return ONLY 
    a Python-formatted list of dictionaries [{'id':..., 'rules_broken':[...]}, ...], where:  
    - All original key-value pairs from the input dictionaries are preserved.  
    - A new key-value pair `'rules_broken': [0, 3]` is added, where `0` and `3` are the 
    numbers of the rules violated by the `'message'` text. Include ALL rules explicitly 
    violated by the text.""" + f'Rules: {rules}' + """
    
    {{'id': 12634673, 'message': 'Я считаю...'}} -> {{'id': 12634673, 'rules_broken': [1,5]}}

    If no rules are violated, `'rules_broken'` must be an empty list. Example:
    [{{'id': 12634673, 'rules_broken': [1,5]}}, {{'id': 126004673, 'rules_broken': []}}, ...]

    Analyze the text STRICTLY by these rules. Ignore general reasoning, comments, or 
    indirect relevance—only include rules that are DIRECTLY and LITERALLY violated. 
    Return ONLY the valid Python list of dictionaries. Do NOT include explanations 
    or additional text."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": condition},
                {"role": "user", "content": text_batch}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT API Error: {e}")
        return None
