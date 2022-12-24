from django.shortcuts import redirect

def notLoggedUsers(view_func) :
    def wrapper_func(request ,*args,**kwargs) :
        if request.user.is_authenticated:
            return redirect('home')
        else:
           return view_func(request ,*args,**kwargs)
    return wrapper_func




def allowedUsers(allowedGroups=[]) :
    def decorator(view_func) :
        def wrapper_func(request ,*args,**kwargs) :
            group = None
            if request.user.groups.exists(): #to sure user in group or not
                group=request.user.groups.all()[0].name  #if user inside the group take the name of group (like admin)
            if group in allowedGroups :
                return view_func(request ,*args, **kwargs) #to allow user to go inside the site
            else :
                return redirect('user_profile')   
        return wrapper_func
    return decorator


def forAminds(view_func) :
        def wrapper_func(request ,*args, **kwargs) :
            group = None
            if request.user.groups.exists(): #to sure user in group or not
                group=request.user.groups.all()[0].name  #if user inside the group take the name of group (like admin)
            if group == 'admin':
                return view_func(request ,*args, **kwargs) #اسمح له بالذهاب الى وجهته 
            if group =='customer':
                return redirect('user_profile')   
                
        return wrapper_func

