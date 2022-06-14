import java.io.*;
import java.util.*;


public class MIPSsim {

    public static void main(String[] args) {

        final String inputFile = args[0];
        final String outputFile1 = "disassembly.txt";
        final String outputFile2 = "simulation.txt";

        Category category = new Category();
        Map<String,List<?>> mapList = translateInstructions(inputFile,category);

        List<String> disassemblyList = (List<String>) mapList.get("disassemblyList");
        final int startAddr = 260;
        List<String> simulationList = execInstruction(mapList,startAddr);

        try {
            if(createFile(new File(outputFile1))){
                writeFile(disassemblyList, outputFile1);
                System.out.println("Created file disassembly.txt at: " + new File(outputFile1).getCanonicalPath());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {
            if(createFile(new File(outputFile2))){
                writeFile(simulationList, outputFile2);
                System.out.println("Created file simulation.txt at: " + new File(outputFile2).getCanonicalPath());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public static class Category{
        private Map<String, String> categorySet;
        private Map<String, String> c1;
        private Map<String, String> c2;
        private Map<String, String> c3;
        public Category(){
            Map<String,String> CategorySet = new HashMap<>();
            Map<String,String> C1 = new HashMap<>();
            Map<String,String> C2 = new HashMap<>();
            Map<String,String> C3 = new HashMap<>();
            CategorySet.put("Category1", "000");
            CategorySet.put("Category2", "001");
            CategorySet.put("Category3", "010");
            C1.put("J","000");
            C1.put("BEQ","001");
            C1.put("BNE","010");
            C1.put("BGTZ","011");
            C1.put("SW","100");
            C1.put("LW","101");
            C1.put("BREAK","110");
            C2.put("ADD","000");
            C2.put("SUB","001");
            C2.put("AND","010");
            C2.put("OR","011");
            C2.put("SRL","100");
            C2.put("SRA","101");
            C2.put("MUL","110");
            C3.put("ADDI","000");
            C3.put("ANDI","001");
            C3.put("ORI","010");
            setC1(C1);
            setC2(C2);
            setC3(C3);
            setCategorySet(CategorySet);
        }

        public void setCategorySet(Map<String, String> categorySet) {
            this.categorySet = categorySet;
        }

        public void setC1(Map<String, String> c1) {
            this.c1 = c1;
        }

        public void setC2(Map<String, String> c2) {
            this.c2 = c2;
        }

        public void setC3(Map<String, String> c3) {
            this.c3 = c3;
        }
    }

    public static class Command {

        private String instruction;
        private int address;
        private int rd;
        private int rs;
        private int rt;
        private int immediate;
        private int offset;
        private int base;
        private int target;
        private String disassembl;

        public void setBinary() {
        }
        public String getDisassembl() {
            return disassembl;
        }
        public void setDisassembl(String disassembl) {
            this.disassembl = disassembl;
        }
        public String getInstruction() {
            return instruction;
        }
        public void setInstruction(String instruction) {
            this.instruction = instruction;
        }
        public int getAddress() {
            return address;
        }
        public void setAddress(int address) {
            this.address = address;
        }
        public int getRd() {
            return rd;
        }
        public void setRd(int rd) {
            this.rd = rd;
        }
        public int getRs() {
            return rs;
        }
        public void setRs(int rs) {
            this.rs = rs;
        }
        public int getRt() {
            return rt;
        }
        public void setRt(int rt) {
            this.rt = rt;
        }
        public int getImmediate() {
            return immediate;
        }
        public void setImmediate(int immediate) {
            this.immediate = immediate;
        }
        public int getOffset() {
            return offset;
        }
        public void setOffset(int offset) {
            this.offset = offset;
        }
        public int getBase() {
            return base;
        }
        public void setBase(int base) {
            this.base = base;
        }
        public int getTarget() {
            return target;
        }
        public void setTarget(int target) {
            this.target = target;
        }
    }
    //Method to translate instructions
    public static Map<String,List<?>> translateInstructions(String inputFileName, Category category){
        final int startAddr = 260;
        boolean isBreak = false;
        int address = startAddr;
        Map<String,List<?>> MapList = new HashMap<>();
        List<String> disassemblyList = new ArrayList<>();
        List<Integer> dataList = new ArrayList<>();
        List<Command> disassemblers = new ArrayList<>();
        List<String> instructionList = readFile(inputFileName);
        List<Integer> registerValueList = new ArrayList<>();
        for(int k = 0; k < 32; k++){
            registerValueList.add(0);
        }
        for (String instruction : instructionList) {
            String out = "";
            if (!isBreak) {
                Command disassemb = new Command();
                String categoryType = null;
                String temp = "";
                String opcode;
                String first3Bits = instruction.substring(0, 3);
                String offsetStr = instruction.substring(instruction.length() - 16);
                int immediate = calculateVal(offsetStr);
                int offset = Integer.parseInt(offsetStr, 2);
                int base = Integer.parseInt(instruction.substring(6, 11), 2);
                int rs, rt, rd;
                if (first3Bits.equals(category.categorySet.get("Category1"))) {
                    opcode = instruction.substring(3, 6);
                    if (opcode.equals(category.c1.get("J"))) {
                        String targetStr = instruction.substring(instruction.length() - 26);
                        int target = Integer.parseInt(targetStr + "00", 2);
                        categoryType = "J";
                        temp = "J" + " #" + target;
                        disassemb.setTarget(target);
                    } else if (opcode.equals(category.c1.get("BEQ"))) {
                        rs = Integer.parseInt(instruction.substring(6, 11), 2);
                        rt = Integer.parseInt(instruction.substring(11, 16), 2);
                        offset = calculateVal(offsetStr + "00");
                        categoryType = "BEQ";
                        temp = "BEQ" + " R" + rs + "," + " R" + rt + "," + " #" + offset;
                        disassemb.setOffset(offset);
                        disassemb.setRs(rs);
                        disassemb.setRt(rt);
                    } else if (opcode.equals(category.c1.get("BNE"))) {
                        rs = Integer.parseInt(instruction.substring(6, 11), 2);
                        rt = Integer.parseInt(instruction.substring(11, 16), 2);
                        offset = calculateVal(offsetStr + "00");
                        categoryType = "BNE";
                        temp = "BNE" + " R" + rs + "," + " R" + rt + "," + " #" + offset;
                        disassemb.setOffset(offset);
                        disassemb.setRs(rs);
                        disassemb.setRt(rt);
                    }else if (opcode.equals(category.c1.get("BGTZ"))) {
                        rs = Integer.parseInt(instruction.substring(6, 11), 2);
                        offset = calculateVal(offsetStr + "00");
                        categoryType = "BGTZ";
                        temp = "BGTZ" + " R" + rs + "," + " #" + offset;
                        disassemb.setOffset(offset);
                        disassemb.setRs(rs);
                    } else if (opcode.equals(category.c1.get("BREAK"))) {
                        temp = "BREAK";
                        categoryType = "BREAK";
                        isBreak = true;
                    } else if (opcode.equals(category.c1.get("SW"))) {
                        categoryType = "SW";
                        rt = Integer.parseInt(instruction.substring(11, 16), 2);
                        temp = "SW" + " R" + rt + "," + " " + offset + "(R" + base + ")";
                        disassemb.setOffset(offset);
                        disassemb.setBase(base);
                        disassemb.setRt(rt);
                    } else if (opcode.equals(category.c1.get("LW"))) {
                        categoryType = "LW";
                        rt = Integer.parseInt(instruction.substring(11, 16), 2);
                        temp = "LW" + " R" + rt + "," + " " + offset + "(R" + base + ")";
                        disassemb.setOffset(offset);
                        disassemb.setBase(base);
                        disassemb.setRt(rt);
                    }
                } else if (first3Bits.equals(category.categorySet.get("Category2"))) {
                    opcode = instruction.substring(3, 6);
                    rd = Integer.parseInt(instruction.substring(6, 11), 2);
                    rs = Integer.parseInt(instruction.substring(11, 16), 2);
                    rt = Integer.parseInt(instruction.substring(16, 21), 2);
                    if (opcode.equals(category.c2.get("ADD"))) {
                        categoryType = "ADD";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " R" + rt;
                    } else if (opcode.equals(category.c2.get("SUB"))) {
                        categoryType = "SUB";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " R" + rt;
                    } else if (opcode.equals(category.c2.get("AND"))) {
                        categoryType = "AND";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " R" + rt;
                    } else if (opcode.equals(category.c2.get("OR"))) {
                        categoryType = "OR";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " R" + rt;
                    } else if (opcode.equals(category.c2.get("SRL"))) {
                        categoryType = "SRL";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " #" + rt;
                    } else if (opcode.equals(category.c2.get("SRA"))) {
                        categoryType = "SRA";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " #" + rt;
                    } else if (opcode.equals(category.c2.get("MUL"))) {
                        categoryType = "MUL";
                        temp = categoryType + " R" + rd + "," + " R" + rs + "," + " R" + rt;
                    }
                    disassemb.setRd(rd);
                    disassemb.setRs(rs);
                    disassemb.setRt(rt);
                } else if (first3Bits.equals(category.categorySet.get("Category3"))) {
                    opcode = instruction.substring(3, 6);
                    rt = Integer.parseInt(instruction.substring(6, 11), 2);
                    rs = Integer.parseInt(instruction.substring(11, 16), 2);

                    immediate = calculateVal(toComplement(instruction.substring(16, 32)));
                    if (opcode.equals(category.c3.get("ADDI"))) {
                        categoryType = "ADDI";
                    } else if (opcode.equals(category.c3.get("ANDI"))) {
                        categoryType = "ANDI";
                    } else if (opcode.equals(category.c3.get("ORI"))) {
                        categoryType = "ORI";
                    }
                    temp = categoryType + " R" + rt + "," + " R" + rs + "," + " #" + immediate;
                    disassemb.setRt(rt);
                    disassemb.setRs(rs);
                    disassemb.setImmediate(immediate);
                }
                disassemb.setDisassembl(temp);
                out += instruction + "    " + address + "    "+  temp;
                disassemb.setBinary();
                disassemb.setAddress(address);
                disassemb.setInstruction(categoryType);
                disassemblers.add(disassemb);
                disassemblyList.add(out);
            } else {
                String complement = toComplement(instruction);
                int result = calculateVal(complement);
                out = instruction + "    " + address + "    " + result;
                disassemblyList.add(out);
                dataList.add(result);
            }
            address += 4;
        }
        MapList.put("disassemblyList",disassemblyList);
        MapList.put("dataList",dataList);
        MapList.put("disassemblers",disassemblers);
        MapList.put("registerValueList",registerValueList);
        return MapList;
    }

    public static int calculateVal(String str) {
        if (null == str || str.isEmpty()) {
            return 0;
        }
        char ch = str.charAt(0);
        str = str.substring(1);
        int result = Integer.parseInt(str, 2);
        if (ch == '1') {
            result *= (-1);
        }
        return result;
    }

    public static String toComplement(String str) {

        if (null == str || str.isEmpty()) {
            return null;
        }
        int num;
        for (int i = 0; i < str.length(); i++) {
            num = str.charAt(i) - '0';
            if (num > 1 || num < 0) {
                return null;
            }
        }
        char ch = str.charAt(0);
        if (ch == '0') {
            return str;
        } else {
            StringBuilder sb = new StringBuilder();
            for (int i = 1; i < str.length(); i++) {
                if (str.charAt(i) == '0') {
                    sb.append('1');
                } else {
                    sb.append('0');
                }
            }
            int result = Integer.parseInt(sb.toString(), 2);
            result++;
            String resultStr = Integer.toBinaryString(result);
            return ch +
                    "0".repeat(Math.max(0, 32 - resultStr.length() - 1)) +
                    resultStr;
        }
    }

    public static List<String> readFile(String fileName) {
        ArrayList<String> instruction_list = new ArrayList<>();
        File file  = new File(fileName);
        Scanner scan = null;
        try {
            scan = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        while (true) {
            assert scan != null;
            if (!scan.hasNext()) break;
            instruction_list.add(scan.nextLine());
        }
        return instruction_list;
    }

    public static boolean createFile(File fileName) {
        boolean flag = false;
        try {
            if (!fileName.exists()) {
                fileName.createNewFile();
            }
            flag = true;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return flag;
    }


    public static void writeFile(List<String> newStrList, String fileName)
            throws IOException {

        FileOutputStream fos = null;
        PrintWriter pw = null;
        try {
            File file = new File(fileName);
            StringBuilder buf = new StringBuilder();
            for(String str : newStrList){
                buf.append(str);
                buf.append("\r\n");
            }

            fos = new FileOutputStream(file);
            pw = new PrintWriter(fos);
            pw.write(buf.toString().toCharArray());
            pw.flush();

        } finally {
            if (pw != null) {
                pw.close();
            }
            if (fos != null) {
                fos.close();
            }
        }
    }

    //execute the instructions
    @SuppressWarnings("unchecked")
    public static List<String> execInstruction(Map<String,List<?>> MapList,int startAddr){

        List<String> simulationList = new ArrayList<>();
        int cycleCount = 0;
        boolean isBreak = false;
        List<Integer> dataList = (List<Integer>) MapList.get("dataList");
        List<Command> disassemblers = (List<Command>) MapList.get("disassemblers");
        List<Integer> registerValueList = (List<Integer>) MapList.get("registerValueList");
        int dataStartAddr = startAddr + disassemblers.size()*4;
        for(int i = 0; i < disassemblers.size(); i++){
            cycleCount++;
            Command disassemb = disassemblers.get(i);
            StringBuilder cycleOut = new StringBuilder();
            String instruction = disassemb.getInstruction();
            String disassembl = disassemb.getDisassembl();
            int rd = disassemb.getRd();
            int rs = disassemb.getRs();
            int rt = disassemb.getRt();
            int offset = disassemb.getOffset();
            int immediate = disassemb.getImmediate();
            int address = disassemb.getAddress();
            int target = disassemb.getTarget();
            int base = disassemb.getBase();
            cycleOut.append("Cycle").append(" ").append(cycleCount).append(":").append("    ").append(address).append("    ").append(disassembl).append("\r\n\r\n");
            final int i1 = ((address + 4) + offset - startAddr) / 4;
            switch (instruction) {
                case "J":
                    i = (target - startAddr) / 4;
                    i--;
                    break;
                case "BEQ":
                    if (registerValueList.get(rs).equals(registerValueList.get(rt))) {
                        i = i1;
                        i--;
                    }
                    break;
                case "BNE":
                    if (!registerValueList.get(rs).equals(registerValueList.get(rt))) {
                        i = i1;
                        i--;
                    }
                break;
                case "BGTZ":
                    if (registerValueList.get(rs) > 0) {
                        i = i1;
                        i--;
                    }
                break;
                case "BREAK":
                    isBreak = true;
                break;
                case "SW":
                    int index = (offset + registerValueList.get(base) - dataStartAddr) / 4;
                    dataList.set(index, registerValueList.get(rt));
                break;
                case "LW":
                    index = (offset + registerValueList.get(base) - dataStartAddr) / 4;
                    registerValueList.set(rt, dataList.get(index));
                break;
                case "ADD":
                    registerValueList.set(rd, registerValueList.get(rs) + registerValueList.get(rt));
                break;
                case "SUB":
                    registerValueList.set(rd, registerValueList.get(rs) - registerValueList.get(rt));
                break;
                case "AND":
                    registerValueList.set(rd, registerValueList.get(rs) & registerValueList.get(rt));
                break;
                case "OR":
                    registerValueList.set(rd, registerValueList.get(rs) | registerValueList.get(rt));
                break;
                case "SRL":
                    registerValueList.set(rd, registerValueList.get(rs) >> registerValueList.get(rt));
                break;
                case "SRA":
                    registerValueList.set(rd, registerValueList.get(rs) >> registerValueList.get(rt));
                break;
                case "MUL":
                    registerValueList.set(rd, registerValueList.get(rs) * registerValueList.get(rt));
                break;
                case "ADDI":
                    registerValueList.set(rt, registerValueList.get(rs) + immediate);
                break;
                case "ANDI":
                    registerValueList.set(rt, registerValueList.get(rs) & immediate);
                break;
                case "ORI":
                    registerValueList.set(rt, registerValueList.get(rs) | immediate);
                break;
            }
            cycleOut.append("Registers" + "\r\n" + "R00:");
            int j = 0;
            for(Integer val : registerValueList){
                cycleOut.append("\t").append(val);
                if((j+1) % 8==0&j+1<32){
                    cycleOut.append("\r\n" + "R");
                    if(j+1==8){
                        cycleOut.append("0").append(j + 1).append(":");
                    }else{
                        cycleOut.append(j + 1).append(":");
                    }
                }
                j++;
            }
            cycleOut.append("\r\n\r\n" + "Data");

            StringBuilder dataStr = new StringBuilder();
            int dataAddr = dataStartAddr;
            for(int k = 0; k < dataList.size(); k++){
                if(k % 8 ==0){
                    dataStr.append("\r\n").append(dataAddr).append(":");
                }
                dataStr.append("\t").append(dataList.get(k));
                dataAddr += 4;
            }
            cycleOut.append(dataStr).append("\r\n").append("--------------------").append("\r\n");
            simulationList.add(cycleOut.toString());

            if(isBreak){
                break;
            }
        }

        return simulationList;
    }
}

