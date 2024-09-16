Here's a README file for your project:

---

# Climate Model Interactive Tool

## Overview

This is an interactive web-based application that helps users simulate climate interventions using Streamlit. The tool allows users to select various parameters, such as the number of actors, regions to protect, emission points, and setpoints for controlling global or regional temperatures and monsoon changes. The model incorporates feedback mechanisms using PID (Proportional-Integral-Derivative) controllers to simulate different intervention scenarios and their impacts on the climate.

The project also includes a climate model that is powered by noise simulations and uses aerosol responses to simulate Solar Radiation Management (SRM) interventions and climate control scenarios.

---

## Features

- **Interactive Pages:** Users can navigate through different pages to set up climate intervention scenarios by selecting actors, regions, emission points, and setpoints.
- **PID Controllers:** Simulate the climate response using PID controllers for each actor.
- **Dynamic Visualization:** The results of the interventions are visualized using dynamic plots generated in real-time.
- **Simulated Noise:** Climate models include noise simulations (white, red, and mixed) for temperature and monsoon changes.
- **Multiple Regions & Emission Points:** Supports different regions (e.g., NHST, SHST, GMST, Monsoon) and emission points (e.g., 60N, 30N, Eq, etc.).
- **Custom Setpoints:** Users can input target setpoints to simulate the desired climate outcomes.

---

## Installation

### Prerequisites

Make sure you have Python 3.8+ installed. You will also need the following packages:

- `streamlit`
- `simple_pid`
- `matplotlib`
- `colorednoise`
- `numpy`
- `argparse`
- `sys`
- `os`
- `myclim`

To install the required packages, you can use:

```bash
pip install streamlit simple_pid matplotlib colorednoise numpy argparse
```

### Running the Application

1. Clone the repository to your local machine.
2. To run the Streamlit app, navigate to the project directory and execute the following command in the terminal:

```bash
streamlit run app.py
```

This will launch the web application in your default browser.

---

## Usage

Once the application is running:

1. **Welcome Page:** You will be greeted with a welcome message. Click "Get Started" to begin the simulation process.
2. **Selection Task #1:** Choose the number of actors involved in the simulation.
3. **Selection Task #2:** For each actor, select a region to protect.
4. **Selection Task #3:** Choose emission points for each actor.
5. **Selection Task #4:** Input a setpoint (e.g., temperature change or monsoon percentage change) for each actor.
6. **Results Page:** Once all parameters are set, the application will generate and display the results of the climate intervention through various plots.

### Model Description

- The **PID Controllers** control the SRM intervention using proportional (`Kp`), integral (`Ki`), and derivative (`Kd`) gains.
- **Regions:** Users can select from regions such as NHST, SHST, GMST, or Monsoon.
- **Emission Points:** Choose from several emission points, like 60N, 30N, Eq, 15S, etc.
- **Noise Models:** The tool supports white noise, red noise, and mixed noise simulations to model uncertainties in temperature and monsoon changes.
- **Plots:** Six plots visualize the impact of SRM intervention on global and regional temperatures, as well as monsoon patterns.

---

## File Structure

- **app.py:** The main Streamlit app that drives the interactive front end.
- **climate_model.py:** Contains the backend logic for running the climate simulation using PID controllers and other tools.
- **test2.py:** Auxiliary functions and models that handle emissions and other computations.
- **assets/**: Directory containing background images or additional media used in the application.
- **plots/**: Directory where the generated plots are saved.

---

## Customization

### Adding a Background Image

You can add a custom background image by replacing the file path in the `add_bg_from_local()` function:

```python
add_bg_from_local('/path/to/your/background.jpg')
```

### Modifying Parameters

- To modify the PID parameters or noise settings, you can edit the `generate_P()` and `run_model()` functions in the Python files.

---

## Contribution

Feel free to fork the project and submit pull requests for new features or bug fixes. Contributions are welcome!

---

## Acknowledgments

Special thanks to the creators of the `myclim` library and to the open-source community for tools like Streamlit and matplotlib.

--- 

### Contact

For any questions or issues, feel free to reach out at [krish.git07@gmail.com].
