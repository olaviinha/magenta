# Magenta for Colab

Work in progress to update Magenta to run on current Colab (Python 3.11)

## Installation

Magenta currently supports **Python 3.11**. Install it with pip and ensure TensorFlow 2.18 is selected:

```bash
pip install magenta "tensorflow>=2.18,<2.19" "keras>=3.5,<4"
```

TensorFlow 2.19+ is not yet supported, and Python versions newer than 3.11 are incompatible. Magenta now requires **Keras 3**. If upgrading from Keras 2, see the [migration guide](https://keras.io/guides/migrating_to_keras_3/).
