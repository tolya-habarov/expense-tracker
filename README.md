# Expense tracker
Учет личных расходов на Django.  
*Проект на стадии MVP*.  

<br>

**Возможности**:
- Добавить/редактировать/удалить счет
- Добавить/редактировать/удалить запись об операции
- Поиск по операциям
- Просмотр операций по месяцам  

<br>

**Запуск**:  
`git clone https://github.com/tolya-maximum/expense-tracker.git`  
`cd expense-tracker`  
`python3 -m venv .venv`  
`source .venv/bin/activate`  
`python3 manage.py migrate`  
`python3 manage.py createdata`  
`python3 manage.py runserver`  

После открыть в браузере http://127.0.0.1:8000/.  
Логин: test_user  
Пароль: test