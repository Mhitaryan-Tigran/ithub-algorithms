# Алгоритмы и структуры данных

Мхитарян Тигран, ИСП9-Х36, IThub. Решения контрольных точек курса, по одной папке на точку.

Каждая программа выводит требуемые результаты и в конце сама проверяет их через `assert` с контрольными значениями из задания (и, где это имеет смысл, со случайными тестами против перебора). Нужен только Python 3.10+, внешних библиотек нет.

```
python3 trees/07-final-helpdesk/helpdesk.py
find . -name "*.py" | sort | while read f; do python3 "$f" > /dev/null && echo "ok $f"; done
```

## Бинарные деревья

| Папка | Контрольная точка |
|---|---|
| [trees/01-bst-node](trees/01-bst-node) | Построение BST: структура узла |
| [trees/02-bst-sequence](trees/02-bst-sequence) | Поиск и модификация в BST: класс дерева, i-й узел по in-order, дерево 17, 6, 5, 20, … |
| [trees/03-balanced-avl](trees/03-balanced-avl) | Сбалансированные деревья: виды, плюсы и минусы, реализация AVL |
| [trees/04-heap](trees/04-heap) | Бинарная куча |
| [trees/05-max-heap-from-tree](trees/05-max-heap-from-tree) | Убывающая куча из любого дерева |
| [trees/06-priority-queue](trees/06-priority-queue) | Очередь с приоритетом и сортировка кучей |
| [trees/07-final-helpdesk](trees/07-final-helpdesk) | Итоговая: «Диспетчер заявок службы поддержки» |

## Хеширование

| Папка | Контрольная точка |
|---|---|
| [hashing/01-hash-function](hashing/01-hash-function) | Хеш-функция и её свойства: DUPLICATES, открытая и закрытая адресация |
| [hashing/02-applications](hashing/02-applications) | Применение хеш-функций |
| [hashing/03-hash-tables](hashing/03-hash-tables) | КТ2-1 Хеш-таблицы |
| [hashing/04-collisions](hashing/04-collisions) | Разрешение коллизий: кукушкино хеширование, Робин Гуд |
| [hashing/05-final-registry](hashing/05-final-registry) | Итоговая: «Реестр оборудования» |

## Графы

| Папка | Контрольная точка |
|---|---|
| [graphs/01-basics](graphs/01-basics) | Основные понятия |
| [graphs/02-representation](graphs/02-representation) | Список и матрица смежности |
| [graphs/03-bfs-dfs](graphs/03-bfs-dfs) | Поиск в ширину и в глубину |
| [graphs/04-topological-sort](graphs/04-topological-sort) | Топологическая сортировка (Кан) |
| [graphs/05-dijkstra](graphs/05-dijkstra) | КТ Дейкстра: «Задержки в сети», «Свадебное путешествие» |
| [graphs/06-mst](graphs/06-mst) | Минимальное остовное дерево |
| [graphs/07-prim](graphs/07-prim) | Алгоритм Прима |
| [graphs/08-kruskal](graphs/08-kruskal) | Алгоритм Краскала с Union-Find |
| [graphs/09-bellman-ford](graphs/09-bellman-ford) | Алгоритм Беллмана — Форда |
| [graphs/10-floyd-warshall](graphs/10-floyd-warshall) | Алгоритм Флойда — Уоршелла |
| [graphs/11-final-campus](graphs/11-final-campus) | Итоговая: «Маршруты кампуса» |

## Динамическое программирование

| Папка | Контрольная точка |
|---|---|
| [dp/01-routes](dp/01-routes) | Количество маршрутов, O(1) по памяти |
| [dp/02-binary-strings](dp/02-binary-strings) | Задача 1: строки из 0 и 1 без двух единиц подряд |
| [dp/03-coin-change](dp/03-coin-change) | Размен банкнотами |
| [dp/04-king-routes](dp/04-king-routes) | Маршруты короля, все три варианта |
| [dp/05-final](dp/05-final) | Итоговая: задача 3, маршрут минимального веса |
