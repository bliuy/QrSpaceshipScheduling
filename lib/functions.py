import typing

# Defining generic functions
GenericFunctionType = typing.Callable[..., typing.Any]


def timer(func: GenericFunctionType):
    pass
