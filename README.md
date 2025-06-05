# Magenta for Colab

Work in progress to update Magenta to run on current Colab (Python 3.11)

## Installation

Magenta currently supports **Python 3.11**. Install it with pip and ensure TensorFlow 2.18 is selected:

```bash
pip install magenta "tensorflow>=2.18,<2.19" "keras<3"
```

TensorFlow 2.19+ is not yet supported, and Python versions newer than 3.11 are incompatible.
