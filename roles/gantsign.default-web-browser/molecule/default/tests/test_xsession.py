import pytest
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_xsession_file_permissions(File):
    config = File('/etc/X11/Xsession.d/80-ansible-default-web-browser')

    assert config.exists
    assert config.is_file
    assert config.user == 'root'
    assert config.group == 'root'
    assert oct(config.mode) == '0644'


@pytest.mark.parametrize('expected', [
    'XDG_CONFIG_DIRS=/etc/xdg/ansible-default-web-browser:"$XDG_CONFIG_DIRS"',
    'XDG_DATA_DIRS=/etc/xdg/ansible-default-web-browser:"$XDG_DATA_DIRS"'
])
def test_xsession_file(File, expected):
    config = File('/etc/X11/Xsession.d/80-ansible-default-web-browser')

    assert config.exists
    assert config.is_file
    assert config.contains(expected)
