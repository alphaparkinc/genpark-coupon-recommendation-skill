import sys
import json
from coupon_recommender import CouponRecommenderClient

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== GenPark Coupon Recommendation Agent Verification ===")
    client = CouponRecommenderClient()

    # 1. Mock Cart items
    cart = [
        {"sku": "SKU-AUDIO-1", "price": 100.00, "quantity": 1, "category": "audio"},
        {"sku": "SKU-CASE-2", "price": 20.00, "quantity": 2, "category": "accessories"}
    ]

    # 2. Available coupons in database
    coupons = [
        {"code": "SAVE10", "discount_type": "percent", "discount_value": 10.0, "min_spend": 50.0},
        {"code": "AUDIO25", "discount_type": "percent", "discount_value": 25.0, "applicable_category": "audio"},
        {"code": "FIXED50", "discount_type": "fixed", "discount_value": 50.0, "min_spend": 200.0}
    ]

    result = client.recommend_coupon(cart, coupons)
    
    print("\n--- Savings Breakdown ---")
    print(json.dumps(result["savings_breakdown"], indent=2))
    
    print("\n--- Recommended Optimal Coupon ---")
    print(json.dumps(result["recommended_coupon"], indent=2))

if __name__ == "__main__":
    main()
