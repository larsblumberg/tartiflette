from typing import Optional, Union

from tartiflette.language.ast.base import Node


class VariableDefinitionNode(Node):
    """
    TODO:
    """

    __slots__ = ("variable", "type", "default_value", "location")

    def __init__(
        self,
        variable: "VariableNode",
        type: Union["NamedTypeNode", "NonNullTypeNode", "ListTypeNode"],
        default_value: Optional["ValueNode"] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param variable: TODO:
        :param type: TODO:
        :param default_value: TODO:
        :param location: TODO:
        :type variable: TODO:
        :type type: TODO:
        :type default_value: TODO:
        :type location: TODO:
        """
        # pylint: disable=redefined-builtin
        self.variable = variable
        self.type = type
        self.default_value = default_value
        self.location = location

    def __eq__(self, other):
        """
        TODO:
        :param other: TODO:
        :type other: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return self is other or (
            isinstance(other, VariableDefinitionNode)
            and (
                self.variable == other.variable
                and self.type == other.type
                and self.default_value == other.default_value
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return (
            "VariableDefinitionNode(variable=%r, type=%r, default_value=%r, location=%r)"
            % (self.variable, self.type, self.default_value, self.location)
        )