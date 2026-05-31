# HoMM Olden Era Hero Configurator — документация

Полное описание проекта: из чего состоит конфигуратор, откуда взяты данные и как их обновлять.

---

## 1. Назначение проекта

**Hero Configurator** — статический веб-инструмент для планирования билда **абстрактного** героя в *Heroes of Might and Magic: Olden Era* по аналогии с Skill Wheel из Heroes V.

Пользователь выбирает **фракцию** и **тип героя** (Might / Magic), собирает 8 навыков (фракционный — в центре колеса), настраивает поднавыки, отслеживает прогресс к подклассу, видит синергии (активные и потенциальные) и минимальный уровень героя для текущего билда. Билд можно экспортировать в JSON или поделиться ссылкой (hash в URL).

Сайт не требует сервера: только HTML, CSS и JavaScript. Хостинг — [GitHub Pages](https://pages.github.com/).

**Live URL:** https://balbomush.github.io/homm-oe-hero-builder/

**Репозиторий:** https://github.com/balbomush/homm-oe-hero-builder

---

## 2. Архитектура (как файлы связаны)

```
index.html
  ├── hero-builder-i18n.js          ← строки интерфейса EN/RU
  ├── hero-builder-synergies.js     ← пары навыков с эффектом ×2
  ├── hero-builder-data.js          ← навыки, классы, фракции
  ├── hero-builder-display-locale.js← локализация названий навыков
  ├── hero-builder-core.js          ← логика билда (без DOM)
  └── hero-builder-app.js           ← UI (колесо, синергии, уровень, шаринг)
```

### Порядок загрузки важен

1. `HOE_BUILDER_I18N` — переводы  
2. `HOE_BUILDER_SYNERGIES` — синергии  
3. `HOE_BUILDER_DATA` — навыки и классы  
4. `HOE_BUILDER_DISPLAY` — отображение названий RU/EN  
5. `HOE_BUILDER_CORE` — чистая логика  
6. `hero-builder-app.js` — инициализация приложения  

### Справочные материалы (не подключаются к сайту напрямую)

| Файл | Роль |
|------|------|
| `rared html/` | Локальные HTML-выгрузки официальной wiki (read-only, в `.gitignore`) |
| `scripts/check_wiki_html_completeness.py` | Проверка полноты 30 навыков в `rared html/` |
| `HoMM_Olden_Era_Skills.md` | Человекочитаемый справочник всех навыков |
| `homm_oe_heroes_export.json` | Архив данных 108 героев (отдельный pipeline, не используется UI) |
| `build_heroes_json.py` | Скрипт сборки JSON героев (не часть конфигуратора) |
| `build_hero_builder_export.py` | Генерация `hero-builder-synergies.js` из SYNERGIES |

---

## 3. Игровая модель (что отражено в данных)

| Параметр | Значение в конфигураторе |
|----------|--------------------------|
| Слотов навыков | 8 (слот 0 — фракционный, locked) |
| Уровни навыка | Basic → Advanced → Expert |
| Поднавыки | Advanced: 1 из 3; Expert: 1 из 3 |
| Подкласс | 5 конкретных навыков на Expert |
| Классы | 12 шаблонов (Knight, Cleric, … Riftspeaker) |
| Фракции | 6 (Temple, Necropolis, Grove, Dungeon, Hive, Schism) |
| Герой | Абстрактный: фракция + Might/Magic |

**Ограничения классов (как в игре):**

- Might-герои не получают Thaumaturgy; Magic — не Combat и не Recruitment  
- Фракционный навык в центре колеса нельзя убрать, но можно прокачивать по tier  

---

## 4. Файлы данных — подробно

### 4.1. `hero-builder-data.js`

Объект `window.HOE_BUILDER_DATA`:

- **`factions`** — 6 фракций и названия фракционных навыков  
- **`skillAliases`** — старые имена → актуальные (Offence→Offense, Intelligence→Wisdom и т.д.)  
- **`skills`** — 30 навыков: категория, ограничения Might/Magic, массивы `adv` / `exp` поднавыков  
- **`classes`** — 12 классов: `type`, `skillChances`, `subclasses` с бонусами и списком 5 навыков для Expert  

**Источники навыков и поднавыков:**

- [wiki.hoodedhorse.com — Skills](https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era/Skills)
- Локальные HTML в `rared html/` (эталон, не изменять)
- Локальный справочник `HoMM_Olden_Era_Skills.md`

### 4.2. `hero-builder-synergies.js`

Массив `window.HOE_BUILDER_SYNERGIES` — пары «навык + поднавык ↔ второй навык» с эффектом удвоения (×2).

Формат записи:

```javascript
{ skill, sub, needs, descEn, descRu }
```

**Источник:** [Hero Skill Synergies](https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era/Hero_Skill_Synergies), `HoMM_Olden_Era_Skills.md`.

### 4.3. `hero-builder-core.js`

Чистая логика без DOM:

- `buildConfiguratorSlots` — стартовое колесо (фракционный навык в слоте 0)  
- `computeSynergies` — статусы `active` / `partial` / `potential` / `inactive`  
- `computeBuildLevelCost` — минимальный уровень и breakdown левелапов  
- `validateBuild` — проверка билда (слоты, ограничения класса)  

### 4.4. `hero-builder-i18n.js`

Объект `window.HOE_BUILDER_I18N` с ключами `en` и `ru`. Язык в `localStorage` (`hoe_builder_lang`).

### 4.5. `hero-builder-app.js`

UI: колесо навыков, редактор слота, подклассы, синергии (4 группы с подсветкой), калькулятор уровня, экспорт/импорт JSON (версия 3), шаринг через `#hash` (base64 JSON).

---

## 5. Проверка wiki HTML

Папка `rared html/` — локальные выгрузки официальной wiki. **Не коммитится** и **не изменяется** скриптами проекта.

```powershell
python scripts/check_wiki_html_completeness.py
```

Ожидаемый результат: **PASS** — 30/30 навыков, Basic/Advanced/Expert, по 3 поднавыка. Скрипт также сравнивает поднавыки с `hero-builder-data.js` (учитывает Defence/Defense).

---

## 6. JSON и скрипты сборки

### `build_hero_builder_export.py`

Генерирует `hero-builder-synergies.js` и `synergies.json` из встроенного массива SYNERGIES.

```powershell
python build_hero_builder_export.py
```

### `build_heroes_json.py` / `homm_oe_heroes_export.json`

Отдельный data-pipeline для 108 героев. **Не используется** конфигуратором.

---

## 7. GitHub Pages — деплой

### Настройки репозитория

1. **Settings → Pages**  
2. Source: **Deploy from a branch**  
3. Branch: **main**, folder: **/ (root)**  

Сайт: `https://balbomush.github.io/homm-oe-hero-builder/`

### Обновление после правок

```powershell
cd b:\hmmOE
Copy-Item hero-builder.html index.html -Force   # если меняли HTML
git add .
git commit -m "Описание изменений"
git push
```

### Файлы, которые **не** попадают в репозиторий

См. `.gitignore`: `rared html/`, `tmp_*.html`, дубликаты JSON, `tests/`.

---

## 8. Экспорт билда (JSON)

Формат экспорта (версия 3):

```json
{
  "version": 3,
  "lang": "ru",
  "faction": "Temple",
  "classType": "Might",
  "targetSubclass": "Crusader",
  "slots": [ ... ]
}
```

Импорт и URL `#hash` восстанавливают фракцию, тип, подкласс, слоты и язык.

---

## 9. Карта источников по типу данных

| Данные | Основной источник | Дополнительно |
|--------|-------------------|---------------|
| Навыки, поднавыки | Hooded Horse Wiki, `rared html/` | `HoMM_Olden_Era_Skills.md` |
| Синергии | Wiki Hero Skill Synergies | `build_hero_builder_export.py` |
| Подклассы | Fandom Advanced class | whisperofthehouse guides |
| Шансы навыков класса | Вики (страницы классов) | olden-era.com |

---

## 10. Контакты и вклад

Репозиторий: https://github.com/balbomush/homm-oe-hero-builder  

Issues и pull requests приветствуются: исправления навыков, поднавыков, синергий и переводов.

---

*Документ актуален для универсального конфигуратора (ветка refactor-skill-wheel). При обновлениях игры сверяйтесь с официальной wiki Hooded Horse.*
