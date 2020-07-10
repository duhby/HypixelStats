import main

quota = main.utils.load_obj("quota")
topusers = {k: v for k, v in sorted(quota.items(), key=lambda item: item[1], reverse=True)}
topusers = main.utils.clean_msg(str(topusers))
topusers = topusers.split(" ")
topusers = topusers[:6] # displays 3 users
topusers = main.utils.clean_msg(str(topusers))
print(f"Unique users - {len(quota)}")
print(f"Total requests - {sum(quota.values())}")
print(f"Top users -\n{topusers}")
input()
