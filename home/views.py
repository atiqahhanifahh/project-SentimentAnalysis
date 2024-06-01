from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *
import requests
import csv

def index(request):
  anies_baswedan = {}
  response = requests.get('http://localhost:8000/api/aniesbaswedan/')
  if response.status_code == 200:
    anies_baswedan = response.json()

  ganjar_pranowo = {}
  response = requests.get('http://localhost:8000/api/ganjarpranowo/')
  if response.status_code == 200:
    ganjar_pranowo = response.json()
  
  # region positif
  anies_baswedan_top_10_positif = []
  ganjar_pranowo_top_10_positif = []
  
  key = 0
  no = 1
  for value in anies_baswedan['data']['data_positif']['Total']:
    anies_baswedan_top_10_positif.append({
      'no': no,
      'kata': anies_baswedan['data']['data_positif']['Kata Positif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  
  key = 0
  no = 1
  for value in ganjar_pranowo['data']['data_positif']['Total']:
    ganjar_pranowo_top_10_positif.append({
      'no': no,
      'kata': ganjar_pranowo['data']['data_positif']['Kata Positif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  #endregion

  # region negatif
  anies_baswedan_top_10_negatif = []
  ganjar_pranowo_top_10_negatif = []
  key = 0
  no = 1
  for value in anies_baswedan['data']['data_negatif']['Total']:
    anies_baswedan_top_10_negatif.append({
      'no': no,
      'kata': anies_baswedan['data']['data_negatif']['Kata Negatif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  key = 0
  no = 1
  for value in ganjar_pranowo['data']['data_negatif']['Total']:
    ganjar_pranowo_top_10_negatif.append({
      'no': no,
      'kata': ganjar_pranowo['data']['data_negatif']['Kata Negatif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  #endregion

  # region neutral
  anies_baswedan_top_10_neutral = []
  ganjar_pranowo_top_10_neutral = []
  key = 0
  no = 1
  for value in anies_baswedan['data']['data_neutral']['Total']:
    anies_baswedan_top_10_neutral.append({
      'no': no,
      'kata': anies_baswedan['data']['data_neutral']['Kata Neutral'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  key = 0
  no = 1
  for value in ganjar_pranowo['data']['data_neutral']['Total']:
    ganjar_pranowo_top_10_neutral.append({
      'no': no,
      'kata': ganjar_pranowo['data']['data_neutral']['Kata Neutral'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  #endregion

  # region cvs
  cvs_anies_baswedan = []
  cvs_max_anies_baswedan = 0
  cvs_min_anies_baswedan = 0
  no = 1
  i = 1
  for value in anies_baswedan['data']['cvs']:
    if i > 5:
      i = 1
    
    cvs_anies_baswedan.append({'no': no, 'total': round(value * 100, 2), 'theme': i})
    if round(value * 100, 2) >= cvs_max_anies_baswedan:
      cvs_max_anies_baswedan = round(value * 100, 2)
    
    if cvs_min_anies_baswedan == 0:
      cvs_min_anies_baswedan = round(value * 100, 2)
    if cvs_min_anies_baswedan >= round(value * 100, 2):
      cvs_min_anies_baswedan = round(value * 100, 2)

    no = no + 1
    i = i + 1

  cvs_ganjar_pranowo = []
  cvs_max_ganjar_pranowo = 0
  cvs_min_ganjar_pranowo = 0
  no = 1
  i = 1
  for value in ganjar_pranowo['data']['cvs']:
    if i > 5:
      i = 1

    cvs_ganjar_pranowo.append({'no': no, 'total': round(value * 100, 2), 'theme': i})
    if round(value * 100, 2) >= cvs_max_ganjar_pranowo:
      cvs_max_ganjar_pranowo = round(value * 100, 2)
    
    if cvs_min_ganjar_pranowo == 0:
      cvs_min_ganjar_pranowo = round(value * 100, 2)
    if cvs_min_ganjar_pranowo >= round(value * 100, 2):
      cvs_min_ganjar_pranowo = round(value * 100, 2)

    no = no + 1
    i = i + 1
  #endregion

  context = {
    'segment': 'index',
    'anies_baswedan': anies_baswedan,
    'ganjar_pranowo': ganjar_pranowo,
    'anies_baswedan_top_10_positif': anies_baswedan_top_10_positif,
    'ganjar_pranowo_top_10_positif': ganjar_pranowo_top_10_positif,
    'anies_baswedan_top_10_negatif': anies_baswedan_top_10_negatif,
    'ganjar_pranowo_top_10_negatif': ganjar_pranowo_top_10_negatif,
    'anies_baswedan_top_10_neutral': anies_baswedan_top_10_neutral,
    'ganjar_pranowo_top_10_neutral': ganjar_pranowo_top_10_neutral,
    'cvs_anies_baswedan': cvs_anies_baswedan,
    'cvs_max_anies_baswedan': cvs_max_anies_baswedan,
    'cvs_min_anies_baswedan': cvs_min_anies_baswedan,
    'cvs_ganjar_pranowo': cvs_ganjar_pranowo,
    'cvs_max_ganjar_pranowo': cvs_max_ganjar_pranowo,
    'cvs_min_ganjar_pranowo': cvs_min_ganjar_pranowo,
    'jumlah_dataset': (anies_baswedan['data']['n_neutral'] + anies_baswedan['data']['n_positif']  + anies_baswedan['data']['n_negatif']),
    'jumlah_dataset2': (ganjar_pranowo['data']['n_neutral'] + ganjar_pranowo['data']['n_positif']  + ganjar_pranowo['data']['n_negatif'])
  }
  return render(request, "pages/index.html", context)

def indexnb(request):
  anies_baswedan = {}
  response = requests.get('http://localhost:8000/api/aniesbaswedannb/')
  if response.status_code == 200:
    anies_baswedan = response.json()

  ganjar_pranowo = {}
  response = requests.get('http://localhost:8000/api/ganjarpranowonb/')
  if response.status_code == 200:
    ganjar_pranowo = response.json()
  
  # region positif
  anies_baswedan_top_10_positif = []
  ganjar_pranowo_top_10_positif = []
  
  key = 0
  no = 1
  for value in anies_baswedan['data']['data_positif']['Total']:
    anies_baswedan_top_10_positif.append({
      'no': no,
      'kata': anies_baswedan['data']['data_positif']['Kata Positif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  
  key = 0
  no = 1
  for value in ganjar_pranowo['data']['data_positif']['Total']:
    ganjar_pranowo_top_10_positif.append({
      'no': no,
      'kata': ganjar_pranowo['data']['data_positif']['Kata Positif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  #endregion

  # region negatif
  anies_baswedan_top_10_negatif = []
  ganjar_pranowo_top_10_negatif = []
  key = 0
  no = 1
  for value in anies_baswedan['data']['data_negatif']['Total']:
    anies_baswedan_top_10_negatif.append({
      'no': no,
      'kata': anies_baswedan['data']['data_negatif']['Kata Negatif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  key = 0
  no = 1
  for value in ganjar_pranowo['data']['data_negatif']['Total']:
    ganjar_pranowo_top_10_negatif.append({
      'no': no,
      'kata': ganjar_pranowo['data']['data_negatif']['Kata Negatif'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  #endregion

  # region neutral
  anies_baswedan_top_10_neutral = []
  ganjar_pranowo_top_10_neutral = []
  key = 0
  no = 1
  for value in anies_baswedan['data']['data_neutral']['Total']:
    anies_baswedan_top_10_neutral.append({
      'no': no,
      'kata': anies_baswedan['data']['data_neutral']['Kata Neutral'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  key = 0
  no = 1
  for value in ganjar_pranowo['data']['data_neutral']['Total']:
    ganjar_pranowo_top_10_neutral.append({
      'no': no,
      'kata': ganjar_pranowo['data']['data_neutral']['Kata Neutral'][key],
      'total': value
    })
    key = key + 1
    no = no + 1
  #endregion

  # region cvs
  cvs_anies_baswedan = []
  cvs_max_anies_baswedan = 0
  cvs_min_anies_baswedan = 0
  no = 1
  i = 1
  for value in anies_baswedan['data']['cvs']:
    if i > 5:
      i = 1
    
    cvs_anies_baswedan.append({'no': no, 'total': round(value * 100, 2), 'theme': i})
    if round(value * 100, 2) >= cvs_max_anies_baswedan:
      cvs_max_anies_baswedan = round(value * 100, 2)
    
    if cvs_min_anies_baswedan == 0:
      cvs_min_anies_baswedan = round(value * 100, 2)
    if cvs_min_anies_baswedan >= round(value * 100, 2):
      cvs_min_anies_baswedan = round(value * 100, 2)

    no = no + 1
    i = i + 1

  cvs_ganjar_pranowo = []
  cvs_max_ganjar_pranowo = 0
  cvs_min_ganjar_pranowo = 0
  no = 1
  i = 1
  for value in ganjar_pranowo['data']['cvs']:
    if i > 5:
      i = 1

    cvs_ganjar_pranowo.append({'no': no, 'total': round(value * 100, 2), 'theme': i})
    if round(value * 100, 2) >= cvs_max_ganjar_pranowo:
      cvs_max_ganjar_pranowo = round(value * 100, 2)
    
    if cvs_min_ganjar_pranowo == 0:
      cvs_min_ganjar_pranowo = round(value * 100, 2)
    if cvs_min_ganjar_pranowo >= round(value * 100, 2):
      cvs_min_ganjar_pranowo = round(value * 100, 2)

    no = no + 1
    i = i + 1
  #endregion

  context = {
    'segment': 'xxnb',
    'anies_baswedan': anies_baswedan,
    'ganjar_pranowo': ganjar_pranowo,
    'anies_baswedan_top_10_positif': anies_baswedan_top_10_positif,
    'ganjar_pranowo_top_10_positif': ganjar_pranowo_top_10_positif,
    'anies_baswedan_top_10_negatif': anies_baswedan_top_10_negatif,
    'ganjar_pranowo_top_10_negatif': ganjar_pranowo_top_10_negatif,
    'anies_baswedan_top_10_neutral': anies_baswedan_top_10_neutral,
    'ganjar_pranowo_top_10_neutral': ganjar_pranowo_top_10_neutral,
    'cvs_anies_baswedan': cvs_anies_baswedan,
    'cvs_max_anies_baswedan': cvs_max_anies_baswedan,
    'cvs_min_anies_baswedan': cvs_min_anies_baswedan,
    'cvs_ganjar_pranowo': cvs_ganjar_pranowo,
    'cvs_max_ganjar_pranowo': cvs_max_ganjar_pranowo,
    'cvs_min_ganjar_pranowo': cvs_min_ganjar_pranowo,
    'jumlah_dataset': (anies_baswedan['data']['n_neutral'] + anies_baswedan['data']['n_positif']  + anies_baswedan['data']['n_negatif']),
    'jumlah_dataset2': (ganjar_pranowo['data']['n_neutral'] + ganjar_pranowo['data']['n_positif']  + ganjar_pranowo['data']['n_negatif'])
  }
  return render(request, "pages/index_nb.html", context)

def input_data(request):
  if request.method == 'POST':
    text = request.POST.get('text')
    response_obj = {}
    response = requests.post('http://localhost:8000/api/preprocessing/', data={'text': text})
    if response.status_code == 200:
      response_obj = response.json()

    context = {
      'segment'  : 'input_data',
      'hasil': response_obj,
      #'products' : Product.objects.all()
    }
    return render(request, "pages/input_data.html", context)
  
  else:
    context = {
      'segment'  : 'input_data',
      #'products' : Product.objects.all()
    }
    return render(request, "pages/input_data.html", context)

def input_preprocessing(request):
  if request.method == 'POST':
    text = request.POST.get('text')
    response_obj = {}
    response = requests.post('http://localhost:8000/api/prediksi/', data={'text': text})
    if response.status_code == 200:
      response_obj = response.json()

    context = {
      'segment'  : 'input_preprocessing',
      'hasil': response_obj['data'][1],
      'hasill': response_obj['dataa'][1],
      #'products' : Product.objects.all()
    }
    return render(request, "pages/hasil_prediksi.html", context)
  
  else:
    context = {
      'segment'  : 'input_preprocessing',
      #'products' : Product.objects.all()
    }
    return render(request, "pages/hasil_prediksi.html", context)

def prediksi_data(request):
  import os
  from .forms import CSVUploadForm
  if request.method == 'POST':
    form = CSVUploadForm(request.POST, request.FILES)
    if form.is_valid():
      csv_file = request.FILES['csv_file']
  
      # unique_identifier = str(uuid.uuid4().hex)
      # new_filename = f'{unique_identifier}.csv'
      new_filename = 'datasets_upload.csv'
        
      file_path = os.path.join('data/', new_filename)
        
      with open(file_path, 'wb') as destination:
        for chunk in csv_file.chunks():
          destination.write(chunk)
    
    # text = request.POST.get('text')
    response_obj = {}
    response = requests.post('http://localhost:8000/api/prediksicsv/', data={})
    # if response.status_code == 200:
    #   response_obj = response.json()

    context = {
      'segment'  : 'prediksi_data',
      'hasil': 'berhasil',
      #'products' : Product.objects.all()
    }
    return render(request, "pages/hasil_prediksi_baru.html", context)
  
  else:
    context = {
      'segment'  : 'prediksi_data',
      #'products' : Product.objects.all()
    }
    return render(request, "pages/hasil_prediksi_baru.html", context)

def hasil_prediksi_svm(request):
  csv_file_path = 'static/hasil_prediksi_svm.csv'  # Update the path accordingly
  data = []
  with open(csv_file_path, 'r', encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file)
    no = 1
    for row in reader:
      row['index'] = no
      no = no + 1
      data.append(row)
  
  context = {
    'segment'  : 'hasil_prediksi_svm',
    'data': data,
    #'products' : Product.objects.all()
  }
  return render(request, "pages/hasil_prediksi_svm.html", context)

def hasil_prediksi_nb(request):
  csv_file_path = 'static/hasil_prediksi_naive_bayes.csv'  # Update the path accordingly
  data = []
  with open(csv_file_path, 'r', encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file)
    no = 1
    for row in reader:
      row['index'] = no
      no = no + 1
      data.append(row)
  
  context = {
    'segment'  : 'hasil_prediksi_nb',
    'data': data,
    #'products' : Product.objects.all()
  }
  return render(request, "pages/hasil_prediksi_nb.html", context)

def datasets_anies(request):
  import os
  from .forms import CSVUploadForm
  if request.method == 'POST':
    form = CSVUploadForm(request.POST, request.FILES)
    if form.is_valid():
      csv_file = request.FILES['csv_file']

      new_filename = 'datasets_anies_upload.csv'
        
      file_path = os.path.join('static/', new_filename)
        
      with open(file_path, 'wb') as destination:
        for chunk in csv_file.chunks():
          destination.write(chunk)
    
    response_obj = {}
    response = requests.post('http://localhost:8000/api/updatemodelanies/', data={})

    try:
      os.remove("data/anies_baswedan_nb.json")
      os.remove("data/anies_baswedan.json")
    except:
      try:
        os.remove("data/anies_baswedan.json")
      except:
        print('')

    return redirect("http://localhost:8000/datasets_anies/")
  else:
    csv_file_path = 'static/datasets_anies.csv'
    data = []
    with open(csv_file_path, 'r', encoding="utf8") as csv_file:
      reader = csv.DictReader(csv_file, delimiter=';')
      no = 1
      for row in reader:
        _row = row
        _row['index'] = no
        no = no + 1
        data.append(_row)
    
    context = {
      'segment'  : 'datasets_anies',
      'data': data,
    }
    return render(request, "pages/datasets_anies.html", context)

def reset_datasets_anies(request):
  import os
  import pandas as pd
  import shutil
  try:
    os.remove("data/anies_baswedan_nb.json")
    os.remove("data/anies_baswedan.json")
  except:
    try:
      os.remove("data/anies_baswedan.json")
    except:
      print('')

  shutil.copy('data/anies_baswedan_nb.json.bak', 'data/anies_baswedan_nb.json')
  shutil.copy('data/anies_baswedan.json.bak', 'data/anies_baswedan.json')

  df = pd.read_csv('static/datasets_anies_default.csv', delimiter=';')
  df.to_csv('static/datasets_anies.csv', sep=';', index=False)

  csv_file_path = 'static/datasets_anies.csv'
  data = []
  with open(csv_file_path, 'r', encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=';')
    no = 1
    for row in reader:
      _row = row
      _row['index'] = no
      no = no + 1
      data.append(_row)
  context = {
    'segment'  : 'datasets_anies',
    'data': data,
  }
  
  # return render(request, "pages/datasets_anies.html", context)
  return redirect("http://localhost:8000/datasets_anies/")

def datasets_ganjar(request):
  import os
  from .forms import CSVUploadForm
  if request.method == 'POST':
    form = CSVUploadForm(request.POST, request.FILES)
    if form.is_valid():
      csv_file = request.FILES['csv_file']

      new_filename = 'datasets_ganjar_upload.csv'
        
      file_path = os.path.join('static/', new_filename)
        
      with open(file_path, 'wb') as destination:
        for chunk in csv_file.chunks():
          destination.write(chunk)
    
    response_obj = {}
    response = requests.post('http://localhost:8000/api/updatemodelganjar/', data={})
    
    try:
      os.remove("data/ganjar_pranowo_nb.json")
      os.remove("data/ganjar_pranowo.json")
    except:
      try:
        os.remove("data/ganjar_pranowo.json")
      except:
        print('')
    
    return redirect("http://localhost:8000/datasets_ganjar/")
  else:
    csv_file_path = 'static/datasets_ganjar.csv'
    data = []
    with open(csv_file_path, 'r', encoding="utf8") as csv_file:
      reader = csv.DictReader(csv_file, delimiter=';')
      no = 1
      for row in reader:
        _row = row
        _row['index'] = no
        no = no + 1
        data.append(_row)
    
    context = {
      'segment'  : 'datasets_ganjar',
      'data': data,
    }
    return render(request, "pages/datasets_ganjar.html", context)

def reset_datasets_ganjar(request):
  import os
  import pandas as pd
  import shutil
  try:
    os.remove("data/ganjar_pranowo_nb.json")
    os.remove("data/ganjar_pranowo.json")
  except:
    try:
      os.remove("data/ganjar_pranowo.json")
    except:
      print('')

  shutil.copy('data/ganjar_pranowo_nb.json.bak', 'data/ganjar_pranowo_nb.json')
  shutil.copy('data/ganjar_pranowo.json.bak', 'data/ganjar_pranowo.json')

  df = pd.read_csv('static/datasets_ganjar_default.csv', delimiter=';')
  df.to_csv('static/datasets_ganjar.csv', sep=';', index=False)

  csv_file_path = 'static/datasets_ganjar.csv'
  data = []
  with open(csv_file_path, 'r', encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file, delimiter=';')
    no = 1
    for row in reader:
      _row = row
      _row['index'] = no
      no = no + 1
      data.append(_row)
  context = {
    'segment'  : 'datasets_ganjar',
    'data': data,
  }
  
  # return render(request, "pages/datasets_ganjar.html", context)
  return redirect("http://localhost:8000/datasets_ganjar/")

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)
