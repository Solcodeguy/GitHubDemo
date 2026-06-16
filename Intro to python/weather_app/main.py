from utils.formatter import format_temp
from utils import fetcher

print("--- WEATHER DASHBOARD ---")
raw_temp = fetcher.get_weather()
print(f"Current Temperature: {format_temp(raw_temp)}")
