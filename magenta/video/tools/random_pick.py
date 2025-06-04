# Copyright 2023 The Magenta Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This tools pick some frames randomly from a folder to an other.

Only useful if used with the --limit flag unless it will copy the whole folder
"""

import logging

import argparse
import glob
import ntpath
import os
import random
import shutil
import sys

logging.basicConfig(level=logging.INFO)

PARSER = argparse.ArgumentParser(description='')
PARSER.add_argument(
    '--path_in',
    dest='path_in',
    default='',
    help='folder where the pictures are',
    required=True)
PARSER.add_argument(
    '--path_out', dest='path_out', default='./', help='Destination folder')
PARSER.add_argument(
    '--delete',
    dest='delete',
    action='store_true',
    help='use this flag to delete the original file after conversion')
PARSER.set_defaults(delete=False)
PARSER.add_argument(
    '--limit',
    dest='limit',
    type=int,
    default=-1,
    help='cap the number of generated pairs')
ARGS = PARSER.parse_args()


def random_pick(path_in, path_out, limit, delete):
  """Pick a random set of jpg files and copy them to an other folder.

  Args:
    path_in: the folder that contains the files
    path_out: the folder to export the picked files
    limit: number of file to pick
    delete: if true, will delete the original files

  Returns:
    nothing

  Raises:
    nothing
  """
  if path_in == path_out:
    logging.warning('path in == path out, that is not allowed, quiting')
    sys.exit()

  path = '{}/*'.format(path_in)
  logging.info('looking for all files in %s', path)
  files = glob.glob(path)
  file_count = len(files)
  logging.info('found %d files', file_count)
  if limit > 0:
    logging.info('will use limit of %d files', limit)
    random.shuffle(files)
    files = files[:limit]

  i = 0
  for image_file in files:
    i += 1
    basename = ntpath.basename(image_file)
    file_out = os.path.join(path_out, basename)

    try:
      if delete:
        logging.info('%d / %d  moving %s to %s', i, limit, image_file, file_out)
        shutil.move(image_file, file_out)
      else:
        logging.info('%d / %d  copying %s to %s', i, limit, image_file, file_out)
        shutil.copyfile(image_file, file_out)
    except:  # pylint: disable=bare-except
      logging.warning("can't pick file %s to %s", image_file, file_out)


if __name__ == '__main__':
  random_pick(ARGS.path_in, ARGS.path_out, ARGS.limit, ARGS.delete)
