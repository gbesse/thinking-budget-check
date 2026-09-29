# Thinking Budget Check

**Mida si activar el razonamiento mejora suficientemente sus decisiones de tickets para justificar la espera.**

[English](README.md) · [Français](README.fr.md) · Español

## Ver el problema con un comando

```sh
python3 compare.py demo --lang es
```

Las respuestas y latencias del ejemplo de dos tickets son ficticias; no evalúa Jeeves.

**Ejemplo de salida**

```text
¿Razonamiento activado o no?
Ejemplo sintético; run mide un endpoint Jeeves real.
off: precisión 1/2; latencia mediana 310 ms
on: precisión 2/2; latencia mediana 3200 ms
```

## Proyectos cercanos

- [PostHog/jeeves](https://github.com/PostHog/jeeves) — Su opción `options.think` y su API local compatible con Jev son la integración directa.
- [fstandhartinger/jevbench](https://github.com/fstandhartinger/jevbench) — Ya compara modelos por precisión, velocidad y coste; esta herramienta solo compara modos de razonamiento de un modelo con sus casos. Sin afiliación.

## Usarlo con sus datos

```sh
python3 compare.py run --cases fixtures/cases.json --endpoint http://127.0.0.1:8009 --lang es
```

Inicie Jeeves e indique su URL local. Cada caso `choice` etiquetado se envía dos veces a `/v1/systemone`, con `options.think` desactivado y activado. La herramienta informa precisión y latencia mediana por modo; no elige la política por usted.

## Alcance y límites

Un servidor Jeeves real requiere pesos y hardware compatibles. Dos solicitudes sucesivas no eliminan variaciones de calentamiento o carga; repita las pruebas antes de decidir. `--token-env NAME` es opcional.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licencia MIT. La demo no requiere cuenta ni clave API.
