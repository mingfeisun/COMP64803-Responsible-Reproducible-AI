import random

#random signals
event_signals = [random.randint(0, 100) for _ in range(5)]
threshold = 80

# #see if any region exceeds threshold
# found = False
# for signal in event_signals:
#     if signal > threshold:
#         found = True
#         break

# print("Event passed threshold:", found)

#use generator instead of evaluating all
passed = any(signal > threshold for signal in event_signals)

print("Event passed threshold:", passed)
