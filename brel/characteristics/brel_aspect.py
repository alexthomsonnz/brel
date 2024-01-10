"""
This module contains the Aspect class.
Aspects are the building blocks of the [Context](./contexts.md) of a fact.
They are split into two categories: core aspects and custom aspects.

Core aspects are the 5 base aspects: concept, period, entity and unit.

Custom aspects are all other aspects that are not core aspects.

====================

- author: Robin Schmidiger
- version: 0.2
- date: 08 January 2024

====================
"""

from brel import BrelLabel, QName


class Aspect:
    """
    Base class for all aspects.
    An an aspect is a wrapper around a string-id.
    This string-id is called the name of the aspect.
    An aspect can also have human readable labels for its name.
    The four core aspects are instances of this class and are accessible as class attributes.

    These four core aspects are available as the following class attributes:

    - `Aspect.CONCEPT`
    - `Aspect.PERIOD`
    - `Aspect.ENTITY`
    - `Aspect.UNIT`

    A lot of reports omit the language aspect, but it can be emulated by using a custom aspect.
    All but the concept aspect are optional for a context.

    """

    CONCEPT: "Aspect"
    PERIOD: "Aspect"
    ENTITY: "Aspect"
    UNIT: "Aspect"

    __aspect_cache: dict[str, "Aspect"] = {}

    def __init__(self, name: str, labels: list[BrelLabel]) -> None:
        self.__name = name
        self.__labels = labels

    # first class citizens
    def get_name(self) -> str:
        """
        Get the name of the aspect.
        """
        return self.__name

    def is_core(self) -> bool:
        """
        Check if the aspect is a core aspect.
        """
        return False

    def get_labels(self) -> list[BrelLabel]:
        """
        Get the labels of the aspect.
        """
        return self.__labels

    def __hash__(self) -> int:
        return hash(self.__name)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Aspect):
            return self.__name == __value.get_name()
        return False

    # second class citizens
    def __str__(self) -> str:
        return self.__name

    # internal methods
    @classmethod
    def from_QName(
        cls, qname: QName, labels: list[BrelLabel] | None = None
    ) -> "Aspect":
        """
        Creates a new aspect from a QName.
        The method `get_name()` of the newly created aspect will return the string generated by `qname.get()`.
        :param qname: the QName to create the aspect from
        :param labels: A list of labels for the aspect. If None, an empty list is used.
        """
        qname_str = qname.get()
        return cls.from_str(qname_str, labels)

    @classmethod
    def from_str(cls, name: str, labels: list[BrelLabel] | None = None) -> "Aspect":
        """
        Creates a new aspect from a string.
        To access the core aspects, use the class attributes
        `Aspect.CONCEPT`, `Aspect.PERIOD`, `Aspect.ENTITY` and `Aspect.UNIT` instead.
        :param name: The name of the aspect
        :param labels: A list of labels for the aspect. If None, an empty list is used.
        """
        if name in cls.__aspect_cache:
            return cls.__aspect_cache[name]

        if labels is None:
            labels = []

        return cls(name, labels)


# initialize the core aspects
concept_labels = [
    BrelLabel("Concept [Axis]", "concept", "en-US"),
    BrelLabel("Konzept [Achse]", "concept", "de-DE"),
    BrelLabel("Concepto [Eje]", "concept", "es-ES"),
]

period_labels = [
    BrelLabel("Period [Axis]", "period", "en-US"),
    BrelLabel("Periode [Achse]", "period", "de-DE"),
    BrelLabel("Periodo [Eje]", "period", "es-ES"),
]

entity_labels = [
    BrelLabel("Entity [Axis]", "entity", "en-US"),
    BrelLabel("Organisation [Achse]", "entity", "de-DE"),
    BrelLabel("Entidad [Eje]", "entity", "es-ES"),
]

unit_labels = [
    BrelLabel("Unit [Axis]", "unit", "en-US"),
    BrelLabel("Einheit [Achse]", "unit", "de-DE"),
    BrelLabel("Unidad [Eje]", "unit", "es-ES"),
]

Aspect.CONCEPT = Aspect("concept", concept_labels)
Aspect.PERIOD = Aspect("period", period_labels)
Aspect.ENTITY = Aspect("entity", entity_labels)
Aspect.UNIT = Aspect("unit", unit_labels)


def true_func() -> bool:
    return True


Aspect.CONCEPT.is_core = true_func
Aspect.PERIOD.is_core = true_func
Aspect.ENTITY.is_core = true_func
Aspect.UNIT.is_core = true_func