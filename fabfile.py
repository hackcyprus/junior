from fabric.api import run, env, cd

env.hosts = ['ubuntu@ec2-54-216-5-240.eu-west-1.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = 'keys/junior-hackathon.pem'

APP_DIR = '/opt/junior/'
ENV_DIR = '/opt/env/junior/'

def update_code():
    run("git pull origin master && {}bin/pip install -r requirements.pip".format(ENV_DIR))

def collectstatic():
    run("{}bin/python manage.py collectstatic --noinput".format(ENV_DIR))

def migrate():
    run("{}bin/python manage.py migrate".format(ENV_DIR))

def restart():
    run('sudo supervisorctl restart all')

def deploy():
    with cd(APP_DIR):
        update_code()
        collectstatic()
        migrate()
        restart()