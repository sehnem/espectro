# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 21:35:23 2016

@author: josue
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#matplotlib.style.use('ggplot')
matplotlib.style.use('fivethirtyeight')

dados = pd.read_hdf('./espectro.h5','spectra')

atenua = dados.Global/dados.Top
atenua.to_frame()

erro20=np.zeros(35)
erro21=np.zeros(35)
erro41=np.zeros(35)
errokz=np.zeros(35)
merito20=np.zeros(35)
merito21=np.zeros(35)
merito41=np.zeros(35)
meritokz=np.zeros(35)

# ajuste para C-Si
referencia = 'Global'
pv = dados[referencia]
    


pira = dados.bpw21*dados.acrilico
calibra15 = (pv*dados.Global).sum()/(pira*dados.Global).sum()
for i in range(1,35):
    espectro = atenua**(i/1.5)*dados.Top
    medida = (pira*espectro).sum()*calibra15
    real = (pv*espectro).sum()
    erro21[i] = (medida-real)/real
    merito21[i] = medida-real
    
    
pira = dados.bpw20*dados.acrilico
calibra15 = (pv*dados.Global).sum()/(pira*dados.Global).sum()
for i in range(1,35):
    espectro = atenua**(i/1.5)*dados.Top
    medida = (pira*espectro).sum()*calibra15
    real = (pv*espectro).sum()
    erro20[i] = (medida-real)/real
    merito20[i] = medida-real

ajuste=1
ajuste2 = 1
erro = 9999999

#ajustar problema dos 50%
for f in range (0,10000):
    pira = (dados.bpw20*dados.acrilico)+(dados.bpw21*dados.acrilico*f*0.001)
    calibra15 = (pv*dados.Global).sum()/(pira*dados.Global).sum()
    for i in range(1,30):
        espectro = atenua**(i/1.5)*dados.Top
        medida = (pira*espectro).sum()*calibra15
        real = (pv*espectro).sum()
        merito41[i] = medida-real
    if abs(merito41.sum())<erro:
        erro=abs(merito41.sum())
        ajuste=f*0.001

if ajuste>9.9:
    ajuste=1
    ajuste2=0

pira = (dados.bpw20*ajuste2*dados.acrilico)+(dados.bpw21*dados.acrilico*ajuste)
calibra15 = (pv*dados.Global).sum()/(pira*dados.Global).sum()
for i in range(1,35):
    espectro = atenua**(i/1.5)*dados.Top
    medida = (pira*espectro).sum()*calibra15
    real = (pv*espectro).sum()
    erro41[i] = (medida-real)/real
    merito41[i] = medida-real  

pira = dados['Kipp & Zonen']
calibra15 = (pv*dados.Global).sum()/(pira*dados.Global).sum()
for i in range(1,35):
    espectro = atenua**(i/1.5)*dados.Top
    medida = (pira*espectro).sum()*calibra15
    real = (pv*espectro).sum()
    errokz[i] = (medida-real)/real
    meritokz[i] = medida-real
    
percentual = 100*(ajuste/(ajuste+ajuste2))

plt.figure()
plt.title('Erro')
ax = plt.plot(erro20, label="BPW20")
plt.plot(erro21, label="BPW21")
plt.plot(erro41, label="BPW20+BPW21")
plt.plot(errokz, label="Kipp & Zonen")
plt.xticks(range(1,35))
plt.xlim([1,30])
plt.legend(bbox_to_anchor=(0.01, 0.25), loc=2, borderaxespad=0.)
#plt.legend(bbox_to_anchor=(0.01, 1.05), loc=2, borderaxespad=0.)
plt.xlabel('Massa de Ar')
plt.ylabel('Erro')
plt.text(25, -0.3, 'Peso BPW21 =' + str(round(percentual)) + '%')
plt.savefig('./imagens/'+ referencia + '_erro.png')
plt.show()

plt.figure()
plt.title('Mérito')
plt.plot(merito20, label="BPW20")
plt.plot(merito21, label="BPW21")
plt.plot(merito41, label="BPW20+BPW21")
plt.plot(meritokz, label="Kipp & Zonen")
plt.legend(bbox_to_anchor=(0.01, 0.25), loc=2, borderaxespad=0.)
plt.xticks(range(1,35))
plt.xlim([1,30])
plt.xlabel('Massa de Ar')
plt.ylabel('Erro (Wm²)')
plt.savefig('./imagens/'+ referencia + '_merito.png')
plt.show()

dados[['Global',referencia]].plot(xlim=[320,2200])
plt.show()



#    l_bpw20 = (dados.bpw20*espectro).sum()
#    p_bpw20 = dados.bpw20.sum()
#    s_bpw20 = l_bpw20/p_bpw20
#
#    l_bpw21 = (dados.bpw21*espectro).sum()
#    p_bpw21 = dados.bpw21.sum()
#    s_bpw21 = l_bpw21/p_bpw21
#
#    rbpw[i-1] = s_bpw20/s_bpw21
#
#    pira = dados.bpw21+dados.bpw20*rbpw[i-1]
#    pira = (pira/pira.sum())*100
#    
#    calibra[i-1] = espectro.sum()/(pira*espectro).sum()

#
