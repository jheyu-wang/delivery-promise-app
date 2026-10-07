---
name: notebook-to-streamlit
description: Converts the logic in Assignment1-Zheyu Wang.ipynb (Rosa's Pizza delivery-promise analysis) into a Streamlit app. Use when building or updating the Streamlit app that recommends the best promised delivery time for a zone and time block, and the app must reuse the notebook's best_promise_time() logic.
---

# Notebook to Streamlit: Rosa's Delivery Promise App

## Purpose and scope

This skill guides the conversion of the analysis in `Assignment1-Zheyu Wang.ipynb` into a Streamlit web app that helps Rosa choose the best promised delivery time.

It covers:
- Extracting the reusable logic from the notebook into a Python module.
- Building the Streamlit UI on top of that module.
- Preparing the repo for GitHub and Streamlit Community Cloud deployment.

It does not cover new analysis, new cost models, or changes to how `delivery_times` simulates data.

## Source logic in the notebook

Reuse these pieces as they are. Do not invent new calculation logic.

- **Data/setup:** `from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times`. The `starter` package comes from `git+https://github.com/zhouy185/rosa-starter.git`.
- **`delivery_times(zone, time_block, promise)`:** returns a NumPy array of simulated delivery times (minutes) for one zone and time block.
- **`best_promise_time(zones, time_blocks, promise_B, costs)`:** the core function. For each candidate promise `p` in `promise_B`:
  - `array = delivery_times(zones, time_blocks, p)`
  - `late_order = np.sum(array > p)`, `total_order = len(array)`
  - `order_profit = total_order * costs["margin"] - late_order * (costs["refund"] + costs["churn_orders"] * costs["margin"])`
  
  It returns `(best_promise, best_profit)` using `np.argmax` over the profits.
- **`COSTS` dict keys:** `"refund"` (default 10.0), `"churn_orders"` (default 1.8, the number of future orders lost per late order), `"margin"` (default 9.0).
- **Default candidate promises:** `list(range(3, 66, 3))`.
- **Optional helpers:** `late_percentage(...)` and `Average_delivery_time(...)` can be reused to show extra context for the chosen promise.

## Workflow

1. **Read the notebook** (`Assignment1-Zheyu Wang.ipynb`) and confirm the current signatures and logic of the functions above before copying anything.
2. **Create a logic module** (e.g. `logic.py`) containing the notebook's functions, copied faithfully:
   - Keep `best_promise_time()` with the same signature and the same profit formula.
   - Remove notebook-only code: `!pip install`, test/print cells, scratch code, and the unused `from IPython.core.history import DummyDB` import.
   - Keep `import numpy as np` and the `starter` imports.
3. **Create `app.py`** (Streamlit) that imports from the logic module and builds the UI (see requirements below).
4. **Wire the inputs to the notebook logic:**
   - Build `promise_B = list(range(min_p, max_p + 1, step))` from the user's range.
   - Build `costs = {"refund": ..., "churn_orders": ..., "margin": ...}` from the user's inputs.
   - Call `best_promise_time(zone, time_block, promise_B, costs)` only when the button is clicked.
5. **Display the result:** the recommended promise (minutes) and the expected profit. Optionally show a table or line chart of profit versus promise by looping over `promise_B` with the same profit formula.
6. **Add `requirements.txt`** with `streamlit`, `numpy`, `pandas` (if used), and `git+https://github.com/zhouy185/rosa-starter.git`.
7. **Test locally** with `streamlit run app.py`, then check the result against the notebook for the same inputs (for example Far West / Lunch with default costs).
8. **Version control and deploy:** create a local git repo and a GitHub repo, push, then deploy through Streamlit Community Cloud pointing at `app.py`.

## Requirements and constraints

**The app must let the user:**
1. Select a zone and a time block from dropdown menus (`st.selectbox`), populated from `ZONES` and `TIME_BLOCKS`.
2. Set the range of promised delivery times to try (e.g. `st.slider` with a min and max, plus a step).
3. Adjust the profit margin per order, the estimated churn per late order, and the refund cost per late order (`st.number_input`), with defaults taken from `COSTS`.
4. Click a button (`st.button`) to display the recommended promised delivery time for the selected zone and time block.

**Rules:**
- Reuse `best_promise_time()` from the notebook. Do not write a separate or unrelated calculation.
- Do not hard-code the zone or time-block lists. Use `ZONES` and `TIME_BLOCKS`.
- Validate the range (min must be less than max, and the step must be positive) and show a clear message instead of crashing.
- Do not compute anything until the button is clicked.
- Keep the UI simple, labelled with units (minutes, dollars).

**Expected files:**
- `app.py`: the Streamlit app.
- `logic.py`: logic copied from the notebook.
- `requirements.txt`: dependencies, including the `rosa-starter` GitHub package.
- `.github/skills/notebook-to-streamlit/SKILL.md`: this file.
- `README.md` (optional): a short description and the deployed app link.

**Limitations:**
- `delivery_times` appears to return different random samples on each call (the notebook's two late-rate tables disagreed). The recommended promise may therefore change slightly between runs. Mention this in the app or README, or fix it with a seed if the instructor allows.
- The app depends on the `starter` package being installable on Streamlit Community Cloud.

## Additional notes

- Treat the notebook as the source of truth. If the notebook logic changes, update `logic.py` to match.
- The notebook's comment says the promise range goes to 60, but the code goes to 63. The app's default range should match the code (3 to 63, step 3).
- Keep the key prompts used with Claude, since the assignment asks for them to be documented.
