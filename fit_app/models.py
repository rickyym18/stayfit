from django.db import models
import bcrypt


class WorkoutManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData["workout"]) < 20:
            errors["workout"] = "workout must be longer than 20 characters"
        return errors



class Workout(models.Model):
    author= models.ForeignKey("User", related_name= "author", on_delete = models.CASCADE)
    workout = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()



class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData["password"]) < 8:
            errors["password"] = "password must be at least 8 characters long"
            return errors
        if postData["password"] != postData["confirm"]:
            errors["password"] = "password doesn't match"
            return errors
        # if postData["password"] != postData["password"]:
        #     errors["password"] = "password is not correct"
        #     return errors
        check_email = self.filter(email=postData["email"])
        if check_email: 
            errors["email"] = "email already in use"
            return errors
    def validation(self, postData):
        errors = {}
        if postData["password"] != postData["password"]:
            errors["password"] = "password is not correct"
            return errors



class User(models.Model):
    first_name = models.CharField(max_length=223)
    last_name = models.CharField(max_length=222)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    confirm = models.CharField(max_length=225)
    my_workout = models.ManyToManyField(Workout, related_name="my_workout", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

