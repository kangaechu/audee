import os

from Audee import Audee
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

if __name__ == '__main__':
    conf_file = os.path.join(os.path.dirname(__file__), "conf/conf.yaml")

    with open(conf_file) as f:
        conf = yaml.load(f, Loader=Loader)

    prog_dir = os.path.join(os.path.dirname(__file__), conf['ProgDir'])

    for program in conf["Programs"]:
        Audee(url=program['Url'], album=program['Name'], prog_dir=prog_dir).download()
