# Inventory Format

The inventory is a dot-point list grouped by file then by unit (class or function). One bullet per case.

**Granularity rules:**

- One bullet per distinct test case — one condition, one expected outcome
- For behaviour that varies across multiple distinct inputs (e.g. parametrised cases), list each variation as a separate bullet rather than collapsing them into one
- Omit private or internal units; test those through the public interface that exercises them

```
- `tests/test_widget_service.py`
  - `WidgetService.get_widget`
    - returns widget when found
    - raises 404 when widget does not exist
    - raises 503 when dependency returns None
    - bypasses validation when feature flag is disabled
    - logs a warning when stale data is used
  - `WidgetCache.get`
    - returns cached value without hitting DB on cache hit
    - populates cache after successful DB fetch
    - evicts entry once TTL expires
    - serves stale value within grace period when DB fails
    - returns None when DB fails and grace period has also expired
    - only hits DB once across concurrent cache misses
- `tests/test_order_processor.py`
  - `OrderProcessor.submit`
    - returns order ID on success
    - raises validation error when required fields are missing
    - raises conflict error when order already exists
  - `OrderProcessor.cancel`
    - cancels a pending order
    - raises error when order is already fulfilled
```

The top-level grouping key is the relevant file for the context in which the inventory is produced — group by whichever file anchors the items being listed.
