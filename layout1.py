import PySimpleGUI as psg

def App_GUI_A():
    psg.theme('TealMono')
    #define layout
    layoutA=[[psg.Text('Velg område', size=(20, 1), font='Lucida', justification='left')],
           [psg.Radio('Ålesund (3)', 'area', key ='10YNO-3--------J'),
            psg.Radio('Oslo (1)', 'area',     key='10YNO-1--------2'),
            psg.Radio('Arendal (2)', 'area',  key='10YNO-2--------T'),
            psg.Radio('Narvik (4)', 'area',   key='10YNO-4--------9'),
            psg.Radio('Bergen (5)', 'area',   key='10Y1001A1001A48H')],
           [psg.Text('Velg år', size=(20, 1), font='Lucida', justification='left')],
           [psg.Radio('2021', 'aar', key='2021'),
            psg.Radio('2020', 'aar', key='2020'),
            psg.Radio('2019', 'aar', key='2019'),
            psg.Radio('2018', 'aar', key='2018'),
            psg.Radio('2017', 'aar', key='2017'),
            psg.Radio('2016', 'aar', key='2016')],
           [psg.Text('Velg uke',size=(20, 1), font='Lucida', justification='left')],
           [psg.InputText(size=(10))],
           [psg.Button('Vis priser', font=('Times New Roman',14)), psg.Button('Glem det', font=('Times New Roman',14))]]
    #Define Window
    win =psg.Window('Hent strømpriser',layoutA)
    e,v=win.read()
    win.close()
    u_a = []
    for val in v:
      if win.find_element(val).get()==True:
            u_a.append(val)
    u_a.append(v[0])
    return u_a


def App_GUI_B():
    psg.theme('SandyBeach')
    #define layout
    layoutb=[[psg.Text('Velg område', size=20, font='Lucida', justification='left')],
           [psg.Radio('Ålesund (3)', 'area',   key='10YNO-3--------J'),
            psg.Radio('Oslo (1)',    'area',   key='10YNO-1--------2'),
            psg.Radio('Arendal (2)', 'area',   key='10YNO-2--------T'),
            psg.Radio('Narvik (4)',  'area',   key='10YNO-4--------9'),
            psg.Radio('Bergen (5)',  'area',   key='10Y1001A1001A48H')],
           [psg.Text('Velg år', size=20, font='Lucida', justification='left')],
           [psg.Radio('2022', 'aar', key='2022'),
            psg.Radio('2021', 'aar', key='2021'),
            psg.Radio('2020', 'aar', key='2020'),
            psg.Radio('2019', 'aar', key='2019'),
            psg.Radio('2018', 'aar', key='2018'),
            psg.Radio('2017', 'aar', key='2017'),
            psg.Radio('2016', 'aar', key='2016')],
           [psg.Text('Uke   eller', size=7, font='Lucida', justification='left'),
            psg.Text('Måned nr:',   size=8, font='Lucida', justification='left')],
           [psg.InputText(size=10, default_text = '0'), psg.InputText(size=10, default_text = '0'),
            psg.Radio('De nærmeste dager', 'aar', key='dagens')],
           [psg.Button('Vis priser', font=('Times New Roman',14)),
            psg.Button('Glem det', font=('Times New Roman',14))]]
    #Define Window
    win =psg.Window('Hent strømpriser', layoutb)

    e, v = win.read()
    win.close()
    u_a = []
    u_a.append(v[0]) # Uke nr
    u_a.append(v[1]) # Mnd nr

    for val in v:
        #print(v)
        if win.find_element(val).get()==True:
            u_a.append(val) # område, år, dagens

    #print(len(v))
    return u_a