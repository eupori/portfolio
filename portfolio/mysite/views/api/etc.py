from rest_framework.views import APIView
from django.http import JsonResponse
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile
import requests


class ImageCrawlingAPIView(APIView):
	def post(self, request, *args, **kwargs):
		img_url = 'https://cdn.pixabay.com/photo/2021/08/25/20/42/field-6574455__340.jpg'
		res = Image.open(requests.get(img_url, stream=True).raw)
		filename = 'sample.jpeg'
		img_object= ImageFile(BytesIO(res.fp.getvalue()), name=filename)
		Crawling.objects.create(image=img_object)
		
		return JsonResponse({"msg": "success."}, status=200)