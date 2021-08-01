from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
import ctypes
from ctypes.wintypes import DWORD, ULONG, HRGN
from ctypes import windll, c_bool, c_int, POINTER, Structure
from ctypes import WINFUNCTYPE
import math
import keyboard
import platform

#Проверка на версию операционной системы (да простит меня Линукс)
if "7" in platform.win32_ver():

    #Настройки размытия для Windows 7
    class DWM_BLURBEHIND(Structure):
        _fields_ = [
            ('dwFlags', DWORD),
            ('fEnable', c_bool),
            ('hRgnBlur', HRGN),
            ('fTransitionOnMaximized', c_bool)
        ]


    prototype = WINFUNCTYPE(c_int, c_int, POINTER(DWM_BLURBEHIND))
    params = (1, "hWnd", 0), (1, "pBlurBehind", 0)
    _DwmEnableBlurBehindWindow = prototype(("DwmEnableBlurBehindWindow", windll.dwmapi), params)

    has_dwm = hasattr(windll, 'dwmapi') and hasattr(windll.dwmapi, 'DwmIsCompositionEnabled')

    def DWM_enable_blur_behind_window(widget):
        DWM_BB_ENABLE = 0x0001

        bb = DWM_BLURBEHIND()
        bb.fEnable = c_bool(True)
        bb.dwFlags = DWM_BB_ENABLE
        bb.hRgnBlur = None

        result = _DwmEnableBlurBehindWindow(c_int(widget.winId()), bb)

        return not result  

elif "8" in platform.win32_ver() or "10" in platform.win32_ver():

    #Настройки размытия для Windows 10 (на вин 8 и 8.1 размытие не работает)
    class AccentPolicy(Structure):
        _fields_ = [
            ('AccentState', DWORD),
            ('AccentFlags', DWORD),
            ('GradientColor', DWORD
            ),
            ('AnimationId', DWORD),
        ]

    class WINCOMPATTRDATA(Structure):
        _fields_ = [
            ('Attribute', DWORD),
            ('Data', POINTER(AccentPolicy)),
            ('SizeOfData', ULONG),
        ]

    SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
    SetWindowCompositionAttribute.restype = c_bool
    SetWindowCompositionAttribute.argtypes = [c_int, POINTER(WINCOMPATTRDATA)]

#Основной класс окна
class Widget(QWidget):
    
    #Функция окна
    def __init__(self):

        #Чета ещё от окна
        super().__init__()

        #Скрытие рамки стандартного окна
        self.setWindowFlags(Qt.FramelessWindowHint)

        #Кастомная рамка
        name = QLabel(self) #создание текста
        name.move(15, 2) #расположение
        name.setText("Калькулятор") #текст названия
        name.setStyleSheet('QLabel {color: white; font-size: 9pt; background-color: transparent;}') #стиль названия

        close = QPushButton('X', self, clicked=self.close) #создание кнопки закрытия
        close.move(275, 0) #расположение
        close.setFixedSize(45, 32) #размер
        close.setStyleSheet('QPushButton {background-color: transparent; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #e81123}') #стиль

        roll_up = QPushButton(' ̶ ', self, clicked=self.showMinimized) #создание кнопки сворачивания
        roll_up.move(230, 0) #расположение
        roll_up.setFixedSize(45, 32) #размер
        roll_up.setStyleSheet('QPushButton {background-color: transparent; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}') #стиль
        

        #Прозрачность окна
        self.setStyleSheet("background-color: #96222222") #фоновый цвет
        self.setWindowOpacity(0.99) #сама прозрачность

        #Основной текст
        self.lbl = QLabel(self) #создание текста
        self.lbl.move(285, 110) #перемещение
        self.lbl.setText("0") #текст
        self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #стиль текста
        self.lbl.setFixedSize(1000, 40) #размер рамки текста

        #Второй текст
        global second
        second = QLabel(self) #создание текста
        second.move(300, 65) #перемещение
        second.setText("") #текст
        second.setStyleSheet('QLabel {color: gray; font-size: 10pt; background-color: transparent; font: bold}') #стиль текста
        second.setFixedSize(1000, 40) #размер рамки текста

        #Вспомогательные функции

        #функция смещения основного текста
        def bias(answer, expression):
                
            #проверка количества символов в строке
            if len(answer) > 11:
                pass
            if len(answer) == 1:

                self.lbl.move(285, 110) #перемещение

            elif len(answer) <5:
                    
                #Проверка на наличие точки в ответе
                if '.' in answer:
                    expression = len(answer) #переменная с колиством символов в строке
                    expression = expression*(10 + ((expression-1)*2.4)) #формула передвижения
                    self.lbl.move(285-expression, 110) #передвижение

                else:        
                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*3))
                    self.lbl.move(285-expression, 110)

            elif len(answer) == 5:  

                if '.' in answer:
                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*2.1))
                    self.lbl.move(285-expression, 110)

                else:    
                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*2.5))
                    self.lbl.move(285-expression, 110)  

            elif len(answer) == 6:

                if '.' in answer:
                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.8))
                    self.lbl.move(285-expression, 110)

                else:
                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*2.3))
                    self.lbl.move(285-expression, 110)

            elif len(answer) < 8:

                if '.' in answer:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.6))
                    self.lbl.move(285-expression, 110)  

                else:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*2.1))
                    self.lbl.move(285-expression, 110)    

            elif len(answer) == 8:

                if '.' in answer:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.6))
                    self.lbl.move(285-expression, 110)  

                else:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.8))
                    self.lbl.move(285-expression, 110)   

            elif len(answer) == 9:

                if '.' in answer:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.4))
                    self.lbl.move(285-expression, 110)  

                else:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.6))
                    self.lbl.move(285-expression, 110)  

            elif len(answer) == 11:    

                if '.' in answer:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.2))
                    self.lbl.move(285-expression, 110)  

                else:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.35))
                    self.lbl.move(285-expression, 110)     

            else:

                if '.' in answer:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.3))
                    self.lbl.move(285-expression, 110)  

                else:

                    expression = len(answer) 
                    expression = expression*(10 + ((expression-1)*1.5))
                    self.lbl.move(285-expression, 110)   

        #функция смещения второго текста
        def second_bias():
            second_expression = (len(second.text()) * 7) #вычисление перемещения
            second.move(300-second_expression, 65)#перемещение              

        #защита от текстовых операций
        global Text 
        Text = False

        #Кнопки
        mode = QPushButton('+/_', self) #создание кнопки
        mode.move(0, 473) #перемещение
        mode.setFixedSize(76, 60) #размер
        mode.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}') #стиль

        zero = QPushButton('0', self)
        zero.move(78, 473)
        zero.setFixedSize(76, 60)
        zero.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        comma = QPushButton(',', self)
        comma.move(156, 473)
        comma.setFixedSize(76, 60)
        comma.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        equals = QPushButton('=', self)
        equals.move(234, 473)
        equals.setFixedSize(83, 60)
        equals.setStyleSheet('QPushButton {background-color: #231747; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #250572}')

        one = QPushButton('1', self)
        one.move(0, 421)
        one.setFixedSize(76, 50)
        one.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        two = QPushButton('2', self)
        two.move(78, 421)
        two.setFixedSize(76, 50)
        two.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        three = QPushButton('3', self)
        three.move(156, 421)
        three.setFixedSize(76, 50)
        three.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        four = QPushButton('4', self)
        four.move(0, 369)
        four.setFixedSize(76, 50)
        four.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        five = QPushButton('5', self)
        five.move(78, 369)
        five.setFixedSize(76, 50)
        five.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        six = QPushButton('6', self)
        six.move(156, 369)
        six.setFixedSize(76, 50)
        six.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        seven = QPushButton('7', self)
        seven.move(0, 317)
        seven.setFixedSize(76, 50)
        seven.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        eight = QPushButton('8', self)
        eight.move(78, 317)
        eight.setFixedSize(76, 50)
        eight.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        nine = QPushButton('9', self)
        nine.move(156, 317)
        nine.setFixedSize(76, 50)
        nine.setStyleSheet('QPushButton {background-color: #000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        plus = QPushButton('+', self)
        plus.move(234, 421)
        plus.setFixedSize(83, 50)
        plus.setStyleSheet('QPushButton {background-color: #64000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        minus = QPushButton('-', self)
        minus.move(234, 369)
        minus.setFixedSize(83, 50)
        minus.setStyleSheet('QPushButton {background-color: #64000000; color: white; font: bold; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        multiply = QPushButton('х', self)
        multiply.move(234, 317)
        multiply.setFixedSize(83, 50)
        multiply.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        division = QPushButton('÷', self)
        division.move(234, 265)
        division.setFixedSize(83, 50)
        division.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        backspace = QPushButton('⌫', self)
        backspace.move(234, 213)
        backspace.setFixedSize(83, 50)
        backspace.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        C = QPushButton('C', self)
        C.move(156, 213)
        C.setFixedSize(76, 50)
        C.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        CE = QPushButton('CE', self)
        CE.move(78, 213)
        CE.setFixedSize(76, 50)
        CE.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        percent = QPushButton('%', self)
        percent.move(0, 213)
        percent.setFixedSize(76, 50)
        percent.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        decimal = QPushButton('1/x', self)
        decimal.move(0, 265)
        decimal.setFixedSize(76, 50)
        decimal.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font: italic; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        square = QPushButton('х²', self)
        square.move(78, 265)
        square.setFixedSize(76, 50)
        square.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font: italic; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        root = QPushButton('√x', self)
        root.move(156, 265)
        root.setFixedSize(76, 50)
        root.setStyleSheet('QPushButton {background-color: #64000000; color: white; border: none; font-size: 12pt;} QPushButton:hover { background-color: #96393939}')

        MC = QPushButton('MC', self)
        MC.move(0, 178)
        MC.setFixedSize(55, 35)
        MC.setStyleSheet('QPushButton {background-color: transparent; color: gray; border: none; font-size: 10pt; font: bold;}')

        MR = QPushButton('MR', self)
        MR.move(50, 178)
        MR.setFixedSize(55, 35)
        MR.setStyleSheet('QPushButton {background-color: transparent; color: gray; border: none; font-size: 10pt; font: bold;}')

        Mplus = QPushButton('M+', self)
        Mplus.move(100, 178)
        Mplus.setFixedSize(55, 35)
        Mplus.setStyleSheet('QPushButton {background-color: transparent; color: white; border: none; font-size: 10pt; font: bold;} QPushButton:hover { background-color: #96393939}')

        Mminus = QPushButton('M-', self)
        Mminus.move(155, 178)
        Mminus.setFixedSize(55, 35)
        Mminus.setStyleSheet('QPushButton {background-color: transparent; color: white; border: none; font-size: 10pt; font: bold;} QPushButton:hover { background-color: #96393939}')

        MS = QPushButton('MS', self)
        MS.move(206, 178)
        MS.setFixedSize(55, 35)
        MS.setStyleSheet('QPushButton {background-color: transparent; color: white; border: none; font-size: 10pt; font: bold;} QPushButton:hover { background-color: #96393939}')

        Mlist = QPushButton('Mˇ', self)
        Mlist.move(260, 178)
        Mlist.setFixedSize(55, 35)
        Mlist.setStyleSheet('QPushButton {background-color: transparent; color: gray; border: none; font-size: 10pt; font: bold;}')

        if "7" in platform.win32_ver():
            #Размытие окна Windows 7
            DWM_enable_blur_behind_window(self)
        elif "10" in platform.win32_ver():
            #Размытие окна Windows 10
            accent_policy = AccentPolicy() #чета нужное
            accent_policy.AccentState = 3 #указание на размытие

            win_comp_attr_data = WINCOMPATTRDATA() #ещё чета нужное
            win_comp_attr_data.Attribute = 19 #ещё одно указание
            win_comp_attr_data.SizeOfData = ctypes.sizeof(accent_policy) #ещё одно нужное
            win_comp_attr_data.Data = ctypes.pointer(accent_policy) #нужное

            hwnd = c_int(self.winId()) #хз зачем, но нужно
            ok = SetWindowCompositionAttribute(hwnd, ctypes.pointer(win_comp_attr_data)) #тоже нужно
            print(ok) #не нужно, но пусть будет

        self.old_pos = None #я ваще не знаю зачем оно, но не трожь
        self.frame_color = Qt.black #типа блэк, но не блэк

        #Функции кнопок 
        def one_click():

            #переменная примера
            expression = self.lbl.text()

            global Text #объявление глобальной переменной

            #Проверка защиты
            if Text == False:
                #проверка на наличие нуля ии точки в начале
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("1") #смена текста
                else:
                    #блокировка чрезмерного перемещения цифр
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26) #переменная перемещения
                        self.lbl.move(move, 110) #перемещение
                        self.lbl.setText(expression + "1") #добавок к тексту
            else:
                self.lbl.setText("1") # при наличии текста в окне - он заменится на 1          
                second.setText("") # очищение второго текста
                self.lbl.move(285, 110) #перемещение текста       
                second.move(300, 65) #перемещение второго текста
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False #указание на отсутствие текста 

        def two_click():

            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("2")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "2")

            else:
                self.lbl.setText("2")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False

        def three_click():
          
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("3")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "3")
            else:
                self.lbl.setText("3")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False               
                
        def four_click():
          
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("4")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "4") 
            else:
                self.lbl.setText("4")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False            
                
        def five_click():
        
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("5")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "5") 
            else:
                self.lbl.setText("5")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False
                
        def six_click():
    
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("6")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "6") 
            else:
                self.lbl.setText("6")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False            
                
        def seven_click():

            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("7")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "7") 
            else:
                self.lbl.setText("7")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False            
                
        def eight_click():
       
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("8")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "8")  
            else:
                self.lbl.setText("8")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False
                 
        def nine_click():
         
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("9")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "9")
            else:
                self.lbl.setText("9")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False             
                
        def minus_click():
            
            expression = self.lbl.text()

            if Text == False:
                #псевдо проверка на целое число
                if expression.endswith(".0"):
                    expression = expression[:-2] #псевдо преобразование в целое число :)

                #формирование текста
                self.lbl.setText("0") #обнуление основного текста
                second.setText(expression + " " + "-") #запись второго текста
                self.lbl.move(285, 110) #передвижение первого

                second_bias()
 
        def plus_click():

            expression = self.lbl.text()

            if Text == False:
                if expression.endswith(".0"):
                    expression = expression[:-2]

                self.lbl.setText("0")
                second.setText(expression + " " + "+")
                self.lbl.move(285, 110)

                second_bias()

        def division_click():
          
            expression = self.lbl.text()

            if Text == False:
                if expression.endswith(".0"):
                    expression = expression[:-2]

                self.lbl.setText("0")
                second.setText(expression + " " + "/")
                self.lbl.move(285, 110)
            
                second_bias()
 
        def multiply_click():
            
            expression = self.lbl.text()

            if Text == False:
                if expression.endswith(".0"):
                    expression = expression[:-2]

                self.lbl.setText("0")
                second.setText(expression + " " + "*")
                self.lbl.move(285, 110)
            
                second_bias()

        def zero_click():
                       
            expression = self.lbl.text()

            global Text

            if Text == False:
                if expression.startswith("0") and "." not in expression:
                    self.lbl.setText("0")
                else:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 26)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + "0") 
            else:
                self.lbl.setText("0")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False            

        def comma_click():
                       
            expression = self.lbl.text()

            if Text == False:
                if "." not in expression:
                    if self.lbl.x() > 25:
                        move = (self.lbl.x() - 15)
                        self.lbl.move(move, 110)
                        self.lbl.setText(expression + ".")
                    
        def equals_click():
            
            expression = self.lbl.text() #переменная основного текста
            second_expression = second.text() #переменная второго текста
            global Text #вызов защиты

            #проверка на наличие знака равенства, а также математических действий во втором тексте
            if "=" not in second_expression and (second_expression.endswith('+') or second_expression.endswith('-') or second_expression.endswith('*') or second_expression.endswith('/')):

                #проверка деления на ноль
                if expression == "0" and second_expression.endswith('/'):
                    self.lbl.move(17, 88)
                    self.lbl.setStyleSheet('QLabel {color: white; font-size: 14pt; font: bold; background-color: transparent;}') #новый стиль текста
                    self.lbl.setText("Деление на ноль невозможно")
                    Text = True #запуск защиты


                else:    
                    second.setText(second_expression + " " + expression + " " + "=") #формирование второго текста
                    self.lbl.move(285, 110) #передвижение основного текста
                    answer = second_expression + expression #объединение примера
                    answer = eval(answer) #вычисление 
                    answer = str(answer) #перевод в строку
                    #проверка на целое число
                    if answer.endswith(".0"):
                        answer = answer[:-2] #типа перевод в целое число
                    #защита от двоичных и ленивых (моих) погрешностей
                    if len(answer) > 11:
                        answer = str(answer[:-(len(answer)-6)]) #находим разницу между ответом и вмещаемым текстом
                        #проверка на бесконечную дробь
                        if "." in answer:
                            answer = float(answer) #перевод в дробь
                            answer = answer.__round__(7) #округление
                            answer = str(answer) #перевод в строку
                        else:    
                            answer = (answer + "e") #я слишком ленив, чтобы вместить число больше 10000000000
                            Text = True #запуск защиты
                            
                    self.lbl.setText(answer) #отображение ответа 

                    bias(answer, expression)
            
                    second_bias()

        def backspace_click():
            
            expression = self.lbl.text()
            global Text

            if Text == False:
                #проверка на наличие точки в конце
                if expression.endswith("."):
                    expression = expression[:-1] #нету больше точки :)
                    self.lbl.setText(expression) #новый текст
                    move = (self.lbl.x() + 15) #формула перемещения
                    self.lbl.move(move, 110) #перемещение

                else:
                    #проверка на длину строки
                    if len(expression) == 1 and expression != 0:
                        self.lbl.setText("0") #если стераем последнее число - оно заменится нулём
                    else:    
                        expression = expression[:-1]
                        self.lbl.setText(expression)
                        move = (self.lbl.x() + 26)
                        self.lbl.move(move, 110)
            else:
                self.lbl.setText("0")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') 
                Text = False

        def C_click(): 

            #полная очистка
            self.lbl.setText("0") #основной текст = 0        
            second.setText("") #минус второй текст
            self.lbl.move(285, 110) #перемещение основного текста
            self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста
            second.move(300, 65) #перемещение второго текста

            #отключение защиты
            global Text 
            Text = False 

        def CE_click():

            expression = second.text()
            global Text

            #проверка на наличие знака равно во втором тексте
            if "=" in expression:

                #полная очистка
                self.lbl.setText("0")           
                second.setText("")
                self.lbl.move(285, 110)        
                second.move(300, 65)
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста 
                Text = False

            else:    

                #очистка текущего ввода
                self.lbl.setText("0")
                self.lbl.move(285, 110) 
                self.lbl.setStyleSheet('QLabel {color: white; font-size: 35pt; background-color: transparent;}') #возврат стиля основного текста
                Text = False

        def mode_click():

            expression = str(self.lbl.text())

            if Text == False:
                #проверка на то, какому числу меняем знак
                if expression == "0":
                    pass #заглушка
                elif expression.startswith("-"):
                    self.lbl.move(self.lbl.x() + 17, 110) #перемещение
                else:
                    self.lbl.move(self.lbl.x() - 17, 110) #тоже перемещение
            
                expression = int(expression) #перевод в число
                expression *= -1 #смена знака
                self.lbl.setText(str(expression)) #отображение числа

        def decimal_click():

            #Думаю, тут всё понятно... Я уже задолбался это всё комментировать :)

            expression = self.lbl.text()
            global Text

            if Text == False:
                #проверка деления на ноль
                if expression == "0":
                    self.lbl.move(17, 88)
                    self.lbl.setStyleSheet('QLabel {color: white; font-size: 14pt; font: bold; background-color: transparent;}') #новый стиль текста
                    self.lbl.setText("Деление на ноль невозможно")
                    Text = True

                else:
                    second.setText("1/(" + expression + ")")
                    answer = second.text()    
                    answer = eval(answer)
                    answer = str(answer)

                    if len(answer) > 11:
                        answer = str(answer[:-(len(answer)-6)])
                        if "." in answer:
                            answer = float(answer)
                            answer = answer.__round__(7)
                            answer = str(answer)
                        else:    
                            answer = (answer + ".e")

                    if answer.endswith(".0"):
                        answer = answer[:-2]
                    self.lbl.setText(answer)

                    #смещение основного текста
                    if '.' in answer:
                        if len(answer) == 3:
                            expression = len(answer)
                            expression = (10+expression*10)
                            self.lbl.move(285-expression, 110)
                        elif len(answer) == 4:
                            expression = len(answer)
                            expression = (10+expression*13)
                            self.lbl.move(285-expression, 110)
                        elif len(answer) == 5:
                            expression = len(answer)
                            expression = (10+expression*16)
                            self.lbl.move(285-expression, 110)
                        elif len(answer) == 6:
                            expression = len(answer)
                            expression = (10+expression*18)
                            self.lbl.move(285-expression, 110)  
                        elif len(answer) == 11:
                            expression = len(answer)
                            expression = (10+expression*22)
                            self.lbl.move(285-expression, 110)        
                        else:
                            expression = len(answer)
                            expression = (10+expression*20)
                            self.lbl.move(285-expression, 110)
                    else:
                        self.lbl.move(285, 110)

                    second_bias()

        def square_click():
            global Text
            if Text == False:
                expression = self.lbl.text()
                second.setText("sqr(" + expression + ")")
                expression = float(expression)
                answer = float(expression * expression)  #возведение в квадрат. Да, я не придумал ничего лучше :D  
                answer = str(answer)
                if len(answer) > 11:
                        answer = str(answer[:-(len(answer)-6)])
                        if "." in answer:
                            answer = float(answer)
                            answer = answer.__round__(7)
                            answer = str(answer)
                        else:    
                            answer = (answer + "e")
                            Text = True
                #псевдо проверка на целое число
                if answer.endswith('.0'):
                    answer = answer[:-2] #псевдо перевод в целое число
                self.lbl.setText(answer)

                bias(answer, expression)
            
                second_bias()

        def root_click():

                if Text == False:
                    expression = self.lbl.text()
                    second.setText("√(" + expression + ")")
                    expression = float(self.lbl.text())
                    answer = str(math.sqrt(expression)) #Вычисление корня, благо без костылей
                    if len(answer) > 11:
                        answer = str(answer[:-(len(answer)-6)])
                        if "." in answer:
                            answer = float(answer)
                            answer = answer.__round__(7)
                            answer = str(answer)
                    if answer.endswith('.0'):
                        answer = answer[:-2]
                    self.lbl.setText(answer)

                    bias(answer, expression)

                    second_bias()
                
        def percent_click():

            expression = self.lbl.text()

            if Text == False:

                #Проверка на пустой текст, ноль и окончания на точку
                if second.text() != "" and not expression.startswith("0") and not expression.endswith("."):

                    expression = float(self.lbl.text()) #перевод основного текста в число
                    second_expression = float(second.text()[:-1]) #перевод второго текста в число
                    answer = (second_expression/100*expression) #формула процента

                    if len(str(answer)) > 11:
                        answer = str(answer)
                        answer = str(answer[:-(len(answer)-6)])
                        if "." in answer:
                            answer = float(answer)
                            answer = answer.__round__(7)
                            answer = str(answer)

                    expression = self.lbl.text() #отображение основного текста
                    second_expression = second.text() #отображение второго текста

                    second_expression = float(second.text()[:-1]) #перевод второго текста в число с игнорированием знака
                    expression = (second_expression, answer) #объединение процента и второго текста
                    answer = str(answer) #перевод в строку
                    #проверка на целое число
                    if answer.endswith(".0"):
                        answer = str(answer)[:-2]  #мне опять нужно это комментировать?
                    self.lbl.setText(answer) #вывод текста, да.

                    bias(answer, expression)

                    second_bias()

        #подключение функций к кнопкам
        one.clicked.connect(one_click) 
        two.clicked.connect(two_click)   
        three.clicked.connect(three_click) 
        four.clicked.connect(four_click)   
        five.clicked.connect(five_click) 
        six.clicked.connect(six_click)   
        seven.clicked.connect(seven_click) 
        eight.clicked.connect(eight_click)  
        nine.clicked.connect(nine_click) 
        zero.clicked.connect(zero_click)   
        minus.clicked.connect(minus_click) 
        plus.clicked.connect(plus_click)   
        division.clicked.connect(division_click) 
        multiply.clicked.connect(multiply_click)   
        comma.clicked.connect(comma_click) 
        equals.clicked.connect(equals_click)   
        backspace.clicked.connect(backspace_click)
        C.clicked.connect(C_click)
        CE.clicked.connect(CE_click)
        mode.clicked.connect(mode_click)
        decimal.clicked.connect(decimal_click)
        square.clicked.connect(square_click)
        root.clicked.connect(root_click)
        percent.clicked.connect(percent_click)  

        #доступ для вызова функций через нажатие клавиши
        self.one = one_click 
        self.two = two_click 
        self.three = three_click 
        self.four = four_click  
        self.five = five_click 
        self.six = six_click 
        self.seven = seven_click 
        self.eight = eight_click   
        self.nine = nine_click 
        self.zero = zero_click 
        self.minus = minus_click 
        self.plus = plus_click  
        self.division = division_click 
        self.multiply = multiply_click 
        self.comma = comma_click 
        self.equals = equals_click  
        self.backspace = backspace_click              

        #холст
        layout = QVBoxLayout()
        self.setLayout(layout)

        
    #Функции перетаскивания мышью
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return

        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)       

#запуск программы
if __name__ == '__main__':

    app = QApplication([]) #присвоение переменной значение программы

    w = Widget() #подключение класса к переменной

    w.__init__() #доступ для функций окна

    #костыль от ложных срабатываний (погрешность модуля keyboard)
    def protect(e):
        key = str(e)
        if "(* up)" in key:
            w.multiply()

        if "ж" in key:
            pass
        elif "(6 up)" in key:
            w.six()

        #формулировка условия - ещё один костыль
        if "(б up)" in key or "(Б up)" in key:
           w.comma()  
        elif "(1 up)" in key:
           w.one()   

        if "(/ up)" in key:
            w.division()
        elif "(, up)" in key or "(decimal up)" in key:
            w.comma()            

    keyboard.hook(protect) #активация костыля
        
    #добавление горячих клавиш для ввода с клавиатуры
    keyboard.add_hotkey('1', lambda: protect)
    keyboard.add_hotkey('2', lambda: w.two())
    keyboard.add_hotkey('3', lambda: w.three())
    keyboard.add_hotkey('4', lambda: w.four())
    keyboard.add_hotkey('5', lambda: w.five())
    keyboard.add_hotkey('6', lambda: protect)
    keyboard.add_hotkey('7', lambda: w.seven())
    keyboard.add_hotkey('8', lambda: w.eight())
    keyboard.add_hotkey('9', lambda: w.nine())
    keyboard.add_hotkey('0', lambda: w.zero())
    keyboard.add_hotkey('/', lambda: protect)
    keyboard.add_hotkey('*', lambda: protect)
    keyboard.add_hotkey('-', lambda: w.minus())
    keyboard.add_hotkey('+', lambda: w.plus())
    keyboard.add_hotkey('Enter', lambda: w.equals())
    keyboard.add_hotkey('Backspace', lambda: w.backspace())
    keyboard.add_hotkey(',', lambda: protect)
    
    
    #отрисовка программы
    w.setWindowTitle('Калькулятор') #название программы
    w.setFixedSize(321, 533) #размер окна
    w.show() #отображение холста

    app.exec() #отрисовка интерфейса

    
      

# И ты попала
# К настоящему колдуну
# Он загубил таких, как ты, не одну!
# Словно куклой и в час ночной
# Теперь он может управлять тобой!
