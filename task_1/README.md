# Solution for the task 1

## Task

https://docs.google.com/document/d/1HSSnsVXZ0pigNSo9aFerq5sFD7BvWsxp/edit

## Solution

### 1.
Ошибка на сервере принявшем запрос. Нужно смотреть логи сервера.
Если веб сервер находится за reverse proxy, то нужно начинать с reverse proxy.

### 2.

1. При выполнении handlers.append() лямбда функция выполнится и в массив будет 
добавлено значение, а нам нужно добавить функцию (объект функции).
Для этого сделаем декоратор make_handler, который возвращает обернутую функцию, 
в теле которой вызов оригинальной функции с нужным значения параметра (param).
И затем будем добавлять в массив уже обернутую функцию.
2. Рекомендуется использовать list comprehension, везде где уместно. Исполняется быстрее чем c append. 
3. Теряется результат выполнения обработчика в execute_handlers.

```python
from typing import Callable, Any


def create_handlers(callback: Callable) -> list[Callable]:
    # Make a new handler with decorator
    def make_handler(original_func: Callable, param: int):
        def new_handler() -> Any:
            return original_func(param)
        return new_handler

    # Adding handlers per each step (from 0 to 4)
    handlers: list = [
        make_handler(callback, step)
        for step in range(5)
    ]
    return handlers


def execute_handlers(handlers: list[Callable]) -> list[Any]:
    # start added handlers (steps from 0 to 4)
    results: list = [
        handler()
        for handler in handlers
    ]
    return results
```

### 3.

File [lab1_3.py](lab1_3.py) in this folder.

### 4.

```python
def get_ip() -> None | str:
    url = "https://ifconfig.me"
    headers = {
        "user-agent": "curl",
    }
    try:
        response = requests.get(url=url, headers=headers)
    except:
        return None
    if response and (response.status_code == 200):
        return response.text
    return None
```

### 5.

```python
def comparison(ver_a: str, ver_b: str) -> int:
    if not ver_a and ver_b:
        return -1
    if ver_a and not ver_b:
        return 1
    if not ver_a and not ver_b:
        return 0

    a = [int(item) for item in ver_a.split('.')]
    b = [int(item) for item in ver_b.split('.')]
    min_len = min(len(a), len(b))
    for i in range(min_len):  
        if a[i] > b[i]:
            return 1
        elif a[i] < b[i]:
            return -1
    max_len = max(len(a), len(b))
    for i in range(min_len, max_len):
        if len(a) > min_len:
            if a[i] > 0:
                return 1
        else:
            if b[i] > 0:
                return -1
    return 0
```