# Thinking Budget Check

**Measure whether enabling reasoning improves your own ticket decisions enough to justify waiting.**

English · [Français](README.fr.md) · [Español](README.es.md)

## See the problem in one command

```sh
python3 compare.py demo --lang en
```

The offline two-ticket fixture has invented answers and latency; it does not benchmark Jeeves.

## Related projects

- [PostHog/jeeves](https://github.com/PostHog/jeeves) — Its `options.think` switch and local Jev-compatible API are the direct integration.
- [fstandhartinger/jevbench](https://github.com/fstandhartinger/jevbench) — Already compares models for accuracy, speed and cost; this tool only compares one model’s reasoning modes on user-labelled tasks. No affiliation.

## Use it on your data

```sh
python3 compare.py run --cases fixtures/cases.json --endpoint http://127.0.0.1:8009 --lang en
```

Start Jeeves and pass its local base URL. Each labelled `choice` case is sent twice to `/v1/systemone`, with `options.think` false and true. The checker reports accuracy and median wall time for each mode; it does not pick a policy for you.

## Scope and limits

A live Jeeves server requires compatible hardware and weights. Paired sequential requests do not remove warmup or load variance; repeat runs before operational decisions. `--token-env NAME` is optional.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. MIT. No account or API key is required for the demo.
