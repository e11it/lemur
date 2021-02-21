from io import open
import subprocess

from flask import current_app

from cryptography.hazmat.primitives import serialization
from lemur.plugins.bases import ExportPlugin
from lemur.plugins import lemur_pkcs8 as pkcs8
from lemur.common.utils import parse_private_key


def run_process(command):
    """
    Runs a given command with pOpen and wraps some
    error handling around it.
    :param command:
    :return:
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    current_app.logger.debug(command)
    stdout, stderr = p.communicate()

    if p.returncode != 0:
        current_app.logger.debug(" ".join(command))
        current_app.logger.error(stderr)
        raise Exception(stderr)


def create_pkcs8(key):
    key_bytes = parse_private_key(key).private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )

    return key_bytes


class PKCS8ExportPlugin(ExportPlugin):
    title = "PKCS8"
    slug = "openssl-pkcs8"
    description = "Exports a PKCS8"
    version = pkcs8.VERSION

    def export(self, body, chain, key, options, **kwargs):
        """
        Creates CSR from certificate

        :param key:
        :param chain:
        :param body:
        :param options:
        :param kwargs:
        """

        raw = create_pkcs8(key)
        extension = "p8"

        # passphrase is None
        return extension, None, raw
