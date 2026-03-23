# Job Search Automation

Автоматизований пошук вакансій з AI-аналізом та веб-дашбордом.
<img width="855" height="585" alt="image" src="https://github.com/user-attachments/assets/68352b33-3946-483f-be53-8d3d77421b20" />


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

## Розгортання за допомогою Claude Code (найпростіший спосіб)

Якщо у вас є [Claude Code](https://claude.ai/claude-code), ви можете розгорнути все за допомогою промптів. Claude Code сам напише код, налаштує сервер, cron та все інше.

### Що потрібно

- Ubuntu сервер (або будь-який Linux з SSH доступом)
- Встановлений Claude Code (`npm install -g @anthropic-ai/claude-code`)
- Groq API ключ (безкоштовно: https://console.groq.com)

### Крок 1: Підключіться до сервера

Зайдіть по SSH на ваш сервер та запустіть Claude Code:

```bash
ssh user@your-server
claude
```

### Крок 2: Скопіюйте цей промпт і вставте в Claude Code

```
Склонуй репозиторій https://github.com/denysosadchyi/job-searcher.git
в ~/job-search. Відредагуй config.py під мій профіль:

- Ім'я: [ВАШЕ ІМ'Я]
- Роль: [ВАША РОЛЬ, наприклад "Senior Python Developer"]
- Досвід: [РОКІВ ДОСВІДУ]
- Зарплата: [ДІАПАЗОН, наприклад "$3000-5000"]
- Шукаю: [ЩО ШУКАЄТЕ, наприклад "remote, product company, B2B SaaS"]
- Не цікавить: [ЩО НЕ ЦІКАВИТЬ, наприклад "outsource, gambling, crypto"]
- Ключовий досвід: [ВАШІ ГОЛОВНІ ДОСЯГНЕННЯ, 3-5 пунктів]

Groq API ключ: [ВАШ КЛЮЧ]

Після редагування запусти setup.py, потім check_new.py,
потім налаштуй systemd сервіс для веб-сервера на порту 8080
і cron для автоперевірки кожні 2 години.
```

### Крок 3: Перевірте результат

Скажіть Claude Code:

```
Покажи скільки вакансій знайшлось і запусти веб-сервер.
Яка IP адреса сервера?
```

### Додаткові промпти для Claude Code

**Додати нове джерело вакансій:**
```
Додай моніторинг вакансій з [САЙТ]. Парси сторінку [URL],
знаходь нові вакансії і додавай в vacancies.md з аналізом.
```

**Змінити критерії фільтрації:**
```
Зміни фільтр вакансій: пропускай все що нижче 4/10.
Додай в критерії скорингу що я шукаю тільки remote позиції
в product компаніях.
```

**Налаштувати Telegram сповіщення:**
```
Коли check_new.py знаходить нову вакансію зі скором 7+,
надсилай повідомлення в мій Telegram бот.
Bot token: [ТОКЕН], Chat ID: [ID].
```

**Проаналізувати конкретну вакансію:**
```
Проаналізуй цю вакансію під мій профіль: [URL ВАКАНСІЇ]
```

**Оновити профіль:**
```
Прочитай мій config.py та оновити profile.md.
Додай що я тепер маю досвід з [НОВА ТЕХНОЛОГІЯ/НАВИЧКА].
```

**Подивитись статистику:**
```
Покажи статистику: скільки вакансій знайдено за останній тиждень,
середній скор, топ-5 найкращих вакансій.
```

**Зробити бекап:**
```
Зроби бекап analyses.json та vacancies.md на /mnt/ssd/backup/
з датою в назві файлу.
```

## Ліцензія

MIT. Використовуйте вільно.
