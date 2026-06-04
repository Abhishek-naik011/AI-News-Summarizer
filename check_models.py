import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6Kbin5QSW2zE8An0nhoM1NJl-VUj35jHuLp3G6GQE9OdQ")

for model in genai.list_models():
    print(model.name)