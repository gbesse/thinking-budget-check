#!/usr/bin/env python3
"""Measure accuracy and latency of one Jev-like model with reasoning on/off."""

import argparse
import json
import os
import statistics
import sys
import time
import urllib.request
from pathlib import Path

TEXT = {
    "en": {"title": "Reasoning on or off?", "demo": "Synthetic fixture; run measures a real Jeeves endpoint.", "accuracy": "accuracy", "latency": "median latency"},
    "fr": {"title": "Raisonnement activé ou non ?", "demo": "Exemple synthétique ; run mesure un vrai endpoint Jeeves.", "accuracy": "précision", "latency": "latence médiane"},
    "es": {"title": "¿Razonamiento activado o no?", "demo": "Ejemplo sintético; run mide un endpoint Jeeves real.", "accuracy": "precisión", "latency": "latencia mediana"},
}


def extract_choice(body):
    value = (body.get("answers") or {}).get("route")
    if not isinstance(value, dict) or not isinstance(value.get("choice"), str):
        raise ValueError("answers.route.choice missing")
    return value["choice"]


def call(endpoint, case, think, model=None, token=None):
    payload = {"state": case["state"], "questions": {"route": {"type": "choice", "instructions": case["instructions"], "criteria": case["options"]}}, "options": {"think": think}}
    if model:
        payload["model"] = model
    headers = {"content-type": "application/json"}
    if token:
        headers["authorization"] = "Bearer " + token
    req = urllib.request.Request(endpoint.rstrip("/") + "/v1/systemone", data=json.dumps(payload).encode(), headers=headers, method="POST")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=180) as response:
        choice = extract_choice(json.load(response))
    return {"choice": choice, "latency_ms": (time.perf_counter() - started) * 1000}


def summarize(cases, observations):
    if not cases:
        raise ValueError("at least one case is required")
    out = {}
    for mode in ("off", "on"):
        results = [observations[case["id"]][mode] for case in cases]
        correct = sum(result["choice"] == case["expected"] for result, case in zip(results, cases))
        out[mode] = {"correct": correct, "total": len(cases), "accuracy": correct / len(cases), "median_latency_ms": statistics.median(r["latency_ms"] for r in results)}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare a Jev-compatible model with reasoning enabled and disabled on your labelled cases.")
    ap.add_argument("command", choices=["demo", "run"])
    ap.add_argument("--lang", choices=TEXT, default="en")
    ap.add_argument("--cases", type=Path, help="JSON array of labelled cases")
    ap.add_argument("--endpoint", help="Base URL for Jeeves")
    ap.add_argument("--model")
    ap.add_argument("--token-env")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.command == "demo":
        obj = json.loads((Path(__file__).parent / "fixtures" / "tickets.json").read_text())
        cases, observations = obj["cases"], obj["observations"]
    else:
        if not args.cases or not args.endpoint:
            ap.error("run requires --cases and --endpoint")
        cases = json.loads(args.cases.read_text())
        token = os.environ.get(args.token_env) if args.token_env else None
        if args.token_env and token is None:
            ap.error("token environment variable not set")
        observations = {case["id"]: {"off": call(args.endpoint, case, False, args.model, token), "on": call(args.endpoint, case, True, args.model, token)} for case in cases}
    try:
        summary = summarize(cases, observations)
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"simulated": args.command == "demo", "summary": summary, "observations": observations}, ensure_ascii=False, indent=2))
    else:
        print(TEXT[args.lang]["title"])
        if args.command == "demo":
            print(TEXT[args.lang]["demo"])
        for mode in ("off", "on"):
            row = summary[mode]
            print(f"{mode}: {TEXT[args.lang]['accuracy']} {row['correct']}/{row['total']}; {TEXT[args.lang]['latency']} {row['median_latency_ms']:.0f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
