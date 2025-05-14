bus_line =['김수몽','이사슴','박밀레']
bus_line.append('최지하')
bus_seat = ['구백녀','서교수']

print("3명 탑승")
bus_seat.append(bus_line.pop(0))
print("버스안 탑승객 =",bus_seat)
bus_seat.append(bus_line.pop(0))
print("버스안 탑승객 =",bus_seat)
bus_seat.append(bus_line.pop(0))
print("버스안 탑승객 =",bus_seat)
bus_seat.append(bus_line.pop(0))
print("버스안 탑승객 =",bus_seat)

print("3명 내림")

bus_line.append(bus_seat.pop(0))
print("버스안 탑승객 =",bus_seat)
bus_line.append(bus_seat.pop(0))
print("버스안 탑승객 =",bus_seat)
bus_line.append(bus_seat.pop(0))
print("버스안 탑승객 =",bus_seat)