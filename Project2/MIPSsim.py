#On my honor, I have neither given nor received unauthorized aid on this assignment


import sys
from collections import OrderedDict
from itertools import repeat

def Instruction_Fetch(inst_str,IF_count):
    Instructions["Executed"]=None
    global write_back 
    global inst_num
    if inst_str == 'BREAK':
        Instructions["Executed"] = 'BREAK'
        IF_count = 9999
        return IF_count
    if Instructions["Waiting"] != None and IF_count != 999: 
        dest, src1, base = get_operands(Instructions["Waiting"])
        raw_hazard = Check_RAW_Hazard(7, dest, src1, base)
        waw_hazard = Check_WAW_Hazard(7, dest, src1, base)
        war_hazard = Check_WAR_Hazard(7, dest, src1, base)
        if raw_hazard==False and waw_hazard == False and war_hazard ==False:
            Instructions["Executed"]=Instructions["Waiting"] 
            Instructions["Waiting"]=None 
            IF_count =0
        
    if (IF_count < 4 or IF_count == 999) and inst_str != None and IF_count<Empty_Buffer1_slots:
        if None in Buff_1.values():
            if inst_str[0:3] in ['BEQ','BNE'] or inst_str[0:4] == 'BGTZ' or inst_str[0:1]=='J':
                if inst_str[0]=='J':
                    Instructions["Executed"]=inst_str
                    IF_count = 887
                else:
                    dest, src1, src2 = get_operands(inst_str)
                    raw_hazard = Check_RAW_Hazard(7, dest, src1, src2)
                    waw_hazard = Check_WAW_Hazard(7, dest, src1, src2)
                    war_hazard = Check_WAR_Hazard(7, dest, src1, src2)
                    if raw_hazard==False and waw_hazard == False and war_hazard ==False:
                        Instructions["Executed"]=inst_str
                        return 4
                    else:
                        Instructions["Waiting"]=inst_str
                        IF_count = 776
            else:
                for key,value in Buff_1.items():
                    if value is None:
                        Buff_1[key] = inst_str
                        break
        IF_count+=1
    elif (IF_count < 4 or IF_count == 999) and inst_str != None and IF_count>=Empty_Buffer1_slots:
        inst_num -=1
        return 4
    return IF_count
    

def get_operands(inst_str):
    if inst_str != None:
        split_instruction = inst_str.split()
        for i in range(len(split_instruction)):
            split_instruction[i]=split_instruction[i].replace(",","")
        if 'ADD' in split_instruction or 'SUB' in split_instruction or 'AND' in split_instruction  or 'MUL' in split_instruction or 'OR' in split_instruction:
            dest = split_instruction[1]
            src1 = split_instruction[2]
            src2 = split_instruction[3]
            return dest,src1,src2
        elif 'ADDI' in split_instruction or 'SRL' in split_instruction or 'SRA' in split_instruction or 'ANDI' in split_instruction or 'ORI' in split_instruction:
            dest = split_instruction[1].replace(",","")
            src1 = split_instruction[2].replace(",","")
            src2 = None
            return dest, src1, src2
        elif 'J' in split_instruction:
            dest = None
            src1 = None
            src2 = None
            
        elif 'BNE' in split_instruction or 'BEQ' in split_instruction :
            src2 = split_instruction[2]
            dest = None
            src1 = split_instruction[1]
            return dest,src1,src2
        elif 'BGTZ' in split_instruction:
            src1 = split_instruction[1]
            src2 = None
            dest = None
            return dest,src1,src2
        elif 'SW' in split_instruction:
            for i in range(len(split_instruction)):
                    split_instruction[i]=split_instruction[i].replace(",","")
            src1 = split_instruction[1]  
            base_offset = split_instruction[2].split('(')
            offset = int(base_offset[0]) 
            base = reg_values[int(base_offset[1].replace("R","").replace(")",""))]
            eff_address = base + offset
            dest = base_offset[1].replace(")","")
            return dest, src1, eff_address
        elif 'LW' in split_instruction:
            for i in range(len(split_instruction)):
                    split_instruction[i]=split_instruction[i].replace(",","")
            dest = split_instruction[1]
            base_offset = split_instruction[2].split('(')
            offset = int(base_offset[0])
            base = reg_values[int(base_offset[1].replace("R","").replace(")",""))]
            eff_address = base + offset
            src1 = eff_address 
            src2 = base_offset[1].replace(")","") 
            return dest, src1, src2
        
    
def Check_WAW_Hazard(Buffer_1_key,dest,src1,src2):
    
        for key in range(Buffer_1_key-1,-1,-1):
            if Buff_1[key] != None:
                rd,rs,rt = get_operands(Buff_1[key])
                if rd == dest:
                    return True
        for key,value in Buff_2.items():
            if value != None and value != 'Curr':
                rd,rs,rt = get_operands(value)
                if rd == dest and dest != None:
                    return True
        for key,value in Buff_3.items():
            if value != None and value != 'Curr' and dest != None:
                rd,rs,rt = get_operands(value)
                if rd == dest:
                    return True
        for key,value in Buff_4.items():
            if value != None and value != 'Curr' and dest != None:
                rd,rs,rt = get_operands(value)
                if rd == dest:
                    return True
        if Buff_6 !=None:
            rd = Buff_6[1]
            if rd == dest and dest != None:
                        return True
        if Buff_7 !=None:
            rd,rs,rt = get_operands(Buff_7)
            if rd == dest:
                        return True
        if Buff_8 !=None:   
            rd,rs = Buff_8[0],Buff_8[1]
            if rd == dest and dest != None:
                        return True
        if Buff_9 !=None:
            rd,rs,rt = get_operands(Buff_9)
            if rd == dest and dest != None:
                        return True
        if Buff_10 !=None:
            rd = Buff_10[1]
            if rd == dest and dest != None:
                        return True
        if write_back!=None:
            for i in write_back:
                rd = i[1]
                if rd == dest and dest != None:
                        return True
        return False
            
def Check_WAR_Hazard(Buffer_1_key,dest,src1,src2):
    
        for key in range(Buffer_1_key-1,-1,-1):
            if Buff_1[key] != None:
                rd,rs,rt = get_operands(Buff_1[key])
                if (dest == rs or dest == rt) and dest != None :
                    return True
        return False

def Check_RAW_Hazard(Buffer_1_key,dest,src1,src2):
    
        for key in range(Buffer_1_key-1,-1,-1):
            if Buff_1[key] != None:
                rd,rs,rt = get_operands(Buff_1[key])
                if (rd == src1 or rd==src2) and rd != None:
                    return True
        for key,value in Buff_2.items():
            if value != None and value != 'Curr':
                rd,rs,rt = get_operands(value)
                if (rd == src1 or rd == src2) and rd != None:
                    return True
        for key,value in Buff_3.items():
            if value != None and value != 'Curr':
                rd,rs,rt = get_operands(value)
                if (rd == src1 or rd == src2) and rd != None:
                    return True
        for key,value in Buff_4.items():
            if value != None and value != 'Curr':
                rd,rs,rt = get_operands(value)
                if (rd == src1 or rd == src2) and rd != None:
                    return True
        if Buff_6 !=None:           
            rd = Buff_6[1]
            if (rd == src1 or rd == src2) and rd != None:
                        return True
        if Buff_7 !=None:
            rd,rs,rt = get_operands(Buff_7)
            if (rd == src1 or rd == src2) and rd != None:
                        return True
        if Buff_8 !=None:        
            rd = Buff_8[1]
            if (rd == src1 or rd == src2) and rd != None:
                        return True
        if Buff_9 !=None:
            rd,rs,rt = get_operands(Buff_9)
            if (rd == src1 or rd == src2) and rd != None:
                        return True
        if Buff_10 !=None:        
            rd = Buff_10[1]
            if (rd == src1 or rd == src2) and rd != None:
                        return True      
        if write_back!=None:
            for i in write_back:
                rd = i[1]
                if (rd == src1 or rd == src2) and rd != None:
                        return True
        
        return False
    
def append_buffer(inst_str,buff_type):
    if buff_type["Entry 0"]==None:
        buff_type["Entry 0"] = inst_str
    elif buff_type["Entry 1"]==None:
        buff_type["Entry 1"] = inst_str

def Structural_Hazard_Check(inst_str,buff_type): #size
    if None not in buff_type.values():
        str_hazard_status = True 
    elif None in buff_type.values():    
        str_hazard_status = False
    return str_hazard_status

def Update_buff_one(Buffer_1_key):
    Buff_1[Buffer_1_key] = None
    for key in range(Buffer_1_key,7,+1):
        Buff_1[key] = Buff_1[key+1]
        
    Buff_1[7] = None
       
def Instruction_Issue(): 
    global Empty_Buffer1_slots 
    Empty_Buffer1_slots = 8
    for key,value in Buff_1.items():
        if value != None:
            Empty_Buffer1_slots-=1

    IS_count=0
    entry_key=0
    while IS_count<6 and entry_key<8:
        if Buff_1[entry_key] != None :
            inst_str = Buff_1[entry_key]
            dest,src1,src2 = get_operands(inst_str)
            waw_hazard = Check_WAW_Hazard(entry_key,dest,src1,src2)
            war_hazard = Check_WAR_Hazard(entry_key,dest,src1,src2)
            raw_hazard = Check_RAW_Hazard(entry_key,dest,src1,src2)
            split_instruction = inst_str.split()
            instr_type = split_instruction[0]
            if (instr_type=="LW" or instr_type=="SW"):
                buff_type = Buff_2
            elif (instr_type=="ADD" or instr_type=="SUB" or instr_type=="AND" or instr_type=="OR" or instr_type=="SRL" or instr_type=="SRA" or instr_type=="ADDI" or instr_type=="ANDI" or instr_type=="ORI"):
                buff_type = Buff_3
            elif (instr_type=="MUL"):
                buff_type = Buff_4
            struct_hazard = Structural_Hazard_Check(inst_str,buff_type)
        
            if raw_hazard == False and waw_hazard == False and war_hazard == False and not struct_hazard:
               if  None in buff_type.values():
                    append_buffer(inst_str,buff_type)
                    Buff_1[entry_key]= None
                    Update_buff_one(entry_key)         
            else:
                entry_key+=1            
            IS_count+=1
        else:
            entry_key+=1  
    for buff_type in [Buff_2,Buff_3,Buff_4]:
        if buff_type["Entry 0"]=="Curr":
            buff_type["Entry 0"]=None
        if buff_type["Entry 1"]=="Curr":
            buff_type["Entry 1"]=None         
        
def ALU1_Exec(inst_str):
    dest, src1, src2 = get_operands(inst_str)
    split_instruction = inst_str.split()
    if split_instruction[0]=='SW':
        res = reg_values[int(src1.replace("R",""))]
        dest = data[src2]
        return [res,src2]  
    else:
        res = data[src1]
        return [res,dest.replace("'","")] 

def get_offset(inst_str):
    split_instruction = inst_str.split('#')
    offset = split_instruction[-1]
    return offset
    
def ALU2_Exec(inst_str):
    
    split_instruction = inst_str.split()
    dest,src1,src2 = get_operands(inst_str)
    if 'ADD' in split_instruction:
        res = reg_values[int(src1[1:])] + reg_values[int(src2[1:])]
    elif 'SUB' in split_instruction:
        res = reg_values[int(src1[1:])] - reg_values[int(src2[1:])]
    elif 'AND' in split_instruction:
        res = reg_values[int(src1[1:])] & reg_values[int(src2[1:])]
    elif 'OR' in split_instruction:
        res = reg_values[int(src1[1:])] | reg_values[int(src2[1:])]
    elif 'SRL' in split_instruction:
        offset = get_offset(inst_str)
        res = (reg_values[int(src1[1:])] % 0x100000000) >> int(offset)     
    elif 'SRA' in split_instruction:
        offset = get_offset(inst_str)
        res = reg_values[int(src1[1:])] >> int(offset)
    elif 'ADDI' in split_instruction:
        offset = get_offset(inst_str)
        res = reg_values[int(src1[1:])] + int(offset)
    elif 'ANDI' in split_instruction:
        offset = get_offset(inst_str)
        res = reg_values[int(src1[1:])] & int(offset)
    elif 'ORI' in split_instruction:
        offset = get_offset(inst_str)
        res = reg_values[int(src1[1:])] | int(offset)
    return [res,dest.replace("'","")]

def Exec_MUL(inst_str):
    dest,src1,src2 = get_operands(inst_str)
    res = reg_values[int(src1[1:])]*reg_values[int(src2[1:])]
    return [res,dest.replace("'","")]

def Execution():
    global Buff_8, Buff_5, Mem, Buff_10, Buff_5_val, Buff_9, Buff_7,Buff_6
 
    if Buff_5 is not None:
        instr_type = Buff_5.split()
        instr_type = instr_type[0]
        
        if instr_type == 'LW':
            Buff_8 = Buff_5_val
            Buff_5_val = None
            Buff_5 = None
        if instr_type == 'SW':
            eff_address = Buff_5_val[1]
            val = Buff_5_val[0]
            data[eff_address] = val    
            Buff_5_val = None
            Buff_5 = None
             
    if Buff_2["Entry 0"] is not None:
        Result = ALU1_Exec(Buff_2["Entry 0"]) 
        Buff_5 = Buff_2["Entry 0"]
        if Buff_2["Entry 1"] != "Curr":
            Buff_2["Entry 0"] = Buff_2["Entry 1"]
            Buff_2["Entry 1"] = "Curr"
        else:
            Buff_2["Entry 0"] = None
        Buff_5_val = Result
        
    if Buff_3["Entry 0"] is not None:
        Result = ALU2_Exec(Buff_3["Entry 0"])
        if Buff_3["Entry 1"] != "Curr":
            Buff_3["Entry 0"] = Buff_3["Entry 1"]
            Buff_3["Entry 1"] = "Curr"
        else:
            Buff_3["Entry 0"] = None
        Buff_6 = Result
    
    if (Buff_9 != Buff_4["Entry 0"])  and Buff_9 != None:
        Buff_10 = Exec_MUL(Buff_9)
        Buff_9 = None
        
    if (Buff_7 != Buff_4["Entry 0"]) and Buff_7 != None :
        Buff_9 = Buff_7 
        Buff_7 = None
        
    if (Buff_4["Entry 0"] is not None):
        Buff_7 = Buff_4["Entry 0"] 
        Buff_4["Entry 0"] = Buff_4["Entry 1"]
        Buff_4["Entry 1"] = "Curr" 
    
def Write_Back():
    global Buff_8, Buff_6, Buff_10
    WB_Count = 0
    if WB_Count<3:
        if Buff_8 is not None:
            dest = Buff_8[1]
            val = Buff_8[0]
            reg_values[int(dest[1:])]= val
            write_back.append(Buff_8)
            Buff_8 = None
            WB_Count+=1
            
        if Buff_6 is not None:
            src = Buff_6[0]
            dest = Buff_6[1]
            reg_values[int(dest[1:])]= src
            write_back.append(Buff_6)
            Buff_6 = None
            WB_Count+=1
        if Buff_10 is not None:
            res = Buff_10[0]
            dest = Buff_10[1]
            reg_values[int(dest[1:])]= res
            write_back.append(Buff_10)
            Buff_10 = None
            WB_Count+=1
            
def print_LW_SW(line,instr_address,instruction_name,offset):
    inst_str=str(instruction_name)+" R"+str(int(line[11:16],2))+", "+str(offset)+"(R"+str(int(line[6:11],2))+")"
    return inst_str
    
def print_BGTZ(line,instr_address,instr_address_new):
    inst_str="BGTZ"+" R"+str(int(line[6:11],2))+", #"+str(instr_address_new)
    return inst_str

def print_J(line,instr_address,instr_address_new):
    inst_str="J"+" #"+str(instr_address_new)
    return inst_str

def print_cat_three_instruct(line,instr_address,instruction_name,imm_val):
    inst_str = str(instruction_name)+" R"+str(int(line[6:11],2))+", R"+str(int(line[11:16],2))+", #"+str(imm_val)
    return inst_str
    
def print_cat_two_instruct(line,instr_address,instruction_name):
    inst_str=str(instruction_name)+" R"+str(int(line[6:11],2))+", R"+str(int(line[11:16],2))+", R"+str(int(line[16:21],2))
    return inst_str
    
def print_cat_one_instruct(line,instr_address,instruction_name,offset):
    inst_str=str(instruction_name)+" R"+str(int(line[6:11],2))+", R"+str(int(line[11:16],2))+", #"+str(offset)
    return inst_str

def get_twos_complement(stri):

    return -int(stri[0]) << len(stri) | int(stri, 2)

def ADD(line,instr_address):

        inst_str=print_cat_two_instruct(line,instr_address,"ADD")
        reg_values[int(line[6:11],2)] = reg_values[int(line[11:16],2)] + reg_values[int(line[16:21],2)]
        return inst_str
   
def SUB(line,instr_address):

        inst_str=print_cat_two_instruct(line,instr_address,"SUB")
        reg_values[int(line[6:11],2)] =   reg_values[int(line[11:16],2)] - reg_values[int(line[16:21],2)]
        return inst_str         
        
def and_instr(line,instr_address):

        inst_str=print_cat_two_instruct(line,instr_address,"AND")
        reg_values[int(line[6:11],2)] = reg_values[int(line[11:16],2)] & reg_values[int(line[16:21],2)] 
        return inst_str
        
def or_instr(line,instr_address):

        inst_str=print_cat_two_instruct(line,instr_address,"OR")
        reg_values[int(line[6:11],2)] = reg_values[int(line[11:16],2)] | reg_values[int(line[16:21],2)]
        return inst_str
        
def shift_right_logical(line,instr_address):
        src1 = reg_values[int(line[11:16],2)]
        src2 = int(line[16:21],2)
        inst_str=print_cat_three_instruct(line,instr_address,"SRL",src2)
        reg_values[int(line[6:11],2)] =  (src1 % 0x100000000) >> src2
        return inst_str
        
def shift_right_arithmetic(line,instr_address):
        
        src1 = reg_values[int(line[11:16],2)]
        src2 = int(line[16:21],2)
        inst_str=print_cat_three_instruct(line,instr_address,"SRA",src2)
        reg_values[int(line[6:11],2)] = src1 >> src2
        return inst_str
        
def MUL(line,instr_address):
        src1 = reg_values[int(line[11:16],2)]
        src2 = reg_values[int(line[16:21],2)]
        inst_str=print_cat_two_instruct(line,instr_address,"MUL")
        reg_values[int(line[6:11],2)]= src1*src2
        return inst_str
        
def ADDI(line,instr_address):
            src1 = reg_values[int(line[11:16],2)]
            imm_val = (line[16:])
            if line[16]=='1':
                imm_val = get_twos_complement(imm_val)
            else: 
                imm_val = int(imm_val,2)

            inst_str=print_cat_three_instruct(line, instr_address, "ADDI",imm_val) 
            reg_values[int(line[6:11],2)] = src1 + imm_val
            return inst_str
            
def ANDI(line,instr_address):
        src1 = reg_values[int(line[11:16],2)]
        imm_val = (line[16:])
        imm_val = int(imm_val,2)
        inst_str=print_cat_three_instruct(line, instr_address, "ANDI",imm_val)
        reg_values[int(line[6:11],2)] = src1 & imm_val
        return inst_str
        
def ORI(line,instr_address):
        src1 = reg_values[int(line[11:16],2)]
        imm_val = (line[16:])

        imm_val = int(imm_val,2) 
        inst_str=print_cat_three_instruct(line, instr_address, "ORI",imm_val)
        reg_values[int(line[6:11],2)] = src1 | imm_val
        return inst_str
 
#CATEGORY_ONE
         
def J(line,instr_address,line_no):
   
    target = line[6:32]+"00"
    count_next =instr_address+4 
    count_next = '{:032b}'.format(count_next)
    MSB_4 = count_next[:4]
    target = MSB_4+target
    instr_address_new= (int(target,2))
    inst_str=print_J(line,instr_address,instr_address_new)
    line_no = ((instr_address_new-260)/4)
    return inst_str,line_no,instr_address_new
    
    
def BEQ(line,instr_address,line_no): 
        target = line[16:32]+"00" 
        count_next =instr_address+4 
        count_next = '{:032b}'.format(count_next)
        pc= instr_address+4
        MSB_14 = count_next[:14]
        target = MSB_14+target
        offset = get_twos_complement(target[16:32])
        inst_str=print_cat_one_instruct(line,instr_address,"BEQ",offset)  
        if reg_values[int(line[6:11],2)] == reg_values[int(line[11:16],2)]:
            instr_address_new = pc + offset
            line_no = ((instr_address_new-260)/4)
        else:
            instr_address_new=instr_address
        
        return inst_str,line_no,instr_address_new
   
def BNE(line,instr_address,line_no):
        target = line[16:32]+"00" 
        count_next =instr_address+4 
        pc= instr_address+4
        count_next = '{:032b}'.format(count_next)
        MSB_14 = count_next[:14]
        target = MSB_14+target
        offset = get_twos_complement(target[16:32])
        inst_str=print_cat_one_instruct(line,instr_address,"BNE",offset) 
        
        if reg_values[int(line[6:11],2)] != reg_values[int(line[11:16],2)]:
            instr_address_new = pc + offset 
            line_no = ((instr_address_new-260)/4)
        else:
            instr_address_new=instr_address
        return inst_str,line_no,instr_address_new
    
def BGTZ(line,instr_address,line_no):
    val = reg_values[int(line[6:11],2)]
    zero =reg_values[int(line[11:16],2)]
    pc= instr_address+4
    target = line[16:32]+"00" 
    count_next =instr_address+4 
    count_next = '{:032b}'.format(count_next)
    MSB_14 = count_next[:14]
    target = MSB_14+target
    offset = get_twos_complement(target[16:32])
    inst_str = print_BGTZ(line,instr_address,offset)  
    if val>zero:
        instr_address_new = pc +offset #####
        line_no = ((instr_address_new-260)/4)
    else:
        instr_address_new=instr_address
    return inst_str,line_no,instr_address_new
    
def SW(line,instr_address):
    base = reg_values[int(line[6:11],2)]
    src = reg_values[int(line[11:16],2)]
    offset = get_twos_complement(line[16:32])
    eff_address = base + offset
    data[eff_address] = src
    inst_str=print_LW_SW(line,instr_address,"SW",offset)
    return inst_str
        
def LW(line,instr_address):
    base = reg_values[int(line[6:11],2)]
    offset = get_twos_complement(line[16:32])
    inst_str=print_LW_SW(line,instr_address,"LW",offset)
    eff_address = base + offset #bug
    reg_values[int(line[11:16],2)] = data[eff_address] 
    return inst_str
     
def BREAK(line,instr_address):
    inst_str="BREAK"
    return inst_str

def first_category(line,instr_address,line_no):
    
    if line[3:6] =='000':
        inst_str,line_no,instr_address_new = J(line,instr_address,line_no)
        return inst_str,line_no,instr_address_new
    elif line[3:6] == '001':
        inst_str,line_no,instr_address_new=BEQ(line,instr_address,line_no)
        return inst_str,line_no,instr_address_new
    elif line[3:6] == '010':
        inst_str,line_no,instr_address_new=BNE(line,instr_address,line_no)
        return inst_str,line_no,instr_address_new
    elif line[3:6] == '011':
        inst_str,line_no,instr_address_new=BGTZ(line,instr_address,line_no)
        return inst_str,line_no,instr_address_new
    elif line[3:6] == '100':
        inst_str=SW(line,instr_address)
        return inst_str,line_no,instr_address
    elif line[3:6] == '101':
        inst_str=LW(line,instr_address)
        return inst_str,line_no,instr_address
    
def second_category(line,instr_address):
    if line[3:6]=='000':
        inst_str=ADD(line,instr_address)
        return inst_str
    elif line[3:6]=='001':
        inst_str=SUB(line,instr_address)
        return inst_str
    elif line[3:6]=='010':
        #and
        inst_str=and_instr(line,instr_address)
        return inst_str
    elif line[3:6]=='011':
        #or
        inst_str=or_instr(line,instr_address)
        return inst_str
    elif line[3:6]=='100':
        #srl
        inst_str=shift_right_logical(line,instr_address)
        return inst_str
    elif line[3:6]=='101':
        #sra
        inst_str=shift_right_arithmetic(line,instr_address)
        return inst_str
    elif line[3:6]=='110':
        #mul
        inst_str=MUL(line,instr_address)
        return inst_str

def third_category(line,instr_address):
    if line[3:6] == '000':
        inst_str = ADDI(line,instr_address) 
        return inst_str
    elif line[3:6] == '001':
        inst_str = ANDI(line,instr_address)
        return inst_str
    elif line[3:6] == '010':
        inst_str = ORI(line,instr_address)
        return inst_str        

filename = sys.argv[1]


file = open("simulation.txt","w+")
file.truncate(0)
file.close()

given_value = 0
reg_values=[]
data ={}
reg_values.extend(repeat(given_value,32))

with open(filename) as f:
    line_list = f.readlines()
    line = line_list[0]
    line = line.strip()
    instr_address = 260
    instr_address_new = instr_address
    flag = 'Y'
    cycle_num=1
    line_no=0
    count_instr=0
    for i in line_list:
        
        if i.strip() == '00011000000000000000000000000000':
            count_instr+=1
            break
        else:
            count_instr+=1
    data_val= (count_instr*4)+260
    start_addr = data_val
    data = {}
    for d in range(0,len(line_list)-count_instr):
        data[data_val]=get_twos_complement(line_list[count_instr].strip())
        data_val+=4
        count_instr+=1
    data_dup = data.copy()
    instr_list = []
    while line:
        
        if flag=='Y':
            if line[0:3] == '000' :
                if line[3:6] == '110':
                    inst_str=BREAK(line,instr_address)
                    instr_list.append(inst_str)
                    instr_address = instr_address+4
                    flag = 'N'
                    line_no=line_no+1
                    
                    for x in range(int(line_no),len(line_list)):
                        line_after_break= line_list[int(x)].strip()
                        num = get_twos_complement(line_after_break)
                        instr_address += 4
                    break
                
                inst_str,line_no_new,instr_address_new = first_category(line,instr_address,line_no)
                
                instr_list.append(inst_str)
                
                if instr_address == instr_address_new:
                    instr_address += 4
                else:
                    instr_address = instr_address_new
                if line_no_new == line_no:
                    line_no+=1
                else:
                    line_no = line_no_new
                
                
            elif line[0:3] =='001':
               inst_str = second_category(line,instr_address)
               line_no+=1
               instr_list.append(inst_str)
               instr_address += 4
               
               
            elif line[0:3] =='010':
                inst_str = third_category(line,instr_address)
                line_no+=1
                instr_list.append(inst_str)
                instr_address += 4
 
            line = line_list[int(line_no)]
            line = line.strip()
            
            cycle_num+=1

        
f.close()

   
for i in range(0,len(reg_values)):
    reg_values[i] = 0

data = data_dup.copy()

Instructions = { "Waiting" : None, "Executed" : None}

Buff_1 = OrderedDict()

Buff_1 = {
     0: None
    ,1: None
    ,2: None
    ,3: None
    ,4: None
    ,5: None
    ,6: None
    ,7: None
    }
Buff_2 = {
    "Entry 0": None
    ,"Entry 1": None
    }

Buff_3 = {
    "Entry 0": None
    ,"Entry 1": None
    }


Buff_4 = {
    "Entry 0": None
    ,"Entry 1": None
    }

Buff_5 = None
Buff_6 = None
Buff_7 = None
Buff_8 = None
Buff_9 = None
Buff_10 = None
Mem = None

Buff_5_val = None

ALU1 = None #Address calculation for load and store
ALU2 = None # ADD, SUB, AND, OR, SRL, SRA, ADDI, ANDI, and ORI
MUL1 = None 
MUL2 = None 
MUL3 = None 
write_back=[]
Empty_Buffer1_slots = 8

IF_count = 0
Clock_cyc = 1
i=instr_list[0]
inst_num =0
while IF_count!= 9999:

    Write_Back()
    Execution()
    Instruction_Issue()
    
    for i in range(inst_num,len(instr_list)):
        if IF_count <4 and IF_count != 999 and IF_count != 777:
            IF_count = Instruction_Fetch(instr_list[i],IF_count)
            i+=1
            inst_num+=1
        else:
            break
    if IF_count == 4:
        IF_count = 0
    if IF_count == 777:
        IF_count = Instruction_Fetch(None,IF_count)
    if IF_count == 888:
        IF_count = 0
        
    inputFile = open('simulation.txt', 'a')
    
    print("--------------------",file = inputFile)
    print("Cycle "+str(Clock_cyc)+":",file = inputFile)
    print(file = inputFile)
    print("IF:",file = inputFile)
    if Instructions["Waiting"]==None:
        print("\tWaiting:",file = inputFile)
    else:
        print("\tWaiting: ["+str(Instructions["Waiting"])+"]",file = inputFile)
    
    if Instructions["Executed"]==None:
        print("\tExecuted:",file = inputFile)
    else:
        print("\tExecuted: ["+str(Instructions["Executed"])+"]",file = inputFile)
    
    print("Buf1:",file = inputFile)
    for i in Buff_1:
        if Buff_1[i] is None:
            print("\tEntry "+str(i)+":",file = inputFile)   
        else:
            print("\tEntry "+str(i)+": ["+str(Buff_1[i])+"]",file = inputFile)
        
    
    print("Buf2:",file = inputFile)
    for i in Buff_2:
        if Buff_2[i] is None or Buff_2[i] == "Curr" :
            print("\t"+str(i)+":",file = inputFile)    
        else:
            print("\t"+str(i)+": ["+str(Buff_2[i])+"]",file = inputFile)
        
    print("Buf3:",file = inputFile)
    for i in Buff_3:
        if Buff_3[i] is None or Buff_3[i] == "Curr" :
            print("\t"+str(i)+":",file = inputFile)    
        else:
            print("\t"+str(i)+": ["+str(Buff_3[i])+"]",file = inputFile)
        
    print("Buf4:",file = inputFile)
    for i in Buff_4:
        if Buff_4[i] is None or Buff_4[i] == "Curr" :
            print("\t"+str(i)+":",file = inputFile)    
        else:
            print("\t"+str(i)+": ["+str(Buff_4[i])+"]",file = inputFile)
    
    if Buff_5 is None:
        print("Buf5:",file = inputFile)
    else:
        print("Buf5: ["+str(Buff_5)+"]",file = inputFile)
    
    if Buff_6 is None:
        print("Buf6:",file = inputFile)
    else:
        print("Buf6: ["+str(Buff_6[0])+", "+str(Buff_6[1])+"]",file = inputFile)
        
    if Buff_7 is None:
        print("Buf7:",file = inputFile)
    else:
        print("Buf7: ["+str(Buff_7)+"]",file = inputFile)
        
    if Buff_8 is None:
        print("Buf8:",file = inputFile)
    else:
        print("Buf8: ["+str(Buff_8[0])+", "+str(Buff_8[1])+"]",file = inputFile)
        
    if Buff_9 is None:
        print("Buf9:",file = inputFile)
    else:
        print("Buf9: ["+str(Buff_9)+"]",file = inputFile)
        
    if Buff_10 is None:
        print("Buf10:",file = inputFile)
    else:
        print("Buf10: ["+str(Buff_10[0])+", "+str(Buff_10[1])+"]",file = inputFile)
    
    print(file = inputFile)
    print("Registers",file = inputFile)
    print("R00:\t"+str(reg_values[0])+"\t"+str(reg_values[1])+"\t"+str(reg_values[2])+"\t"+str(reg_values[3])+"\t"+str(reg_values[4])+"\t"+str(reg_values[5])+"\t"+str(reg_values[6])+"\t"+str(reg_values[7]),file = inputFile)
    print("R08:\t"+str(reg_values[8])+"\t"+str(reg_values[9])+"\t"+str(reg_values[10])+"\t"+str(reg_values[11])+"\t"+str(reg_values[12])+"\t"+str(reg_values[13])+"\t"+str(reg_values[14])+"\t"+str(reg_values[15]),file = inputFile)
    print("R16:\t"+str(reg_values[16])+"\t"+str(reg_values[17])+"\t"+str(reg_values[18])+"\t"+str(reg_values[19])+"\t"+str(reg_values[20])+"\t"+str(reg_values[21])+"\t"+str(reg_values[22])+"\t"+str(reg_values[23]),file = inputFile)
    print("R24:\t"+str(reg_values[24])+"\t"+str(reg_values[25])+"\t"+str(reg_values[26])+"\t"+str(reg_values[27])+"\t"+str(reg_values[28])+"\t"+str(reg_values[29])+"\t"+str(reg_values[30])+"\t"+str(reg_values[31]),file = inputFile)
    print(file = inputFile)
    print("Data",file = inputFile)
    data_count = 0
    data_cnt=0
    for i in data:
        if data_count == 0  :
            print(str(start_addr+(data_cnt*4))+":",end='\t',file = inputFile)
        if data_count == 7:
            print(data[i],file = inputFile)
            data_count=0
            data_cnt+=1
            
        else:
            print(data[i],end='\t',file = inputFile)
            data_count+=1
            data_cnt+=1
    inputFile.close()
    write_back=[]
    Clock_cyc+=1 
      
              
            
            
            

        

        
