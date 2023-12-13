import numpy as np
import matplotlib.pyplot as plt

# To label the max value on a plot
def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= r"$d={:.1f}$m, $T={:.1f}$N$\cdot$m".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(.96,0.8), **kw)

N = 1000        # Number of data points

h_crater = 200  # The crater depth
w_crater = 2000 # The crater diameter

# Radius of the crater arc assuming it is spherical
R_crater = (h_crater/2) + ((w_crater**2)/(8*h_crater))
g = 1.62        # Acceleration due to gravity on the moon

M_rover = np.array([100, 200, 400]) # Various rover masses
MD_cable = .692 # Mass density of the cable
R_a = 0.4       # Outer radius of the winch spool
R_b = 0.05      # Inner radius of the winch spool

# The initial steepness angle of the crater wall
theta_0 = np.arctan((w_crater/2) / (R_crater - h_crater))
theta = np.linspace(theta_0, 0, N)  # Steepness along the crater

l_cable = theta_0 * R_crater        # Length of the cable
L = np.linspace(0, l_cable, N)      # Data points along the cable

# Area of the spool decreases linearly as the cable is pulled out
# This can then be converted into a change in radius for finding torque
A_0 = np.pi * (R_a**2 - R_b**2)
A = (1 - L/l_cable) * A_0 + np.pi * R_b**2
R = np.sqrt(A / np.pi)

# Force from the cable weight and rover weight
# Assumes the entire cable is not on the ground
F = g * (L * MD_cable + np.outer(M_rover, np.sin(theta)))
T = F * R       # The motor torque required


# Plot formatting
ax = plt.subplot(111)
ax.plot(L, T[0,:], label=r'$M_{rover} = 100$kg')
ax.plot(L, T[1,:], '-.', label=r'$M_{rover} = 200$kg')
ax.plot(L, T[2,:], '--', label=r'$M_{rover} = 400$kg')
annot_max(L, T[2,:], ax)
ax.set_ylim(0, 300)
ax.set_xlim(0, 1200)

ax.spines[['right', 'top']].set_visible(False)
ax.spines[['left', 'bottom']].set_linewidth(2)
ax.tick_params(direction='in', width=2)

ax.set_ylabel(r"Torque (N$\cdot$m)")
ax.set_xlabel("Distance Traveled (m)")
ax.legend()

ax.axhline(600, ls='--', color='black', lw="0.5", alpha=0.5)
ax.axvline(l_cable, ls='--', color='black', lw="0.5", alpha=0.5)

plt.show()