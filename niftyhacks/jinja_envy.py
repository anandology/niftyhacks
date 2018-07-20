"""
Tool to render a Jinja template using values in the environment.
"""
from __future__ import print_function
import argparse
import jinja2
import os

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("template", help="template to render")
    return p.parse_args()

def main():
    args = parse_args()
    t = jinja2.Template(open(args.template).read(), undefined=jinja2.StrictUndefined)
    print(t.render(**os.environ))

if __name__ == '__main__':
    main()
