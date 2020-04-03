# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:42:13 2020

@author: Sebas
"""


def string_compressor(input_string: str):
        
        len_half = int((len(input_string) - len(input_string)%2)/2)

        
        i=0
        
        max_len =0
        max_index=0
        max_mult=1
         
        
        #abcabbaabba
        #i   j
        while i <=  len(input_string)-max_len:
            temp_max_len = 1
            temp_mult = 1
            j=min (len_half, len(input_string)-i)
            while j> 0:
                cur_mult =1
                if input_string[i:i+j] == input_string[i+j:i+j+j]:
                    while (i+(cur_mult+1)*j<= len(input_string) 
                           and input_string[i:i+j] == input_string[i+cur_mult*j:i+(cur_mult+1)*j]): 
                        cur_mult +=1
                    if j*cur_mult>= temp_max_len*temp_mult:
                        temp_max_len = j
                        temp_mult = cur_mult
                j -= 1
            if(temp_max_len*temp_mult >= max_len*max_mult):
                max_len = temp_max_len
                max_mult = temp_mult
                max_index = i
            i += 1
            
            #print(input_string[max_index:max_index+max_len])
            #print(max_mult)
            
        if max_len == 1 and max_mult ==1:
            return input_string
        else:
            output_string = string_compressor(input_string[0:max_index])
            if max_len ==1:
                output_string += (string_compressor(input_string[max_index:max_index+max_len])+
                                 power_escape(max_mult))
            else:
                 output_string += ("(" +string_compressor(input_string[max_index:max_index+max_len])+
                                   ")"+power_escape(max_mult))
            output_string +=string_compressor(input_string[max_index+max_len*max_mult:])
            return output_string

def power_escape(number: int):
    input_string= str(number)
    return input_string.replace("0", u'\u2070').replace("1",u'\u00B9').replace("2",u'\u00B2').replace("3", u'\u00B3').replace("4", u'\u2074').replace("5", u'\u2075').replace("6", u'\u2076').replace("7", u'\u2077').replace("8", u'\u2078').replace("9", u'\u2079')
            
            