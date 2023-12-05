import lxml
import lxml.etree

from brel import QName
from brel.networks import INetwork, CalculationNetworkNode, INetworkNode
from brel.reportelements import *

from typing import cast

class CalculationNetwork(INetwork):
    """
    Class for representing a presentation network.
    A presentation network is a network of nodes that represent the presentation of a Component.
    """
    def __init__(self, roots: list[CalculationNetworkNode], link_role: str, link_name: QName) -> None:
        roots_copy = [cast(INetworkNode, root) for root in roots]
        super().__init__(roots_copy, link_role, link_name, True)
    
    
    # second class citizens
    def validate(self, filing) -> bool:
        """
        Validate the presentation network against the Filing
        @param filing: Filing to validate against
        @return: bool indicating whether the presentation network is valid
        """
        # TODO: make nice
        # TODO: look at validation of calculation networks again
        def __validate_subtree(node: CalculationNetworkNode) -> bool:
            """
            Validate a subtree of the presentation network
            @param node: NetworkNode representing the root of the subtree
            @return: bool indicating whether the subtree is valid
            """
            # if the node has no children, then it is valid
            if len(node.get_children()) == 0:
                return True

            # validate the children
            for child in node.get_children():
                if not __validate_subtree(child):
                    return False
            
            # validate the node itself
            # get the report element
            concept = cast(Concept, node.get_report_element())

            # get the fact value associated with the concept
            facts = filing.get_facts_by_concept(concept)

            for fact in facts:
                fact_value = float(fact.get_value())

                children_aggregate = 0

                for child_node in node.get_children():
                    child_concept = cast(Concept, child_node.get_report_element())
                    child_facts = filing.get_facts_by_concept(child_concept)

                    # get the right fact by comparing the context
                    # TODO: currently just gets the right context by finding the one where the period is the same. Extend this to also check the entity, unit, etc.
                    child_fact = next(filter(lambda x: x.get_context() == fact.get_context(), child_facts), None)

                    child_fact_value = float(child_fact.get_value())
                    child_weight = float(child_node.get_weight())

                    children_aggregate += child_fact_value * child_weight
                
                if fact_value != children_aggregate:
                    return False
            
            return True
        
        return __validate_subtree(self.__roots)
                