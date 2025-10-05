# import google.generativeai as genai
# import yaml
# import os

# models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]


# def get_gemini_model(model_name=models[0]):
#     model_name = f"models/{model_name}"
#     config_path = os.path.expanduser("config.yaml")
#     with open(config_path) as f:
#         config = yaml.safe_load(f)
#     genai.configure(api_key=config["GEMINI_API_KEY"])
#     return genai.GenerativeModel(model_name)

# def gemini_generate_content(prompt,model_names=models):
#     last_exception = None
#     for model_name in model_names:
#         try:
#             model = get_gemini_model(model_name)
#             response = model.generate_content(prompt)
#             return response.text.strip()
#         except Exception as e :
#             last_exception = e
#             continue
#     raise RuntimeError(f"All Gemini models failed.Last Error : {last_exception}")

#!/usr/bin/env python3
from openai import OpenAI
import os

# Create Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_active_models() -> list[str]:
    """Fetch all currently active models from Groq API."""
    try:
        models = client.models.list().data
        # Filter for text-based models
        text_models = [m.id for m in models if any(x in m.id.lower() for x in ["llama", "qwen", "mixtral", "gemma"])]
        return text_models if text_models else [m.id for m in models]
    except Exception as e:
        print(f"Failed to fetch models: {e}")
        return []

def groq_generate(prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """Generate a response using the first active model with fallback."""
    active_models = get_active_models()
    
    # Fallback models if fetch fails
    fallback_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    
    model_list = active_models if active_models else fallback_models
    
    last_exception = None
    for model in model_list:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            last_exception = e
            print(f"Model {model} failed, trying next...")
            continue

    return f"Error: All models failed. Last error: {last_exception}"

def groq_chat(prompt: str) -> str:
    """Convenience wrapper for chat-style interactions."""
    return groq_generate(prompt, max_tokens=1024)



# last_exception = None
# Initializes a variable to store the last exception encountered.
# This is useful for debugging: if all models fail, we can see why the last one failed.


# 1. gemini_generate_content() takes a prompt and a list of Gemini models to try.
# 2. last_exception variable is initialized to store the last error encountered.
# 3. The function loops through each model in the given list.
# 4. For each model, it tries to create a Gemini model object using get_gemini_model().
# 5. Then it calls model.generate_content(prompt) to get the AI response.
# 6. If the model succeeds, response.text is stripped of whitespace and returned immediately.
# 7. If the model fails (raises an exception), the exception is stored in last_exception.
# 8. The function then continues to try the next model in the list.
# 9. If all models fail, a RuntimeError is raised with the message of the last exception.
# 10. This ensures fallback works, first success is returned, errors are logged, and the function is robust for AI CLI usage.
