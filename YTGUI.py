# !/usr/bin/env python
# coding=utf-8

import wx
import YTdownGUI
from threading import Thread
import time
import youtube_dl
from pubsub import pub


videoSavePath = './downYT/'    # 保存地址

def progress_hook(response):
    if response["status"] == "finished":
        file_name = response["filename"]
        print('下載後的路徑名稱: ' + file_name)
    else:
        pub.sendMessage("update", mstatus=str(response["downloaded_bytes"]))
        with open("strat.txt", 'w') as f1:
            f1.write('{} {}'.format(str(response["downloaded_bytes"]), str(response["total_bytes"])))


def down(url_1):
    # 参数信息
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio/best',   # 保存为MP4格式
        'progress_hooks': [progress_hook],
        'outtmpl': videoSavePath + "%(id)s.%(ext)s"  # 默认是'%(title)s-%(id)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_1])

def schedule():
    with open("strat.txt", 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(' ')
        print(line)

class YTGUIFrame(YTdownGUI.MyFrame1):
    def __init__(self, parent):
        YTdownGUI.MyFrame1.__init__(self, parent)
        pub.subscribe(self.updateDisplay, "update")

    def text_Clear(self, event):
        self.m_textCtrl2.Clear()

    def downbtn(self, event):
        url = self.m_textCtrl2.GetValue()
        print('按下按鈕' + str(url))
        thread_1 = Thread(target=YTGUIFrame.text_Clear(self, event), name='T1')
        thread_2 = Thread(target=down(url), name='T2')
        thread_3 = Thread(target=schedule, name='T3')
        thread_1.start()
        thread_2.start()
        thread_3.start()
        # thread_1.join()
        print('按鈕事件結束')

    def updateDisplay(self, mstatus):
        self.m_staticText2.SetLabel(mstatus)


if __name__ == '__main__':
    app = wx.App()
    frm = YTGUIFrame(None)
    frm.Show()
    app.MainLoop()
