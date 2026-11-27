# Рисунки мелками (Wortreise)

Стиль: детский рисунок восковыми мелками (зернистый край, штриховка зигзагом, лица с точками-глазами и румянцем),
контур тёмно-коричневый #3a2a20. У каждой картинки своя бумага и 3–4 мелка из коробки `BOX` (kid.py) по смыслу слова,
главная деталь — самым ярким цветом. Букв в картинках нет (исключение — облачка «du» / «Sie»).

Сцены темы N — файл `tNNN.py` (словарь `SC` сцен и `KEYS` слово → сцена). Герои и постоянные персонажи — функции в t001.py
(rosa, amir, klaus, brandl, guenter, malik, clara, petra, lilli, hannah, tom, teen) — переносить в общий модуль, когда появятся в других темах.

    cd tools/art
    python3 render.py t001 out1            # все SVG → PNG 520 px + контактные листы out1/sheet_*.png (смотреть!)
    python3 render.py t001 out1 hallo,tag  # перерисовать выбранные сцены
    python3 export.py t001 out1 ../../words/img/T001   # → a_<slug>.webp 480 px (≈18 КБ)
    cd ../.. && python3 tools/build_words.py           # слова получают img (рисунок a_* имеет приоритет)

Нужны: rsvg-convert (librsvg2-bin), Pillow. out*/ не коммитить.

## Семья на диване (комментаторы тренажёра)
`family.py` — шесть персонажей (Даня, Ника, Ирина, Игорь, Людмила Ивановна, Виктор Петрович), ники на одежде (RU/UK — `FAMLANG`),
4 эмоции (joy, facepalm, wow, told) и сцена у телевизора. Экспорт в тренажёр:

    python3 export_family.py ../../words/img/fam     # → words/img/fam/{ru,uk}/<кто>[_<эмоция>|_head].webp, scene.webp

Для подписей нужен шрифт Caveat в ~/.fonts (ttf из words/fonts/*.woff2 через fontTools).
Каналы Lindenbrück и диван: `words/src/kanal/T###.txt`, `words/src/divan/T###.json` → `python3 tools/build_kanal.py`.

## Английский вариант
Тексты: `words/src_en/s*.txt` (тот же формат, что `words/src`, + NAME и уровень слова) → `python3 tools/build_en.py` → `words/data_en/`.
Каналы и диван: `words/src_en/{kanal,divan}` → `python3 tools/build_kanal.py en`. Реакции семьи — `words/data_en/family.json`.
Рисунки к словам берутся из немецкой темы (`img/T001/a_*.webp`) по таблице IMG в build_en.py.

## 3D-фигурки семьи (сейчас на сайте)
`tools/art3d/` — свой маленький 3D-рендер (ray marching, numba): фигурки из шаров, капсул и скруглённых блоков,
мягкие тени, пластилиновая фактура, ники на одежде — текстурой (шрифт Caveat). Нужны numpy, numba, Pillow.

    cd tools/art3d && python3 export3d.py ../../words/img/fam      # ≈ 6 мин на оба языка
Рисунки мелками семьи (tools/art/family.py) остаются в истории и могут быть возвращены export_family.py.
Короткие 3D-ролики эмоций (анимированный webp, 240 px): `cd tools/art3d && python3 anim3d.py ../../words/img/fam` (≈ 9 мин на оба языка);
они заменяют статичные <кто>_<эмоция>.webp. Анимация реплик на диване — CSS в words/app.css («фигурки оживают»).
Фирменные движения с предметами (`<кто>_act.webp`, главная страница): `cd tools/art3d && python3 act3d.py ../../words/img/fam`.
Жесты-подсказки («Крокодил»: член семьи показывает слово): `cd tools/art3d && python3 gestures.py ../../words/img/fam`
(≈ 25 мин) → `<lang>/g_<жест>.webp` и `words/data{,_en}/gesture.json` (слово → жест). Новые слова — добавить в MAP, новый жест — в G() и GEST.
