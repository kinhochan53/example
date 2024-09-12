"""      
   ************************************************************** 
   ASP 1 - 2024.2
   Aluno : Marcos Vinicius
   **************************************************************
"""
import numpy as np
import  cmath
'''-----------Dados de entrada-----------'''

'''Gerador'''
Sg1=    100e6   # Potência em VA
Vg1=    13800       # Tensão em V
Xsg1=   0.9j        # Reatância em PU

''' Transformador 1'''
St1=    65e6          # Potência em VA
V1t1=   230000            # Tensão primário em V
V2t1=   14000             # Tensão Secundário em V
Zt1=    0.1j              # Impedância em PU

''' Linha de transmissão'''
Zlt= 150j           # Impedância em Ohms

'''Transformador 2'''
St2=    40e6       # Potência em VA
V1t2=   242000         # Tensão primário em V
V2t2=   10000          # Tensão Secundário em V
Zt2=    0.08j          # Impedância em PU

'''Carga'''
Sc=     60000000       #Potência em VA
Vf=     10000          #Tensão em V
FP=     0.8            # Fator de potência

'------Passando todos os componentes para as bases 100 MVA e 230KV na LT----'
Sb=     100000000       # Potência base do circuito
Vb2=    230000          # Tensão base na linha de transmissão (Circuito 2)

Vb1= Vb2 * (V2t1 / V1t1)    # Tensão base no circuito 1
Vb3= Vb2 * (V2t2 / V1t2)    # Tensão base no circuito 3

'Função de mudança de base'
def mud_base(Zba,Sba,Sbn,Vba,Vbn):
    ''' Zba = IMPEDÂNCIA NA BASE ANTIGA \n
        Sba = POTÊNCIA BASE ANTIGA\n
        Sbn = POTÊNCIA BASE NOVA\n 
        Vba = TENSÃO BASE ANTIGA\n
        Vbn = TENSÃO BASE NOVA'''
    Zbn = Zba * (Sbn/Sba)*((Vba/Vbn)**2)
    return Zbn

'Gerador'
Zg1_pu = mud_base(Xsg1, Sg1, Sb, Vg1, Vb1)

'Transformador T1'
Zt1_pu = mud_base(Zt1, St1, Sb, V2t1, Vb2)

'Linha de Transmissão'
Zlt_pu = Zlt/((Vb2**2)/Sb)

'Transformador T2'
Zt2_pu = mud_base(Zt2, St2, Sb, V2t2, Vb3)

'-----Tensão na Carga------'
Vf_pu_mod = Vf / Vb3  #Módulo da Tensão na Carga

Vf_pu = cmath.rect(Vf_pu_mod, np.radians(0)) # Tensão na carga em PU

"-----Corrente na Carga-----"
Sc_pu = Sc/Sb             # Potência da carga em pu

Ic_pu_mod =  (Sc/Sb)/(Vf/Vb3)    #Módulo da corrente de carga em PU

Ic_ang = -np.arccos(FP)    #fase da corrente de carga

Ic_pu = cmath.rect(Ic_pu_mod, Ic_ang) # Corrente de carga em PU

'-----Tensão na barra 1-----'
Vbarra1 = Vf_pu + (Zt1_pu + Zlt_pu + Zt2_pu) * Ic_pu

'-----correntes en cada fase-----'

a = cmath.rect(1, np.radians(240))

'Circuito 3'

Ia_c3 = Ic_pu
Ib_c3 = Ic_pu * a**2
Ic_c3 = Ic_pu * a

'circuito 2'

Ia_c2 = Ia_c3 * cmath.rect(1, np.radians(-30))
Ib_c2 = Ia_c2 * a**2
Ic_c2 = Ia_c2 * a

'circuito 1'

Ia_c1 = Ia_c2 * cmath.rect(1, np.radians(-210))
Ib_c1 = Ia_c2 * a**2
Ic_c1 = Ia_c2 * a


# Geração de Arquivo de Saída
nome_arq = 'saída.txt'
g = (nome_arq == '')

texto = '**********************************************************'
texto1 = 'Tarefa - ASP 1 - 2024.2                                    '
texto2 = 'Exercício de Sistema PU                      '
texto3 = 'Aluno: Marcos Vinicius Carneiro da Cruz                         '
texto4 = 'Número: 40  '            

if not g:
    with open(nome_arq, 'wt') as fid:
        fid.write(f'{texto}\n')
        fid.write(f'{texto1}\n')
        fid.write(f'{texto2}\n')
        fid.write(f'{texto3}\n')
        fid.write(f'{texto4}\n')
        fid.write(f'{texto}\n')
        fid.write(f''' 
----- Dados de entrada-----  

    - Gerador : 100 MVA, 13,8 kV , Xs = j0,9 pu
    - Transformador 1 : 65 MVA, YNd7, 230/14 kV , Zt= 10%
    - Linha de Transmissão: Zlt = j150 Ohms
    - Transformador 2 : 40 MVA , YNd1, 242/10 kV, Zt = 8%
    - Carga: 60 MVA em 10 kV com FP 0,8 IND
    
-----Resultados-----
    - Componentes em PU nas bases {Sb/1000000:.0f} MVA e {Vb2/1000:.0f} kV na LT
        Tesão base Circuito 1 = {Vb1/1000:.0f} kV
        Tesão base Circuito 2 = {Vb2/1000:.0f} kV
        Tesão base Circuito 3 = {Vb3/1000:.0f} kV
        
        G1 = {Zg1_pu:.4f} pu
        T1 = {Zg1_pu:.4f} pu
        LT = {Zlt_pu:.4f} pu
        T2 = {Zt2_pu:.4f} pu

    Correntes no Circuito
    
    - Circuito 1
        Ia = {abs(Ia_c1):.4f}*e^(j{np.arctan((np.imag(Ia_c1))/(np.real(Ia_c1)))*180.0/np.pi:.2f}º)  pu
        Ib = {abs(Ib_c1):.4f}*e^(j{np.arctan((np.imag(Ib_c1))/(np.real(Ib_c1)))*180.0/np.pi:.2f}º)  pu
        Ic = {abs(Ic_c1):.4f}*e^(j{np.arctan((np.imag(Ic_c1))/(np.real(Ic_c1)))*180.0/np.pi:.2f}º)  pu
    
    - Circuito 2
        Ia = {abs(Ia_c2):.4f}*e^(j{np.arctan((np.imag(Ia_c2))/(np.real(Ia_c2)))*180.0/np.pi:.2f}º)  pu
        Ib = {abs(Ib_c2):.4f}*e^(j{np.arctan((np.imag(Ib_c2))/(np.real(Ib_c2)))*180.0/np.pi:.2f}º)  pu
        Ic = {abs(Ic_c2):.4f}*e^(j{np.arctan((np.imag(Ic_c2))/(np.real(Ic_c2)))*180.0/np.pi:.2f}º)  pu

    - Circuito 3
        Ia = {abs(Ia_c3):.4f}*e^(j{np.arctan((np.imag(Ia_c3))/(np.real(Ia_c3)))*180.0/np.pi:.2f}º)  pu
        Ib = {abs(Ib_c3):.4f}*e^(j{np.arctan((np.imag(Ib_c3))/(np.real(Ib_c3)))*180.0/np.pi:.2f}º)  pu
        Ic = {abs(Ic_c3):.4f}*e^(j{np.arctan((np.imag(Ic_c3))/(np.real(Ic_c3)))*180.0/np.pi:.2f}º)  pu
        ''')        
        