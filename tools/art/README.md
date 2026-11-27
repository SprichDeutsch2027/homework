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
