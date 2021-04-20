from django.shortcuts import render, redirect, get_object_or_404
from .models import User, UserManager, Workout, WorkoutManager
from .forms import UserForm, WorkoutForm
import bcrypt
from django.contrib import messages

def login_reg(request):
    form = UserForm()
    return render(request, "login_reg.html", {"form":form} )

def login(request):
    if request.method == "POST":
        errors = User.objects.validation(request.POST)
        if errors is not None and len(errors) > 0 :
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ("/")
    if request.method == "POST":
        user = User.objects.filter(email = request.POST["email"])
        if user: 
            print(user)
            if bcrypt.checkpw(request.POST["password"].encode(), user[0].password.encode()):
                request.session["user_id"] = user[0].id
                print(request.session["user_id"])
                return redirect("/home")
    return redirect("/")

def register(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)

    if errors is not None and len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    password = request.POST["password"]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first_name = request.POST["first_name"], last_name= request.POST["last_name"], email= request.POST["email"], password= pw_hash)
    request.session["user_id"] = user.id
    if user is not None:
        return redirect('/')
    return redirect("/")

def home_page(request):
    current_user = User.objects.get(id=request.session['user_id'])
    #print(User.objects.filter(my_workout))
    context = {
        "workouts": Workout.objects.all(),
        "current_user": current_user,
        "favorite":  User.objects.all()
    }
    return render(request, "home.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def edit_workout(request, id):
    if request.method == "POST":
        errors = Workout.objects.validate(request.POST)
        if len(errors) > 0 :
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f"/edit/{id}")
        current_user = User.objects.get(id=request.session['user_id'])
        workout_update = Workout.objects.get(id=id)
        workout_update.workout = request.POST["workout"]
        workout_update.save()
        return redirect(f"/edit/{id}")
    context = {
        "workout": Workout.objects.get(id=id)
    }
    return render(request, "edit_workout.html", context)

def add_workout(request):
    if request.method == "POST":
        errors = Workout.objects.validate(request.POST)
        if errors is not None and len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/add/workout")
        else:
            current_user = User.objects.get(id=request.session['user_id'])
            new_workout = Workout.objects.create(workout=request.POST["workout"], author = current_user)
            #new_workout.my_workout.add(current_user)
            return redirect("/home")
    return redirect("/home")

def current_user(request):
	return User.objects.get(id = request.session['user_id'])


def remove_workout(request, id):
    user = current_user(request)
    my_workout = Workout.objects.get(id=id)
    user.my_workout.remove(my_workout)
    return redirect("/home")

def add_favorite(request, id):
    user = current_user(request)
    favorite = Workout.objects.get(id=id)
    user.my_workout.add(favorite)
    return redirect("/home")

def delete(request, id):
    delete_me = Workout.objects.get(id=id)
    delete_me.delete()
    return redirect("/home")
    