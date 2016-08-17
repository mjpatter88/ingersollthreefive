from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://github.com/mjpatter88/ingersollthreefive.git'
SITE_NAME = "ingersollthreefive"


# Assuming you have a username with root privileges
# Usage 'fab provision --host=username@hostname --password=<PASSWORD>
def provision():
    _install_deps()
    _provision_pyenv()
    _install_nginx()

def _install_deps():
    dep_command = 'apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils'
    sudo(dep_command)

def _provision_pyenv():
    pyenv_dir = '/home/{}/.pyenv/'.format(env.user)
    pyenv_command = 'curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash'
    if not exists(pyenv_dir):
        run(pyenv_command)
    _append_pyenv_bashrc()

    pyenv_exe = '{}/bin/pyenv'.format(pyenv_dir)
    if not exists('{}/versions/3.5.2'.format(pyenv_dir)):
        run('{} install 3.5.2'.format(pyenv_exe))

    if not exists('{}/versions/{}'.format(pyenv_dir, SITE_NAME)):
        run('{} virtualenv 3.5.2 {}'.format(pyenv_exe, SITE_NAME))

    run('{}/versions/{}/bin/pip install --upgrade pip'.format(pyenv_dir, SITE_NAME))

def _append_pyenv_bashrc():
    bashrc_file = '/home/{}/.bashrc'.format(env.user)
    append(bashrc_file, 'export PATH="/home/{}/.pyenv/bin:$PATH"'.format(env.user))
    append(bashrc_file, 'eval "$(pyenv init -)"')
    append(bashrc_file, 'eval "$(pyenv virtualenv-init -)"')
    run('source {}'.format(bashrc_file))

def _install_nginx():
    command = 'sudo apt-get install -y nginx'
    sudo(command)


def deploy():
    site_name = SITE_NAME
    site_folder = '/home/{}/sites/{}'.format(env.user, site_name)
    source_folder = site_folder + '/source'
    virtual_env_folder = '/home/{}/.pyenv/versions/{}'.format(env.user, site_name)

    _create_directory_structure_if_neccessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder, env.user, virtual_env_folder, site_name)
    #_update_static_files(source_folder, virtual_env_folder)
    #_update_database(source_folder, virtual_env_folder)

    _deploy_nginx_if_neccessary(source_folder, site_name, env.host)
    _deploy_gunicorn_if_neccessary(source_folder, site_name)
    _restart_nginx()

def _create_directory_structure_if_neccessary(site_folder):
    for subfolder in ('database', 'static', 'source'):
        run('mkdir -p {}/{}'.format(site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {} && git pull'.format(source_folder))
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))

def _update_settings(source_folder, host_name):
    settings_path = source_folder + '/{}/settings.py'.format(SITE_NAME)
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'ALLOWED_HOSTS = .+$', 'ALLOWED_HOSTS = ["{}"]'.format(host_name))

    secret_key_file = source_folder + '/{}/secret_key.py'.format(SITE_NAME)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder, user_name, virtual_env_folder, site_name):
    pyenv_bin = '/home/{}/.pyenv/bin'.format(user_name)
    if not exists(virtual_env_folder):
        run('{}/pyenv virtualenv 3.5.2 {}'.format(pyenv_bin, site_name))
    run('{}/bin/pip install -r {}/requirements.txt'.format(virtual_env_folder, source_folder))

def _update_static_files(source_folder, virtual_env_folder):
    run('cd {} && {}/bin/python manage.py collectstatic --noinput'.format(source_folder, virtual_env_folder))

def _update_database(source_folder, virtual_env_folder):
    run('cd {} && {}/bin/python manage.py migrate --noinput'.format(source_folder, virtual_env_folder))

def _deploy_nginx_if_neccessary(source_folder, site_name, host_name):
    # write config file to sites-available
    nginx_dir = '/etc/nginx/sites-available/'
    nginx_file_name = site_name

    if not exists(nginx_dir + nginx_file_name):
        new_config_file = '{}/deploy_tools/{}'.format(source_folder, site_name)
        run('cp {}/deploy_tools/nginx-template.conf {}'.format(source_folder, new_config_file))
        sed(new_config_file, 'HOSTNAME', host_name)
        sed(new_config_file, 'SITENAME', site_name)
        sudo('mv {} /etc/nginx/sites-available/'.format(new_config_file))
        sudo('ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/{}'.format(site_name, site_name))

def _deploy_gunicorn_if_neccessary(source_folder, site_name):
    gunicorn_dir = '/etc/systemd/system/'
    gunicorn_file_name = 'gunicorn-{}.service'.format(site_name)

    if not exists(gunicorn_dir + gunicorn_file_name):
        new_config_file = '{}/deploy_tools/{}'.format(source_folder, gunicorn_file_name)
        run('cp {}/deploy_tools/gunicorn-template.service {}'.format(source_folder, new_config_file))
        sed(new_config_file, 'SITENAME', site_name)
        sudo('mv {} {}'.format(new_config_file, gunicorn_dir))

        # start the servie and enable it
        sudo('systemctl start {}'.format(gunicorn_file_name))
        sudo('systemctl enable {}'.format(gunicorn_file_name))

def _restart_nginx():
    sudo('service nginx reload')

