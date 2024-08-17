from typing import Literal, Union
from textwrap import indent, dedent


def indent_4(s: str) -> str:
    return indent(s, "    ")


def get_symbol_priority(kind: Literal["binary", "unary"], symbol):
    """
    Get the priority of symbols.
    """
    if kind == "binary":
        return {
            "&": 6,
            "||": 6,
            "^": 6,
            ">=": 5,
            "<=": 5,
            ">": 5,
            "<": 5,
            "=": 5,
            "!=": 5,
            "+": 4,
            "-": 4,
            "<<": 4,
            ">>": 4,
            "*": 3,
            "/": 3,
            "%": 3,
        }[symbol]
    else:
        return {"A<>": 10}[symbol]


def get_expr_priority(expr: "Expr"):
    match expr:
        case BinaryOperator():
            return get_symbol_priority("binary", expr.operator)
        case UnaryOperator():
            return get_symbol_priority("unary", expr.operator)
        case Identifier() | Const():
            return -1  # Highest priority
        case _:
            raise NotImplementedError(expr)


def to_dict_handler(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    elif isinstance(obj, (list, tuple, set)):
        return [to_dict_handler(i) for i in obj]
    else:
        return obj


class BasicSemantic:
    def to_dict(self):
        new_dict = {"_cls": self.__class__.__name__}
        for k, v in self.__dict__.items():
            # if isinstance(v, BasicSemantic):
            #     new_dict[k] = v.to_dict()
            # if isinstance(v, list):
            #     new_dict[k] = [(x.to_dict() if hasattr(x, 'to_dict') else x )for x in v]
            # else:
            new_dict[k] = to_dict_handler(v)
        return new_dict

    def unparse(self):
        """
        Unparse and print the LTL formula.
        """
        raise NotImplementedError(self.__class__)

    @classmethod
    def unparse_list(cls, elements: list, separator: str = "\n"):
        return separator.join([e.unparse() for e in elements])


class Type(BasicSemantic):
    pass


class BooleanType(Type):
    def unparse(self):
        return "boolean"


class ModuleType(Type):
    # identifier LPAREN parameter_list RPAREN
    def __init__(self, identifier: "Identifier", parameter_list: list["Expr"]):
        self.identifier = identifier
        self.parameter_list = parameter_list

    def unparse(self):
        params_unparsed = ", ".join([expr.unparse() for expr in self.parameter_list])
        return f"{self.identifier.unparse()}({params_unparsed})"


class EnumerationTypeValue(Type):
    def __init__(self, identifier: Union["Identifier", "Const"]):
        self.identifier = identifier


class EnumerationType(Type):
    def __init__(self, body: list[EnumerationTypeValue]):
        self.body = body

    def unparse(self):
        s = ", ".join([value.identifier.unparse() for value in self.body])
        return "{" + s + "}"


# class BasicSemantic:
#     def __init__(self, location: "Location"):
#         self.location = location


class Expr(BasicSemantic):
    pass
    # def to_dict(self):
    #     new_dict = {}
    #     for k, v in self.__dict__.items():
    #         if isinstance(v, Expr):
    #             new_dict[k] = v.to_dict()
    #         else:
    #             new_dict[k] = v
    #     return new_dict

    # def unparse(self):
    #     """
    #     Unparse and print the LTL formula.
    #     """
    #     raise NotImplementedError


class Identifier(Expr):
    def __init__(self, name: str) -> None:
        self.name = name

    # def __str__(self) -> str:
    #     return self.name

    def unparse(self):
        return self.name


class ComplexIdentifier(Expr):
    def __init__(
        self, target: Expr, item: Expr, type: Literal["index", "field", "none"]
    ) -> None:
        self.item = item
        self.type = type
        self.target = target

    def unparse(self):
        target_uparsed = self.target.unparse() if self.target else ""
        item_uparsed = self.item.unparse() if self.item else ""
        match self.type:
            case "none":
                return f"{target_uparsed}"
            case "index":
                return f"{target_uparsed}[{item_uparsed}]"
            case "field":
                return f"{target_uparsed}.{item_uparsed}"
            case _:
                raise NotImplementedError(self.type)


class Const(Expr):
    def __init__(
        self, value: str | int | bool, type: Literal["int", "boolean", "string"]
    ) -> None:
        self.value = value
        self.type = type

    def unparse(self):
        match self.type:
            case "boolean":
                return str(self.value).upper()
            case _:
                return str(self.value)


class UnaryOperator(Expr):
    def __init__(self, operator, operand) -> None:
        self.operator = operator
        self.operand = operand

    # def __str__(self) -> str:
    #     return f"({self.operator} {self.operand})"

    def unparse(self):
        priority_this = get_expr_priority(self)
        priority_operator = get_expr_priority(self.operand)
        operand_parsed = self.operand.unparse()
        if priority_operator >= priority_this:
            return f"{self.operator} ({operand_parsed})"
        else:
            return f"{self.operator} {operand_parsed}"


# class VarDeclaration(Expr):
#     def __init__(self, name: str, type: str) -> None:
#         self.name = name
#         self.type = type

#     def unparse(self):
#         return f"{self.type} {self.name}"


class Module(BasicSemantic):
    # identifier, body等属性
    def __init__(self, name: Identifier, body: list) -> None:
        self.name = name
        self.body = body

    def unparse(self):
        payload = "\n".join([item.unparse() for item in self.body])
        s = dedent(
            """
        MODULE {name}
        {payload}
        """
        )
        return s.format(name=self.name.unparse(), payload=payload)


class VarDeclItem(BasicSemantic):
    def __init__(self, identifier: Identifier, type_specifier: Union[BooleanType, EnumerationType]) -> None:
        self.identifier = identifier
        self.type_specifier = type_specifier

    def unparse(self):
        return f"{self.identifier.unparse()} : {self.type_specifier.unparse()} ;"


class Assign(BasicSemantic):
    def __init__(
        self,
        target: Identifier,
        expr: Expr,
        modifier: Literal["init", "next", "none"] = "none",
    ) -> None:
        self.target = target
        self.expr = expr
        assert self.target is not None
        assert self.expr is not None
        self.modifier = modifier

    def unparse(self):
        match self.modifier:
            case "init":
                return f"init({self.target.unparse()}) := {self.expr.unparse()};"
            case "next":
                return f"next({self.target.unparse()}) := {self.expr.unparse()};"
            case "none":
                return f"{self.target.unparse()} := {self.expr.unparse()};"
            case _:
                raise ValueError(self.modifier)


class SetExpr(Expr):
    def __init__(self, set_body: list[Expr]) -> None:
        self.set_body = set_body

    def unparse(self):
        return "{" + self.unparse_list(self.set_body, ", ") + "}"


class CaseBodyItem(BasicSemantic):
    def __init__(self, condition: Expr, expr: Expr) -> None:
        self.condition = condition
        self.expr = expr

    def unparse(self):
        return f"{self.condition.unparse()} : {self.expr.unparse()} ;"


class CaseExpr(BasicSemantic):
    def __init__(self, case_body: list[BasicSemantic]) -> None:
        self.case_body = case_body

    def unparse(self):
        template = dedent(
            """
            case
            {case_body}
            esac
            """
        )
        # return  self.unparse_list(self.case_body) + "\nesac"
        return template.format(
            case_body=indent_4(self.unparse_list(self.case_body, "\n"))
        )


class AssignConstraint(BasicSemantic):
    def __init__(self, assigns_list: list[Assign|CaseExpr]) -> None:
        self.assigns_list = assigns_list

    def unparse(self):
        template = dedent(
            """
            ASSIGN
            {assigns_list}
            """
        )
        return template.format(
            assigns_list=indent_4(self.unparse_list(self.assigns_list))
        )


class VarDeclaration(BasicSemantic):
    def __init__(self, var_list: list[VarDeclItem]) -> None:
        self.var_list = var_list

    def unparse(self):
        template = dedent(
            """
                                           VAR
                                           {var_list}
                                           """
        )

        return template.format(var_list=indent_4(self.unparse_list(self.var_list)))


# class VarList(BasicSemantic):
#     def __init__(self, var_list: list[VarDeclItem]) -> None:
#         self.var_list = var_list


class BinaryOperator(Expr):
    def __init__(self, left, operator, right) -> None:
        self.left: Expr = left
        self.operator = operator
        self.right: Expr = right

    # def __str__(self) -> str:
    #     return f"({self.left} {self.operator} {self.right})"

    def unparse(self):
        """
        Compare the priority on this level (priority_this) and
            the sub-expressions (priority_left, priority_right).
        """

        priority_this = get_expr_priority(self)
        priority_left = get_expr_priority(self.left)
        priority_right = get_expr_priority(self.right)
        left_unparsed = self.left.unparse()
        right_unparsed = self.right.unparse()

        # If left operand does not have priority
        # then add brackets
        if priority_left >= priority_this:
            left_unparsed = f"({left_unparsed})"
        # If right operand does not have priority
        # then add brackets
        if priority_right >= priority_this:
            right_unparsed = f"({right_unparsed})"
        return f"{left_unparsed} {self.operator} {right_unparsed}"
