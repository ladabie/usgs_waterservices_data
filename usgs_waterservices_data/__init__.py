hard_dependencies = ("pandas","requests","re")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n"+"\n".join(missing_dependencies)
    )

from .daily_services_data import WaterStationDailyData
