# pylint: disable=import-error

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from dotenv import load_dotenv
load_dotenv()
import os
import supabase
from supabase import create_client, Client # type: ignore

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = supabase.create_client(url, key) # type: ignore

# Create your views here.
from django.http import HttpResponse

techs = ['Augmented / Virtual Reality', 'Artificial Intelligence / Machine Learning', 'Big Data / Business Intelligence', 'Blockchain', 'Cloud Services', 'Cybersecurity', 'eCommerce', 'Internet of Things (IoT)', 'IT Services', 'Software Development', 'Software Testing', 'Web Development']

arvr_vendors = supabase.table('shovl_arvr').select("*").execute()

def index(request, techs=techs):
    context = {
        'techs': techs
    }
    return render(request, 'search/index.html', context)

def arvr(request):
    context = {
        'arvr_vendors': arvr_vendors.data,
        'overall_stars': [],
        'overall_blank_stars': [],
        'review_ratings': [],

        'review1_stars': [],
        'review1_blank_stars': [],
        'review1_title': "",
        'review1_text': "",
        'review1_author': "",
        'review1_date': "",

        'review2_stars': [],
        'review2_blank_stars': [],
        'review2_title': "",
        'review2_text': "",
        'review2_author': "",
        'review2_date': "",
    }

    for vendor in arvr_vendors.data:
        rating = vendor['rating']
        rounded = round(rating)
        for i in range(rounded):
            context['overall_stars'].append('star')
    for i in range(5 - len(context['overall_stars'])):
        context['overall_blank_stars'].append('star')

    for vendor in arvr_vendors.data:
        reviews = vendor['reviews']
        for review in reviews:
            rating = review['rating']
            context['review_ratings'].append(rating)
    
    for rating in range(context['review_ratings'][0]):
        context['review1_stars'].append('star')
    
    for i in range(5 - len(context['review1_stars'])):
        context['review1_blank_stars'].append('star')

    context['review1_title'] = arvr_vendors.data[0]['reviews'][0]['title']
    context['review1_text'] = arvr_vendors.data[0]['reviews'][0]['text']
    context['review1_author'] = arvr_vendors.data[0]['reviews'][0]['author']
    context['review1_date'] = arvr_vendors.data[0]['reviews'][0]['date']

    if len(context['review_ratings']) > 1:
        for rating in range(context['review_ratings'][1]):
            context['review2_stars'].append('star')
        for i in range(5 - len(context['review2_stars'])):
            context['review2_blank_stars'].append('star')

    context['review2_title'] = arvr_vendors.data[0]['reviews'][1]['title']
    context['review2_text'] = arvr_vendors.data[0]['reviews'][1]['text']
    context['review2_author'] = arvr_vendors.data[0]['reviews'][1]['author']
    context['review2_date'] = arvr_vendors.data[0]['reviews'][1]['date']

    return render(request, 'search/categories/arvr.html', context)

def ai(request):
    return render(request, 'search/categories/ai.html')

def bigdata(request):
    return render(request, 'search/categories/bigdata.html')

def blockchain(request):
    return render(request, 'search/categories/blockchain.html')

def cloud(request):
    return render(request, 'search/categories/cloud.html')

def cybersecurity(request):
    return render(request, 'search/categories/cybersecurity.html')

def ecommerce(request):
    return render(request, 'search/categories/ecommerce.html')

def iot(request):
    return render(request, 'search/categories/iot.html')

def it(request):
    return render(request, 'search/categories/it.html')

def softwaredev(request):
    return render(request, 'search/categories/softwaredev.html')

def softwaretesting(request):
    return render(request, 'search/categories/softwaretesting.html')

def webdev(request):
    return render(request, 'search/categories/webdev.html')

def invalid(request):
    return render(request, 'search/categories/invalid.html')

def results(request):
    query = request.GET.get('q', '').lower()
    words = query.lower().split()
    if 'virtual' in words and 'reality' in words or 'vr' in words or 'augmented' in words and 'reality' in words or 'ar' in words:
        return redirect(reverse('search-arvr'))
    elif 'artificial' in words and 'intelligence' in words or 'ai' in words or 'machine' in words and 'learning' in words or 'ml' in words:
        return redirect(reverse('search-ai'))
    elif 'big' in words and 'data' in words or 'business' in words and 'intelligence' in words or 'bi' in words:
        return redirect(reverse('search-bigdata'))
    elif 'blockchain' in words or 'web3' in words:
        return redirect(reverse('search-blockchain'))
    elif 'cloud' in words:
        return redirect(reverse('search-cloud'))
    elif 'cybersecurity' in words or 'cyber' in words and 'security' in words:
        return redirect(reverse('search-cybersecurity'))
    elif 'ecommerce' in words or 'e-commerce' in words or 'ecomm' in words:
        return redirect(reverse('search-ecommerce'))
    elif 'internet' in words and 'things' in words or 'iot' in words:
        return redirect(reverse('search-iot'))
    elif 'it' in words and 'services' in words or 'it' in words:
        return redirect(reverse('search-it'))
    elif 'software' in words and 'development' in words:
        return redirect(reverse('search-softwaredev'))
    elif 'software' in words and 'testing' in words:
        return redirect(reverse('search-softwaretesting'))
    elif 'web' in words and 'development' in words or 'web' in words and 'dev' in words:
        return redirect(reverse('search-webdev'))
    return redirect(reverse('search-invalid'))