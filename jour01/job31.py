print("JOB 31 ###################################################################################################################")

mot = input('Entrez un mot: ')

have_upper = False
for ele in mot:
    if ele.isupper():
        have_upper = True
        break
    
if not mot.isalpha() or have_upper:
    print('Erreur: Le mot doit contenir seulement des lettres de l\'alphabet, toutes en minuscules, et aucun autre charactère!')
else:
    lettres = list(mot)
    result = lettres
    
    if (sorted(lettres, reverse=True) != lettres):
        lettres_triees = sorted(lettres)
    
        letter_toswitch_index = -1
        switched_letter_index = -2
        
        while (lettres_triees.index(lettres[letter_toswitch_index]) <= lettres_triees.index(lettres[switched_letter_index])):
            switched_letter_index -= 1
            if switched_letter_index < -len(lettres):
                letter_toswitch_index -= 1
                switched_letter_index = letter_toswitch_index - 1
        
        result[letter_toswitch_index], result[switched_letter_index] = result[switched_letter_index], result[letter_toswitch_index]
        
        result = result[0:switched_letter_index+1] + sorted(result[switched_letter_index+1:])
        
    print(f'Le nouveau mot est: {"".join(result)}')
    