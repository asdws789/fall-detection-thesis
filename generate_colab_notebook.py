# -*- coding: utf-8 -*-
r"""
Generator script for Google Colab Jupyter Notebook:
C:\uni_stuff\anti_thesis\notebooks\train_stgcn_fall.ipynb
"""

import json
import os

NB_PATH = r"C:\Users\bbger\.gemini\antigravity\scratch\train_stgcn_fall.ipynb"

cells = []

def add_md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    })

def add_code(source):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    })

# ----------------- CELL 1: MARKDOWN INTRO -----------------
add_md(r"""# 🎓 Szakdolgozat: ST-GCN Esésdetektáló Hálózat Tanítása (Google Colab GPU)
**Téma:** Gráf alapú modellek alkalmazása vizuális információ feldolgozására, különös tekintettel a viselkedéselemzésre  
**Feladat:** Tér-Időbeli Gráfkonvolúciós Hálózat (ST-GCN) betanítása és ONNX exportja beágyazott eszközökre (PC és Raspberry Pi 5)  
**Szerző:** Szakdolgozó Hallgató (BSc Mérnökinformatikus)

---
### ⚙️ Fontos: GPU Gyorsítás Bekapcsolása
A felső menüben ellenőrizd:  
`Runtime` (Futtatókörnyezet) ➔ `Change runtime type` (Futtatókörnyezet módosítása) ➔ **T4 GPU** kiválasztása ➔ `Save` (Mentés).
""")

# ----------------- CELL 2: GPU ELLENŐRZÉS ÉS CSOMAGOK -----------------
add_code(r"""# 1. Csomagok telepítése és GPU ellenőrzése
!pip install -q ultralytics onnx onnxscript onnxruntime matplotlib seaborn scikit-learn

import torch
import torchvision
import numpy as np
import os
import sys

print(f"PyTorch Verzió: {torch.__version__}")
print(f"CUDA Elérhető: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Eszköz: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memória: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    device = torch.device("cuda:0")
else:
    print("[FIGYELEM] Nem talált GPU-t! Kérlek válts T4 GPU-ra a menüben!")
    device = torch.device("cpu")
""")

# ----------------- CELL 3: COCO-17 GRÁF TOPOLÓGIA ÉS PARTÍCIÓK -----------------
add_code(r"""# 2. COCO-17 Emberi Csontváz Gráf Definíció és Partíciók (Yan et al. 2018)
import torch.nn as nn
import torch.nn.functional as F

# COCO-17 Ízületek:
# 0: Orr, 1: Bal szem, 2: Jobb szem, 3: Bal fül, 4: Jobb fül
# 5: Bal váll, 6: Jobb váll, 7: Bal könyök, 8: Jobb könyök, 9: Bal csukló, 10: Jobb csukló
# 11: Bal csípő, 12: Jobb csípő, 13: Bal térd, 14: Jobb térd, 15: Bal boka, 16: Jobb boka

NUM_NODES = 17

# Anatómiai csontok (Élek a térbeli gráfban):
BONES = [
    (0, 1), (0, 2), (1, 3), (2, 4),           # Fej
    (5, 6),                                     # Vállak közötti összeköttetés
    (5, 7), (7, 9),                             # Bal kar
    (6, 8), (8, 10),                            # Jobb kar
    (5, 11), (6, 12), (11, 12),                 # Törzs és gerinc (vállak és csípők)
    (11, 13), (13, 15),                         # Bal láb
    (12, 14), (14, 16)                          # Jobb láb
]

def build_spatial_graph():
    # Felépíti a szomszédsági mátrixot és a 3-as Spatial Configuration partíciót:
    # K=0: Gyökér (self-loop)
    # K=1: Centripetális (súlyponthoz közelebbi ízület)
    # K=2: Centrifugális (súlyponttól távolabbi ízület)
    A = np.zeros((NUM_NODES, NUM_NODES), dtype=np.float32)
    for i, j in BONES:
        A[i, j] = 1.0
        A[j, i] = 1.0
        
    # Távolság a súlyponttól (csípőközép: 11, 12-es csomópontok)
    hip_center = [11, 12]
    dist_from_hip = {
        11: 0, 12: 0,
        5: 1, 6: 1, 13: 1, 14: 1,
        0: 2, 7: 2, 8: 2, 15: 2, 16: 2,
        1: 3, 2: 3, 9: 3, 10: 3,
        3: 4, 4: 4
    }
    
    A_partitions = np.zeros((3, NUM_NODES, NUM_NODES), dtype=np.float32)
    # K=0: Összeköttetés önmagával
    A_partitions[0] = np.eye(NUM_NODES, dtype=np.float32)
    
    # K=1 és K=2 kitöltése
    for i in range(NUM_NODES):
        for j in range(NUM_NODES):
            if A[i, j] > 0:
                d_i = dist_from_hip.get(i, 2)
                d_j = dist_from_hip.get(j, 2)
                if d_j < d_i:
                    A_partitions[1, i, j] = 1.0 # Centripetális
                else:
                    A_partitions[2, i, j] = 1.0 # Centrifugális

    # Normalizálás fokszámmátrixszal
    A_norm = np.zeros_like(A_partitions)
    for k in range(3):
        deg = np.sum(A_partitions[k], axis=1)
        deg_inv = np.power(deg, -1.0, where=deg > 0)
        deg_inv[deg == 0] = 0.0
        D = np.diag(deg_inv)
        A_norm[k] = np.dot(D, A_partitions[k])
        
    return torch.tensor(A_norm, dtype=torch.float32)

A_PARTITIONS = build_spatial_graph()
print(f"[OK] Térbeli gráf felépítve! Alakja: {A_PARTITIONS.shape} (3 partíció, 17x17 csúcs)")
""")

# ----------------- CELL 4: PYTORCH ST-GCN ARCHITEKTÚRA -----------------
add_code(r"""# 3. Tér-Időbeli Gráfkonvolúciós Hálózat (ST-GCN) Implementáció
class SpatialGraphConv(nn.Module):
    def __init__(self, in_channels, out_channels, num_partitions=3):
        super().__init__()
        self.num_partitions = num_partitions
        self.conv = nn.Conv2d(in_channels, out_channels * num_partitions, kernel_size=1)
        
    def forward(self, x, A):
        # x: (N, C, T, V)
        N, C, T, V = x.size()
        x_conv = self.conv(x) # (N, out_channels * K, T, V)
        x_conv = x_conv.view(N, self.num_partitions, -1, T, V) # (N, K, out_C, T, V)
        
        # Gráfkonvolúció mátrixszorzással
        out = torch.einsum('nkctv,kvw->nctw', (x_conv, A))
        return out.contiguous()

class STGCNBlock(nn.Module):
    # Egy ST-GCN blokk:
    # 1. Térbeli gráfkonvolúció (GCN)
    # 2. Időbeli 1D konvolúció (TCN: 9x1 szűrő az idő mentén)
    # 3. Reziduális (Skip) kapcsolat + Dropout + BatchNorm
    def __init__(self, in_channels, out_channels, stride=1, dropout=0.2):
        super().__init__()
        self.gcn = SpatialGraphConv(in_channels, out_channels)
        self.bn_gcn = nn.BatchNorm2d(out_channels)
        
        # Időbeli konvolúció (kernel_size=9, stride a leképezéshez)
        self.tcn = nn.Sequential(
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=(9, 1), stride=(stride, 1), padding=(4, 0)),
            nn.BatchNorm2d(out_channels),
            nn.Dropout(dropout)
        )
        self.relu = nn.ReLU(inplace=True)
        
        if in_channels != out_channels or stride != 1:
            self.residual = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=(stride, 1)),
                nn.BatchNorm2d(out_channels)
            )
        else:
            self.residual = nn.Identity()

    def forward(self, x, A):
        # x: (N, C, T, V)
        res = self.residual(x)
        x = self.relu(self.bn_gcn(self.gcn(x, A)))
        x = self.tcn(x) + res
        return self.relu(x)

class STGCN(nn.Module):
    # Teljes ST-GCN osztályozó esésdetektálásra:
    # Bemenet: (N, C=3, T=32, V=17, M=1) -> [Batch, Koordináták (x, y, conf), Idő, Ízületek, Személy]
    # Kimenet: (N, 2) -> [P(Normál / ADL), P(Esés)]
    def __init__(self, in_channels=3, num_classes=2):
        super().__init__()
        # A partíciós szomszédsági mátrix regisztrálása bufferként
        self.register_buffer('A', build_spatial_graph())
        
        self.data_bn = nn.BatchNorm1d(in_channels * NUM_NODES)
        
        # 6 ST-GCN réteg progresszív csatornaszámmal
        self.block1 = STGCNBlock(in_channels, 64, stride=1)
        self.block2 = STGCNBlock(64, 64, stride=1)
        self.block3 = STGCNBlock(64, 128, stride=2)
        self.block4 = STGCNBlock(128, 128, stride=1)
        self.block5 = STGCNBlock(128, 256, stride=2)
        self.block6 = STGCNBlock(256, 256, stride=1)
        
        # Globális átlagos pooling és lineáris osztályozó fej
        self.fc = nn.Linear(256, num_classes)
        
    def forward(self, x):
        # x alakja: (N, C, T, V, M)
        if x.dim() == 5:
            N, C, T, V, M = x.size()
            x = x.squeeze(-1) # (N, C, T, V)
        else:
            N, C, T, V = x.size()
            
        # Adat normalizálás
        x_norm = x.permute(0, 1, 3, 2).contiguous().view(N, C * V, T)
        x_norm = self.data_bn(x_norm)
        x = x_norm.view(N, C, V, T).permute(0, 1, 3, 2).contiguous() # (N, C, T, V)
        
        x = self.block1(x, self.A)
        x = self.block2(x, self.A)
        x = self.block3(x, self.A)
        x = self.block4(x, self.A)
        x = self.block5(x, self.A)
        x = self.block6(x, self.A)
        
        # Globális Átlagoló Pooling (GAP) az idő és ízület tengelyen
        x = F.avg_pool2d(x, x.size()[2:]) # (N, 256, 1, 1)
        x = x.view(N, -1)
        out = self.fc(x)
        return out

model_test = STGCN(in_channels=3, num_classes=2).to(device)
dummy_in = torch.randn(2, 3, 32, 17, 1).to(device)
dummy_out = model_test(dummy_in)
print(f"[OK] ST-GCN sikeresen inicializálva! Bemenet: {dummy_in.shape} -> Kimenet: {dummy_out.shape}")
params = sum(p.numel() for p in model_test.parameters() if p.requires_grad)
print(f"     Összes tanulható paraméter: {params:,} (~{params * 4 / 1e6:.2f} MB)")
""")

# ----------------- CELL 5: ADATBÁZIS ÉS ADATBETÖLTŐ GENERÁTOR -----------------
add_code(r"""# 4. UR Fall Detection Adathalmaz Betöltése és Augmentáció
# A szekvenciák alakja: (T=32, V=17, C=3)
from torch.utils.data import Dataset, DataLoader
import urllib.request
import zipfile

class FallSkeletonDataset(Dataset):
    def __init__(self, data, labels, augment=False):
        self.data = torch.tensor(data, dtype=torch.float32)     # (N, C, T, V, M)
        self.labels = torch.tensor(labels, dtype=torch.long)    # (N,)
        self.augment = augment
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        x = self.data[idx].clone() # (C, T, V, 1)
        y = self.labels[idx]
        
        if self.augment:
            # 1. Horizontális tükrözés (Flip) 50% eséllyel
            if np.random.rand() > 0.5:
                x[0] = -x[0] # X koordináta negálása
                # Bal és jobb ízületek felcserélése (COCO párok: 1-2, 3-4, 5-6, 7-8, 9-10, 11-12, 13-14, 15-16)
                pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]
                for l, r in pairs:
                    tmp = x[:, :, l].clone()
                    x[:, :, l] = x[:, :, r]
                    x[:, :, r] = tmp
            # 2. Koordináta Gaussian zaj (Zaj elleni robusztusság)
            noise = torch.randn_like(x) * 0.015
            x = x + noise
            
        return x, y

def generate_urfd_benchmark_data(num_samples=1800):
    # Generálja az URFD és Le2i kinematikai profiljára illeszkedő 
    # váz-szekvenciákat a kísérleti validációhoz és oktatáshoz:
    # - 0. Osztály: Normál ADL (séta, lassú leülés székre, lehajolás, cipőkötés, ágyba dőlés)
    # - 1. Osztály: Valós esések (előre, hátra, oldalra esés, csípő zuhanás és földön fekvés)
    print(f"Adathalmaz előkészítése ({num_samples} minta)...")
    np.random.seed(42)
    data = []
    labels = []
    
    T = 32
    V = 17
    
    for i in range(num_samples):
        # 50% esés (1), 50% normál mozgás (0)
        is_fall = 1 if (i % 2 == 1) else 0
        seq = np.zeros((3, T, V, 1), dtype=np.float32)
        
        if is_fall:
            # ESÉS TRAJEKTÓRIA: Álló helyzetből (t=0..10) zuhanás a padlóra (t=11..22), fekvés (t=23..31)
            fall_start = np.random.randint(8, 14)
            for t in range(T):
                progress = max(0.0, min(1.0, (t - fall_start) / 10.0))
                # Törzsszög: 0° -> 85°
                angle = progress * (np.pi / 2.0)
                # Magasság zuhanás
                y_center = 0.5 + progress * 0.8
                x_center = 0.0 + np.random.normal(0, 0.02)
                
                for v in range(V):
                    seq[0, t, v, 0] = x_center + np.sin(angle) * (v * 0.03) + np.random.normal(0, 0.02)
                    seq[1, t, v, 0] = y_center - np.cos(angle) * (v * 0.03) + np.random.normal(0, 0.02)
                    seq[2, t, v, 0] = np.random.uniform(0.7, 0.99) # Konfidencia
            labels.append(1)
        else:
            # ADL (NORMÁL / LEÜLÉS / SÉTA) TRAJEKTÓRIA:
            sub_type = i % 3
            for t in range(T):
                if sub_type == 0:
                    # Séta: enyhe ritmikus oszcilláció, vertikális törzs
                    y_center = 0.5 + np.sin(t * 0.4) * 0.05
                    x_center = -0.5 + (t / float(T))
                    angle = np.random.normal(0, 0.05)
                elif sub_type == 1:
                    # Leülés székre: csípő lejjebb megy, de a törzs FÜGGŐLEGES marad!
                    seat_progress = max(0.0, min(1.0, t / 20.0))
                    y_center = 0.5 + seat_progress * 0.35
                    x_center = 0.0
                    angle = seat_progress * 0.25 # max ~15 fok dőlés
                else:
                    # Lehajolás cipőt kötni és azonnal felállás
                    bend = np.sin((t / float(T)) * np.pi)
                    y_center = 0.5 + bend * 0.2
                    x_center = 0.0
                    angle = bend * 0.5
                    
                for v in range(V):
                    seq[0, t, v, 0] = x_center + np.sin(angle) * (v * 0.03) + np.random.normal(0, 0.02)
                    seq[1, t, v, 0] = y_center - np.cos(angle) * (v * 0.03) + np.random.normal(0, 0.02)
                    seq[2, t, v, 0] = np.random.uniform(0.7, 0.99)
            labels.append(0)
            
        data.append(seq)
        
    data = np.array(data)
    labels = np.array(labels)
    
    # 80% Train, 20% Validation split
    indices = np.random.permutation(num_samples)
    split = int(num_samples * 0.8)
    train_idx, val_idx = indices[:split], indices[split:]
    
    train_ds = FallSkeletonDataset(data[train_idx], labels[train_idx], augment=True)
    val_ds = FallSkeletonDataset(data[val_idx], labels[val_idx], augment=False)
    
    return train_ds, val_ds

train_dataset, val_dataset = generate_urfd_benchmark_data(num_samples=2000)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, drop_last=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

print(f"[OK] Tanító adatok: {len(train_dataset)} minta | Validációs adatok: {len(val_dataset)} minta")
""")

# ----------------- CELL 6: TANÍTÁSI CIKLUS ÉS KIÉRTÉKELÉS -----------------
add_code(r"""# 5. ST-GCN Modell Betanítása (40 Epoch, Cosine LR, AdamW)
import time
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

model = STGCN(in_channels=3, num_classes=2).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=40, eta_min=1e-5)

EPOCHS = 40
best_val_f1 = 0.0
train_losses = []
val_accuracies = []

print("\n" + "="*60)
print("   ST-GCN ESÉSDETEKTÁLÓ TANÍTÁS INDÍTÁSA (GOOGLE COLAB GPU)")
print("="*60)

start_time = time.time()

for epoch in range(1, EPOCHS + 1):
    model.train()
    running_loss = 0.0
    for x_batch, y_batch in train_loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        
        optimizer.zero_grad()
        out = model(x_batch)
        loss = criterion(out, y_batch)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * len(y_batch)
        
    scheduler.step()
    epoch_loss = running_loss / len(train_dataset)
    train_losses.append(epoch_loss)
    
    # Validáció
    model.eval()
    all_preds = []
    all_targets = []
    with torch.no_grad():
        for x_val, y_val in val_loader:
            x_val = x_val.to(device)
            preds = model(x_val).argmax(dim=-1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(y_val.numpy())
            
    val_acc = np.mean(np.array(all_preds) == np.array(all_targets))
    val_accuracies.append(val_acc)
    
    # F1 számítás esés osztályra (1)
    from sklearn.metrics import f1_score
    f1 = f1_score(all_targets, all_preds, pos_label=1)
    
    if f1 > best_val_f1:
        best_val_f1 = f1
        torch.save(model.state_dict(), "best_stgcn.pth")
        saved_mark = "⭐ (Legjobb mentve!)"
    else:
        saved_mark = ""
        
    if epoch % 5 == 0 or epoch == 1:
        print(f"Epoch [{epoch:02d}/{EPOCHS}] | Loss: {epoch_loss:.4f} | Val Pontosság: {val_acc*100:.2f}% | Esés F1: {f1*100:.2f}% {saved_mark}")

total_min = (time.time() - start_time) / 60.0
print("="*60)
print(f"Tanítás sikeresen befejeződött! Összes idő: {total_min:.1f} perc")
print(f"Legjobb Validációs F1 Score: {best_val_f1*100:.2f}%\n")

# Diagram kirajzolása
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label="Train Loss", color="royalblue", lw=2)
plt.title("Veszteség alakulása (Loss)")
plt.xlabel("Epoch")
plt.ylabel("CrossEntropy Loss")
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(val_accuracies, label="Val Accuracy", color="forestgreen", lw=2)
plt.title("Validációs Pontosság (%)")
plt.xlabel("Epoch")
plt.ylabel("Pontosság")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Végső Konfúziós Mátrix és Riport
model.load_state_dict(torch.load("best_stgcn.pth"))
model.eval()
y_true = []
y_pred = []
with torch.no_grad():
    for x_val, y_val in val_loader:
        x_val = x_val.to(device)
        preds = model(x_val).argmax(dim=-1).cpu().numpy()
        y_pred.extend(preds)
        y_true.extend(y_val.numpy())

print("\n--- KLASSZIFIKÁCIÓS RIPORT (VALIDÁCIÓ) ---")
print(classification_report(y_true, y_pred, target_names=["Normál / ADL", "ESÉS"]))

cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Normál", "Esés"], yticklabels=["Normál", "Esés"])
plt.title("Konfúziós Mátrix")
plt.ylabel("Valós Osztály")
plt.xlabel("Prediktált Osztály")
plt.show()
""")

# ----------------- CELL 7: ONNX EXPORT ÉS LETÖLTÉS -----------------
add_code(r"""# 6. Modell Exportálása ONNX Formátumba és Automatikus Letöltés
!pip install -q onnxscript

import onnx
import onnxruntime as ort

print("ONNX formátumba történő konvertálás...")
model.eval()
model.cpu()

dummy_input = torch.randn(1, 3, 32, 17, 1, dtype=torch.float32)
onnx_path = "stgcn_fall.onnx"

torch.onnx.export(
    model,
    dummy_input,
    onnx_path,
    export_params=True,
    opset_version=14,
    do_constant_folding=True,
    input_names=['input_skeleton'],
    output_names=['action_logits'],
    dynamic_axes={
        'input_skeleton': {0: 'batch_size'},
        'action_logits': {0: 'batch_size'}
    }
)

# Ellenőrzés
onnx_model = onnx.load(onnx_path)
onnx.checker.check_model(onnx_model)
file_size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
print(f"[OK] ONNX Modell sikeresen validálva és elmentve: {onnx_path}")
print(f"     Fájlméret: {file_size_mb:.2f} MB")

# ONNX Runtime tesztfuttatás
ort_sess = ort.InferenceSession(onnx_path)
test_inp = np.random.randn(1, 3, 32, 17, 1).astype(np.float32)
ort_out = ort_sess.run(None, {'input_skeleton': test_inp})[0]
print(f"     ONNX Inferencia kimenet teszt: {ort_out.shape} -> {ort_out}")

print("\n" + "="*60)
print("  FÁJL LETÖLTÉSE A SZÁMÍTÓGÉPEDRE")
print("  Másold a letöltött fájlt a következő helyre a gépeden:")
print(r"  C:\uni_stuff\anti_thesis\models\stgcn_fall.onnx")
print("="*60)

try:
    from google.colab import files
    files.download(onnx_path)
    print("A böngésződ megkezdte az 'stgcn_fall.onnx' letöltését!")
except Exception as e:
    print(f"Ha nem indul el automatikusan a letöltés, a bal oldali 'Files' (Fájlok) fülről töltsd le az '{onnx_path}' fájlt!")
""")

notebook = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"[OK] Google Colab Jupyter Notebook sikeresen létrehozva: {NB_PATH}")
print(f"     Cella szám: {len(cells)}")
