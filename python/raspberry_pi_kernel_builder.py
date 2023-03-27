import os
import shutil
import subprocess
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStatusBar,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.build_button = QPushButton("Build Kernel")
        self.build_dir_label = QLabel("Build Directory:")
        self.build_dir_edit = QLineEdit()
        self.download_button = QPushButton("Download Source")
        self.status_label = QLabel("")

        self.build_button.clicked.connect(self.build_kernel)
        self.download_button.clicked.connect(self.download_source)

        build_dir_layout = QHBoxLayout()
        build_dir_layout.addWidget(self.build_dir_label)
        build_dir_layout.addWidget(self.build_dir_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.build_button)
        button_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(build_dir_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setWindowTitle("Raspberry Pi Kernel Builder")
        self.resize(400, 300)

    def build_kernel(self):
        build_dir = self.build_dir_edit.text()
        if not build_dir:
            self.status_label.setText("Please enter build directory")
            return

        self.status_label.setText("Building kernel...")

        os.chdir(build_dir)

        if not self.run_command("./build_rpi_kernel.sh"):
            self.status_label.setText("Error building kernel")
            return

        if not self.run_command("make -j4"):
            self.status_label.setText("Error building kernel")
            return

        if not self.install_kernel():
            self.status_label.setText("Error installing kernel")
            return

        if not self.cleanup():
            self.status_label.setText("Error cleaning up")
            return

        self.status_label.setText("Finished.")

    def download_source(self):
        build_dir = self.build_dir_edit.text()
        if not build_dir:
            self.status_label.setText("Please enter build directory")
            return

        self.status_label.setText("Downloading kernel source...")

        os.chdir(build_dir)

        if not self.run_command("wget https://github.com/raspberrypi/linux/archive/rpi-3.18.y.zip"):
            self.status_label.setText("Error downloading kernel source")
            return

        if not self.run_command("unzip rpi-3.18.y.zip"):
            self.status_label.setText("Error unzipping kernel source")
            return

        self.status_label.setText("Kernel source downloaded successfully")

    def install_kernel(self):
        self.status_label.setText("Installing kernel...")

        if not self.run_command("sudo make modules_install"):
            return False

        if not self.run_command("sudo make headers_install"):
            return False

        return True

    def cleanup(self):
        self.status_label.setText("Cleaning up...")

        build_dir = self.build_dir_edit.text()

        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        return True

    def run_command(self, command):
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as err:
            self.status_label.setText("Command failed: " + str(err))
            return False

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

