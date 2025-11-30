from decimal import Decimal


def calculate_group_discount(group_size):
    """
    Calculate group discount based on group size
    Returns discount percentage as Decimal
    """
    if group_size >= 10:
        return Decimal("0.15")  # 15% discount for groups of 10+
    elif group_size >= 6:
        return Decimal("0.10")  # 10% discount for groups of 6+
    elif group_size >= 4:
        return Decimal("0.05")  # 5% discount for groups of 4+
    return Decimal("0")  # No discount for smaller groups


def calculate_total_price_with_discount(base_price, group_size):
    """
    Calculate total price with group discounts applied
    """
    base_price = Decimal(str(base_price))
    subtotal = base_price * group_size
    discount_percentage = calculate_group_discount(group_size)
    discount_amount = subtotal * discount_percentage
    final_price = subtotal - discount_amount

    return {
        "base_price_per_person": base_price,
        "group_size": group_size,
        "subtotal": subtotal,
        "discount_percentage": float(discount_percentage * 100),
        "discount_amount": round(discount_amount, 2),
        "final_price": round(final_price, 2),
    }
