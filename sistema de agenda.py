import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class AgendaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_events()
        self.avatar_path = None  # Variable para almacenar la ruta del avatar

    def init_ui(self):
        self.setWindowTitle('Agenda de Notas')
        self.setGeometry(100, 100, 800, 400)

        # Cargar la imagen de fondo
        self.background = QLabel(self)
        pixmap = QPixmap('background_image.jpg')  # Reemplaza 'background_image.jpg' con tu ruta de imagen
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())

        # Widgets de información personal
        self.name_label = QLabel('Nombre:')
        self.name_edit = QLineEdit()

        self.lastname_label = QLabel('Apellido:')
        self.lastname_edit = QLineEdit()

        self.ci_label = QLabel('Cédula de Identidad:')
        self.ci_edit = QLineEdit()

        self.address_label = QLabel('Dirección:')
        self.address_edit = QLineEdit()

        # Imagen de información personal
        self.personal_image_label = QLabel(self)
        self.personal_image_label.setFixedSize(150, 150)  # Tamaño fijo para la imagen de perfil
        self.personal_image_label.setPixmap(QPixmap('default_avatar.png'))  # Imagen de avatar por defecto
        self.personal_image_label.setStyleSheet("border: 2px solid black;")  # Borde para la imagen de perfil

        # Botón para cargar imagen de perfil
        self.load_image_button = QPushButton('Cargar imagen')
        self.load_image_button.clicked.connect(self.load_avatar)

        # Layout para imagen de perfil
        avatar_layout = QVBoxLayout()
        avatar_layout.addWidget(self.personal_image_label, alignment=Qt.AlignCenter)
        avatar_layout.addWidget(self.load_image_button, alignment=Qt.AlignCenter)
        avatar_layout.setAlignment(Qt.AlignCenter)

        # Layout para información personal
        personal_info_layout = QVBoxLayout()
        personal_info_layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.name_edit, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.lastname_label, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.lastname_edit, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.ci_label, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.ci_edit, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.address_label, alignment=Qt.AlignCenter)
        personal_info_layout.addWidget(self.address_edit, alignment=Qt.AlignCenter)
        personal_info_layout.addLayout(avatar_layout)
        personal_info_layout.setAlignment(Qt.AlignCenter)

        # Widgets de información de evento
        self.date_label = QLabel('Fecha:')
        self.date_edit = QLineEdit()

        self.time_label = QLabel('Hora:')
        self.time_edit = QLineEdit()

        self.desc_label = QLabel('Nota del Alumno:')
        self.desc_edit = QLineEdit()

        # Layout para información de evento
        event_info_layout = QVBoxLayout()
        event_info_layout.addWidget(self.date_label, alignment=Qt.AlignCenter)
        event_info_layout.addWidget(self.date_edit, alignment=Qt.AlignCenter)
        event_info_layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        event_info_layout.addWidget(self.time_edit, alignment=Qt.AlignCenter)
        event_info_layout.addWidget(self.desc_label, alignment=Qt.AlignCenter)
        event_info_layout.addWidget(self.desc_edit, alignment=Qt.AlignCenter)
        event_info_layout.setAlignment(Qt.AlignCenter)

        # Botones
        self.add_button = QPushButton('Agregar evento')
        self.edit_button = QPushButton('Editar evento seleccionado')
        self.delete_button = QPushButton('Eliminar evento seleccionado')
        self.clear_all_button = QPushButton('Limpiar todo')
        self.save_button = QPushButton('Guardar')  # Botón para guardar los eventos
        self.help_button = QPushButton('Ayuda')  # Botón de ayuda

        self.add_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.edit_button.setStyleSheet("background-color: #008CBA; color: white;")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white;")
        self.clear_all_button.setStyleSheet("background-color: #555555; color: white;")
        self.save_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.help_button.setStyleSheet("background-color: #FFC107; color: black;")  # Estilo del botón de ayuda

        # Conectar botones a métodos
        self.add_button.clicked.connect(self.add_event)
        self.edit_button.clicked.connect(self.edit_event)
        self.delete_button.clicked.connect(self.delete_event)
        self.clear_all_button.clicked.connect(self.clear_all_fields)
        self.save_button.clicked.connect(self.save_all_events)
        self.help_button.clicked.connect(self.show_help)  # Conectar el botón de ayuda

        # Añadir los botones al layout de botones
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.edit_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.delete_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.clear_all_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.help_button, alignment=Qt.AlignCenter)
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Lista de eventos
        self.events_list = QListWidget()
        self.events_list.itemClicked.connect(self.populate_event_fields)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addLayout(personal_info_layout)
        main_layout.addLayout(event_info_layout)
        main_layout.addWidget(self.events_list)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def load_avatar(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen de perfil", "", "Archivos de imagen (*.jpg *.png *.jpeg)", options=options)
        if file_path:
            self.avatar_path = file_path
            pixmap = QPixmap(file_path)
            self.personal_image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))  # Escalar imagen al tamaño fijo

    def add_event(self):
        name = self.name_edit.text()
        lastname = self.lastname_edit.text()
        ci = self.ci_edit.text()
        address = self.address_edit.text()

        date = self.date_edit.text()
        time = self.time_edit.text()
        desc = self.desc_edit.text()

        if not all([name, lastname, ci, address, date, time, desc]):
            QMessageBox.warning(self, 'Error', 'Por favor, completa todos los campos.')
            return

        event_str = f'Nombre: {name}, Apellido: {lastname}, CI: {ci}, Dirección: {address} - Fecha: {date}, Hora: {time}, Nota del Alumno: {desc}'
        self.events_list.addItem(event_str)

        self.save_event(name, lastname, ci, address, date, time, desc)

        self.clear_fields()

    def save_event(self, name, lastname, ci, address, date, time, desc):
        with open('events.txt', 'a') as f:
            event_str = f'Nombre: {name}, Apellido: {lastname}, CI: {ci}, Dirección: {address} - Fecha: {date}, Hora: {time}, Nota del Alumno: {desc}\n'
            f.write(event_str)

    def load_events(self):
        try:
            with open('events.txt', 'r') as f:
                for line in f:
                    self.events_list.addItem(line.strip())
        except FileNotFoundError:
            return

    def populate_event_fields(self, item):
        event_details = item.text()
        details_list = event_details.split(' - ')
        personal_details = details_list[0].split(', ')
        event_info = details_list[1].split(': ')

        self.name_edit.setText(personal_details[0].split(': ')[1])
        self.lastname_edit.setText(personal_details[1].split(': ')[1])
        self.ci_edit.setText(personal_details[2].split(': ')[1])
        self.address_edit.setText(personal_details[3].split(': ')[1])

        self.date_edit.setText(event_info[1].split(', ')[0])
        self.time_edit.setText(event_info[2].split(', ')[0])
        self.desc_edit.setText(event_info[3])

    def edit_event(self):
        current_item = self.events_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, 'Error', 'Por favor, selecciona un evento para editar.')
            return

        name = self.name_edit.text()
        lastname = self.lastname_edit.text()
        ci = self.ci_edit.text()
        address = self.address_edit.text()
        date = self.date_edit.text()
        time = self.time_edit.text()
        desc = self.desc_edit.text()

        if not all([name, lastname, ci, address, date, time, desc]):
            QMessageBox.warning(self, 'Error', 'Por favor, completa todos los campos.')
            return

        event_str = f'Nombre: {name}, Apellido: {lastname}, CI: {ci}, Dirección: {address} - Fecha: {date}, Hora: {time}, Nota del Alumno: {desc}'
        current_item.setText(event_str)

        self.save_to_file()

    def delete_event(self):
        current_item = self.events_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, 'Error', 'Por favor, selecciona un evento para eliminar.')
            return

        self.events_list.takeItem(self.events_list.row(current_item))
        self.save_to_file()

    def save_to_file(self):
        with open('events.txt', 'w') as f:
            for index in range(self.events_list.count()):
                event_item = self.events_list.item(index)
                event_details = event_item.text() + '\n'
                f.write(event_details)

    def save_all_events(self):
        with open('events.txt', 'w') as f:
            for index in range(self.events_list.count()):
                event_item = self.events_list.item(index)
                event_details = event_item.text() + '\n'
                f.write(event_details)

    def clear_fields(self):
        self.name_edit.clear()
        self.lastname_edit.clear()
        self.ci_edit.clear()
        self.address_edit.clear()
        self.date_edit.clear()
        self.time_edit.clear()
        self.desc_edit.clear()

    def clear_all_fields(self):
        self.clear_fields()
        self.events_list.clear()

    def show_help(self):
        QMessageBox.information(self, 'Ayuda', 
            'Esta es la aplicación de Agenda. Aquí puedes agregar, editar y eliminar eventos.\n\n'
            'Para agregar un evento:\n'
            '1. Completa todos los campos de información personal y de evento.\n'
            '2. Haz clic en "Agregar evento".\n\n'
            'Para editar un evento:\n'
            '1. Selecciona el evento que deseas editar.\n'
            '2. Modifica los campos necesarios.\n'
            '3. Haz clic en "Editar evento seleccionado".\n\n'
            'Para eliminar un evento:\n'
            '1. Selecciona el evento que deseas eliminar.\n'
            '2. Haz clic en "Eliminar evento seleccionado".\n\n'
            'Para limpiar todos los campos y eventos:\n'
            '1. Haz clic en "Limpiar todo".\n\n'
            'Para guardar todos los eventos en un archivo:\n'
            '1. Haz clic en "Guardar".')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    agenda_app = AgendaApp()
    agenda_app.show()
    sys.exit(app.exec_())


