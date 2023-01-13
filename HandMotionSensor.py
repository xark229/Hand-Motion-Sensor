import Vmouse as vm
import Volcontrol as vc
import vbrightness as vb
import Drag_Drop_Module as DD

print("----------------------------------Hand Motion Detector----------------------------------------")
print(" a) Volume control using finger")
print(" b) Brightness control using Finger")
print(" c) Drag and Drop using finger")
print(" d) Virtual Cursor")
print(" e) Exit")
while True:
    a=input("Enter choice : ")
    if a=='a':
        vc.volControl()
    elif a=='b':
        vb.brightness_control()
    elif a=='c':
        print("select shape")
        print("a) Rectangle")
        print("b) Circle")
        s=input("Enter your Shape: ")
        if s=='a':
            n=int(input("How many shapes are required"))
            rec=DD.drag_rectangle(n)
            DD.dgdr(rec,1)
        elif s=='b':
            n = int(input("How many shapes are required"))
            rec = DD.drag_rectangle(n)
            DD.dgdr(rec, 0)
        else:
            print ("unidentified shape chosen")

    elif a=='d':
        vm.virtualMouse()
    elif a=='e':
        print("Thank you")
        exit(0)
    else:
        print("Unrecognized choice")

