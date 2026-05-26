# HoMM Olden Era — Hero Builder

Интерактивный конструктор героя для **Heroes of Might and Magic: Olden Era**: колесо из 8 навыков, поднавыки, специализации, подклассы, синергии и планировщик левелапов. Интерфейс на **русском и английском**.

**Демо (GitHub Pages):** https://balbomush.github.io/homm-oe-hero-builder/

## Возможности

- 108 героев (6 фракций × 18)
- Skill Wheel: Basic / Advanced / Expert и поднавыки
- Трекер подкласса (5 навыков на Expert)
- Панель синергий между навыками
- Симулятор выбора навыков при левелапе
- Экспорт и импорт билда в JSON

## Локальный запуск

Откройте `index.html` в браузере. Все скрипты подключаются локально, сервер не нужен.

## Структура

| Файл | Назначение |
|------|------------|
| `index.html` | Точка входа для сайта |
| `hero-builder-app.js` | Логика интерфейса |
| `hero-builder-data.js` | Навыки, классы, подклассы |
| `hero-builder-heroes.js` | 108 героев |
| `hero-builder-synergies.js` | Синергии навыков |
| `hero-builder-i18n.js` | Переводы EN / RU |
| `HoMM_Olden_Era_Skills.md` | Справочник навыков |
| `DOCUMENTATION.md` | Полное описание данных и источников |

## Обновление данных

Подробности — в [DOCUMENTATION.md](DOCUMENTATION.md). Кратко: правки вносятся в JS/MD-файлы, затем `git push`; GitHub Pages обновится через 1–2 минуты.

## Источники

Официальная вики Hooded Horse, Fandom, olden-era.com и материалы сообщества. Полный список — в [DOCUMENTATION.md](DOCUMENTATION.md).

## Лицензия

Фан-проект. Heroes of Might and Magic — торговая марка Ubisoft / Hooded Horse. Данные собраны из открытых источников для некоммерческого использования.
