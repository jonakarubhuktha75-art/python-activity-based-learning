

def calculate_discount(subtotal):
    if subtotal >= 5000:
        return 0.20
    elif subtotal >= 3000:
        return 0.10
    elif subtotal >= 1000:
        return 0.05
    return 0.0


def calculate_total(basket):
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in basket
    )

    discount_rate = calculate_discount(subtotal)
    discount = subtotal * discount_rate
    total = subtotal - discount

    return subtotal, discount, total, discount_rate


def reduce_basket(basket, budget):
    basket = [item.copy() for item in basket]

    reductions = []

    basket.sort(key=lambda item: item["priority"])

    while True:
        subtotal, discount, total, rate = calculate_total(basket)

        if total <= budget:
            break

        candidates = [
            item for item in basket
            if item["quantity"] > 0
        ]

        if not candidates:
            break

        item = candidates[0]
        item["quantity"] -= 1
        reductions.append(item["name"])

    basket.sort(key=lambda item: item["original_order"])

    return basket, reductions


def main():
    print("=== MULTI-PRODUCT SHOPPING BUDGET ===")

    budget = float(input("Enter your shopping budget (Rs.): "))

    if budget < 0:
        print("Budget cannot be negative.")
        return

    basket = []
    product_count = int(input("Enter number of products: "))

    if product_count <= 0:
        print("Number of products must be positive.")
        return

    for i in range(product_count):
        print(f"\nProduct {i + 1}")

        name = input("Product name: ").strip()
        price = float(input("Price per unit (Rs.): "))
        quantity = int(input("Quantity: "))
        priority = int(
            input("Priority (1 = reduce first, 3 = keep if possible): ")
        )

        if not name or price < 0 or quantity < 0 or priority < 1:
            print("Invalid product details.")
            return

        basket.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "priority": priority,
            "original_order": i
        })

    subtotal, discount, total, rate = calculate_total(basket)

    print("\n========== ORIGINAL BASKET ==========")
    for item in basket:
        print(
            f"{item['name']}: {item['quantity']} x "
            f"Rs. {item['price']:.2f} = "
            f"Rs. {item['quantity'] * item['price']:.2f}"
        )

    print(f"\nSubtotal       : Rs. {subtotal:.2f}")
    print(f"Discount       : {rate * 100:.0f}%")
    print(f"Discount amount: Rs. {discount:.2f}")
    print(f"Final total    : Rs. {total:.2f}")
    print(f"Budget         : Rs. {budget:.2f}")

    if total <= budget:
        print("\nStatus: Shopping basket is within budget.")
        return

    print(f"\nOver budget by Rs. {total - budget:.2f}")
    print("Reducing low-priority products...")

    revised_basket, reductions = reduce_basket(basket, budget)

    subtotal, discount, total, rate = calculate_total(revised_basket)

    print("\n========== REVISED BASKET ==========")
    for item in revised_basket:
        print(
            f"{item['name']}: {item['quantity']} unit(s) "
            f"= Rs. {item['quantity'] * item['price']:.2f}"
        )

    print(f"\nRevised subtotal: Rs. {subtotal:.2f}")
    print(f"Discount rate   : {rate * 100:.0f}%")
    print(f"Discount amount : Rs. {discount:.2f}")
    print(f"Final total     : Rs. {total:.2f}")
    print(f"Remaining budget: Rs. {budget - total:.2f}")

    print("\nPRODUCT REDUCTION SUMMARY")
    if reductions:
        for name in dict.fromkeys(reductions):
            print(f"- Reduced quantity of {name}")
    else:
        print("No products reduced.")

    if total <= budget:
        print("\nStatus: Budget constraint satisfied.")
    else:
        print("\nStatus: Budget could not be satisfied.")


if __name__ == "__main__":
    main()
