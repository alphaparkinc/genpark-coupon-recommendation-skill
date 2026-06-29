# GenPark Coupon Recommendation Agent Skill

This repository contains the **GenPark Coupon Recommendation Agent Skill** — an agent configuration skill config (`skill.json`), a production-ready Python SDK client (`coupon_recommender.py`), and executable verification tests. It is designed to compare cart contents against a list of active discount vouchers, verify minimum spend thresholds and category constraints, and return the optimal coupon code.

---

## 🚀 Capabilities

* **Category Restriction Audits:** Limits percentage/fixed coupon values strictly to matching product categories.
* **Optimal Value Solver:** Compares all active discount results to select the voucher code producing the maximum savings.
* **Spend Threshold Protection:** Automatically flags and disqualifies coupons if cart totals fall below rules.

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 SDK Usage Reference

```python
from coupon_recommender import CouponRecommenderClient

client = CouponRecommenderClient()

result = client.recommend_coupon(
    cart_items=[{"sku": "SKU-01", "price": 100, "quantity": 1, "category": "audio"}],
    coupons=[
        {"code": "SAVE10", "discount_type": "percent", "discount_value": 10},
        {"code": "AUDIO25", "discount_type": "percent", "discount_value": 25, "applicable_category": "audio"}
    ]
)

print(result["recommended_coupon"])
```

---

## 📜 License
This project is licensed under the MIT License.
