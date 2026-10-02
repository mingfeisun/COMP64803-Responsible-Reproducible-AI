from decimal import Decimal

rate = Decimal('1.45')
time = Decimal(3*60 + 42)
cost = rate * time / Decimal(60)
print(cost)

print(Decimal('1.45'))
print(Decimal(1.45))