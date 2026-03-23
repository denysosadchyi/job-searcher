# Job Search Automation

Автоматизований пошук вакансій з AI-аналізом та веб-дашбордом.

## Що робить

- Моніторить українські job-борди (Djinni, DOU, Work.ua) кожні 2 години
- AI аналізує кожну вакансію під ваш профіль (скор відповідності 1-10)
- Веб-дашборд з фільтрами, пошуком та видаленням (mobile-first)
- Автоматично пропускає нерелевантні вакансії (скор <= 2)
- Безкоштовно: використовує Groq API (Llama 3.3 70B) для аналізу

## Швидкий старт (5 хвилин)

### 1. Клонуйте та відредагуйте конфіг

```bash
git clone https://github.com/denysosadchyi/job-searcher.git ~/job-search
cd ~/job-search
nano config.py    # <-- Впишіть СВІЙ профіль, ключові слова, зарплату тощо
```

### 2. Отримайте безкоштовний Groq API ключ

1. Зареєструйтесь на https://console.groq.com
2. Створіть API ключ
3. Впишіть його в `config.py` → `GROQ_API_KEY`

### 3. Запустіть налаштування

```bash
python3 setup.py
```

Це створить:
- `profile.md` з вашого конфігу
- `vacancies.md` з пошуковими URL
- Запропонує налаштувати systemd (веб-сервер) та cron (автоперевірка)

### 4. Перший запуск

```bash
python3 check_new.py     # Знайти вакансії
python3 analyze_new.py   # Проаналізувати AI
```

### 5. Відкрийте дашборд

```
http://IP_ВАШОГО_СЕРВЕРА:8080
```

## Що змінити в config.py

| Секція | Що змінити |
|---|---|
| `PROFILE` | Ваше ім'я, цільова роль, досвід, діапазон зарплати |
| `TARGET` | Що шукаєте (буллет-поінти) |
| `NOT_INTERESTED` | Що не цікавить |
| `FIT_CRITERIA` | Таблиця скорингу для AI |
| `KEY_EXPERIENCE` | Ваші досягнення для порівняння |
| `SEARCH_KEYWORDS` | Пошукові запити для job-бордів |
| `TITLE_KEYWORDS` | Слова, які мають бути в назві вакансії |
| `SOURCES` | URL job-бордів (змініть пошукові запити!) |
| `GROQ_API_KEY` | Ваш безкоштовний ключ з console.groq.com |

## Структура файлів

```
job-search/
  config.py          # <-- ВАШІ налаштування (редагуйте це!)
  setup.py           # Запустити раз після редагування конфігу
  app.py             # Веб-сервер (Flask)
  index.html         # UI дашборду
  check_new.py       # Скрапер вакансій (cron)
  analyze_new.py     # AI аналізатор (Groq)
  profile.md         # Автогенерований з конфігу
  vacancies.md       # Список вакансій (оновлюється автоматично)
  analyses.json      # Результати AI аналізу
  check.log          # Лог скрапера
```

## Приклади config.py для різних ролей

### Python Developer
```python
SEARCH_KEYWORDS = ["python developer", "backend developer", "django"]
TITLE_KEYWORDS = ["python", "backend", "django", "developer"]
SOURCES = {
    "Djinni": {"enabled": True, "url": "https://djinni.co/jobs/keyword-python/"},
    "DOU": {"enabled": True, "url": "https://jobs.dou.ua/vacancies/?search=Python+Developer"},
    "Work.ua": {"enabled": True, "url": "https://www.work.ua/en/jobs-python+developer/"},
}
```

### UI/UX Designer
```python
SEARCH_KEYWORDS = ["ux designer", "ui designer", "product designer"]
TITLE_KEYWORDS = ["design", "ux", "ui", "product design"]
SOURCES = {
    "Djinni": {"enabled": True, "url": "https://djinni.co/jobs/keyword-ui_ux/"},
    "DOU": {"enabled": True, "url": "https://jobs.dou.ua/vacancies/?search=UI/UX+Designer"},
    "Work.ua": {"enabled": True, "url": "https://www.work.ua/en/jobs-ui+ux+designer/"},
}
```

### DevOps Engineer
```python
SEARCH_KEYWORDS = ["devops", "sre", "platform engineer"]
TITLE_KEYWORDS = ["devops", "sre", "platform", "infrastructure", "cloud"]
SOURCES = {
    "Djinni": {"enabled": True, "url": "https://djinni.co/jobs/keyword-devops/"},
    "DOU": {"enabled": True, "url": "https://jobs.dou.ua/vacancies/?search=DevOps"},
    "Work.ua": {"enabled": True, "url": "https://www.work.ua/en/jobs-devops/"},
}
```

### Data Analyst
```python
SEARCH_KEYWORDS = ["data analyst", "bi analyst", "analytics"]
TITLE_KEYWORDS = ["data", "analyst", "analytics", "bi"]
SOURCES = {
    "Djinni": {"enabled": True, "url": "https://djinni.co/jobs/keyword-data+analyst/"},
    "DOU": {"enabled": True, "url": "https://jobs.dou.ua/vacancies/?search=Data+Analyst"},
    "Work.ua": {"enabled": True, "url": "https://www.work.ua/en/jobs-data+analyst/"},
}
```

### Project Manager
```python
SEARCH_KEYWORDS = ["project manager", "product manager", "scrum master"]
TITLE_KEYWORDS = ["project", "product", "manager", "scrum", "agile"]
SOURCES = {
    "Djinni": {"enabled": True, "url": "https://djinni.co/jobs/keyword-project+manager/"},
    "DOU": {"enabled": True, "url": "https://jobs.dou.ua/vacancies/?search=Project+Manager"},
    "Work.ua": {"enabled": True, "url": "https://www.work.ua/en/jobs-project+manager/"},
}
```

## Вимоги

- Python 3.8+
- Flask (`pip install flask`)
- Groq API ключ (безкоштовно: https://console.groq.com)
- Linux сервер (рекомендовано Ubuntu) для моніторингу 24/7
  - Також працює на Mac/Windows для ручного запуску

## Ручні команди

```bash
# Перевірити нові вакансії зараз
python3 check_new.py

# Проаналізувати непроаналізовані вакансії
python3 analyze_new.py

# Запустити веб-сервер вручну
python3 app.py

# Переглянути логи
tail -f check.log
```

## Як це працює

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Djinni.co  │    │   DOU.ua     │    │  Work.ua    │
└──────┬──────┘    └──────┬───────┘    └──────┬──────┘
       │                  │                   │
       └──────────────────┼───────────────────┘
                          │
                   check_new.py (cron кожні 2 год)
                          │
                   ┌──────▼──────┐
                   │ Groq API    │ AI аналіз (безкоштовно)
                   │ Llama 3.3   │
                   └──────┬──────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
        vacancies.md  analyses.json  check.log
              │           │
              └─────┬─────┘
                    │
              ┌─────▼─────┐
              │  app.py   │ Flask веб-сервер
              │  :8080    │
              └─────┬─────┘
                    │
              ┌─────▼─────┐
              │ index.html│ Mobile-first дашборд
              └───────────┘
```

## Ліцензія

MIT. Використовуйте вільно.
