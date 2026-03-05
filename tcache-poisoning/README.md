# tcache-poisoning (CTF task)

Задание на утечку libc из unsorted bin и tcache poisoning через double-free.

## 1) Уязвимости

1) Неочищенная память при повторном выделении.
   Если освободить большой чанк (в unsorted bin) и затем снова выделить его,
   в начале остаются `fd`/`bk` указатели main_arena (утечка libc).

2) Double-free (2free) + UAF.
   Удаление заметки не обнуляет указатель, повторное удаление разрешено.
   Это позволяет сделать tcache poisoning.

## 2) Как запускать

```bash
cd tcache-poisoning
docker compose up --build -d
```

Сервис слушает `127.0.0.1:1337`.

## 3) Флаг

Флаг задаётся через `docker-compose.yml` переменной окружения `FLAG`.

## 4) Идея эксплуатации

1) Создать большой чанк (>0x410), освободить его.
2) Снова выделить тот же размер, **не записывать данные**.
3) Посмотреть первые байты (`Dump note bytes`) и получить fd/bk из unsorted bin → libc leak.
4) Для tcache poisoning:
   - создать два small-чанка
   - free(A), free(B), free(A) (double-free)
   - через UAF записать fake fd в freed chunk (с учётом safe-linking)
   - выделить чанк, который укажет на глобальный `speak_fn`, и перезаписать его адресом `win`
   - вызвать `Speak note`

## 5) PoC

Есть примерный PoC: `solve.py`.

```bash
python3 solve.py HOST=127.0.0.1 PORT=1337
```

Примечание: PoC использует `libc.so.6` и `ld-linux-x86-64.so.2`, лежащие рядом с задачей.
