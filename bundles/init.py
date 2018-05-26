# After it installed, docker-bundle will import it.

def init(args = []):
    print('Initial Project Config')

    # TODO, input your init action here
    # for example, put your PROJECT_NAME into .env file in folder
    project_name = input("Please input your project name: ")
    env = open('.env', 'w')
    env.write("PROJECT_NAME='%s'"%project_name)
    env.flush()
    env.close()

# Put your action here.
# It's the register of your handle function.
# Don't forgot write your action's description.
actions = {
    'init': {
        'desc': 'Initial Project Config',
        'action': init
    }
#   ,
#   'other': {
#       'desc': 'Other Actions....Like this',
#       'action': <Put your function here>
#   }
#   ....
}
