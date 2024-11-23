import numpy as np
import matplotlib.pyplot as plt

display_labels = ['PV Adoption Rate',  r'$\mathregular{LCOE^{-1}}$', 'Battery Adoption Rate','Retailer Profit'] 
labels = ['PV Adoption Rate', 'LCOEs', 'Battery Adoption Rate', 'Retailer Profit %']
BM_1 = [0.388,  1/0.2488, 0, 14.54]
#BM_2_Netmetering = [0.744, 1/0.2314, -7.50]
#BM_2_Variable = [0.744, 1/0.2374, -5.44]
BM_2_Fixed = [0.544, 1/0.2410, 0, 7.68]
BM_3 = [0.356, 1/0.2434, 0, 11.79]
#BM_4_Arbitrage = [0, 1/0.2176, 9.62]
BM_4_Peakshaving = [0, 1/0.2046, 0.9, 6.84]

models = [BM_1, BM_2_Fixed, BM_3, BM_4_Peakshaving]
model_names = [
    '1: Business as Usual',
    '2: Asymmetric Fixed',
    '3: Energy Subscription',
    '4: Peak Shaving'
]

scales = {
    'PV Adoption Rate': (0, 0.78),
    'Battery Adoption Rate': (0, 1),
    'LCOEs': (4, 5),       
    'Retailer Profit %': (5, 16) 
}

normalized_models = []
for model in models:
    normalized_model = []
    for value, label in zip(model, labels):
        min_val, max_val = scales[label]
        norm_value = (value - min_val) / (max_val - min_val)
        normalized_model.append(norm_value)
    normalized_models.append(normalized_model)

num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 18

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

markers = ['o-', 's-', '*-', 'd-']

colors = ['blue', 'red', 'black', 'green']
for model, name, color, marker in zip(normalized_models, model_names, colors, markers):
    data = np.concatenate((model, [model[0]])) 
    ax.plot(angles, data, marker, linewidth=1, label=name, color=color, zorder=100)
    ax.fill(angles, data, alpha=0.25, color=color, zorder=100)

for r in range(1, 6):
    ax.plot(angles, [r * 1 / 5] * (num_vars + 1), '-', color='gray', alpha=0.5, linewidth=0.5,zorder=0)

for i in range(num_vars):
    angle_rad = angles[i]
    next_angle_rad = angles[(i + 1) % num_vars]  # Get the next angle, wrapping around if necessary
    x1 = 1 * np.cos(angle_rad)
    y1 = 1 * np.sin(angle_rad)
    x2 = 1 * np.cos(next_angle_rad)
    y2 = 1 * np.sin(next_angle_rad)
    ax.plot([angle_rad, next_angle_rad], [1, 1], '-', color='gray', linewidth=1)


# Labels
ax.set_thetagrids(np.degrees(angles[:-1]), display_labels)  # We only want the labels for the original 5 points
for label, angle in zip(ax.get_xticklabels(), angles):
    label.set_rotation(angle * 180 / np.pi - 90)
    # x, y = label.get_position() 
    # adjustment = adjustments[display_labels.get_text()] 
    # label.set_position((x, y + adjustment)) 

label_objects = ax.get_xticklabels()  
label_objects[1].set_position((0, -0.1))  
label_objects[3].set_position((-0.1, -0.2)) 

# Remove Radial Ticks and Circular Gridlines
ax.set_rticks([])
ax.grid(False)
ax.spines['polar'].set_visible(False)

plt.legend(loc='upper left',bbox_to_anchor=(-0.3, 1.1), labelspacing=0.3, fontsize=16, frameon=False)


plt.tight_layout()
plt.savefig("radar.png", dpi=1200, bbox_inches='tight')

plt.show()
