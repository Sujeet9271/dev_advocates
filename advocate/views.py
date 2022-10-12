import math

from django.urls import reverse
from advocate.models import Advocate, Company
from advocate.serializers import AdvocateSerializer, CompanyDetailSerializer, CompanySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination



@api_view(['GET'])
def index(request):
    return Response({
        'companies':request.build_absolute_uri(reverse('companies')),
        'advocates':request.build_absolute_uri(reverse('advocates')),
        })

@api_view(['GET'])
def get_companies(request):
    try:
        query = request.GET.get('query')
        if query:
            qs = Company.objects.filter(name__icontains=query)
        else:
            qs = Company.objects.all()
        serializer = CompanySerializer(qs,many=True)
        return Response({'total':qs.count(),'companies':serializer.data})
    except Exception as e:
        return Response({'error':'Something went wrong','detail':e.args},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_company(request,id):
    try:
        company = Company.objects.prefetch_related('advocates','advocates__links').get(id=id)
        serializer = CompanyDetailSerializer(company)
        return Response(serializer.data)
    except Company.DoesNotExist:
        return Response({'error':'Company Not Found','detail':f'Company with {id=} doesnot exists'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error':'Something went wrong','detail':e.args},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_advocates(request):
    try:
        limit = int(request.GET.get('limit',10))
        page = int(request.GET.get('page',1))
        query = request.GET.get('query')
        paginator = PageNumberPagination()
        paginator.page_size = limit
        if query:
            print(query)
            qs=Advocate.objects.prefetch_related('links').select_related('company').filter(name__icontains=query)
        else:
            qs = Advocate.objects.prefetch_related('links').select_related('company').all()
        result_page = paginator.paginate_queryset(qs, request)    
        total = paginator.page.paginator.count
        serializer = AdvocateSerializer(result_page,many=True)
        return Response({
            'limit':limit,
            'results':total,
            'total_pages':math.ceil(total/limit),
            'page':page,
            'advocates':serializer.data
        })
    except Exception as e:
        return Response({'error':'Something went wrong','detail':e.args},status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_advocate(request,id):
    try:
        advocate = Advocate.objects.prefetch_related('links').select_related('company').get(id=id)
        serializer = AdvocateSerializer(advocate)
        return Response(serializer.data)
    except Advocate.DoesNotExist:
        return Response({'error':'Advocate Not Found','detail':f'Advocate with {id=} doesnot exists'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error':'Something went wrong','detail':e.args},status=status.HTTP_400_BAD_REQUEST)