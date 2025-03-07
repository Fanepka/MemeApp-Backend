
# 🎭 Meme App (Backend) 🚀

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Это серверная часть приложения для обмена мемами и фотографиями. Проект написан на Python с использованием FastAPI и SQLite3. В будущем планируется переход на PostgreSQL для улучшения производительности и масштабируемости. 🛠️

---

## 📚 Оглавление

1. [Описание](#-описание)
2. [Технологии](#-технологии)
3. [Установка и запуск](#-установка-и-запуск)
4. [API Endpoints](#-api-endpoints)
5. [Структура проекта](#-структура-проекта)
6. [Лицензия](#-лицензия)

---

## 📝 Описание

Проект представляет собой REST API для приложения, где пользователи могут:
- 📝 Регистрироваться и авторизоваться.
- 🖼️ Создавать посты с текстом и изображениями.
- ❤️ Лайкать и комментировать посты.
- � Создавать сообщества и присоединяться к ним.
- 🔔 Получать уведомления о новых событиях.

---

## 🛠️ Технологии

- **Python** 🐍 — основной язык программирования.
- **FastAPI** ⚡ — фреймворк для создания API.
- **SQLite3** 🗄️ — временная база данных для хранения информации (в будущем будет заменена на PostgreSQL).
- **SQLAlchemy** 🔧 — ORM для работы с базой данных.
- **Pydantic** 📄 — валидация данных.
- **JWT** 🔐 — аутентификация пользователей.

---

## 🚀 Установка и запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/your-username/meme-app-backend.git
cd meme-app-backend
```

### 2. Установи зависимости

Убедись, что у тебя установлен Python 3.8 или выше. Затем установи зависимости:

```bash
pip install -r requirements.txt
```

### 3. Настрой базу данных

SQLite3 автоматически создаст файл базы данных `meme_app.db` при первом запуске сервера. В будущем планируется переход на PostgreSQL для улучшения производительности и масштабируемости. 🚀

### 4. Запусти сервер

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000). 🌐

---

## 📡 API Endpoints

### 🔐 Аутентификация

- **POST /auth/register** — регистрация нового пользователя.
- **POST /auth/login** — вход и получение токена.
- **POST /auth/refresh-token** — обновление токена.
- **POST /auth/logout** — выход из системы.

### 👤 Пользователи

- **GET /users/me** — информация о текущем пользователе.

### 📄 Посты

- **GET /posts** — список всех постов.
- **POST /posts** — создание нового поста.
- **POST /posts/{post_id}/like** — лайк поста.
- **POST /posts/{post_id}/comment** — добавление комментария.

### � Сообщества

- **GET /communities** — список всех сообществ.
- **POST /communities** — создание нового сообщества.
- **POST /communities/{community_id}/join** — присоединение к сообществу.

### 🔔 Уведомления

- **GET /notifications** — список уведомлений для текущего пользователя.

---

## 🗂️ Структура проекта

```
meme-app-backend/
├── .env
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
├── auth.py
├── requirements.txt
└── README.md
```

- **main.py** — точка входа в приложение.
- **models.py** — модели базы данных.
- **schemas.py** — схемы для валидации данных.
- **crud.py** — функции для работы с базой данных.
- **database.py** — настройка подключения к базе данных.
- **auth.py** — логика аутентификации.
- **requirements.txt** — список зависимостей.

---

## 📜 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE). 📄