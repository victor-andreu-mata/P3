import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('img', exist_ok=True)

# Cargar features (pot, r1norm, rmaxnorm)
features = np.loadtxt('features.txt')
pot      = features[:, 0]
r1norm   = features[:, 1]
rmaxnorm = features[:, 2]

# Cargar f0 estimado
f0 = np.loadtxt('prueba.f0')
# Alinear longitudes
n = min(len(pot), len(f0))
pot      = pot[:n]
r1norm   = r1norm[:n]
rmaxnorm = rmaxnorm[:n]
f0       = f0[:n]

frame_shift = 0.015  # 15 ms
t = np.arange(n) * frame_shift

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
fig.suptitle('Features para la decisión sonoro/sordo — prueba.wav', fontsize=13, fontweight='bold')

# F0
axes[0].plot(t, f0, color='steelblue', linewidth=1)
axes[0].set_ylabel('f0 (Hz)')
axes[0].set_title('Pitch estimado (0 = sordo)')
axes[0].grid(True, alpha=0.3)

# Potencia
axes[1].plot(t, pot, color='darkorange', linewidth=1)
axes[1].axhline(0, color='red', linestyle='--', linewidth=1, label='umbral pot=0 dB')
axes[1].set_ylabel('Potencia (dB)')
axes[1].set_title('r[0] — Potencia de la trama')
axes[1].legend(fontsize=8)
axes[1].grid(True, alpha=0.3)

# r1norm
axes[2].plot(t, r1norm, color='green', linewidth=1)
axes[2].axhline(0.6, color='red', linestyle='--', linewidth=1, label='umbral r1norm=0.6')
axes[2].set_ylabel('r1norm')
axes[2].set_title('r[1]/r[0] — Autocorrelación normalizada en lag=1')
axes[2].legend(fontsize=8)
axes[2].grid(True, alpha=0.3)

# rmaxnorm
axes[3].plot(t, rmaxnorm, color='purple', linewidth=1)
axes[3].axhline(0.6, color='red', linestyle='--', linewidth=1, label='umbral rmaxnorm=0.6')
axes[3].set_ylabel('rmaxnorm')
axes[3].set_title('r[lag]/r[0] — Autocorrelación en el máximo secundario')
axes[3].legend(fontsize=8)
axes[3].set_xlabel('Tiempo (s)')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('img/features_voicing.png', dpi=150, bbox_inches='tight')
print("Guardado en img/features_voicing.png")