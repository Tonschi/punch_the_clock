from datetime import datetime as dt
import uuid

CurrentPosixTime = dt.timestamp(dt.now())
Timestamp = dt.fromtimestamp(CurrentPosixTime)
Day = Timestamp.strftime("%d")
Month = Timestamp.strftime("%m")
Year = Timestamp.strftime("%Y")

print(Timestamp)
print(Day, Month, Year)
i = 0
while i < 5:
    print(uuid.uuid4())
    i += 1
