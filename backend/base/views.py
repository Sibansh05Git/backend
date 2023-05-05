from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
import json
from django.conf import settings
from django.core.serializers import serialize
import socket #For Host IP

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import F
from django.http import JsonResponse

import pandas as pd
import numpy as np

from rest_framework import generics, permissions
from .serializers import UserSerializer, LoginSerializer

class UserCreate(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


df = pd.read_csv("static/crop_recommendation.csv")
df_mean = df.groupby("label").mean()[["N", "P", "K"]]
df_std = df.groupby("label").std()[["N", "P", "K"]]
df_ll = df_mean - 0.3 * df_std
df_ul = df_mean + 0.3 * df_std

def check(n, p, k, label):
    stats = pd.concat([df_ll.loc[[label]].T.rename(columns={label: "lower_limit"}),
                       df_ul.loc[[label]].T.rename(columns={label: "upper_limit"})], axis=1)
    n_ll = stats["lower_limit"].loc["N"]
    p_ll = stats["lower_limit"].loc["P"]
    k_ll = stats["lower_limit"].loc["K"]
    n_ul = stats["upper_limit"].loc["N"]
    p_ul = stats["upper_limit"].loc["P"]
    k_ul = stats["upper_limit"].loc["K"]
    d = dict()
    if n_ll <= n <= n_ul:
        d["N"] = 0
    elif n < n_ll:
        d["N"] = n_ll - n
    else:
        d["N"] = n_ul - n
    if p_ll <= p <= p_ul:
        d["P"] = 0
    elif p < p_ll:
        d["P"] = p_ll - p
    else:
        d["P"] = p_ul - p
    if k_ll <= k <= k_ul:
        d["k"] = 0
    elif k < k_ll:
        d["K"] = k_ll - k
    else:
        d["K"] = k_ul - k
    return d

# Create your views here.

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def crop_recommendation(request):
    n1 = request.data['n'],
    p1 = request.data['p'],
    k1 = request.data['k'],
    label1 = request.data['label'],

    #Convert n p k and label to int
    n = int(n1[0])
    p = int(p1[0])
    k = int(k1[0])
    label = str(label1[0])

    response = check(n, p, k, label)
    data = response
    # content = {'response': response}            
    return JsonResponse(data, status=status.HTTP_200_OK)
