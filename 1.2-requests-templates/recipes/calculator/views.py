from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# def recipe(request, dish, servings=1):
#     recipe_data = DATA.get(dish)

#     if recipe_data:
#         context = {'recipe': {}}
#         for ingredient, amount in recipe_data.items():
#             context['recipe'][ingredient] = amount * servings
#         context['dish'] = dish
#         return render(request, 'calculator/index.html', context)
#     else:
#         return HttpResponse('Рецепт не найден', status=404)

# def home(request):
#     return render(request, 'calculator/index.html', context={})


def recipe(request, dish=None):
    if dish:
        servings = request.GET.get('servings', 1)
        try:
            servings = int(servings)
            if servings <= 0:
                servings = 1
        except ValueError:
            servings = 1

        recipe_data = DATA.get(dish)

        if recipe_data:
            context = {'recipe': {}}
            for ingredient, amount in recipe_data.items():
                context['recipe'][ingredient] = amount * servings
            context['dish'] = dish
            return render(request, 'calculator/index.html', context) # Изменено здесь
        else:
            return HttpResponse('Рецепт не найден', status=404)
    else:
        context = {'recipe': list(DATA.keys())}
        return render(request, 'calculator/index.html', context) # Изменено здесь
    
