from typing import Self, Optional

from world.feature import Feature


class World:
    def __init__(self, features: Optional[set[Feature]] = None):
        self.features = features if features else set()

    def register_feature(self, feature: Feature) -> Self:
        self.features.add(feature)
        return self

    def emit(self) -> Self:
        for feature in self.features:
            feature.sample()

        return self
