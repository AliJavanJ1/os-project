from django.shortcuts import render, redirect
from .forms import NewUserForm, NewAIModelForm, NewProjectForm, NewRunForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import AIModel, Run, Project
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("app:models")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="app/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("app:models")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="app/login.html", context={"login_form": form})


@login_required(login_url='app:login')
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("app:models")


@login_required(login_url='app:login')
def models_page(request):
    """
    Show all models of this user and a form to create a new model
    :param request:
    :return:
    """
    if request.method == "POST":
        form = NewAIModelForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(request.user, commit=True)
            messages.success(request, "Model created successfully.")
            return redirect("app:models")
        messages.error(request, "Unsuccessful creation. Invalid information.")
    form = NewAIModelForm()
    models = AIModel.objects.filter(user=request.user)
    return render(request=request, template_name="app/models.html", context={"new_model_form": form, "models": models})


@login_required(login_url='app:login')
def delete_model(request, model_name):
    """
    Delete a model if model is for this user
    :param request:
    :param model_name:
    :return:
    """
    try:
        model = AIModel.objects.get(model_name=model_name)
        if model.user == request.user:
            model.delete()
            messages.success(request, "Model deleted successfully.")
            return redirect("app:models")
        else:
            messages.error(request, "You are not allowed to delete this model.")
            return redirect("app:models")
    except AIModel.DoesNotExist:
        messages.error(request, "Model does not exist.")
        return redirect("app:models")


@login_required(login_url='app:login')
def projects_page(request, model_name):
    """
    Show all projects of a model if model is for this user and a form to start a new project
    :param request:
    :param model_name:
    :return:
    """
    try:
        model = AIModel.objects.get(model_name=model_name)
        if model.user == request.user:
            if request.method == "POST":
                form = NewProjectForm(request.POST, request.FILES)
                if form.is_valid(model=model):
                    project = form.save(model, commit=True)
                    messages.success(request, "Project created successfully.")
                    return redirect("app:projects", model_name=model.model_name)
                messages.error(request, "Unsuccessful creation. Invalid information.")
            form = NewProjectForm()
            projects = model.project_set.all()
            return render(request=request,
                          template_name="app/projects.html",
                          context={"model_name": model.model_name, "new_project_form": form, "projects": projects})
        else:
            messages.error(request, "You are not allowed to view this model.")
            return redirect("app:models")
    except AIModel.DoesNotExist:
        messages.error(request, "Model does not exist.")
        return redirect("app:models")


@login_required(login_url='app:login')
def delete_project(request, model_name, data_name):
    """
    Delete a project by this id if it belongs to current user otherwise show proper error messages
    :param request:
    :param model_name:
    :param data_name:
    :return:
    """
    try:
        model = AIModel.objects.get(model_name=model_name)
        if model.user == request.user:
            project = model.project_set.get(data_name=data_name)
            project.delete()
            messages.success(request, "Project deleted successfully.")
            return redirect("app:projects", model_name=model.model_name)
        else:
            messages.error(request, "You are not allowed to delete this project.")
            return redirect("app:models")
    except AIModel.DoesNotExist:
        messages.error(request, "Model does not exist.")
        return redirect("app:models")
    except project.DoesNotExist:
        messages.error(request, "Project does not exist.")
        return redirect("app:models")


@login_required(login_url='app:login')
def runs_page(request, model_name, data_name):
    """
    Show all runs of a project if project is for this user and a form to start a new run
    :param request:
    :param model_name:
    :param data_name:
    :return:
    """
    try:
        model = AIModel.objects.get(model_name=model_name)
        project = model.project_set.get(data_name=data_name)
        if model.user == request.user:
            if request.method == "POST":
                form = NewRunForm(request.POST)
                if form.is_valid():
                    run = form.save(project, commit=True)
                    messages.success(request, "Run created successfully.")
                    return redirect("app:runs", model_name=model.model_name, data_name=project.data_name)
                messages.error(request, "Unsuccessful creation. Invalid information.")
            form = NewRunForm()
            runs = project.run_set.all()
            return render(request=request,
                          template_name="app/runs.html",
                          context={"model_name": model.model_name, "data_name": project.data_name,
                                   "new_run_form": form, "runs": runs})
        else:
            messages.error(request, "You are not allowed to view this model.")
            return redirect("app:models")
    except AIModel.DoesNotExist:
        messages.error(request, "Model does not exist.")
        return redirect("app:models")
    except Project.DoesNotExist:
        messages.error(request, "Project does not exist.")
        return redirect("app:projects", model_name=model.model_name)


@login_required(login_url='app:login')
def delete_run(request, model_name, data_name, run_id):
    """
    Delete a run by this id if it belongs to current user otherwise show proper error messages
    :param request:
    :param model_name:
    :param data_name:
    :param run_id:
    :return:
    """
    try:
        model = AIModel.objects.get(model_name=model_name)
        project = model.project_set.get(data_name=data_name)
        run = project.run_set.get(id=run_id)
        if model.user == request.user:
            run.delete()
            messages.success(request, "Run deleted successfully.")
            return redirect("app:runs", model_name=model.model_name, data_name=project.data_name)
        else:
            messages.error(request, "You are not allowed to delete this run.")
            return redirect("app:models")
    except AIModel.DoesNotExist:
        messages.error(request, "Model does not exist.")
        return redirect("app:models")
    except Project.DoesNotExist:
        messages.error(request, "Project does not exist.")
        return redirect("app:projects", model_name=model.model_name)
    except Run.DoesNotExist:
        messages.error(request, "Run does not exist.")
        return redirect("app:runs", model_name=model.model_name, data_name=project.data_name)


@login_required(login_url='app:login')
def run_details_page(request, model_name, data_name, run_id):
    """
    Show details of a run if it belongs to current user otherwise show proper error messages
    :param request:
    :param model_name:
    :param data_name:
    :param run_id:
    :return:
    """
    try:
        model = AIModel.objects.get(model_name=model_name)
        project = model.project_set.get(data_name=data_name)
        run = project.run_set.get(id=run_id)
        if model.user == request.user:
            return render(request=request,
                          template_name="app/run_details.html",
                          context={"model_name": model.model_name, "data_name": project.data_name,
                                   "run": run})
        else:
            messages.error(request, "You are not allowed to view this model.")
            return redirect("app:models")
    except AIModel.DoesNotExist:
        messages.error(request, "Model does not exist.")
        return redirect("app:models")
    except Project.DoesNotExist:
        messages.error(request, "Project does not exist.")
        return redirect("app:projects", model_name=model.model_name)
    except Run.DoesNotExist:
        messages.error(request, "Run does not exist.")
        return redirect("app:runs", model_name=model.model_name, data_name=project.data_name)
