# Bond Service

Zpracování zadání [Bond Service](https://github.com/cfgtech/bond-service-interview-assignment) 

Toto [README](README.md) obsahuje informace o struktuře projektu a návod pro spuštění aplikace, další popis fungování aplikace se nachází v kódu 

Pro zpracování úlohy jsem použil přístup [DRF](https://www.django-rest-framework.org) ViewSetů, a Serializerů.


## Spuštění aplikace

Návod pro spuštění projektu v [Dockeru](https://www.docker.com).

S nainstalovaným Dockerem můžete spustit příkazy:

```bash
docker compose -f docker-compose.local.yml build
```

```bash
docker compose -f docker-compose.local.yml up
```

Poté lze přitoupit na server na adrese `http://localhost:8000/`.

Pro vytvoření superuživatele s username `admin`

lze spustit příkaz:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py populate_superuser
```

V terminálu bude výstup s API tokenem, který budete potřebovat pro přístup k API.

Spuštění testů:

```bash
docker compose -f docker-compose.local.yml run --rm django coverage run -m pytest
docker compose -f docker-compose.local.yml run --rm django coverage report
```

## Co dál?

Pokud jste již vytvořili uživatele, můžete vyzkoušet API.

API je zdokumentované pomocí [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) a [drf-yasg](https://drf-yasg.readthedocs.io/en/latest/).

Dokumentace API je dostupná na adrese `http://localhost:8000/`, která přesměruje na `http://localhost:8000/api/docs/`.

Zde se ve webovém prostředí dají vyzkoušet endpointy.

## Autor

[Lukáš Jánský](https://github.com/janskylukas)

Kdyby cokoliv, neváhejte mě kontaktovat na emailu: [lukas.jansky22@gmail.com](mailto:lukas.jansky22@gmail.com)
