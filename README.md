# Magenta YOLO for Colab

YOLO'd version of Google AI [Magenta](https://magenta.tensorflow.org/) for Colab, as [original repository](https://github.com/magenta/magenta) is no longer maintained in that regard. This is a set of questionable duct-tape workarounds that keeps the stuff I need from Magenta working in Colab (Jun 2025).

### Installation

#### Cell 1: install required packages & restart runtime
```
REQUIRED_PACKAGES = [
    'absl-py>=1.4',
    'dm-sonnet>=2.0.0',
    'scikit-image>=0.22',
    'imageio>=2.31',
    'librosa>=0.10.1',
    'matplotlib>=3.8',
    'mido>=1.3',
    'mir_eval>=0.7',
    'note-seq>=0.0.5',
    'numba>=0.58',
    'numpy>=1.25',
    'pillow>=10',
    'pretty_midi>=0.2.10',
    'pygtrie>=2.5',
    'python-rtmidi>=1.5.8',
    'scipy>=1.11',
    'six>=1.16',
    'sk-video>=1.1.10',
    'soundfile==0.12.1',
    'sox>=1.4.1',
    'tensorflow>=2.15',
    'tensorflow-datasets>=4.9',
    'tensorflow-probability>=0.23',
    'tf_slim>=1.1',
    'wheel>=0.41',
    'protobuf>=3.20',
    'pychord' # I don't think Magenta itself actually needs this but uhh I do...
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
