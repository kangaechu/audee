from Audee import Audee
import yaml

if __name__ == '__main__':
    conf_file = "conf/conf.yaml"
    with open(conf_file) as f:
        conf = yaml.load(f, Loader=yaml.CLoader)

    for program in conf["Programs"]:
        Audee(url=program['Url'], album=program['Name'], prog_dir=conf['ProgDir']).download()
