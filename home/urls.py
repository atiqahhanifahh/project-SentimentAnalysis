from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
  path('indexnb/', views.indexnb, name='indexnb'),
  path('tables/', views.tables, name='tables'),
  path('input_data/', views.input_data, name='input_data'),
  path('datasets_ganjar/', views.datasets_ganjar, name='datasets_ganjar'),
  path('datasets_anies/', views.datasets_anies, name='datasets_anies'),
  path('reset_datasets_ganjar/', views.reset_datasets_ganjar, name='reset_datasets_ganjar'),
  path('reset_datasets_anies/', views.reset_datasets_anies, name='reset_datasets_anies'),
  path('input_preprocessing/', views.input_preprocessing, name='input_preprocessing'),
  path('prediksi_data/', views.prediksi_data, name='prediksi_data'),
  path('hasil_prediksi_svm/', views.hasil_prediksi_svm, name='hasil_prediksi_svm'),
  path('hasil_prediksi_nb/', views.hasil_prediksi_nb, name='hasil_prediksi_nb'),
]
