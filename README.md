# Magenta YOLO for Colab

YOLO'd version of Google AI [Magenta](https://magenta.tensorflow.org/) for Colab, as [original repository](https://github.com/magenta/magenta) is no longer maintained in that regard. This is set of duct-tape workarounds that keeps the stuff I need from Magenta working in Colab (Jun 2025).

### Installation

#### Cell 1: install required packages & restart runtime
```
REQUIRED_PACKAGES = [
    'absl-py==1.2.0',
    'dm-sonnet==2.0.0',
    'scikit-image==0.19.3',
    'imageio==2.20.0',
    'librosa==0.10.0',
    'matplotlib==3.5.2',
    'mido==1.2.6',
    'mir_eval==0.7',
    'note-seq==0.0.3',
    'numba==0.58.1',
    'numpy==1.22',
    'pillow==9.2.0',
    'pretty_midi==0.2.9',
    'pygtrie==2.5.0',
    'python-rtmidi==1.5.8',
    'scipy==1.9.2',
    'six==1.16.0',
    'sk-video==1.1.10',
    'sox==1.4.1',
    'tensorflow==2.12.0',
    'tensorflow-datasets==4.6.0',
    'tensorflow-probability==0.17.0',
    'tf_slim==1.1.0',
    'wheel==0.37.1',
    'protobuf==3.20.0',
    'pychord'
]

for pkg in REQUIRED_PACKAGES:
  !pip install {pkg}

import os
os.kill(os.getpid(), 9)
```

#### Cell 2: clone the repo
Pay attention how we do NOT run Magenta's own installation, `!pip install .`, or anything like that.
```
%cd /content
!git clone https://github.com/olaviinha/magenta.git
%cd /content/magenta
```

### Usage

Run like this:
```
!python -m magenta.models.melody_rnn.melody_rnn_generate --config=attention_rnn --num_outputs=10 ...
```

**NOT** like this, as instructed in original Magenta repo:
```
!melody_rnn_generate --config=attention_rnn --num_outputs=10 ...
```
