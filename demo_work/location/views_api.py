from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from location.models import RegionCity
from location.serializers import RegionCitySerializer

# class LocationInfor(APIView):
#     queryset = RegionCity.objects.all()
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         response = {}
#         region_city = RegionCity.objects.all()
#         if request.data:
#             match request.data['search_for']:
#                 case 'region':
#                     if 'search' in request.data and request.data['search']:
#                         for reg in region_city:
#                             if request.data['search'].lower() in str(reg.region).lower():
#                                 response.update({reg.region.id: str(reg.region)})
#                     else:
#                         response.update({'Error': 'Not existent region'}, code=401)
#                 case 'city':
#                     if 'search' in request.data and request.data['search']:
#                         response_list = []
#                         for city in region_city:
#                             if request.data['search'].lower() in str(city.city).lower():
#                                 response_list.append({'region': {'id': city.region.id,
#                                                                  'name': str(city.region)},
#                                                       'city': {'id': city.city.id,
#                                                                'name': str(city.city)}})
#                         return JsonResponse({'data': response_list})
#                     else:
#                         response.update({'Error': 'Bad request'}, code=401)
#         else:
#             response.update({'Error': 'Bad request'}, code=401)
#         if not response:
#             response.update({'Error': 'Bad request'}, code=401)
#         return JsonResponse(response)


class LocationInforViewSet(ViewSet):

    queryset = RegionCity.objects.all()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        response = {}
        if request.data:
            match request.data['search_for']:
                case 'region':
                    if 'search' in request.data and request.data['search']:
                        for reg in self.queryset:
                            if request.data['search'].lower() in str(reg.region).lower():
                                response.update({reg.region.id: str(reg.region)})
                    else:
                        response.update({'Error': 'Not existent region'}, code=401)
                case 'city':
                    if 'search' in request.data and request.data['search']:
                        response_list = []
                        for city in self.queryset:
                            if request.data['search'].lower() in str(city.city).lower():
                                response_list.append({'region': {'id': city.region.id,
                                                                 'name': str(city.region)},
                                                      'city': {'id': city.city.id,
                                                               'name': str(city.city)}})
                        return JsonResponse({'data': response_list})
                    else:
                        response.update({'Error': 'Bad request'}, code=401)
        else:
            response.update({'Error': 'Bad request'}, code=401)
        if not response:
            response.update({'Error': 'Bad request'}, code=401)
        return JsonResponse(response)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serialize = RegionCitySerializer(item)
        return Response(serialize.data)

