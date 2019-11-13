from django.http import JsonResponse
from django.forms.models import model_to_dict  

def test(request):
    if(request.method == 'POST'):
        concat = request.POST
        postBody = request.body
        data = model_to_dict(concat)
        print(data)
        result = {"status":"错误","data":"","city":"北京"}
        return JsonResponse(result)
    