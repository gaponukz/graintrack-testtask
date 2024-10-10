# graintrack-testtask

## Задача: Розробити REST API для інтернет-магазину.
Задача кандидату - самостійно спроектувати структуру обʼєктів.

### Вимоги до реалізації:
API має підтримувати операції:
- отримання списку товарів
- фільтр товарів за категоріями, підкатегоріями
- додавання товару
- зміна ціни
- старт акції (процент знижки)
- видалення товару
- резервування товару
- скасування резерву
- продажа товару
- звіт про товари що були продані можливими фільтрами

### Додатково:
- Кожен товар має бути в відповіді тільки якщо вільний залишок > 0.
- Користувачі можуть резервувати, відміняти бронювання і купувати.
- При резервування вільний залишок товару має зменшитись.
- При відміні резервування вільний залишок товару має збільшитись.
- Необхідно використовувати відповідні HTTP статуси і коди обробки помилок (404, 400, 403 ітд)
- README файл з описом методів

### Буде плюсом:
- Використання swagger для опису операцій API
- посторінкова навигація в списках

### Инструменты и технологии:
довільні

### Требования к исходному коду
- Проект має бути організовано відповідно до принципів предметно-орієнтованого програмування (DDD)
- Проект має бути опубліковано в публічному GitHub
- За історією commit'ів має бути видно самостійно розробку кандидата.

### Критерії оцінювання тестового завдання
- Відповідність DDD:
- нормалізация даних
- Чистота кода
- читаемость кода и его структурированность
- ефективність реалізації
- відсутність зайвого коду та дублювання
- зберігання code-style по всьому проекту
- Структура даних:
- Робота усіх методів API

## Методи API
soon...
