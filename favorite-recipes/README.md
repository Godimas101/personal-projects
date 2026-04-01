# 🍽️ Favorite Recipes

> **"Life is too short for bad recipes — or ones you can't remember."**

Recipes we've tried and liked, saved for easy reference and reuse.

## Purpose 🎯

A growing collection of go-to recipes, formatted in markdown for easy LLM use. When asking an AI for new recipe suggestions, reference this folder alongside the [kitchen inventory](../kitchen-inventory/) so it understands my cooking style and flavour preferences.

## Macro & Protein Rating Format 📊

Every recipe in this collection includes a macro summary line immediately after the title:

```
📊 Protein: Xg | Fat: Xg | Carbs: Xg | Calories: X | Protein Rating: X/10
```

**Protein Rating scale** (ratio = protein×10 ÷ calories):

| Ratio | Rating |
|-------|--------|
| ≥ 1.50 | 10/10 |
| 1.30–1.49 | 9/10 |
| 1.00–1.29 | 8/10 |
| 0.80–0.99 | 7/10 |
| 0.65–0.79 | 6/10 |
| 0.50–0.64 | 5/10 |
| < 0.50 | 4/10 |

## LLM Instructions 🤖

When using an AI to suggest new recipes or meals, include this in your prompt:

> For each recipe or meal provided, calculate and display the estimated macronutrients and a protein efficiency rating. This must appear in identical format for every meal, with no exceptions.
>
> Required format (one line, immediately following the meal name/description):
> 📊 Protein: Xg | Fat: Xg | Carbs: Xg | Calories: X | Protein Rating: X/10
>
> Protein Rating calculation:
> - Calculate the protein score: protein (g) × 10
> - Divide by total calories: protein score ÷ calories = ratio
> - Assign rating using the scale above
>
> Base all estimates on the full serving size as described in the recipe. If a range is possible, use the midpoint. Do not skip this block for any meal, regardless of how simple or incomplete the recipe details are — estimate if necessary and note it.

## Recipes 🥘

| File | Description | Category |
|------|-------------|----------|
| [air-fryer-chicken-drumsticks.md](air-fryer-chicken-drumsticks.md) | Crispy drumsticks with roasted veggies, all in the air fryer | 🍗 Chicken |
| [maple-ground-beef-baked-beans.md](maple-ground-beef-baked-beans.md) | Hearty maple baked beans with ground beef | 🥩 Beef |
| [tuna-salad-wraps.md](tuna-salad-wraps.md) | Flexible tuna salad with customizable flavour twists | 🐟 Seafood |
| [healthy-yogurt-egg-salad-wraps.md](healthy-yogurt-egg-salad-wraps.md) | High-protein egg salad with yogurt instead of mayo, for wraps | 🥚 Egg |
| [indian-spiced-beans.md](indian-spiced-beans.md) | Warm curry-style spiced beans — great over rice or with flatbread | 🌱 Veggie |
| [quick-seafood-congee.md](quick-seafood-congee.md) | Creamy rice congee with tilapia, salmon, and fish balls — light but filling | 🐟 Seafood |
| [chia-pudding.md](chia-pudding.md) | Overnight chia pudding with protein powder, hemp hearts, flax, and blueberries | 🌱 Veggie |
| [weekday-lunch.md](weekday-lunch.md) | Batch-prepped egg cups, spiced bean salad, and frozen veg — meal-prep friendly | 🥚 Egg |
| [saturday-pancakes.md](saturday-pancakes.md) | Flourish protein pancakes with blueberries and maple syrup — Saturday tradition | 🥞 Breakfast |

---

*"The best meal is the one you already know how to make."*
