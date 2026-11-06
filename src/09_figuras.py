import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
AZ, NA_, GR, OR = "#1F4E79", "#B7B7B7", "#F2F2F2", "#C55A11"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
# 1 flujo
fig, ax = plt.subplots(figsize=(10, 3.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3.6)
pasos = [("1. Pregunta","hipótesis H1 y H0\nfijadas antes\nde medir"),("2. Captura","18.206 avisos\n9 fuentes\n06/11/2026"),("3. Selección","reglas escritas:\nrol de IA, entrada,\nvigencia"),
         ("4. Muestra","97 avisos\n61 empresas"),("5. Medición","avisos: línea\nde base; planes:\n10 habilidades\ncon cita"),("6. Resultado","Δ con bootstrap\npor institución;\nsensibilidades"),("7. Producto","ficha por carrera;\nentrevistas;\nlímites a la vista")]
w = 1.22
for i, (t, d) in enumerate(pasos):
    x = 0.1 + i * 1.4
    ax.add_patch(FancyBboxPatch((x, 0.9), w, 2.1, boxstyle="round,pad=0.02", fc=GR, ec=AZ, lw=1.2))
    ax.text(x + w/2, 2.65, t, ha="center", va="center", fontweight="bold", color=AZ, fontsize=8.2)
    ax.text(x + w/2, 1.8, d, ha="center", va="center", fontsize=7.2)
    if i < len(pasos)-1: ax.annotate("", xy=(x+1.38, 1.95), xytext=(x+w+0.02, 1.95), arrowprops=dict(arrowstyle="->", color=AZ))
ax.text(5, 0.35, "Todo paso queda registrado: archivos sin modificar, huella SHA-256, reglas con semilla 2026 y archivo de codificación con cita y URL.", ha="center", fontsize=8.5, style="italic")
fig.savefig("informe/fig_flujo.png", dpi=200, bbox_inches="tight"); plt.close()
# 2 embudo
pasos = ["Avisos únicos capturados","Rol de IA por título","Nivel de entrada\ny rol de IA","Vigentes (≤365 d)","Con ≥100 palabras","Sin repetir\nempresa y título","Muestra (tope 10\npor empresa)"]
vals = [18206,1413,166,163,161,104,97]
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.barh(range(len(vals))[::-1], vals, color=AZ); ax.set_xscale("log"); ax.set_yticks(range(len(vals))[::-1]); ax.set_yticklabels(pasos, fontsize=8.5)
for y, v in zip(range(len(vals))[::-1], vals): ax.text(v*1.08, y, f"{v:,}".replace(",", "."), va="center", fontsize=9)
ax.set_xlim(50, 60000); ax.set_xlabel("Avisos (escala logarítmica)"); fig.savefig("informe/fig_embudo.png", dpi=200, bbox_inches="tight"); plt.close()
# 3 heatmap planes
d = pd.read_csv("config/codificacion_planes.csv"); d["x"] = (pd.to_numeric(d["valor"], errors="coerce") == 1)
car = ["UADE Lic. IA y Ciencia de Datos","Palermo Ing. en IA","Palermo Lic. en IA","UNL Ing. en IA","UTN-FRLP Lic. en IA"]
lab = ["UADE","Palermo (Ing.)","Palermo (Lic.)","UNL","UTN-FRLP"]
hab = ["Python","SQL","Estadística","ML clásico","Deep learning","Integración","Despliegue","Monitoreo","Nube/contenedores","Git"]
M = np.array([[d[(d.carrera==c)&(d.habilidad==h)].x.iloc[0] for h in hab] for c in car])
fig, ax = plt.subplots(figsize=(9, 3.4))
for i in range(5):
    for j in range(10):
        ax.add_patch(plt.Rectangle((j, 4-i), 0.94, 0.9, fc=(AZ if M[i,j] else GR), ec="white"))
        ax.text(j+0.47, 4-i+0.45, "1" if M[i,j] else "NA", ha="center", va="center", color="white" if M[i,j] else "#555", fontsize=9, fontweight="bold" if M[i,j] else "normal")
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.set_xticks(np.arange(10)+0.47); ax.set_xticklabels(hab, rotation=35, ha="right", fontsize=8.5)
ax.set_yticks(np.arange(5)+0.45); ax.set_yticklabels(lab[::-1]); ax.axvline(5-0.03, color="k", lw=1); ax.tick_params(length=0); ax.spines[:].set_visible(False)
ax.text(2.5, 5.12, "Base", ha="center", fontweight="bold", color=AZ); ax.text(7.5, 5.12, "Producción", ha="center", fontweight="bold", color=OR)
fig.savefig("informe/fig_planes.png", dpi=200, bbox_inches="tight"); plt.close()
# 4 brecha
b = pd.read_csv("data/processed/resultados_demanda_linea_base.csv"); b = b[b.grupo.isin(["base","produccion"])].set_index("habilidad").loc[hab]
cov = M.sum(axis=0)/5*100
fig, ax = plt.subplots(figsize=(8.6, 4.6)); y = np.arange(10)[::-1]
for yi, h, c in zip(y, hab, cov):
    col = AZ if b.loc[h,"grupo"]=="base" else OR
    ax.plot([b.loc[h,"pct"], c], [yi, yi], color="#999", lw=1.2, zorder=1)
    ax.scatter(b.loc[h,"pct"], yi, s=60, color=col, marker="o", zorder=2); ax.scatter(c, yi, s=60, facecolor="white", edgecolor=col, marker="s", lw=1.8, zorder=2)
ax.set_yticks(y); ax.set_yticklabels(hab); ax.set_xlim(-3, 108); ax.axhline(4.5, color="k", lw=0.6, ls=":")
ax.set_xlabel("Porcentaje")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([],[],marker="o",color="w",markerfacecolor="#555",ms=8,label="Avisos de entrada que la piden (%, n=95)"),Line2D([],[],marker="s",color="w",markerfacecolor="white",markeredgecolor="#555",ms=8,label="Carreras con evidencia publicada (%, de 5)")],loc="lower right",fontsize=8,frameon=True)
ax.text(104, 9.4, "Base (azul)", ha="right", color=AZ, fontsize=8.5, fontweight="bold"); ax.text(104, 4.1, "Producción (naranja)", ha="right", color=OR, fontsize=8.5, fontweight="bold")
fig.savefig("informe/fig_brecha.png", dpi=200, bbox_inches="tight"); plt.close()
# 5 delta
inst = {"UADE":0.2,"Palermo":0.8,"UNL":0.8,"UTN-FRLP":0.4}
esc = [("Principal",0.55,0.30,0.80),("Casos límite de UNL y UTN\ncomo evidencia",0.60,0.35,0.80),("UADE integración = NA",0.60,0.40,0.80)]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.2), gridspec_kw={"width_ratios":[1,1.2]})
a1.scatter(list(inst.values()), range(4)[::-1], color=AZ, s=70); a1.set_yticks(range(4)[::-1]); a1.set_yticklabels(inst.keys()); a1.axvline(0, color="k", lw=0.8)
for v, yy in zip(inst.values(), range(4)[::-1]): a1.hlines(yy, 0, v, color="#bbb", lw=1)
a1.set_xlim(-0.05, 1.0); a1.set_xlabel("Δ por institución"); a1.set_title("Cada institución", fontsize=10)
for k, (n, m, lo, hi) in enumerate(esc):
    yy = 2-k; a2.hlines(yy, lo, hi, color=AZ, lw=3); a2.scatter(m, yy, color=AZ, s=60, zorder=3); a2.text(hi+0.02, yy, f"{m:.2f} [{lo:.2f}; {hi:.2f}]".replace(".", ","), va="center", fontsize=8)
a2.set_yticks([2,1,0]); a2.set_yticklabels([e[0] for e in esc], fontsize=8.5); a2.axvline(0, color="k", lw=0.8); a2.set_xlim(-0.05, 1.2); a2.set_xlabel("Δ promedio con IC 95 %"); a2.set_title("Promedio y sensibilidad", fontsize=10)
fig.tight_layout(); fig.savefig("informe/fig_delta.png", dpi=200, bbox_inches="tight"); plt.close()
print("ok")
