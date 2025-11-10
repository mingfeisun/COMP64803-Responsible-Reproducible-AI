# Dict comprehension

floors = ["floor 1", "floor 2", "floor 3", "floor 4"]

rooms = [("m1", 2), ("n2", 3), ("Meeting room 1", 1)]

rooms_dict = {room: floors[i] for (room, i) in rooms}

print(rooms_dict)