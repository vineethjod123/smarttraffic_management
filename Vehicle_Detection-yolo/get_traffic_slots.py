def get_traffic_slots(list):
    nlanes = len(list)
    baseTimer = 20 # baseTimer = int(input("Enter the base timer value"))
    trafficlight = []
    for i in list:
        t = round(i / sum(list) * baseTimer)
        # print(t)
        trafficlight.append(t)
    return baseTimer, trafficlight