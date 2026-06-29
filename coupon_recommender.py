import os
from typing import List, Dict, Any, Optional

class CouponRecommenderClient:
    """
    Production-grade discount recommendation engine. Audits complex category rules
    and minimum spend thresholds to recommend the optimal promo voucher code.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("COUPON_API_KEY")

    def recommend_coupon(self, cart_items: List[Dict[str, Any]], coupons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates savings across all coupons and returns the absolute best candidate.
        """
        # Calculate subtotal and category totals
        subtotal = 0.0
        category_totals = {}
        for item in cart_items:
            price = float(item["price"])
            qty = int(item["quantity"])
            category = item.get("category", "general").lower()
            
            total_item_val = price * qty
            subtotal += total_item_val
            category_totals[category] = category_totals.get(category, 0.0) + total_item_val

        breakdown = []
        best_code = None
        max_savings = 0.0

        for cp in coupons:
            code = cp["code"]
            dtype = cp["discount_type"]
            val = float(cp["discount_value"])
            min_spend = float(cp.get("min_spend", 0.0))
            app_category = cp.get("applicable_category")

            # Check min spend
            if subtotal < min_spend:
                breakdown.append({
                    "code": code,
                    "eligible": False,
                    "savings": 0.0,
                    "reason": f"Cart subtotal (${subtotal:.2f}) is below the required minimum spend (${min_spend:.2f})."
                })
                continue

            # Check category specific limit
            eligible_base = subtotal
            if app_category:
                app_cat_lower = app_category.lower()
                eligible_base = category_totals.get(app_cat_lower, 0.0)
                if eligible_base <= 0.0:
                    breakdown.append({
                        "code": code,
                        "eligible": False,
                        "savings": 0.0,
                        "reason": f"Coupon only applies to the '{app_category}' category, which is not in the cart."
                    })
                    continue

            # Calculate savings
            savings = 0.0
            if dtype == "percent":
                savings = round(eligible_base * (val / 100.0), 2)
            elif dtype == "fixed":
                savings = min(eligible_base, val)

            breakdown.append({
                "code": code,
                "eligible": True,
                "savings": savings,
                "reason": f"Successfully applied. Total savings: ${savings:.2f}"
            })

            if savings > max_savings:
                max_savings = savings
                best_code = code

        return {
            "recommended_coupon": {
                "code": best_code,
                "savings_amount": max_savings
            },
            "savings_breakdown": breakdown
        }
