

"""msg = 'Su nombre es: \nLeonardo Gonzalez Gutierrez'
f = open ('../Information/summaryAnswer.txt','w')
f.write(msg)
f.close()
"""

initDialog = True
while initDialog:
    print('-------------------------------------------------------')
    print("Inicio de procesamiento. \n********* Seleccione los modelos de predicción *********")
    print("CNN (y/n)")
    cnn = input()
    print("RestNet50 (y/n)")
    resnt = input()
    print("MobileNet (y/n)")
    mobil = input()

    if cnn in 'n' and resnt in 'n' and mobil in 'n':
        print('###### Por favor seleccione al menos un modelo ######')
        initDialog = True
    else:

        print('###### Modelos seleccionados ######')
        if cnn in 'y':
            # add model
            print('CNN')
        if resnt in 'y':
            print('RestNet50')
        if mobil in 'y':
            print('MobileNet')

        print('###### Confirmar envio (y/n) ######')
        proces = input()
        if proces in 'y':
            print('Iniciando procesamiento...')

            print('#####################################')
            initDialog = False
        else:
            print('Proceso finalizado')
            initDialog = True #Change

            print('-------------------------------------------------------')
            #Clear data to answer


