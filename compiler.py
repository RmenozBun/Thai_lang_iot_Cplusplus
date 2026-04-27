with open("program.thai", "r", encoding="utf-8") as f:
    lines = f.readlines()

cpp = []
global_code = []
setup_code = []
loop_code = []

in_loop = False
mode = "cpp"

# ตรวจโหมด (แก้ bug)
for line in lines:
    line = line.strip()
    if line.startswith("โหมด"):
        mode = line.split()[1].strip().lower()

# HEADER
if mode == "cpp":
    cpp.append("#include <iostream>")
    cpp.append("#include <clocale>")
    cpp.append("using namespace std;")
    cpp.append("int main(){")
    cpp.append('system("chcp 65001");')
    cpp.append('setlocale(LC_ALL, "th_TH.UTF-8");')

elif mode == "arduino":
    cpp.append("#include <Arduino.h>")
    cpp.append("")

# BODY
for line in lines:

    line = line.strip()

    if line == "" or line == "เริ่ม" or line == "จบ":
        continue

    if line.startswith("โหมด"):
        continue

    # LOOP CONTROL
    if line == "วนซ้ำ":
        in_loop = True
        continue

    if line == "จบวน":
        in_loop = False
        continue

    target = loop_code if in_loop else setup_code

    # ตัวแปร (เก็บไว้ก่อน)
    if line.startswith("จำนวนเต็ม"):
        name = line.split()[1]
        value = line.split()[3]
        global_code.append(f"int {name} = {value};")
        continue

    elif line.startswith("จำนวนทศนิยม"):
        name = line.split()[1]
        value = line.split()[3]
        global_code.append(f"double {name} = {value};")
        continue

    elif line.startswith("คำ"):
        name = line.split()[1]
        value = line.split()[3]
        global_code.append(f'string {name} = "{value}";')
        continue

    elif line.startswith("อักษร"):
        name = line.split()[1]
        value = line.split()[3]
        global_code.append(f"char {name} = '{value}';")
        continue

    elif line.startswith("ตรรกะ"):
        name = line.split()[1]
        value = line.split()[3]
        value = "true" if value == "จริง" else "false"
        global_code.append(f"bool {name} = {value};")
        continue

    # แสดงผล (แก้ comma bug)
    elif line.startswith("แสดง"):
        value = line.replace("แสดง", "").strip()
        parts = [p.strip() for p in value.split(",")]

        if mode == "cpp":
            output = " << \" \" << ".join(parts)
            cpp.append(f"cout << {output} << endl;")
        else:
            target.append(f"Serial.println({parts[0]});")

        continue

    # IF / ELSE
    elif line.startswith("ถ้า"):
        cond = line.replace("ถ้า", "").strip()

        if mode == "cpp":
            cpp.append(f"if({cond})"+"{")
        else:
            target.append(f"if({cond})"+"{")

        continue

    elif line == "มิฉะนั้น":
        if mode == "cpp":
            cpp.append("} else {")
        else:
            target.append("} else {")
        continue

    elif line == "จบถ้า":
        if mode == "cpp":
            cpp.append("}")
        else:
            target.append("}")
        continue

    # FOR LOOP
    elif line.startswith("ทำซ้ำ"):
        n = line.split()[1]

        if mode == "cpp":
            cpp.append(f"for(int i=0;i<{n};i++)"+"{")
        else:
            target.append(f"for(int i=0;i<{n};i++)"+"{")

        continue

    elif line == "จบทำซ้ำ":
        if mode == "cpp":
            cpp.append("}")
        else:
            target.append("}")
        continue

    # Arduino
    elif mode == "arduino":

        if line.startswith("ตั้งค่า"):
            pin = line.split()[1]
            m = line.split()[3]
            target.append(f"pinMode({pin}, {m});")

        elif line.startswith("เปิด"):
            pin = line.split()[1]
            target.append(f"digitalWrite({pin}, HIGH);")

        elif line.startswith("ปิด"):
            pin = line.split()[1]
            target.append(f"digitalWrite({pin}, LOW);")

        elif line.startswith("หน่วงเวลา"):
            t = line.split()[1]
            target.append(f"delay({t});")

# FOOTER
if mode == "cpp":

    new_cpp = []

    new_cpp.append("#include <iostream>")
    new_cpp.append("#include <clocale>")
    new_cpp.append("using namespace std;")
    new_cpp.append("int main(){")
    new_cpp.append('system("chcp 65001");')
    new_cpp.append('setlocale(LC_ALL, "th_TH.UTF-8");')

    for g in global_code:
        new_cpp.append("    " + g)

    for line in cpp[6:]:
        new_cpp.append("    " + line)

    new_cpp.append("    return 0;")
    new_cpp.append("}")

    cpp = new_cpp

elif mode == "arduino":

    new_cpp = []
    new_cpp.append("#include <Arduino.h>")
    new_cpp.append("")

    for g in global_code:
        new_cpp.append(g)

    new_cpp.append("")

    new_cpp.append("void setup(){")
    new_cpp.append("    Serial.begin(9600);")
    for s in setup_code:
        new_cpp.append("    " + s)
    new_cpp.append("}")

    new_cpp.append("")

    new_cpp.append("void loop(){")
    for l in loop_code:
        new_cpp.append("    " + l)
    new_cpp.append("}")

    cpp = new_cpp

# WRITE FILE
import os

if mode == "arduino":
    os.makedirs("output", exist_ok=True)
    with open("output/output.ino", "w", encoding="utf-8") as f:
        f.write("\n".join(cpp))
else:
    with open("output.cpp", "w", encoding="utf-8") as f:
        f.write("\n".join(cpp))

print("Compile Thai -> C++/Arduino เสร็จแล้ว")