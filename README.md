# Job Search Automation

Автоматизований пошук вакансій з AI-аналізом та веб-дашбордом.

<img width="1118" height="872" alt="image" src="https://github.com/user-attachments/assets/e3a4bb91-7e83-4b4b-8fec-1ad3124444c4" />

## Що робить

- Моніторить українські job-борди (Djinni, DOU, Work.ua) кожні 2 години
- AI аналізує кожну вакансію під ваш профіль (скор відповідності 1-10)
- Автоматично пропускає нерелевантні вакансії (скор ≤ 2)
- Безкоштовно: використовує Groq API (Llama 3.3 70B) для аналізу

## Веб-дашборд

Mobile-first інтерфейс у стилі [Linear](https://linear.app) design system з повним набором інструментів:

- **Дизайн-система Linear** — Inter шрифт, indigo-violet акценти, translucent бордери, luminance-based elevation
- **Фільтри** — All, Hot (6+), OK (4-5), Skip (<4), New, Favorites, Notes, Pipeline
- **Розумний пошук** — AND-логіка по словах з підсвіткою збігів, клавіша `/` для фокусу
- **Сортування** — за замовчуванням, за скором, за датою
- **Два режими відображення** — Card (повні картки) та List (компактний список), клавіша `v`
- **Статистика** — панель з кількістю вакансій, середнім балом, розподілом оцінок, джерелами
- **★ Обране** — збереження цікавих вакансій з фільтром та лічильником
- **Pipeline** — трекінг статусу відгуків (Applied → Interview → Offer → Rejected)
- **Нотатки** — текстові нотатки до кожної вакансії (контакти, враження, дати)
- **Свіжість вакансій** — кольорове кодування дат (зелений→сірий→жовтий→червоний), приглушення застарілих
- **Сховати застарілі** — toggle для повного приховування вакансій >14 днів, клавіша `h`
- **Клавіатурна навігація** — j/k, Enter, o, f, s, n, x, v, h, /, ? для швидкого перегляду
- **Розумне оновлення** — toast-нотифікації про нові вакансії замість мовчазного перерендеру
- **Динамічний заголовок** — лічильник нових вакансій у вкладці браузера `(N) Job Search`
- **Експорт CSV** — вивантаження всіх вакансій з оцінками, статусами та нотатками
- **Changelog** — окрема сторінка з історією автоматичних покращень

Всі дані користувача (обране, pipeline, нотатки) зберігаються в localStorage браузера.

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
  changelog.html     # Сторінка історії змін
  check_new.py       # Скрапер вакансій (cron)
  analyze_new.py     # AI аналізатор (Groq)
  ensure_server.sh   # Автоперевірка та перезапуск сервера (cron)
  nightly.sh         # Нічний цикл автопокращень
  profile.md         # Автогенерований з конфігу
  vacancies.md       # Список вакансій (оновлюється автоматично)
  analyses.json      # Результати AI аналізу
  changelog.md       # Лог автоматичних покращень
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

## Автоматичне обслуговування

Проект включає систему автоматичних нічних покращень через Claude Code:

- `nightly.sh` запускається о 3:00 через cron
- `ensure_server.sh` перевіряє та перезапускає сервер о 2:53
- Кожну ніч Claude Code аналізує стан проекту і вносить одне покращення
- За 17 днів автоматично реалізовано 18 покращень (пошук, статистика, обране, pipeline, нотатки, CSV експорт, клавіатурна навігація, Linear дизайн-система та інше)
- Всі зміни логуються в `changelog.md` та відображаються на сторінці `/changelog`

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
              │  app.py   │ Flask веб-сервер (:8080)
              │           │
              └─────┬─────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
    index.html  changelog  /api/vacancies
    (дашборд)   (історія)  (REST API)
```

## Розгортання за допомогою Claude Code

Якщо у вас є [Claude Code](https://claude.ai/claude-code), ви можете розгорнути все за допомогою промптів:

```bash
ssh user@your-server
claude
```

Вставте:
```
Склонуй репозиторій https://github.com/denysosadchyi/job-searcher.git
в ~/job-search. Відредагуй config.py під мій профіль:

- Ім'я: [ВАШЕ ІМ'Я]
- Роль: [ВАША РОЛЬ]
- Досвід: [РОКІВ]
- Зарплата: [ДІАПАЗОН]
- Шукаю: [ЩО ШУКАЄТЕ]
- Не цікавить: [ЩО НЕ ЦІКАВИТЬ]
- Groq API ключ: [КЛЮЧ]

Після редагування запусти setup.py, потім check_new.py,
потім налаштуй systemd сервіс для веб-сервера на порту 8080
і cron для автоперевірки кожні 2 години.
```

## Вимоги

- Python 3.8+
- Flask (`pip install flask`)
- Groq API ключ (безкоштовно: https://console.groq.com)
- Linux сервер (рекомендовано Ubuntu) для моніторингу 24/7

## Ліцензія

MIT. Використовуйте вільно.
