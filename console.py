def Add(balances, rate):
    amounts = [num for num in balances] 
    for i in range(len(balances)):
        amounts[i]*=1+rate
    return 1, 2
def test():
    amounts = [23,3242,432,652]
    rate = 0.5
    x,y = Add(amounts, rate)
    print(amounts)
    print(x)
    print(y)

test()