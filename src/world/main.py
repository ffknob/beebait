import asyncio

from world.world import World
from world.feature import Temperature, RelativeHumidity
from world.model import FeatureStatistics


async def main():
    temperature = Temperature(
        FeatureStatistics(min=21, max=30, mean=25, median=26)
    )
    relative_humidity = RelativeHumidity(
        FeatureStatistics(min=21, max=30, mean=25, median=26)
    )

    world = World(features={temperature, relative_humidity})

    world.emit()


if __name__ == "__main__":
    asyncio.run(main())
