def function(
    posonly_nohint,
    posonly_nonboolhint: int,
    posonly_boolhint: bool,
    posonly_boolstrhint: "bool",
    /,
    offset,
    posorkw_nonvalued_nohint,
    posorkw_nonvalued_nonboolhint: int,
    posorkw_nonvalued_boolhint: bool,
    posorkw_nonvalued_boolstrhint: "bool",
    posorkw_boolvalued_nohint=True,
    posorkw_boolvalued_nonboolhint: int = True,
    posorkw_boolvalued_boolhint: bool = True,
    posorkw_boolvalued_boolstrhint: "bool" = True,
    posorkw_nonboolvalued_nohint=1,
    posorkw_nonboolvalued_nonboolhint: int = 2,
    posorkw_nonboolvalued_boolhint: bool = 3,
    posorkw_nonboolvalued_boolstrhint: "bool" = 4,
    *,
    kwonly_nonvalued_nohint,
    kwonly_nonvalued_nonboolhint: int,
    kwonly_nonvalued_boolhint: bool,
    kwonly_nonvalued_boolstrhint: "bool",
    kwonly_boolvalued_nohint=True,
    kwonly_boolvalued_nonboolhint: int = False,
    kwonly_boolvalued_boolhint: bool = True,
    kwonly_boolvalued_boolstrhint: "bool" = True,
    kwonly_nonboolvalued_nohint=5,
    kwonly_nonboolvalued_nonboolhint: int = 1,
    kwonly_nonboolvalued_boolhint: bool = 1,
    kwonly_nonboolvalued_boolstrhint: "bool" = 1,
    **kw,
):
    ...


def used(do):
    return do


def b():
    used(True)


class MyClass:

    @property
    def some_attribute(self) -> bool:
        return self._attribute

    @some_attribute.setter
    def some_attribute(self, value: bool) -> None:
        self._atrribute = value

    @decorator
    def non_setter(self, value: bool) -> None:
        ...
