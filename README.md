# Loose Version Comparator

Compares version strings that do not follow any strict spec by splitting on non-numeric boundaries.

```python
from loose_version_comparator import Version, compare

assert Version("1.10") > Version("1.9")
assert compare("2.0", "1.0") == 1
assert Version("1.0") == Version("1.0.0")
```

## Why this exists

Real-world version strings are a mess: `1.10.3`, `2.0-alpha`, `1.0.0rc1`, `2024.06.15`. A strict semver parser rejects most of them; a naive string compare says `"1.10" < "1.9"` because `'10'` sorts before `'9'` lexically. This library splits on every alphanumeric/non-alphanumeric boundary, promotes pure-digit chunks to integers, and compares position by position.

## The one rule you will trip over

There is no `alpha < beta < rc < release` keyword ladder. A numeric release token is always greater than a non-numeric prerelease token at the same position (`1.0.0 > 1.0.0-alpha`), and two non-numeric tokens at the same position are compared by ordinal string order (`alpha < beta < rc` only because that happens to be alphabetical). If you need real semver prerelease semantics, use a semver library — this one deliberately does not try.

## Two more decisions worth stating

- Trailing zero segments are a no-op: `1.0 == 1.0.0`.
- A trailing prerelease token makes the version lesser than its bare release counterpart: `1.0-alpha < 1.0`.

## Exports

- `Version(raw: str)` — parseable, comparable, hashable.
- `compare(a: str, b: str) -> int` — returns `-1`, `0`, or `1`.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

