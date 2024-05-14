from functools import wraps
from django.shortcuts import redirect

def user_type_required(allowed_user_types):
    """
    Декоратор для ограничения доступа к представлениям в зависимости от типа пользователя.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('404')  # Перенаправляем на страницу входа, если пользователь не аутентифицирован

            # Получаем тип пользователя из его профиля или другого места
            user_type = request.user.user_type

            # Проверяем, имеет ли пользователь необходимые права доступа
            if user_type not in allowed_user_types:
                return redirect('404')  # Перенаправляем на страницу отказа в доступе

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
