import requests
from requests.compat import quote_plus
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .models import Search
# Create your views here.
def home(request):
  return render(request, 'main_app/index.html')

def new_search(request):
  BASE_CRAIGSLIST_URL = 'https://www.jumia.com.ng/catalog/?q='
  search = request.POST.get('search')

  Search.objects.create(search=search)
  search_url = BASE_CRAIGSLIST_URL + quote_plus(search)
  response = requests.get(search_url)
  data = response.text 

  soup = BeautifulSoup(data, features='html.parser')
  cards = soup.find_all('article', {'class': "prd"})
  cleaned_cards = []
  for card in cards:
 
    card_name = card.find(class_='name').text
    card_price = card.find(class_='prc').text
   


    if card.find(class_='img').get('data-src'):
      link = card.find(class_='core').get('href')
      card_link = 'https://www.jumia.com.ng'+ link
    else:
      card_link = None
      
    if card.find(class_='img').get('data-src'):
      card_img = card.find(class_='img').get('data-src')
    else:
      card_img = None
      
    card_obj = {
      'img': card_img,
      'name': card_name,
      'price': card_price,
      'link': card_link
    }
    cleaned_cards.append(card_obj)

  if not search:
    return redirect("/")

  data_for_result = {
    'search': search,
    'result': cleaned_cards
    }
  return render(request, 'main_app/search-result.html', data_for_result)


def detail_page(request):
  pass

def post_product(request):
  pass