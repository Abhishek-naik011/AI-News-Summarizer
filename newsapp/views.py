from django.shortcuts import render
from .models import NewsArticle
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def home(request):

    selected_category = None
    articles = []

    if request.method == "POST":

        keyword = request.POST.get('keyword')
        selected_category = request.POST.get('category')

        print("Keyword:", keyword)
        print("Category:", selected_category)

        # If user searches a keyword
        if keyword:

            url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"

        # Otherwise use category dropdown
        else:

            url = f"https://newsapi.org/v2/top-headlines?country=us&category={selected_category}&apiKey={API_KEY}"

        response = requests.get(url)

        data = response.json()

        articles = data.get('articles', [])

        for article in articles[:3]:

            description = article.get('description')

            if description:

                prompt = f"""
                Summarize this news in 2 simple sentences:

                {description}
                """

                try:
                    ai_response = model.generate_content(prompt)
                    article['summary'] = ai_response.text

                    NewsArticle.objects.create(
                        title=article.get('title', ''),
                        summary=article['summary'],
                        category=selected_category if selected_category else keyword
                    )

                except Exception:
                    article['summary'] = "AI Summary not available right now."

    return render(
        request,
        'home.html',
        {
            'category': selected_category,
            'articles': articles
        }
    )