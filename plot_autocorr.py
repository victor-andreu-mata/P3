import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

os.makedirs('img', exist_ok=True)

rate, data = wavfile.read('prueba.wav')
if data.dtype != np.float32:
    data = data.astype(np.float32) / np.iinfo(data.dtype).max

frame_len = int(0.030 * rate)
n_start = int(0.35 * rate)
frame = data[n_start:n_start + frame_len]

hamming = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(frame_len) / (frame_len - 1))
frame_w = frame * hamming

r = np.correlate(frame_w, frame_w, mode='full')
r = r[len(r)//2:]
r = r / (r[0] if r[0] != 0 else 1e-10)

min_lag = int(rate / 500)
max_lag = min(int(rate / 50), frame_len // 2)

lag_max = np.argmax(r[min_lag:max_lag]) + min_lag
f0_est = rate / lag_max
t_pitch = lag_max / rate * 1000

t_frame = np.arange(frame_len) / rate * 1000
lags = np.arange(len(r)) / rate * 1000

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
fig.suptitle('Análisis de pitch — segmento sonoro (30 ms)', fontsize=13, fontweight='bold')

ax1.plot(t_frame, frame, color='steelblue', linewidth=1)
for k in range(1, 5):
    xpos = k * t_pitch
    if xpos < t_frame[-1]:
        ax1.axvline(xpos, color='tomato', linestyle='--', linewidth=1.2,
                    label=f'T₀ = {t_pitch:.2f} ms' if k == 1 else '')
ax1.set_xlabel('Tiempo (ms)')
ax1.set_ylabel('Amplitud')
ax1.set_title(f'Señal temporal — fonema sonoro (f₀ ≈ {f0_est:.1f} Hz)')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, t_frame[-1]])

ax2.plot(lags[:max_lag+50], r[:max_lag+50], color='steelblue', linewidth=1)
ax2.axhline(0, color='gray', linewidth=0.8)
ax2.plot(lags[lag_max], r[lag_max], 'o', color='tomato', markersize=9,
         label=f'Máximo secundario: lag={lag_max} muestras (T₀={t_pitch:.2f} ms, f₀={f0_est:.1f} Hz)')
ax2.axvline(lags[lag_max], color='tomato', linestyle='--', linewidth=1.2)
ax2.axvspan(lags[min_lag], lags[max_lag], alpha=0.08, color='orange',
            label='Rango de búsqueda (50–500 Hz)')
ax2.set_xlabel('Retardo (ms)')
ax2.set_ylabel('r[l] / r[0]')
ax2.set_title('Autocorrelación normalizada')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([0, lags[max_lag+40]])

plt.tight_layout()
plt.savefig('img/autocorr_analysis.png', dpi=150, bbox_inches='tight')
print("Imagen guardada en img/autocorr_analysis.png")