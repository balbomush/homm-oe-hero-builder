# HoMM Olden Era — Hero Configurator

Универсальный конфигуратор билда для **Heroes of Might and Magic: Olden Era**: выберите фракцию и тип героя (Might / Magic), соберите колесо из 8 навыков, поднавыки, подкласс, синергии и калькулятор необходимого уровня. Интерфейс на **русском и английском**.

**Демо (GitHub Pages):** https://balbomush.github.io/homm-oe-hero-builder/

**Шаринг билда:** кнопка «Ссылка на билд» или URL вида `https://balbomush.github.io/homm-oe-hero-builder/#<hash>`

## Возможности

- Абстрактный герой: фракция + Might / Magic (без пресет-героев)
- Skill Wheel: Basic / Advanced / Expert и поднавыки (центр — фракционный навык)
- Синергии: активные, почти активные, возможные и неактивные (с подсветкой)
- Калькулятор уровня: минимальный уровень героя и путь левелапов
- Трекер подкласса (5 навыков на Expert)
- Экспорт / импорт JSON и шаринг через URL

## Локальный запуск

Откройте `index.html` в браузере. Все скрипты подключаются локально, сервер не нужен.

## Проверка данных wiki

Локальные HTML-выгрузки с официальной вики лежат в папке `rared html/` (не в git). Проверка полноты:

```powershell
python scripts/check_wiki_html_completeness.py
```

## Структура

| Файл | Назначение |
|------|------------|
| `index.html` | Точка входа для сайта |
| `hero-builder-app.js` | Логика интерфейса |
| `hero-builder-core.js` | Логика билда (слоты, синергии, уровень) |
| `hero-builder-data.js` | Навыки, классы, подклассы |
| `hero-builder-synergies.js` | Синергии навыков |
| `hero-builder-i18n.js` | Переводы EN / RU |
| `scripts/check_wiki_html_completeness.py` | Read-only проверка wiki HTML |
| `HoMM_Olden_Era_Skills.md` | Справочник навыков |
| `DOCUMENTATION.md` | Полное описание данных и источников |

## Обновление данных

Подробности — в [DOCUMENTATION.md](DOCUMENTATION.md). Кратко: правки вносятся в JS/MD-файлы, затем `git push`; GitHub Pages обновится через 1–2 минуты.

## Источники

Официальная вики Hooded Horse, olden-era.com и материалы сообщества. Полный список — в [DOCUMENTATION.md](DOCUMENTATION.md).

## Лицензия

Фан-проект. Heroes of Might and Magic — торговая марка Ubisoft / Hooded Horse. Данные собраны из открытых источников для некоммерческого использования.
