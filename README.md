# Warehouse Inventory & Order API - Coding Exercise

**Position:** Senior Python Developer / Tech Lead

---

## Part 1: Fix the Bugs

**Make all the tests pass by fixing the implementation files (not the tests).**

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests.py -v
```

### Files to Fix

| File | What to Fix |
|------|-------------|
| `service.py` | `search_products()` - Needs case-insensitive partial matching. |
| `service.py` | `process_order()` - Needs to handle missing products and atomic stock deduction. |

---

## Part 2: Code Review & Refactoring

After fixing the bugs, review these methods in `service.py` and discuss how you would improve them:

- **`calculate_order_totals()`**: Look for redundant loops and poor naming.
- **`generate_invoice()`**: Identify violations of the Open/Closed principle (Strategy Pattern).
- **`validate_shipping()`**: Address the "Pyramid of Doom" (Deep Nesting).

These methods might "work" for basic cases but are not production-ready for a scaling system. Be prepared to explain your refactoring strategy.

---

## Notes
- You may refactor existing code as needed.
- You may add helper functions or utility classes.
- Ensure your solution handles edge cases (empty orders, invalid SKUs, etc.) gracefully.

Good luck!
