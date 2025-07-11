from django.shortcuts import redirect

from django.shortcuts import render

def onboarding_view(request):
    return render(request, 'onboarding1.html')  

def onboarding_view2(request):
    return render(request, 'onboarding2.html')

def onboarding_view3(request):
    return render(request, 'onboarding3.html')

def finish_onboarding(request):
    request.user.has_onboarded = True
    request.user.save()
    return redirect('users:login')  

