""" myArgs - parse arguments for CLI

import myArgs
args = myArgs.Parse(
    verbose=False,                     # optional boolean, verbose alone will set it
    due='',                            # optional string
    timeout=30,                        # optional int
    limit=int,                         # required int
    assignment=str,                    # required string
    _config="{assignment}/config.json" # read values from a config file too.
)

_config allows me to specify the path to a json configuration file to pick up values
that may be overridden. The path is interpolated with all the args using the
string `format` method.

The returned value is a named tuple with attributes given by the key word arguments
and an attribute `extra_` that gathers other arguments.

In the shell I can run a Python script the normal with args like this:

python3 script.py verbose limit=5 assignment=A2 rain.txt

I went for this minimalist key=value format because it is simple to implement
and meets my needs.
"""

import os.path as osp
import sys
import json
from collections import namedtuple


def Parse(**kwargs):
    """Return an object containing arguments collected from an optional
    configuration file, then the values specified here, then values from
    the sys.argv, the URL query string, or an environment variable."""

    args = {}
    types = {}
    extra = []
    required = set()
    supplied = set()

    def addValue(k, v):
        if v is None:
            if k in types and types[k] is bool:
                args[k] = True
            elif k not in types:
                extra.append(k)
            else:
                raise ValueError(
                    "{k} without value expected {t}".format(k=k, t=types[k])
                )
        elif k in types:
            if types[k] is bool:
                if isinstance(v, str):
                    args[k] = v.lower() not in ["0", "false"]
                else:
                    args[k] = bool(v)
            else:
                try:
                    args[k] = types[k](v)
                except ValueError:
                    raise ValueError(
                        "{k}={v} expected {t}".format(k=k, v=v, t=types[k])
                    )
        else:
            raise ValueError("{k}={v} unexpected argument".format(k=k, v=v))
        supplied.add(k)

    # first fill the defaults
    for k, v in kwargs.items():
        if k.startswith("_"):
            continue
        if isinstance(v, type):  # a required argument
            required.add(k)
            types[k] = v

        else:
            args[k] = v
            types[k] = type(v)

    try:
        # get values from argv
        for a in sys.argv[1:]:
            if "=" in a:
                k, v = a.split("=")
            else:
                k, v = a, None
            addValue(k, v)

        # get the values from the config file but don't overwrite supplied values
        if "_config" in kwargs:
            path = kwargs["_config"].format(**args)
            if osp.exists(path):
                with open(path, "r") as fp:
                    for k, v in json.load(fp).items():
                        if k not in supplied:
                            addValue(k, v)

        # make sure we got the required values
        omitted = required - supplied
        if omitted:
            raise ValueError(
                "missing required argument{} {}".format(
                    "s"[len(omitted) == 1:], omitted
                )
            )
    except ValueError:
        # print a usage message
        print(
            "args:", " ".join(["{}={}".format(k, t.__name__) for k, t in types.items()])
        )
        raise

    attrs = sorted(args.keys())
    attrs.append("extra_")
    args["extra_"] = extra

    return namedtuple("Args", attrs)(**args)


if __name__ == '__main__':
    args = Parse(
        verbose=False,                     # optional boolean, verbose alone will set it
        due='',                            # optional string
        timeout=30,                        # optional int
        limit=int,                         # required int
        assignment=str,                    # required string
        _config="config.json"  # read values from a config file too.
    )
    print(args)
