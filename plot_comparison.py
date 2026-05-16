import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('img', exist_ok=True)

# Cargar f0 de vuestro estimador
f0_ours = np.loadtxt('prueba.f0')

# Cargar f0 de wavesurfer
data_ws = np.loadtxt('prueba_wavesurfer.f0')
f0_wavesurfer = data_ws[:, 0] if data_ws.ndim > 1 else data_ws

# Alinear longitudes
n = min(len(f0_ours), len(f0_wavesurfer))
f0_ours       = f0_ours[:n]
f0_wavesurfer = f0_wavesurfer[:n]

frame_shift = 0.015  # 15 ms
t = np.arange(n) * frame_shift

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
fig.suptitle('Comparación estimador propio vs Wavesurfer — prueba.wav',
             fontsize=13, fontweight='bold')

# Panel 1: nuestro estimador
ax1.plot(t, f0_ours, color='steelblue', linewidth=1)
ax1.set_ylabel('f0 (Hz)')
ax1.set_title('Estimador propio')
ax1.set_ylim([-10, 550])
ax1.grid(True, alpha=0.3)

# Panel 2: wavesurfer
ax2.plot(t, f0_wavesurfer, color='darkorange', linewidth=1)
ax2.set_ylabel('f0 (Hz)')
ax2.set_title('Estimador Wavesurfer')
ax2.set_ylim([-10, 550])
ax2.grid(True, alpha=0.3)

# Panel 3: comparación superpuesta
ax3.plot(t, f0_ours, color='steelblue', linewidth=1, label='Estimador propio')
ax3.plot(t, f0_wavesurfer, color='darkorange', linewidth=1,
         alpha=0.7, label='Wavesurfer')
ax3.set_ylabel('f0 (Hz)')
ax3.set_xlabel('Tiempo (s)')
ax3.set_title('Comparación superpuesta')
ax3.set_ylim([-10, 550])
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('img/comparison_wavesurfer.png', dpi=150, bbox_inches='tight')
print("Guardado en img/comparison_wavesurfer.png")