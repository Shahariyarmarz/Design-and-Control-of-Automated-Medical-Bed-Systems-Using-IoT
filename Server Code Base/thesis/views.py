from django.http import HttpResponse

def home(request):

    html="""

    <h1>ami</h1>

    """
    return HttpResponse(html)


def contact(request):
    return HttpResponse("contact")
