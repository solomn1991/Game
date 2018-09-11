import objgraph, sys


class OBJ(object):
    pass


def show_direct_cycle_reference():
    a = OBJ()
    a.attr = a
    objgraph.show_backrefs(a, max_depth=5, filename="direct.dot")


def show_indirect_cycle_reference():
    a, b = OBJ(), OBJ()
    a.attr_b = b
    b.attr_a = a
    objgraph.show_backrefs(a, max_depth=5, filename="indirect.dot")


if __name__ == '__main__':
    # show_direct_cycle_reference()
    # show_indirect_cycle_reference()
    objgraph.show_backrefs(a, max_depth=5, filename="indirect.dot")
