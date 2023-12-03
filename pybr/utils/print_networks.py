from pybr.networks import *
from pybr.reportelements import *
from pybr.resource import *
from pybr import BrelLabelRole

ELBOW = "└──"
PIPE  = "│  "
TEE   = "├──"
SPACE = "   "

def __print_subnetwork(node: INetworkNode, last=True, header='') -> None:
    output_string = ""


    node_is_a = node.is_a()
    if node_is_a == "resource":
        resource = node.get_resource()
        if isinstance(resource, BrelLabel):
            label_role = resource.get_role()
            label_role_str = label_role.split("/")[-1]
            label_language = resource.get_language()
            label_content = resource.get_content()[None]
            type_str = f"[LABEL] ({label_role_str} {label_language}) {label_content}"
        elif isinstance(resource, BrelReference):
            type_str = f"[REFERENCE] {resource.get_content()}"
        else:
            type_str = "[RESOURCE]"
        
        output_string += type_str
    elif node_is_a == "report element":
        re = node.get_report_element()
        node_labels = re.get_labels()

        if hasattr(re, "get_preferred_label_role"):
            label_role = getattr(re, "get_preferred_label_role")()
        else:
            label_role = BrelLabelRole.STANDARD_LABEL
        
        node_preferred_label = next(filter(lambda label: label.get_label_role() == label_role, node_labels), str(re.get_name()))
        node_as_str = str(node_preferred_label)

        if isinstance(re, PyBRDimension):
            type_str = "[DIMENSION]"
        elif isinstance(re, PyBRMember):
            type_str = "[MEMBER]"
        elif isinstance(re, PyBRLineItems):
            type_str = "[LINE ITEMS]"
        elif isinstance(re, PyBRHypercube):
            type_str = "[HYPERCUBE]"
        elif isinstance(re, PyBRConcept):
            type_str = "[CONCEPT]"
        elif isinstance(re, PyBRAbstract):
            type_str = "[ABSTRACT]"
        else:
            type_str = "[REPORT ELEMENT]"
        
        output_string += type_str + " " + node_as_str
    
    if hasattr(node, "get_weight"):
        weight = getattr(node, "get_weight")()
        weight_str = f"[W={weight:4}] "
    else:
        weight_str = ""

    # this adds some padding to the type header so that the node name is aligned
    padding = 14  # TODO: maybe not hardcode this
    if len(weight_str) != 0:
        padding_str = " " * (padding - len(weight_str))
    else:
        padding_str = ""

    output_string = weight_str + padding_str + output_string
    
    print(header + (ELBOW if last else TEE) + output_string)
    children = node.get_children()
    for index, child in enumerate(children):
        is_last_child = index == len(children) - 1
        child_header = header + (SPACE if last else PIPE)
        __print_subnetwork(child, is_last_child, child_header)

def pprint_network_node(node: INetworkNode):
    
    if node is None:
        return
    __print_subnetwork(node)

def pprint_network(network: INetwork | None):
    if network is None:
        return
    
    print(f"Network (link role: {network.get_link_role()}), link name: {network.get_link_name()}")
    print(f"arc roles: {network.get_arc_roles()}, arc name: {network.get_arc_name()}")
    
    for index, root in enumerate(network.get_roots()):
        is_last_root = index == len(network.get_roots()) - 1
        __print_subnetwork(root, is_last_root)
    print()
