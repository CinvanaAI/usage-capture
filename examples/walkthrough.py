"""Compare interpretation boundaries using synthetic text, with no desktop access."""
import json
from dataclasses import asdict
from codex_usage_grabber.core import parse_usage as codex
from ollama_usage_grabber.core import parse_usage as ollama

results = []
for adapter, parser, label in (("codex", codex, "5h"), ("ollama", ollama, "Session")):
    cases = {"labeled": f"{label}: 73% Weekly: 41%", "partial": "Weekly: 41%", "position": "73% 41%", "invalid": "-5% then 1000.5%"}
    for name, text in cases.items():
        result = parser(text)
        assert result.complete == (name in {"labeled", "position"})
        assert result.strategy == ("labels" if name in {"labeled", "partial"} else "position")
        results.append({"adapter": adapter, "case": name, "synthetic_text": text, **asdict(result), "complete": result.complete})
print(json.dumps({"synthetic": True, "desktop_actions": 0, "cases": results}, indent=2))
