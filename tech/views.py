from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from .models import Request, WorkAssignment, Comment
from .forms import WorkAssignmentForm, RequestForm, UserRequestForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def index(request):
    return render(request, template_name='base.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'admin'


def is_ispolnitel(user):
    return user.is_authenticated and user.userprofile.role == 'ispolnitel'


def is_user(user):
    return user.is_authenticated and user.userprofile.role == 'user'


def is_user_or_admin(user):
    return is_user(user) or is_admin(user)


@login_required(login_url='login')
@user_passes_test(is_ispolnitel, login_url='login')
def job_list(request):
    jobs = WorkAssignment.objects.filter(assigned_to=request.user.userprofile)
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required(login_url='login')
def request_list(request):
    if request.user.userprofile.role == 'admin':
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(client=request.user.userprofile)

    search_query = request.GET.get('search_query')
    if search_query:
        requests = requests.filter(
            Q(number__icontains=search_query) |
            Q(equipment__name__icontains=search_query) |
            Q(issue_type__name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(client__user__username__icontains=search_query)
        )

    return render(request, 'request_list.html', {'requests': requests})


@login_required(login_url='login')
def request_detail(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)

    if not (
            request.user.userprofile.role == 'admin' or
            request.user.userprofile == request_obj.client or
            (
                    request.user.userprofile.role == 'ispolnitel' and request_obj.workassignment.assigned_to == request.user.userprofile)
    ):
        raise Http404("Заявка не найдена")

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')
        if comment_text:
            Comment.objects.create(request=request_obj, author=request.user.userprofile, text=comment_text)
            return HttpResponseRedirect(request.path)

    comments = request_obj.comments.all()

    return render(request, 'request_detail.html', {'request': request_obj, 'comments': comments})


@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user.is_authenticated and (
            request.user.userprofile.role == 'admin' or request.user.userprofile == comment.request.client or (
            request.user.userprofile.role == 'ispolnitel' and comment.request.workassignment.assigned_to == request.user.userprofile)):
        comment.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def assign_work(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)

    try:
        work_assignment = request_obj.workassignment
    except WorkAssignment.DoesNotExist:
        work_assignment = WorkAssignment(request=request_obj)

    if request.method == 'POST':
        form = WorkAssignmentForm(request.POST, instance=work_assignment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request_obj.get_absolute_url())
    else:
        form = WorkAssignmentForm(instance=work_assignment)

    return render(request, 'assign_work.html', {'form': form, 'request_obj': request_obj})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def delete_request(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)
    request_obj.delete()
    return redirect('index')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def delete_work_assignment(request, request_pk):
    work_assignment = get_object_or_404(WorkAssignment, request__pk=request_pk)
    work_assignment.delete()
    return redirect('request_detail', pk=work_assignment.request.pk)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def edit_request(request, pk):
    request_obj = get_object_or_404(Request, pk=pk)

    if request.method == 'POST':
        form = RequestForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            return redirect('request_detail', pk=pk)
    else:
        form = RequestForm(instance=request_obj)

    return render(request, 'edit_request.html', {'form': form, 'request_obj': request_obj})


@login_required(login_url='login')
@user_passes_test(is_user_or_admin, login_url='login')
def create_request(request):
    form = UserRequestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.client = request.user.userprofile
            request_instance.save()
            return redirect('request_list')

    return render(request, 'create_request.html', {'form': form})
