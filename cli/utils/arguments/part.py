from enum import Enum

from cli.utils.part import Part


class PartArg(str, Enum):
    """Argument version of Part since typer does not like IntEnum."""

    A = "a"
    B = "b"

    def to_part(self) -> Part:
        """Convert PartArg to Part."""
        match self:
            case PartArg.A:
                return Part.A
            case PartArg.B:
                return Part.B
