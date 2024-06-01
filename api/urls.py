from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from api.views import *

urlpatterns = [

	re_path("product/((?P<pk>\d+)/)?", csrf_exempt(ProductView.as_view())),
	re_path("aniesbaswedan/((?P<pk>\d+)/)?", csrf_exempt(AniesBaswedan.as_view())),
	re_path("ganjarpranowo/((?P<pk>\d+)/)?", csrf_exempt(GanjarPranowo.as_view())),
	re_path("aniesbaswedannb/((?P<pk>\d+)/)?", csrf_exempt(AniesBaswedanNB.as_view())),
	re_path("ganjarpranowonb/((?P<pk>\d+)/)?", csrf_exempt(GanjarPranowoNB.as_view())),
	re_path("preprocessing/((?P<pk>\d+)/)?", csrf_exempt(PreProcessing.as_view())),
	re_path("prediksi/((?P<pk>\d+)/)?", csrf_exempt(Prediksi.as_view())),
	re_path("prediksicsv/((?P<pk>\d+)/)?", csrf_exempt(PrediksiCsv.as_view())),
	re_path("updatemodelanies/((?P<pk>\d+)/)?", csrf_exempt(UpdateModelAnies.as_view())),
	re_path("updatemodelganjar/((?P<pk>\d+)/)?", csrf_exempt(UpdateModelGanjar.as_view())),

]