from subprocess import call
from configparser import ConfigParser
from pathlib import Path


class Namespace:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, Namespace(**v) if isinstance(v, dict) else v)

    def __repr__(self):
        return "Namespace(%s)" % ", ".join(
            "=".join([k, repr(v)]) for k, v in self.__dict__.items()
        )


def load(file: Path):
    config = ConfigParser()

    config.read(file)

    return Namespace(
        **{
            section: Namespace(
                **{
                    header: toInt(config.get(section, header).strip('"'))
                    for header in config[section]
                }
            )
            for section in config.sections()
        }
    )


def toInt(num: str) -> int:
    try:
        return int(num)
    except ValueError:
        return num


if __name__ == "__main__":
    config = load("res/config/config.ini")
    version = config.Meta.version

    call(f"./scripts/buildscript.sh {version}".split())
