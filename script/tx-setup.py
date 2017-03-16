#!/usr/bin/env python
import argparse
import os
import sys
import subprocess


SOURCE_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DOCS_DIR = 'docs'
FILE_EXTENSION = ".md"
TRANSLATION_DOCS_DIR = 'docs-locale'
DOCS_ROOT = os.path.join(SOURCE_ROOT, DOCS_DIR)
TX_PROJEC_SLUG = 'electron'
TX_RESOURCE_TYPE = 'GITHUBMARKDOWN'
TX_SET_CMD = ("tx set --auto-local --resource {project}.{resource} "
              "--source-lang en --type {type} --source-file {source_file} "
              "{expr} --execute")


def tx_exists():
    return subprocess.call("type tx", shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def slugfy(file_path):
    return file_path[:-len(FILE_EXTENSION)].replace('/', '_')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Setup transifex-client config file (.tx/config) to have '
                    'a configuration entry for each `{}` file under the `{}` '
                    'directory.'.format(FILE_EXTENSION, DOCS_DIR))
    parser.add_argument(
        '--execute', default=False, action='store_true',
        help='Call `tx` command to actually write the configuration file')

    return parser.parse_args()


def main():
    args = parse_args()
    call_cmd = args.execute

    os.chdir(SOURCE_ROOT)
    for root, dirs, files in os.walk(DOCS_ROOT):
        for file_name in files:
            if file_name.endswith(FILE_EXTENSION):

                file_relpath_full = os.path.join(
                    root, file_name).split(SOURCE_ROOT)[1][1:]

                resource = slugfy(file_relpath_full)

                file_relpath = file_relpath_full.split(DOCS_DIR)[1][1:]

                source_file = os.path.join(DOCS_DIR, file_relpath)
                expr = os.path.join(TRANSLATION_DOCS_DIR, '<lang>',
                                    file_relpath)

                cmd = TX_SET_CMD.format(
                    project=TX_PROJEC_SLUG,
                    resource=resource,
                    type=TX_RESOURCE_TYPE,
                    source_file=source_file,
                    expr=expr
                )
                if call_cmd:
                    if tx_exists:
                        subprocess.call(cmd.split())
                    else:
                        error = ('Transifex-client not installed. Please run '
                                 '`pip install transifex-client` first\n')
                        sys.stderr.write(error)
                        sys.stderr.flush()
                        return 1
                else:
                    print cmd


if __name__ == '__main__':
    sys.exit(main())
