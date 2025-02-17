# [WHODUNIT: Evaluation Benchmark for Culprit Detection in Mystery Stories]((https://arxiv.org/pdf/2502.07747))

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) [![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/kjgpta/whodunit/actions)

**[WHODUNIT](https://arxiv.org/pdf/2502.07747)** is a rigorously curated benchmark designed to evaluate the deductive reasoning capabilities of large language models (LLMs) within narrative contexts. This dataset comprises full texts and excerpts from public domain mystery novels and short stories and includes systematic augmentations to assess model robustness under varied entity naming conventions.

---

## Table of Contents

- [Overview](#overview)
- [Research Publication](#research-publication)
- [Dataset Overview](#dataset-overview)
- [Installation & Setup](#installation--setup)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)
- [Contact](#contact)

---

## Overview

In recent years, large language models have excelled in tasks ranging from text generation to complex reasoning. However, their ability to perform nuanced deductive reasoning—especially in extended narrative contexts—remains an open challenge. **[WHODUNIT](https://arxiv.org/pdf/2502.07747)** addresses this gap by offering:

- **Comprehensive Data Sources:** Curated public domain texts enriched with metadata (including title, author, page length, and culprit identifiers).
- **Robust Augmentation Techniques:** Multiple entity replacement strategies (e.g., swapping names with those from popular franchises or celebrities) to examine model dependence on memorized associations versus contextual reasoning.
- **Industry-Relevant Evaluations:** A benchmark setup that supports structured comparisons across diverse prompting techniques and model architectures.

This resource is intended to serve researchers and practitioners seeking to enhance narrative comprehension and deductive reasoning in LLMs.

---

## Research Publication

The methodology and evaluation protocols are detailed in the accompanying research paper:

**WHODUNIT: Evaluation Benchmark for Culprit Detection in Mystery Stories**  
*Kshitij Gupta, BITS Pilani*  
[Download PDF](https://arxiv.org/pdf/2502.07747) | [View Abstract & Citation](https://arxiv.org/abs/2502.07747)

---

## Dataset Overview

The dataset is available via Hugging Face and comprises both original and augmented text corpora.

- **Hugging Face Dataset:** [WhoDunIt on Hugging Face](https://huggingface.co/datasets/kjgpta/WhoDunIt)
- **Data Structure:**
  - **Original Dataset:**
    - `text` (string): Full text or excerpt from the literary work.
    - `title` (string): Title of the work.
    - `author` (string): Name of the author.
    - `length` (integer): Number of pages.
    - `culprit_ids` (list of strings): Identified culprit(s).
  - **Augmented Dataset:**
    - Inherits all original fields.
    - Additional `metadata` (dict): Information on entity replacement strategies (e.g., style of replacement, mapping details).

The dataset is derived from classic literary works (e.g., those from Project Gutenberg) and processed to ensure diversity in narrative style and reasoning complexity.

---

## Installation & Setup

To integrate the benchmark into your workflow, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/kjgpta/whodunit.git
   cd whodunit
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Examples

Below is an example demonstrating how to load and interact with the dataset using the Hugging Face Datasets library:

```python
from datasets import load_dataset

# Load the WhoDunIt dataset
dataset = load_dataset("kjgpta/WhoDunIt")

# Access the training split
train_data = dataset["train"]

# Display the first sample
print(train_data[0])
```

For detailed examples, refer to [HuggingFace](https://huggingface.co/datasets/kjgpta/WhoDunIt) .

---

## Contributing

Contributions are welcome and encouraged. To propose changes or improvements:

1. **Fork the Repository.**
2. **Create a Feature Branch:** Develop your feature or bug fix in a separate branch.
3. **Submit a Pull Request:** Provide clear documentation and tests for your changes.
4. **Discussion:** For major modifications, please open an issue to discuss your approach.

---

## License

This project is distributed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for further details.

---

## Citation

If you use the WHODUNIT benchmark in your research, please cite our work:

```bibtex
@misc{gupta2025whodunitevaluationbenchmarkculprit,
      title={WHODUNIT: Evaluation benchmark for culprit detection in mystery stories}, 
      author={Kshitij Gupta},
      year={2025},
      eprint={2502.07747},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.07747}, 
}
```

---

## Contact

For further inquiries or feedback, please contact at [mailguptakshitij@gmail.com](mailto:mailguptakshitij@gmail.com)
