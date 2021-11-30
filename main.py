# katalog.py

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap,QIcon
from config import config
import psycopg2

class LoginScreen(QDialog):
    
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        #logoLM.setPixmap(pixmap.scaled(myWidth, myHeight, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        self.logoLM.setPixmap(QPixmap('./images/logo.jpeg'))
        self.logoLM.setScaledContents(True)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.usernameField.text()
        password = self.passwordField.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")

        else:
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = 'SELECT password FROM admin WHERE username =\''+user+"\'"
            cur.execute(query)
            rowChecked = cur.rowcount
            # apabila username/ password ga ada
            if rowChecked == 1:
                result_pass = cur.fetchone()[0]
                if result_pass == password:
                    print("Successfully logged in.")
                    self.gotoKatalogProduk()
                    # self.error.setText(result_pass)

                else:
                    self.error.setText("Invalid username or password")
            else:
                self.error.setText("Invalid username or password")
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
            
class KatalogScreen(QDialog):
    def __init__(self):
        super(KatalogScreen, self).__init__()
        loadUi("katalog.ui",self)
        
        #set gambar
        self.logoLM.setPixmap(QPixmap('./images/logo.jpeg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        #redirect clicked button
        self.tambahproduk.clicked.connect(self.gotoadd)
        self.editButton.clicked.connect(self.gotoEditProduk)
        self.hapusButton.clicked.connect(self.gotoHapusProduk)
        self.reloadButton.clicked.connect(self.showProdukfunction)
        self.showProdukfunction()

        # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        # event = EventScreen()
        # widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        # konten = KontenScreen()
        # widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
    def gotoForumDiskusi(self):
        # forumDiskusi = ForumDiskusiScreen()
        # widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #fungsi untuk tambah produk
    def gotoadd(self):
        addProduk = AddProdukScreen()
        widget.addWidget(addProduk)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    #fungsi untuk tambah produk
    def gotoEditProduk(self):
        editProduk = EditProdukScreen()
        widget.addWidget(editProduk)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    # def gotofilter(self):
    #     conn = None
    #     params = config()
    #     conn = psycopg2.connect(**params)
    #     cur = conn.cursor()
    #     try:
    #         batch = self.inputBatch.text()
    #         try:
    #             # kalo ada input kategori
    #             kategori = self.inputKategori.text()
    #             if ((kategori != 'Atasan') and (kategori != 'Bawahan') and (kategori !='Outer') and (kategori !='Masker' ) and (kategori != 'Aksesoris')):
    #                 self.error.setText("Kategori tidak ada. Pilih salah satu diantara 'Atasan', 'Bawahan', 'Outer', 'Masker', dan 'Aksesoris'")
    #             else: 
    #                 filter_info= (batch,kategori)
    #                 query = """SELECT * FROM produk WHERE batch=%s and kategori = %s"""
    #                 result = cur.execute(query,filter_info)
    #                 rowNumber = cur.rowcount
    #                 # currRow = 0
    #                 self.tabelProduk.setRowCount(0)
    #                 if rowNumber ==0:
    #                     self.error.setText("Tidak ada data yang sesuai")
    #                 else:
    #                 # apabila username/ password ga ada
    #                     for row_number,row_data in enumerate(result):
    #                         self.tabelProduk.insertRow(row_number)
    #                         for column_number, data in enumerate(row_data):
    #                             self.tabelProduk.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

    #         # kalo ga ada input kategori
    #         except (ValueError):
    #             filter_info= (batch)
    #             query = """SELECT * FROM produk WHERE batch=%s"""
    #             result = cur.execute(query,filter_info)
    #             rowNumber = cur.rowcount
    #             # currRow = 0
    #             self.tabelProduk.setRowCount(0)
    #             if rowNumber ==0:
    #                 self.error.setText("Tidak ada data yang sesuai")
    #             else:
    #             # apabila username/ password ga ada
    #                 for row_number,row_data in enumerate(result):
    #                     self.tabelProduk.insertRow(row_number)
    #                     for column_number, data in enumerate(row_data):
    #                         self.tabelProduk.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
    #     # kalo ga ada input batch 
    #     except(ValueError):
    #         try:
    #             # kalo ada input kategori
    #             kategori = self.inputKategori.text()
    #             if ((kategori != 'Atasan') and (kategori != 'Bawahan') and (kategori !='Outer') and (kategori !='Masker' ) and (kategori != 'Aksesoris')):
    #                 self.error.setText("Kategori tidak ada. Pilih salah satu diantara 'Atasan', 'Bawahan', 'Outer', 'Masker', dan 'Aksesoris'")
    #             else: 
    #                 filter_info= (kategori)
    #                 query = """SELECT * FROM produk WHERE kategori = %s"""
    #                 result = cur.execute(query,filter_info)
    #                 rowNumber = cur.rowcount
    #                 # currRow = 0
    #                 self.tabelProduk.setRowCount(0)
    #                 if rowNumber ==0:
    #                     self.error.setText("Tidak ada data yang sesuai")
    #                 else:
    #                 # apabila username/ password ga ada
    #                     for row_number,row_data in enumerate(result):
    #                         self.tabelProduk.insertRow(row_number)
    #                         for column_number, data in enumerate(row_data):
    #                             self.tabelProduk.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

    #         # kalo ga ada input kategori
    #         except(ValueError):
    #             self.error.setText("Masukkan inputan yang valid untuk difilter!")
               
        
    #     # connect to the PostgreSQL server
    #     conn = None
    #     params = config()
    #     conn = psycopg2.connect(**params)
    #     cur = conn.cursor()
    #     # query = 'SELECT password FROM admin WHERE username =\''+user+"\'"
    #     filter_info= (batch, kategori)
    #     query = """SELECT * FROM produk WHERE batch=%s and kategori = %s"""
    #     result = cur.execute(query,filter_info)
    #     rowNumber = cur.rowcount
    #     # currRow = 0
    #     self.tabelProduk.setRowCount(0)
    #     if rowNumber ==0:
    #         self.error.setText("Tidak ada data yang sesuai")
    #     else:
    #     # apabila username/ password ga ada
    #         for row_number,row_data in enumerate(result):
    #             self.tabelProduk.insertRow(row_number)
    #             for column_number, data in enumerate(row_data):
    #                 self.tabelProduk.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))



    #fungsi untuk hapus produk
    def gotoHapusProduk(self):
        idProdukCRUD = self.inputidProduk.text()
        if (len(idProdukCRUD) != 0):
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "DELETE FROM produk WHERE idProduk =\'"+idProdukCRUD+"\'"
            cur.execute(query)
            conn.commit()
            self.error.setText("Berhasil menghapus produk.")
            cur.close()
        else: 
            self.error.setText("Pastikan id Produk yang ingin dihapus valid dan ada!")
    
    def showProdukfunction(self):

        # Membersihkan apabila ada pesan error sebelumnya         
        self.error.setText('')

        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = 'SELECT * FROM produk'
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.tabelProduk.setRowCount(0)
        if rowNumber ==0:
            self.error.setText("Belum ada data.")
        else:
        # apabila username/ password ga ada
            for row_number,row_data in enumerate(result):
                self.tabelProduk.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelProduk.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

# Untuk edit screen  
class EditProdukScreen(QDialog):

    def __init__(self):
        super(EditProdukScreen, self).__init__()
        loadUi("editKatalog.ui",self)
        # set gambar
        self.logoLM.setPixmap(QPixmap('./images/logo.jpeg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        # redirect clicked button
        self.editButton.clicked.connect(self.editProdukfunction)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)
        self.H_Logout.clicked.connect(self.gotoLogin)

    # fungsi sidebar.
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def editProdukfunction(self):
        try:
            namaProduk = self.inputNama.text()
            batch = int(self.inputBatch.text())
            kategori = self.inputKategori.text()
            harga = float(self.inputHarga.text())
            quantity = int(self.inputKuantitas.text())
            berat = float(self.inputBerat.text())
            deskripsi = self.inputDeskripsi.toPlainText()
            link = self.inputLink.text()
            idProdukCRUD = self.inputidProduk.text()
            if ((kategori != 'Atasan') and (kategori != 'Bawahan') and (kategori !='Outer') and (kategori !='Masker' ) and (kategori != 'Aksesoris')):
                self.error.setText("Kategori tidak ada. Pilih salah satu diantara 'Atasan', 'Bawahan', 'Outer', 'Masker', dan 'Aksesoris'")
            else: 
                try: 
                    # connect to the PostgreSQL server
                    conn = None
                    params = config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    # query = 'SELECT password FROM admin WHERE username =\''+user+"\'"
                    # produk_info = [namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link]
                    produk_info = (namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link, idProdukCRUD)
                    query = """UPDATE produk SET namaProduk=%s, batch=%s, kategori=%s, harga=%s, quantity=%s, berat=%s, deskripsi=%s, link=%s WHERE idProduk =%s"""
                    cur.execute(query,produk_info)
                    conn.commit()
                    conn.close()
                    QMessageBox.about(self,'Edit Produk', 'Produk berhasil diedit!')
                    self.error.setText('')
                except:
                    QMessageBox.about(self, 'Edit Produk', 'Produk gagal diupload. Pastikan semua data terisi!')
        except:
            self.error.setText('Pastikan semua data terisi dan valid!')

     
class AddProdukScreen(QDialog):
    def __init__(self):
        super(AddProdukScreen, self).__init__()
        loadUi("tambahProdukKatalog.ui",self)

        # set gambar
        self.logoLM.setPixmap(QPixmap('./images/logo.jpeg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        # redirect clicked button
        self.unggahproduk.clicked.connect(self.addProdukFunction)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)
        self.H_Homepage.clicked.connect(self.reload)
        self.H_Logout.clicked.connect(self.gotoLogin)

    # fungsi sidebar.
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def reload(self):
        reload = AddProdukScreen()
        widget.addWidget(reload)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # fungsi sidebar
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addProdukFunction(self):
        try:
            namaProduk = self.inputNama.text()
            batch = int(self.inputBatch.text())
            kategori = self.inputKategori.text()
            harga = float(self.inputHarga.text())
            quantity = int(self.inputKuantitas.text())
            berat = float(self.inputBerat.text())
            deskripsi = self.inputDeskripsi.toPlainText()
            link = self.inputLink.text()
            
            if ((kategori != 'Atasan') and (kategori != 'Bawahan') and (kategori !='Outer') and (kategori !='Masker' ) and (kategori != 'Aksesoris')):
                self.error.setText("Kategori tidak ada. Pilih salah satu diantara 'Atasan', 'Bawahan', 'Outer', 'Masker', dan 'Aksesoris'")
            else:
                try: 
                    # connect to the PostgreSQL server
                    conn = None
                    params = config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    produk_info = (namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link)
                    query = """INSERT INTO produk(idProduk,namaProduk, batch, kategori, harga, quantity, berat, deskripsi, link) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cur.execute(query,produk_info)
                    conn.commit()
                    conn.close()
                    QMessageBox.about(self,'Tambah Produk', 'Produk berhasil ditambah!')
                    self.reload()
                except:
                    QMessageBox.about(self, 'Tambah Produk', 'Produk gagal diupload. Pastikan semua data terisi!')
                
        except:
            self.error.setText('Pastikan semua data terisi dan valid!')   



# main
app = QApplication(sys.argv)
start = LoginScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(start)
widget.setFixedHeight(1080)
widget.setFixedWidth(1920)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")