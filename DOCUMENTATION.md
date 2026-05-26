# HoMM Olden Era Hero Builder — документация

Полное описание проекта: из чего состоит конструктор, откуда взяты данные и как их обновлять.

---

## 1. Назначение проекта

**Hero Builder** — статический веб-инструмент для планирования билда героя в *Heroes of Might and Magic: Olden Era* по аналогии с Skill Wheel из Heroes V.

Пользователь выбирает героя, собирает 8 навыков (включая фракционный), настраивает поднавыки, отслеживает прогресс к подклассу, видит активные синергии и может смоделировать выбор навыков при левелапе.

Сайт не требует сервера: только HTML, CSS и JavaScript. Хостинг — [GitHub Pages](https://pages.github.com/).

**Live URL:** https://balbomush.github.io/homm-oe-hero-builder/

**Репозиторий:** https://github.com/balbomush/homm-oe-hero-builder

---

## 2. Архитектура (как файлы связаны)

```
index.html
  ├── hero-builder-i18n.js      ← строки интерфейса EN/RU
  ├── hero-builder-synergies.js ← пары навыков с эффектом ×2
  ├── hero-builder-heroes.js    ← 108 героев
  ├── hero-builder-data.js      ← навыки, классы, фракции
  └── hero-builder-app.js       ← логика UI (колесо, план левелапов)
```

### Порядок загрузки важен

1. `HOE_BUILDER_I18N` — переводы  
2. `HOE_BUILDER_SYNERGIES` — синергии  
3. `HOE_BUILDER_HEROES` — массив героев  
4. `HOE_BUILDER_DATA` — навыки и классы; в конце файла heroes подмешиваются из `HOE_BUILDER_HEROES`  
5. `hero-builder-app.js` — инициализация приложения  

### Справочные материалы (не подключаются к сайту напрямую)

| Файл | Роль |
|------|------|
| `HoMM_Olden_Era_Skills.md` | Человекочитаемый справочник всех навыков; основа для `hero-builder-data.js` и `hero-builder-synergies.js` |
| `homm_oe_heroes_export.json` | Машиночитаемый экспорт 108 героев и 12 классов; эталон для сверки |
| `build_heroes_json.py` | Скрипт сборки JSON из агрегированных данных вики/сообщества |

---

## 3. Игровая модель (что отражено в данных)

| Параметр | Значение в конструкторе |
|----------|-------------------------|
| Слотов навыков | 8 (включая фракционный) |
| Уровни навыка | Basic → Advanced → Expert |
| Поднавыки | Advanced: 1 из 3; Expert: 1 из 2 |
| Подкласс | 5 конкретных навыков на Expert |
| Классы | 12 (Knight, Cleric, … Riftspeaker) |
| Фракции | 6 (Temple, Necropolis, Grove, Dungeon, Hive, Schism) |
| Герои | 108 (18 на фракцию) |

**Ограничения классов (как в игре):**

- Might-герои не получают Thaumaturgy, Recruitment (для Magic), Combat (для Magic) — и наоборот для Magic-героев  
- Стартовые навыки героя в конструкторе **заблокированы** (нельзя убрать)

---

## 4. Файлы данных — подробно

### 4.1. `hero-builder-heroes.js`

Массив `window.HOE_BUILDER_HEROES` — **108 записей**.

Поля одного героя:

| Поле | Описание |
|------|----------|
| `id` | URL-safe идентификатор |
| `name` | Имя в игре |
| `faction` | Temple / Necropolis / Grove / Dungeon / Hive / Schism |
| `class` | Knight, Druid, Enforcer и т.д. |
| `specialty` | Название специализации |
| `specialtyDescEn` | Описание специализации (англ.) |
| `specialtyDescRu` | Описание специализации (рус.) |
| `start` | `[{ skill, tier: "Basic" \| "Advanced" }]` — стартовые навыки |
| `spell` | Стартовое заклинание (если есть) |
| `subclassHint` | Рекомендуемый подкласс (подсказка UI) |
| `universal` | `true` — универсальный герой фракции (Advanced фракционный навык) |

**Источники имён, классов и стартовых навыков:**

- [Официальная вики Hooded Horse — Heroes](https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era)
- [Fandom — Heroes (OE)](https://mightandmagic.fandom.com/wiki/Heroes_of_Might_and_Magic:_Olden_Era)
- [olden-era.com — Heroes](https://olden-era.com/en/heroes)
- Steam Community — списки героев Temple / Necropolis / Schism
- [Keengamer — Best Heroes](https://www.keengamer.com/articles/guides/heroes-of-might-and-magic-olden-era-best-heroes-in-each-faction/) (Grove, Hive, Schism)
- [The Games Edge — Hive Faction Guide](https://thegamesedge.com/heroes-of-might-magic-olden-era-hive-faction-guide/)
- YouTube-обзоры сообщества (ранжирование героев Grove)

Сверка с `homm_oe_heroes_export.json` (собран subagent + `build_heroes_json.py`).

### 4.2. `hero-builder-data.js`

Объект `window.HOE_BUILDER_DATA`:

- **`factions`** — 6 фракций и названия фракционных навыков  
- **`skillAliases`** — старые имена → актуальные (Offence→Offense, Intelligence→Wisdom и т.д.)  
- **`skills`** — ~29 навыков: категория, ограничения Might/Magic, массивы `adv` / `exp` поднавыков  
- **`classes`** — 12 классов: `type`, `skillChances` (% при левелапе), `subclasses` с `bonusEn` / `bonusRu` и списком 5 навыков для Expert  

**Источники навыков и поднавыков:**

- [wiki.hoodedhorse.com — Skills](https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era/Skills)
- [olden-era.com — Skills](https://www.olden-era.com/en/skills)
- [Fandom — Advanced class (OE)](https://mightandmagic.fandom.com/wiki/Advanced_class_(OE))
- Локальный справочник `HoMM_Olden_Era_Skills.md`

**Примечание:** у Grove / Hive / Riftspeaker часть `skillChances` может быть пустой — на вики проценты появлялись не для всех классов; симулятор левелапов в таком случае использует равные веса.

### 4.3. `hero-builder-synergies.js`

Массив `window.HOE_BUILDER_SYNERGIES` — пары «навык + поднавык ↔ второй навык» с эффектом удвоения (×2).

Формат записи:

```javascript
{ skill, sub, needs, descEn, descRu }
```

**Источник:** раздел «Синергии» в `HoMM_Olden_Era_Skills.md`, сверенный с olden-era.com и вики.

### 4.4. `hero-builder-i18n.js`

Объект `window.HOE_BUILDER_I18N` с ключами `en` и `ru` для всех строк интерфейса, включая названия фракций и сообщения планировщика.

Выбор языка сохраняется в `localStorage` (`hoe_builder_lang`).

### 4.5. `hero-builder-app.js`

Логика приложения: колесо навыков, редактор слота, подклассы, синергии, план левелапов (уровни 2–25), экспорт/импорт JSON (версия 2).

---

## 5. Справочник `HoMM_Olden_Era_Skills.md`

Отдельный markdown-файл (~840 строк) — **полный справочник механик**:

- Might / Magic / General / фракционные навыки  
- Поднавыки и синергии  
- Подклассы всех 12 классов  
- Holy Sigils, Hero Abilities  

На GitHub Pages доступен по прямой ссылке:  
https://balbomush.github.io/homm-oe-hero-builder/HoMM_Olden_Era_Skills.md

---

## 6. JSON и скрипт сборки

### `homm_oe_heroes_export.json`

Структура:

```json
{
  "heroes": [ ... 108 объектов ... ],
  "classes": { ... 12 классов с skillRollChances и subclasses ... }
}
```

Используется для сверки и будущей автоматической генерации `hero-builder-heroes.js`.  
**Не подключается** к работающему сайту.

### `build_heroes_json.py`

Python-скрипт, собирающий `homm_oe_heroes_export.json` из захардкоженных данных, синхронизированных с вики/Fandom/Steam.

Запуск (опционально, для пересборки JSON):

```powershell
python build_heroes_json.py
```

После правок JSON нужно вручную или скриптом обновить `hero-builder-heroes.js` — автоматической связки пока нет.

---

## 7. GitHub Pages — деплой

### Настройки репозитория

1. **Settings → Pages**  
2. Source: **Deploy from a branch**  
3. Branch: **main**, folder: **/ (root)**  
4. Save  

Сайт: `https://balbomush.github.io/homm-oe-hero-builder/`

### Что публикуется

Корень репозитория = корень сайта. Главная страница — **`index.html`** (копия `hero-builder.html`).

### Обновление после правок

```powershell
cd b:\hmmOE
Copy-Item hero-builder.html index.html -Force   # если меняли HTML
git add .
git commit -m "Описание изменений"
git push
```

### Файлы, которые **не** попадают в репозиторий

См. `.gitignore`: `tmp_*.html`, `wiki_skills_extract.txt`, дубликаты JSON.

---

## 8. Известные ограничения и расхождения

| Тема | Комментарий |
|------|-------------|
| Описания специализаций EN | У части старых героев английский текст может совпадать с русским; новые герои Grove/Hive/Schism переведены полнее |
| Имена в раннем EA | Adahn/Adhan, Echolilly/Echolie, Neve/Niev — возможны расхождения с финальной локализацией |
| Hive Herald | Два героя (Scarab, Brood Voice) добавлены по механике фракции; имена могут измениться в патче |
| Grove skillChances | На вики иногда 0% — в игре герои всё равно получают Murmuring + второй навык |
| Wiki 403 | Прямой curl к hoodedhorse.com иногда блокируется; данные собирались через браузер, Fandom, olden-era.com |

---

## 9. Карта источников по типу данных

| Данные | Основной источник | Дополнительно |
|--------|-------------------|---------------|
| Навыки, поднавыки | [Hooded Horse Wiki — Skills](https://wiki.hoodedhorse.com/Heroes_of_Might_and_Magic_Olden_Era/Skills) | olden-era.com, `HoMM_Olden_Era_Skills.md` |
| Синергии | olden-era.com, вики | Fandom |
| Подклассы | [Fandom — Advanced class](https://mightandmagic.fandom.com/wiki/Advanced_class_(OE)) | whisperofthehouse subclass guides |
| Шансы навыков класса | Вики / Fandom (страницы классов) | olden-era.com |
| Герои Temple, Necropolis | Steam hero list, Fandom | Keengamer |
| Герои Dungeon | Fandom, вики | Keengamer |
| Герои Grove | Keengamer, YouTube tier lists | Sportskeeda |
| Герои Hive | The Games Edge guide | Keengamer |
| Герои Schism | Steam list, Keengamer | Fandom |
| Фракционные навыки | Вики, olden-era.com | In-game names |

---

## 10. Экспорт билда (JSON)

Формат экспорта (версия 2):

```json
{
  "version": 2,
  "lang": "ru",
  "heroId": "gorel",
  "faction": "Grove",
  "targetSubclass": "Fortune's Favored",
  "slots": [ ... ],
  "levelPlan": { "2": "Luck", "3": "Scouting" }
}
```

Импорт восстанавливает героя, слоты, подкласс, язык и план левелапов.

---

## 11. Контакты и вклад

Репозиторий: https://github.com/balbomush/homm-oe-hero-builder  

Issues и pull requests приветствуются: исправления имён героев, стартовых навыков, переводов и процентов классов.

---

*Документ актуален для первой публикации на GitHub Pages. При крупных обновлениях игры (Early Access) данные могут устареть — сверяйтесь с официальной вики Hooded Horse.*
