"""
This module contains the class for representing a calculation network.
A calculation network is a network of nodes that represent the calculation of a Component.
Calculation networks also contain helper functions for checking the consistency of the calculation network specifically.

@author: Robin Schmidiger
@version: 0.3
@date: 29 December 2023
"""

DEBUG = False

from brel import QName, Fact
from brel.networks import INetwork, CalculationNetworkNode, INetworkNode
from brel.characteristics import BrelAspect, ICharacteristic
from brel.reportelements import *

from typing import cast


class CalculationNetwork(INetwork):
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a Component.
    """

    def __init__(
        self, roots: list[CalculationNetworkNode], link_role: str, link_name: QName
    ) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, True)

    # second class citizen
    def is_balance_consisent(self) -> bool:
        """
        Returns true if the network is balance consistent.
        A network is balance consistent iff, for each parent-child relationship
        - if the two concepts have the same balance (credit/credit or debit/debit), then the child weight must be positive
        - if the two concepts have different balances (credit/debit or debit/credit), then the child weight must be negative
        """

        def is_subtree_balance_consistent(node: CalculationNetworkNode) -> bool:
            """
            Returns true if the subtree rooted at node is balance consistent.
            Operates recursively.
            Returns false if
            - Any parent or child balance is None
            - The parent and child balances are the same, but the child weight is negative
            - The parent and child balances are different, but the child weight is positive
            - Any child subtree is not balance consistent
            Returns true otherwise
            """
            # get the balance of the parent
            parent_balance = node.get_concept().get_balance_type()
            if parent_balance is None:
                return False

            # check the balance of the children
            for child in node.get_children():
                child = cast(CalculationNetworkNode, child)

                child_balance = child.get_concept().get_balance_type()
                if child_balance is None:
                    return False

                if parent_balance == child_balance:
                    if child.get_weight() < 0:
                        return False
                else:
                    if child.get_weight() > 0:
                        return False

                # check the balance of the children of the child
                if not is_subtree_balance_consistent(child):
                    return False

            return True

        # check the balance of the roots
        for root in self.get_roots():
            root = cast(CalculationNetworkNode, root)
            if not is_subtree_balance_consistent(root):
                return False

        return True

    def is_aggregation_consistent(self, facts: list[Fact]) -> bool:
        """
        A calculation network is aggregation consistent iff for all nodes, all children add up to the parent
        :returns: True iff the network is aggregation consistent
        """

        def is_subnetwork_aggregation_consistent(node: CalculationNetworkNode) -> bool:
            """
            Returns true if the subtree rooted at node is aggregation consistent.
            Operates recursively.
            Returns false if
            - the sum of all children values does not equal the parent value
            - any child subtree is not aggregation consistent
            Returns true otherwise
            """
            # if the node is a leaf, it is aggregation consistent
            # even though this case would be captured by the following code, it is more efficient to short circuit the trivial case without querying the facts
            if node.is_leaf():
                return True

            concept = node.get_concept()
            node_facts = list(
                filter(lambda fact: fact.get_concept().get_value() == concept, facts)
            )

            for node_fact in node_facts:
                node_value = node_fact.get_value_as_float()

                # get the sum of the children values
                children_sum: float = 0
                for child in node.get_children():
                    child = cast(CalculationNetworkNode, child)
                    child_concept = child.get_concept()
                    child_facts = filter(
                        lambda fact: fact.get_concept().get_value() == child_concept,
                        facts,
                    )
                    # go over each aspect of the node fact (except the concept) and filter the child facts by that aspect
                    for node_aspect in node_fact.get_aspects():
                        if node_aspect != BrelAspect.CONCEPT:
                            node_characteristic = node_fact.get_characteristic(
                                node_aspect
                            )
                            child_facts = filter(
                                lambda fact: fact.get_characteristic(node_aspect)
                                == node_characteristic,
                                child_facts,
                            )

                    # there should only be one child fact left
                    child_fact = next(child_facts)
                    children_sum += child_fact.get_value_as_float() * child.get_weight()

                if DEBUG:  # pragma: no cover
                    print(
                        f"node concept: {concept}, node value: {node_value}, children sum: {children_sum}"
                    )

                if node_value != children_sum:
                    return False

                # check the children
                for child in node.get_children():
                    child = cast(CalculationNetworkNode, child)
                    if not is_subnetwork_aggregation_consistent(child):
                        return False

            return True

        # check the roots
        for root in self.get_roots():
            root = cast(CalculationNetworkNode, root)
            if not is_subnetwork_aggregation_consistent(root):
                return False

        return True
