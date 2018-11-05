import os

def line_seperator(sep_str, max_len = None):
    line_len = os.get_terminal_size().columns
    out_len = min(max_len or line_len, line_len)
    out_str = sep_str
    if len(out_str) > 0 and out_len > len(out_str):
        out_str = sep_str * (out_len // len(out_str))
    return out_str

def load_env():
    try:
        for e in list(filter(lambda x:x!='', map(lambda x:x.strip(), open('.env').readlines()))):
            k,v = e.split('=')
            os.environ[k] = v
    except:
        pass

def input_default(text, default):
    value = input(text + ' [' + default + ']:')
    if value == '':
        value = default
    return value

def input_num(hint, default, num_range, error):
    while True:
        value = input_default(hint, default)
        try:
            num = int(value)
        except:
            num = None
        if num in num_range:
            return num
        else:
            print(error)

def input_clean(str):
    return str.replace(' ', '_').replace(':', '_')

def input_format(text, default):
    return input_default(text, default).replace(' ', '_').replace(':', '_')

def init(args = []):
    print()

    inits = [
        ('PROJECT_NAME',  lambda :(input_format("Please input your project name",
                                                 os.environ.get('PROJECT_NAME') or os.path.basename(os.path.dirname(os.getcwd()))))),
        ('SERVICE_NAME',  lambda :(input_format("Please input your service name",
                                                 os.environ.get('SERVICE_NAME') or 'app'))),
    ]

    config_data = ''
    for item in inits:
        key,runner = item
        value = runner()
        os.environ[key] = value
        config_data += "%s=%s\n"%(key,value)

    env_file = open('.env', 'w')
    env_file.write(config_data)
    env_file.close()

    print()

#--------------------------------------------------------------------------------------

load_env()

if not os.environ.get('PROJECT_NAME'):
    init()

config_file_name = 'docker-compose.yml'
env = os.environ['ENV'] = os.environ.get('ENV', 'development')
project_name = os.environ.get('PROJECT_NAME')

DOCKER_COMPOSE='docker-compose'
WINPTY = 'winpty'
if 0 == os.system('type %s > /dev/null 2>&1'%WINPTY):
    DOCKER_COMPOSE=WINPTY + ' ' + DOCKER_COMPOSE


def docker_compose(command):
    return "%s --project-name %s -f %s %s "%(DOCKER_COMPOSE, project_name + '_' + env, config_file_name, command)

def docker_compose_env(command):
    env_compose_file = ' -f %s.%s '%(config_file_name, env)
    return docker_compose(env_compose_file + command)

def action(command):
    def _run(args = []):
        _command = command
        if len(args) > 0:
            _command += (' ' + ' '.join(args))
        return os.system(_command)
    return _run

SERVICE_NAME = os.environ['SERVICE_NAME']

up = lambda :('up --build -d %s'%SERVICE_NAME)
down = lambda :('down --remove-orphans')
start = lambda :('start')
stop = lambda :('stop')
_exec = lambda :('exec %s'%SERVICE_NAME)
logs  = lambda :('logs')

def restart(args = []):
    arg_str = ''
    if len(args) > 0:
        arg_str = (' ' + ' '.join(args))
    return os.system(docker_compose_env(stop() + arg_str) + " && " + docker_compose_env(start() + arg_str))

def run(args = [], *, run_args = ''):
    return ("run %s --rm %s sh -c '%s'"%(run_args, SERVICE_NAME, ' '.join(args)))

def shell(args = []):
    arg_str = ' sh -c "bash || exit 0" '
    return 0 == os.system(docker_compose_env(_exec() + arg_str)) or \
            0 == os.system(docker_compose_env(run([arg_str])))

def action_run(args = []):
    return os.system(docker_compose_env(run(args)))

#--------------------------------------------------------------------------------------

exports = {
    'env:init': {'desc': 'Initial Project Env Config','action': init},
    'run': {'desc': 'Run a command with a container', 'action': action_run},
    'exec': {'desc': 'Exec a command in container', 'action': action(docker_compose_env(_exec()))},
    'shell': {'desc': 'Open a Shell into container, if container not start, use `run bash`', 'action': shell},
    'logs': {'desc': 'Show logs', 'action': action(docker_compose_env(logs()))},
    'up': {'desc': 'Create && start server', 'action': action(docker_compose_env(up()))},
    'down': {'desc': 'Stop && remove  server', 'action': action(docker_compose_env(down()))},
    'start': {'desc': 'Start server', 'action': action(docker_compose_env(start()))},
    'stop': {'desc': 'Stop server', 'action': action(docker_compose_env(stop()))},
    'restart': {'desc': 'Restart specify server, if not, restart all', 'action': restart},
    'ps': {'desc': 'Show containers', 'action': action(docker_compose_env('ps'))},
    'compose': {'desc': 'Use as docker-compose\n' + line_seperator(' -', 100), 'action': action(docker_compose_env(''))},
}
