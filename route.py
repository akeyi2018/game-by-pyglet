def generate_routes(current_pos, target_pos):
    routes = []
    for i in range(min(len(current_pos), len(target_pos))):
        start = current_pos[i]
        end = target_pos[i]
        route = [start]
        
        current = start
        while current != end:
            x, y = current
            tx, ty = end
            
            # X方向の移動
            if x < tx:
                x += 1
            elif x > tx:
                x -= 1
            # Y方向の移動
            elif y < ty:
                y += 1
            elif y > ty:
                y -= 1
            
            current = (x, y)
            route.append(current)
        
        routes.append(route)
    return routes

def move_customers_one_by_one(routes):
    current_positions = [route[0] for route in routes]
    customer_routes = routes
    max_steps = max(len(route) for route in customer_routes) if customer_routes else 0
    all_arrived = False

    for step in range(max_steps):
        if all(current_positions[i] == route[-1] for i, route in enumerate(customer_routes)):
            print("\nAll customers have arrived at their targets. Simulation ended.")
            all_arrived = True
            break

        print(f"\nStep {step + 1}:")
        for i, route in enumerate(customer_routes):
            if current_positions[i] != route[-1]:  # 到着していない顧客のみ移動
                if step < len(route) - 1:
                    next_pos = route[step + 1]
                    current_positions[i] = next_pos
                    print(f"Customer {i + 1} moves from {route[step]} to {next_pos}")
                else:
                    current_positions[i] = route[-1]  # 最終位置に到着
                    print(f"Customer {i + 1} has reached the target position {route[-1]}")
            else:
                print(f"Customer {i + 1} is already at the target position {route[-1]}")

        print(f"Current positions after step {step + 1}: {current_positions}")

    if not all_arrived and all(current_positions[i] == route[-1] for i, route in enumerate(customer_routes)):
        print("\nAll customers have arrived at their targets. Simulation ended.")

# 例の使用
current_pos = [(14, 1)]
target_pos = [(17, 13)]

routes = generate_routes(current_pos, target_pos)
for i, route in enumerate(routes):
    print(f"Route from {current_pos[i]} to {target_pos[i]}:")
    print(route)

# 顧客を1人ずつ移動
move_customers_one_by_one(routes)