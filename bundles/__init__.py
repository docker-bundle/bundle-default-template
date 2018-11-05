import env

def include(*libs):
    actions = {}
    for lib in libs:
        actions.update(lib.exports)
    return actions

actions = include(env)
