# 📊 Portfolio Risk Engine
**A Python-based tool for measuring and analyzing financial portfolio risk.**

The project provides tools for loading market data, representing investment portfolios, calculating risk metrics, and evaluating risk models using historical observations.

---

## 🔎 Overview

Portfolio risk management focuses on estimating how much a portfolio could lose under normal or stressed market conditions.

This project provides a foundation for exploring common quantitative risk-management techniques, including:

- **Value at Risk (VaR)**
- **Condition Value at Risk (CVaR)**
- **Historical portfolio analysis**
- **Parametric risk estimation**
- **Portfolio profit-and-loss calculation**
- **Risk-model backtesting**
- **VaR exception analysis**

## ⚙️ Installation

### Clone the repository
```bash
git clone https://github.com/quintoorschot/portfolio-risk-engine.git
cd portfolio-risk-engine
```

### Create a virtual environment
#### Linux/MacOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Verify installation (optional)
Run the test suite to confirm that the installation was successful:
```bash
pytest
```
If all tests pass, the environment is ready for use.

## ⚠️ Disclaimer

This project is intended for educational, research, and experimental purposes.

It does not provide financial, investment, trading, or professional risk-management advice. Model outputs should be independently validated before being used for real financial decisions.

## 🙏 Acknowledgements

This project was informed in part by material from MIT OpenCourseWare, alongside independent study and implementation.

<p align="center">
  <a href="https://ocw.mit.edu/">
    <img
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbXwMQlvlr3o5wbotF_9b9uXMBJF-WIJ3sV9BNHsOaBz-ZO2A53LBdQMxP&s=10"
      alt="MIT OpenCourseWare logo"
      width="200"
    />
  </a>
</p>
