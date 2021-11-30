import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from config import config

import psycopg2

class KontenScreen(QDialog):
    def __init__(self):
        super(KontenScreen, self).__init__()
        loadUi("Konten.ui", self)
        self.logo.setPixmap(QPixmap('logo.jpg'))
        self.logo.setScaledContents(True)
        self.tabelKonten.setColumnWidth(0,50)
        self.tabelKonten.setColumnWidth(1,450)
        self.tabelKonten.setColumnWidth(2,900)

        # CRUD
        self.addButton.clicked.connect(self.gotoAdd)
        self.edit.clicked.connect(self.gotoEdit)
        self.delete_2.clicked.connect(self.gotoDelete)
        self.updatedata.clicked.connect(self.showKonten)
        self.showKonten()

        # Sidebar
        self.H_Logout.clicked.connect(self.gotoLogout)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        # katalogProduk = KatalogScreen()
        # widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogout(self):
        # homepage = HomepageScreen()
        # widget.addWidget(homepage)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        # event = EventScreen()
        # widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoForumDiskusi(self):
        # forumDiskusi = ForumDiskusiScreen()
        # widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoAdd(self):
        addkonten = AddContent()
        widget.addWidget(addkonten)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEdit(self):
        editkonten = EditContent()
        widget.addWidget(editkonten)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoDelete(self):
        idKonten = self.insertid.text()
        if (len(idKonten) != 0):
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "DELETE FROM konten WHERE idKonten = \'"+idKonten+"\' AND idKonten NOT IN (SELECT idKonten FROM feedbackblog)"
            cur.execute(query)
            conn.commit()
            rowChecked = cur.rowcount
            if rowChecked == 0:
                self.error.setText("Tidak dapat menghapus karena ada feedback")
                cur.close()
            else:
                self.error.setText("Konten berhasil dihapus!")
                cur.close()
        else: 
            self.error.setText("Pastikan ID Konten yang ingin dihapus valid dan ada!")

    def showKonten(self):
        # Membersihkan apabila ada pesan error sebelumnya         
        self.error.setText('')
        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = 'SELECT * FROM konten'
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.tabelKonten.setRowCount(0)
        if rowNumber ==0:
            self.error.setText("Belum ada data.")
        else:
            for row_number,row_data in enumerate(result):
                self.tabelKonten.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelKonten.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

class AddContent(QDialog):
    def __init__(self):
        super(AddContent, self).__init__()
        loadUi("Konten-addnew.ui", self)
        self.logo.setPixmap(QPixmap('logo.jpg'))
        self.logo.setScaledContents(True)
        self.uploadButton.clicked.connect(self.addfunc)
        self.H_Konten.clicked.connect(self.gotoKonten)

    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addfunc(self):
        try:
            judul = self.insertjudul.text()
            isi = self.insertisi.toPlainText()

            # connect to the PostgreSQL server
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            produk_info = (judul, isi)
            query = """INSERT INTO konten(idKonten, judulkonten, deskripsi) VALUES (DEFAULT,%s,%s)"""
            cur.execute(query,produk_info)
            conn.commit()
            conn.close()
            QMessageBox.about(self,'Tambah Konten Baru', 'Konten berhasil ditambah!')
            self.error.setText('')
        except:
            self.error.setText('Pastikan semua bagian terisi dengan valid ya!')

class EditContent(QDialog):
    def __init__(self):
        super(EditContent, self).__init__()
        loadUi("Konten-edit.ui", self)
        self.logo.setPixmap(QPixmap('logo.jpg'))
        self.logo.setScaledContents(True)
        self.updateButton.clicked.connect(self.updatefunc)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.tabelFeedback.setColumnWidth(0,50)
        self.tabelFeedback.setColumnWidth(1,200)
        self.tabelFeedback.setColumnWidth(2,1150)
        self.showfeedback()

    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def showfeedback(self):
        # Membersihkan apabila ada pesan error sebelumnya         
        self.error_2.setText('')
        # connect to the PostgreSQL server
        # idKonten = self.insertid.text()
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = """SELECT idfeedback, idresponden,feedback FROM feedbackblog"""
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.tabelFeedback.setRowCount(0)
        if rowNumber ==0:
            self.error_2.setText("Belum ada feedback.")
        else:
            for row_number,row_data in enumerate(result):
                self.tabelFeedback.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelFeedback.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

    def updatefunc(self):
        try:
            judul = self.judul.text()
            isi = self.isi.toPlainText()
            idKonten = self.insertid.text()

            # connect to the PostgreSQL server
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            produk_info = (judul, isi, idKonten)
            query = """UPDATE konten SET judulkonten=%s, deskripsi=%s WHERE idKonten=%s"""
            cur.execute(query,produk_info)
            conn.commit()
            conn.close()
            QMessageBox.about(self,'Edit Konten', 'Konten berhasil diupdate!')
            self.error.setText('')
        except:
            self.error.setText('Pastikan semua bagian terisi dengan valid ya!')


#if __name__ == "__konten__":
app = QApplication(sys.argv)
konten = KontenScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(konten)
widget.setFixedHeight(1080)
widget.setFixedWidth(1920)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")