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

# 🧮 Risk Metrics

## Value-at-Risk (VaR)

The engine supports multiple VaR methodologies:

### Historical VaR

Uses empirical historical returns to estimate potential portfolio losses.

### Parametric VaR

Uses statistical assumptions about return distributions.

## Conditional Value-at-Risk (CVaR)
CVaR measures the expected loss beyond the VaR threshold.

Also known as Expected Shortfall

Supported methods:

- Historical CVaR
- Parametric CVaR

# 🔄 Backtesting

The engine includes historical backtesting to evaluate VaR model performance by comparing predicted losses against realized portfolio returns. The framework identifies VaR breaches and measures whether the observed violation frequency aligns with the expected confidence level.

To statistically validate VaR accuracy, the engine implements the **Kupiec Proportion of Failures (POF) test**. The test evaluates the null hypothesis that the observed breach probability matches the expected VaR failure rate, providing a statistical measure of whether a risk model is correctly calibrated.

# 📄 License

This project is licensed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the conditions of the license.

## 🙏 Acknowledgements

This project was developed alongside my ongoing studies at Eindhoven University of Technology (TU/e), combining academic learning with independent research and implementation. The project was informed in part by material from MIT OpenCourseWare, alongside my own exploration of quantitative finance, risk modelling, and portfolio analytics.

<p align="center">
  <a href="https://ocw.mit.edu/">
    <img
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbXwMQlvlr3o5wbotF_9b9uXMBJF-WIJ3sV9BNHsOaBz-ZO2A53LBdQMxP&s=10"
      alt="MIT OpenCourseWare logo"
      width="200"
    />
  </a>
  <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
  <a href="">
    <img
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0as6Zrck2G2too3qxUP5-3iTE7Mb7_CljRxOR_R8aIkMtAUozwpA0jKZ5&s=10"
      alt="TU Eindhoven logo"
      width="200"
    />
  </a>
</p>
