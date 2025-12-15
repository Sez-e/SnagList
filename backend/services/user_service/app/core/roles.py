class Roles:
    OBSERVER = "observer"   # Только просмотр
    ENGINEER = "engineer"   # Создание и редактирование дефектов
    MANAGER = "manager"     # Назначение задач и отчёты
    ADMIN = "admin"         # Управление пользователями

    ALL = {OBSERVER, ENGINEER, MANAGER, ADMIN}
