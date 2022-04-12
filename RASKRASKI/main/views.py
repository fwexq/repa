from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *
from .models import *
from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin




class Index(DataMixin, ListView):
    model = picture
    template_name = 'main/index.html'
    context_object_name = 'pictures'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['cat_selected'] = 0
        #context['title'] = 'Главная страница'
        c_def = self.get_user_context(title='Главная')

        return context|c_def


# СТАРОЕ ОТОБРАЖЕНИЕ ГЛАВНОЙ СТРАНИЦЫ С ПОМОЩЬЮ ФУНКЦИИ
# def index(request):
#     pictures = picture.objects.all()
#     #cats = Category.objects.all()
#     context = {
#         'title': 'Главная страница сайта',
#         #'cats': cats,
#         'pictures': pictures,
#         'cat_selected': 0
#     }
#     return render(request, 'main/index.html', context)




class create(DataMixin, CreateView):
    form_class = pictureForm
    template_name = 'main/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание поста')
        return context | c_def

# def create(request):
#    if request.method == 'POST':
#        form = pictureForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            return redirect('home')
#    else:
#         form = pictureForm()
#    context = {
#        'title': 'Создание поста',
#        'form': form,
#    }
#    return render(request, 'main/create.html', context)



class show_category(DataMixin, ListView):
    model = picture
    template_name = 'main/category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return picture.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                                                  cat_selected=context['posts'][0].cat_id)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id
        return context | c_def



# class Search(ListView):
#     model = picture
#     template_name = 'main/search_results.html'
#     context_object_name = 'object_list'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = picture.objects.filter(
#             Q(title__icontains=query) | Q(opisanie__icontains=query)
#         )
#         return object_list


# class Search(ListView):
#     model = picture
#     template_name = 'search_results.html'
#     def get_queryset(self):
#         return picture.objects.filter(title__contains=self.request.GET['q'])
#
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['q'] = self.request.GET.get['q']
#         return context



class Search(ListView):
    model = picture
    template_name = 'main/search_results.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return picture.objects.filter(title__icontains=self.request.GET['q'])


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET['q']
        return context

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Создание поста')
        return context | c_def


    def form_valid(self, form):      #Для перенаправления пользователдя после регистрации
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'


    def get_user_context(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return c_def | context

    def get_success_url(self):
        return reverse_lazy('home')



def logoutuser(request):
    logout(request)
    return redirect('login')


#  СТАРОЕ ОТОБРАЖЕНИЕ КАТЕГОРИЙ С ПОМОЩЬЮ ФУНКЦИИ
# def show_category(request, cat_slug):
#    #return HttpResponse(f"Отображение категории с id = {cat_id}")
#    с = Category.objects.get(slug=cat_slug)
#    posts = с.picture_set.all()
#    #cats = Category.objects.all()
#    context = {
#        #'cats': cats,
#        'posts': posts,
#        'title': 'Отображение по рубрикам',
#        'cat_selected': cat_slug,
#    }
#    return render(request, 'main/category.html', context=context)




#{% block content%} <br><br><br>Текст</br></br></br>
#    {% for el in pictures %}
#        <div class="alert alert-warning mt-2">
#                <h3>{{el.title}}</h3>
#            {% if el.photo %}
#                <p><img class="img-article-left thumb" src="{{el.photo}}"></p>
#            {% endif %}
#        </div>
#    {% endfor %}
#{% endblock%}

#ятебялюблююююююююююююююююююююююююююююююююююююююююю




#{% for m in menu %}
#	{% if not forloop.last %}
#			<li><a href="{% url m.url_name %}">{{m.title}}</a></li>
#	{% else %}
#			<li class="last"><a href="{% url m.url_name %}">{{m.title}}</a></li>
#	{% endif %}
#{% endfor %}
#
#
# {% if cat_selected == 0 %}
# 		<li class="selected">Все категории</li>
# {% else %}
# 		<li><a href="{% url 'home' %}">Все категории</a></li>
# {% endif %}

# {% for c in cats %}
# 	{% if c.pk == cat_selected %}
# 		<li class="selected">{{c.name}}</li>
# 	{% else %}
# 		<li><a href="{{ c.get_absolute_url }}">{{c.name}}</a></li>
# 	{% endif %}
# {% endfor %}





#
# {% load main_tags%}
#
# <!doctype html>
# <html lang="ru">
# <head>
#     <title>{% block title%}{% endblock%}</title>
# <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
# </head>
# <body>
#
#        <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
#     <div class="container-fluid">
#       <a class="navbar-brand" href="{% url 'home' %}">ВСЕ ФИЛЬМЫ</a>
#       <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
#         <span class="navbar-toggler-icon"></span>
#       </button>
#       <div class="collapse navbar-collapse" id="navbarCollapse">
#         <ul class="navbar-nav me-auto mb-2 mb-md-0">
#            <li class="nav-item">
#
#
#
#
#           <li class="nav-item">
#             <a class="nav-link" href="{% url 'create'%}">Создание поста</a>
#           </li>
#           <li class="nav-item">
#             <a class="nav-link disabled">Авторизация</a>
#           </li>
#         </ul>
#         <form class="d-flex">
#           <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
#           <button class="btn btn-outline-success" type="submit">Искать</button>
#         </form>
#       </div>
#     </div>
#
#
#   </nav>
#         </form>
#       </div>
#     </div>
#   </nav>
# </header>
#
#          <div class="container">
#               {% block content%}{% endblock%}
#          </div>
#
# </body>
# </html>




# {% for el in pictures %}
#     <div class="alert alert-warning mt-2">
#         <h3>{{el.title}}</h3>
#         <h3>{{el.opisanie}}</h3>
#             {% if el.photo %}
#             <p><img class="img-article-left thumb" src="{{el.photo.url}}"></p>
#         {% endif %}
#
#
#         </div>
#     {% endfor %}

#     < form
#     action = "{% url 'search' %}"
#     method = "get" >
#     < input
#
#     class ="form-control me-2" type="search" placeholder="Search" name='q' aria-label="Search" >
#
#     < button
#
#     class ="btn btn-outline-success" type="submit" value="search" > Искать < / button >
#
# < / form >
