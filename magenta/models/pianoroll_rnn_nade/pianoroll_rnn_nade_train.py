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

"""Train and evaluate a RNN-NADE model."""

import os

import magenta
from magenta.models.pianoroll_rnn_nade import pianoroll_rnn_nade_graph
from magenta.models.pianoroll_rnn_nade import pianoroll_rnn_nade_model
from magenta.models.shared import events_rnn_train
import tensorflow as tf
from absl import app, flags, logging

FLAGS = flags.FLAGS
flags.DEFINE_string('run_dir', '/tmp/rnn_nade/logdir/run1',
                           'Path to the directory where checkpoints and '
                           'summary events will be saved during training and '
                           'evaluation. Separate subdirectories for training '
                           'events and eval events will be created within '
                           '`run_dir`. Multiple runs can be stored within the '
                           'parent directory of `run_dir`. Point TensorBoard '
                           'to the parent directory of `run_dir` to see all '
                           'your runs.')
flags.DEFINE_string('config', 'rnn-nade', 'The config to use')
flags.DEFINE_string('sequence_example_file', '',
                           'Path to TFRecord file containing '
                           'tf.SequenceExample records for training or '
                           'evaluation.')
flags.DEFINE_integer('num_training_steps', 0,
                            'The the number of global training steps your '
                            'model should take before exiting training. '
                            'Leave as 0 to run until terminated manually.')
flags.DEFINE_integer('num_eval_examples', 0,
                            'The number of evaluation examples your model '
                            'should process for each evaluation step.'
                            'Leave as 0 to use the entire evaluation set.')
flags.DEFINE_integer('summary_frequency', 10,
                            'A summary statement will be logged every '
                            '`summary_frequency` steps during training or '
                            'every `summary_frequency` seconds during '
                            'evaluation.')
flags.DEFINE_integer('num_checkpoints', 10,
                            'The number of most recent checkpoints to keep in '
                            'the training directory. Keeps all if 0.')
flags.DEFINE_boolean('eval', False,
                            'If True, this process only evaluates the model '
                            'and does not update weights.')
flags.DEFINE_string('log', 'INFO',
                           'The threshold for what messages will be logged '
                           'DEBUG, INFO, WARN, ERROR, or FATAL.')
flags.DEFINE_string(
    'hparams', '',
    'Comma-separated list of `name=value` pairs. For each pair, the value of '
    'the hyperparameter named `name` is set to `value`. This mapping is merged '
    'with the default hyperparameters.')


def main(unused_argv):
  logging.set_verbosity(FLAGS.log)

  if not FLAGS.run_dir:
    logging.fatal('--run_dir required')
    return
  if not FLAGS.sequence_example_file:
    logging.fatal('--sequence_example_file required')
    return

  sequence_example_file_paths = tf.io.gfile.glob(
      os.path.expanduser(FLAGS.sequence_example_file))
  run_dir = os.path.expanduser(FLAGS.run_dir)

  config = pianoroll_rnn_nade_model.default_configs[FLAGS.config]
  config.hparams.parse(FLAGS.hparams)

  mode = 'eval' if FLAGS.eval else 'train'
  build_graph_fn = pianoroll_rnn_nade_graph.get_build_graph_fn(
      mode, config, sequence_example_file_paths)

  train_dir = os.path.join(run_dir, 'train')
  tf.io.gfile.makedirs(train_dir)
  logging.info('Train dir: %s', train_dir)

  if FLAGS.eval:
    eval_dir = os.path.join(run_dir, 'eval')
    tf.io.gfile.makedirs(eval_dir)
    logging.info('Eval dir: %s', eval_dir)
    num_batches = (
        (FLAGS.num_eval_examples or
         magenta.common.count_records(sequence_example_file_paths)) //
        config.hparams.batch_size)
    events_rnn_train.run_eval(build_graph_fn, train_dir, eval_dir, num_batches)

  else:
    events_rnn_train.run_training(build_graph_fn, train_dir,
                                  FLAGS.num_training_steps,
                                  FLAGS.summary_frequency,
                                  checkpoints_to_keep=FLAGS.num_checkpoints)


def console_entry_point():
  app.run(main)


if __name__ == '__main__':
  console_entry_point()
