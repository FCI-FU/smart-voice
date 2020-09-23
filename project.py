# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\SmartVoice\project.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!
import sys
import webbrowser

import pygame
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
import time
import pyaudio
import wave
import speech_recognition as sr
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import sqlite3
from queue import PriorityQueue
import threading

lyrics = []
matched = [1,2]
path = ""

class Ui_Form(QWidget):
    global lyrics

    def find(self, index, word):
        for i in range(index, len(lyrics)):
            if lyrics[i] == word:
                return i
        return -1
    
    def record(self):
        self.state.setText("Recording ...")
        global lyrics
        label_language=self.language.text()
        search_language=""
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 20
        WAVE_OUTPUT_FILENAME = "file.wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print("recording...")
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        r = sr.Recognizer()
        text = ""
        with sr.AudioFile("file.wav") as source:
            audio = r.listen(source)
            print("enter")
            try:
                text = r.recognize_google(audio, key=None, language=self.lang)
            except:
                text = "NOT FOUND"
        if len(text) > 3 and text != "NOT FOUND":
            con = sqlite3.connect('Tracks.db')
            cur = con.cursor()
            row = cur.execute("select * from TrackInfo")
            q = PriorityQueue()
            text = text.split(" ")
            for item in row:
                lyrics = item[5].split(" ")
                idx, score = 0, 0
                for word in text:
                    temp = self.find(idx, word)
                    if temp != -1:
                        idx = temp + 1
                        score += 1
                q.put((-score, item[0]))
            global matched
            matched = q.get()
            score = -matched[0]
            if score >= 3:
                self.Home.hide()
                self.details.show()
                con = sqlite3.connect('Tracks.db')
                cur = con.cursor()
                row = cur.execute("select * from TrackInfo WHERE ID ='"+str(matched[1])+"'")
                url = ""
                global path
                for item in row:
                    print(item[3])
                    print(item[1])
                    print(item[4])
                    print(item[9])
                    print(item[8])
                    print(item[6])
                    self.singerName.setText(str(item[3]))
                    self.songName.setText(str(item[1]))
                    self.date.setText(str(item[4]))
                    self.views.setText(str(item[9]))
                    url = item[8]
                    path = item[6]
                print("3")
                self.youtube.clicked.connect(lambda: self.open_webbrowser(url))
                self.open.clicked.connect(self.Open_audio)
                self.backgroundDetails.setPixmap(QtGui.QPixmap("artists/"+path+".jpg"))
                #self.backgroundDetails.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
                print("4")
        else:
            self.state.setText("ERROR ...")
    def again(self):
        self.Home.show()
        self.details.hide()

    def changeLaguage(self):
        if self.lang == "ar-EG" :
            self.lang = "en-US"
            self.language.setText("English")
        else:
            self.lang = "ar-EG"
            self.language.setText("اللغة العربية")
    
    def setupUi(self, Form):
        self.id = ""
        self.lang = "ar-EG"
        Form.setObjectName("Form")
        Form.resize(314, 510)
        Form.setMinimumSize(QtCore.QSize(314, 510))
        Form.setMaximumSize(QtCore.QSize(314, 510))
        Form.setWindowTitle("Smart Voice")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("photos/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        Form.setWindowIcon(icon)
        self.details = QtWidgets.QGroupBox(Form)
        self.details.setGeometry(QtCore.QRect(0, 0, 311, 511))
        self.details.setTitle("")
        self.details.setObjectName("details")
        self.backgroundDetails = QtWidgets.QLabel(self.details)
        self.backgroundDetails.setGeometry(QtCore.QRect(-4, 0, 321, 511))
        self.backgroundDetails.setStyleSheet("background:white")
        self.backgroundDetails.setText("")
        self.backgroundDetails.setPixmap(QtGui.QPixmap("photos/asala.jpg"))
        self.backgroundDetails.setScaledContents(True)
        self.backgroundDetails.setObjectName("backgroundDetails")
        self.singerName = QtWidgets.QTextEdit(self.details)
        self.singerName.setEnabled(False)
        self.singerName.setGeometry(QtCore.QRect(90, 32, 201, 51))
        self.singerName.setStyleSheet("QTextEdit {\n"
"    color:#000;\n"
"    background:transparent;\n"
"    border:none;\n"
"    border-bottom:2px solid #7047ff\n"
"}")
        self.singerName.setObjectName("singerName")
        self.date = QtWidgets.QTextEdit(self.details)
        self.date.setEnabled(False)
        self.date.setGeometry(QtCore.QRect(90, 172, 201, 41))
        self.date.setStyleSheet("QTextEdit {\n"
"    color:#000;\n"
"    background:transparent;\n"
"    border:none;\n"
"    border-bottom:2px solid #7047ff\n"
"}")
        self.date.setObjectName("date")
        self.songName = QtWidgets.QTextEdit(self.details)
        self.songName.setEnabled(False)
        self.songName.setGeometry(QtCore.QRect(90, 102, 201, 41))
        self.songName.setStyleSheet("QTextEdit {\n"
"    color:#000;\n"
"    background:transparent;\n"
"    border:none;\n"
"    border-bottom:2px solid #7047ff\n"
"}")
        self.songName.setObjectName("songName")
        self.artistIcon = QtWidgets.QLabel(self.details)
        self.artistIcon.setGeometry(QtCore.QRect(20, 32, 51, 41))
        self.artistIcon.setText("")
        self.artistIcon.setPixmap(QtGui.QPixmap("photos/icons8-standing-man-64.png"))
        self.artistIcon.setScaledContents(True)
        self.artistIcon.setObjectName("artistIcon")
        self.musicIcon = QtWidgets.QLabel(self.details)
        self.musicIcon.setGeometry(QtCore.QRect(20, 92, 51, 51))
        self.musicIcon.setText("")
        self.musicIcon.setPixmap(QtGui.QPixmap("photos/icons8-musical-notes-64.png"))
        self.musicIcon.setScaledContents(True)
        self.musicIcon.setObjectName("musicIcon")
        self.dateIcon = QtWidgets.QLabel(self.details)
        self.dateIcon.setGeometry(QtCore.QRect(20, 162, 51, 51))
        self.dateIcon.setText("")
        self.dateIcon.setPixmap(QtGui.QPixmap("photos/icons8-date-64.png"))
        self.dateIcon.setScaledContents(True)
        self.dateIcon.setObjectName("dateIcon")
        self.views = QtWidgets.QTextEdit(self.details)
        self.views.setEnabled(False)
        self.views.setGeometry(QtCore.QRect(90, 242, 201, 41))
        self.views.setStyleSheet("QTextEdit {\n"
"    color:#000;\n"
"    background:transparent;\n"
"    border:none;\n"
"    border-bottom:2px solid #7047ff\n"
"}")
        self.views.setObjectName("views")
        self.viewsIcon = QtWidgets.QLabel(self.details)
        self.viewsIcon.setGeometry(QtCore.QRect(20, 230, 61, 61))
        self.viewsIcon.setText("")
        self.viewsIcon.setPixmap(QtGui.QPixmap("photos/icons8-video-conference-96.png"))
        self.viewsIcon.setScaledContents(True)
        self.viewsIcon.setObjectName("viewsIcon")
        self.open = QtWidgets.QPushButton(self.details)
        self.open.setGeometry(QtCore.QRect(60, 335, 101, 61))
        self.open.setStyleSheet("QPushButton{\n"
"    border-radius:75px;\n"
"    image:url(\"photos/icons8-play-96.png\")\n"
"}\n"
"\n"
"\n"
"QPushButton:hover{\n"
"    image:url(\"photos/icons8-circled-play-96.png\")\n"
"}")
        self.open.setText("")
        self.open.setIconSize(QtCore.QSize(120, 120))
        self.open.setObjectName("open")
        self.youtube = QtWidgets.QPushButton(self.details)
        self.youtube.setGeometry(QtCore.QRect(160, 330, 101, 71))
        self.youtube.setStyleSheet("QPushButton{\n"
"    border-radius:75px;\n"
"    image:url(\"photos/icons8-youtube-squared-512.png\")\n"
"}\n"
"QPushButton:hover{\n"
"    image:url(\"photos/icons8-youtube-hover.png\")\n"
"}")
        self.youtube.setText("")
        self.youtube.setIconSize(QtCore.QSize(80, 80))
        self.youtube.setObjectName("youtube")
        self.back = QtWidgets.QPushButton(self.details)
        self.back.setGeometry(QtCore.QRect(10, 430, 61, 71))
        self.back.setStyleSheet("QPushButton{\n"
"    border-radius:75px;\n"
"    image:url(\"photos/icons8-go-back-96.png\")\n"
"}\n"
"QPushButton:hover{\n"
"    image:url(\"photos/icons8-back-arrow-96.png\")\n"
"}")
        self.back.setText("")
        self.back.setIconSize(QtCore.QSize(64, 64))
        self.back.setObjectName("back")
        self.back.clicked.connect(self.again)
        self.Home = QtWidgets.QGroupBox(Form)
        self.Home.setGeometry(QtCore.QRect(0, 0, 321, 511))
        self.Home.setTitle("")
        self.Home.setObjectName("Home")
        self.startRecord = QtWidgets.QPushButton(self.Home)
        self.startRecord.setGeometry(QtCore.QRect(70, 110, 171, 151))
        self.startRecord.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.startRecord.setStyleSheet("QPushButton {\n"
"    border-radius:75px;\n"
"     image:url(\"photos/aq.png\")\n"
" }\n"
"\n"
"QPushButton:hover {\n"
"     image:url(\"photos/hover.png\")\n"
" }")
        self.startRecord.setText("")
        self.startRecord.setIconSize(QtCore.QSize(120, 120))
        self.startRecord.setObjectName("startRecord")
        self.startRecord.clicked.connect(self.record)
        self.backgroundHome = QtWidgets.QLabel(self.Home)
        self.backgroundHome.setGeometry(QtCore.QRect(-370, 0, 991, 511))
        self.backgroundHome.setStyleSheet("background-color:white")
        self.backgroundHome.setText("")
        self.backgroundHome.setPixmap(QtGui.QPixmap("photos/2.jpg"))
        self.backgroundHome.setObjectName("backgroundHome")
        self.language = QtWidgets.QLabel(self.Home)
        self.language.setGeometry(QtCore.QRect(60, 20, 61, 21))
        self.language.setText("اللغة العربية")
        self.language.setObjectName("language")
        self.logo = QtWidgets.QLabel(self.Home)
        self.logo.setGeometry(QtCore.QRect(0, 330, 311, 131))
        self.logo.setStyleSheet("font-size:40px;\n"
"color:#000")
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("photos/SmartVoice.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.languageBtn = QtWidgets.QPushButton(self.Home)
        self.languageBtn.setGeometry(QtCore.QRect(10, 10, 41, 41))
        self.languageBtn.setStyleSheet("QPushButton{\n"
"    border-radius:75px;\n"
"    image:url(\"photos/icons8-geography-100.png\")\n"
" }\n"
"\n"
"QPushButton:hover {\n"
"     image:url(\"photos/icons8-geography-96.png\")\n"
" }")
        self.languageBtn.setText("")
        self.languageBtn.setObjectName("pushButton")
        self.languageBtn.clicked.connect(self.changeLaguage)
        self.state = QtWidgets.QLabel(self.Home)
        self.state.setGeometry(QtCore.QRect(125, 270, 151, 41))
        self.state.setText("")
        self.state.setObjectName("state")
        self.backgroundHome.raise_()
        self.startRecord.raise_()
        self.language.raise_()
        self.state.raise_()
        self.logo.raise_()
        self.languageBtn.raise_()
        
        self.retranslateUi(Form)
    def retranslateUi(self, Form):
        pass




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
