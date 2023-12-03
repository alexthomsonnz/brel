from pybr.resource import BrelLabel
from pybr.networks import INetworkNode
from pybr.reportelements import IReportElement
from pybr import QName

from typing import cast

from pybr.resource import IResource

DEBUG = False

class LabelNetworkNode(INetworkNode):
    """
    Class for representing a label network node in a label network.
    Label networks are essentially sets of individual report elements.
    """
    def  __init__(
            self,
            points_to: IReportElement|BrelLabel,
            arc_role: str,
            arc_name: QName,
            link_role: str,
            link_name: QName,
                  ) -> None:

        self.__points_to = points_to
        self.__arc_role = arc_role
        self.__arc_name = arc_name
        self.__link_role = link_role
        self.__link_name = link_name
        self.__children: list[INetworkNode] = []
    
    # First class citizens
    def get_report_element(self) -> IReportElement:
        if not isinstance(self.__points_to, IReportElement):
            raise ValueError("LabelNetworkNodes do not point to report elements")
        return self.__points_to
    
    def get_resource(self) -> BrelLabel:
        if not isinstance(self.__points_to, BrelLabel):
            raise ValueError("LabelNetworkNodes do not point to resources")
        return self.__points_to
    
    def is_a(self) -> str:
        if isinstance(self.__points_to, IReportElement):
            return 'report element'
        elif isinstance(self.__points_to, BrelLabel):
            return 'resource'
        else:
            raise ValueError("LabelNetworkNodes do not point to report elements or resources")
    
    def get_children(self) -> list[INetworkNode]:
        return self.__children
    
    def get_order(self) -> int:
        return 1
    
    def get_arc_role(self) -> str:
        return self.__arc_role
    
    def get_arc_name(self) -> QName:
        return self.__arc_name
    
    def get_link_role(self) -> str:
        return self.__link_role
    
    def get_link_name(self) -> QName:
        return self.__link_name
    
    # Internal methods
    def add_child(self, child: INetworkNode):
        self.__children.append(child)
    
        