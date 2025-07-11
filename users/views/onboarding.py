from django.shortcuts import redirect

def finish_onboarding(request):
    request.user.has_onboarded = True
    request.user.save()
    return redirect('login')  
