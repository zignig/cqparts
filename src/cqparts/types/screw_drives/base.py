import six
import cadquery

from ...params import *

class ScrewDrive(ParametricObject):
    diameter = PositiveFloat(3.0, doc="screw drive's diameter")
    depth = PositiveFloat(3.0, doc="depth of recess into driven body")

    def apply(self, workplane, offset=(0, 0, 0)):
        """
        Application of screwdrive indentation into a workplane (centred around it's origin)
        """
        raise NotImplementedError("apply function not overridden in %r" % self)


# Screw Drive register
#   Create your own screw drive like so...
#
#       @screw_drive('some_name')
#       class MyScrewDrive(ScrewDrive):
#           my_param = 1.2
#
#           def apply(self, workplane, offset):
#               tool = cadquery.Workplane("XY") \
#                   .rect(self.diameter, self.diameter) \
#                   .extrude(-self.depth) \
#                   .faces(">Z") \
#                   .rect(self.my_param, self.diameter / 2) \
#                   .extrude(-self.depth)
#               return workplane.cut(tool.translate(offset))

screw_drive_map = {}


def screw_drive(*names):
    assert all(isinstance(n, six.string_types) for n in names), "bad screw drive name"
    def inner(cls):
        """
        Add screw drive class to mapping
        """
        assert issubclass(cls, ScrewDrive), "class must inherit from ScrewDrive"
        for name in names:
            assert name not in screw_drive_map, "more than one screw_drive named '%s'" % name
            screw_drive_map[name] = cls
        return cls

    return inner


def find(name):
    return screw_drive_map[name]
