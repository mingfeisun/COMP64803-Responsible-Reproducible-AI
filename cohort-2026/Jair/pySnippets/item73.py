import heapq
tasks = []

heapq.heappush(tasks, (3, "Fix critical bug"))
heapq.heappush(tasks, (2, "Reply to emails"))
heapq.heappush(tasks, (4, "Write documentation"))
heapq.heappush(tasks,(1, "Fix login issue"))
heapq.heappush(tasks,(5, "Update user profile page"))

while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"Priority {priority}: {task}")
