from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import *
import sys

import test2
from src.namevariationfunctions import *


class MainWindow(QMainWindow, test2.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.input_path_txt = None
        self.output_path_txt = None
        self.number_test_cases = None
        self.number_test_cases_lst = None
        self.function_list = None
        self.perc_list = None
        self.final_perc = None
        self.perc_dict = None
        self.df_loaded = None
        self.final_df = None
        self.final_df_len = None
        self.columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name",
                        "Resulting Name", "Success"]

        self.submitButton.clicked.connect(self.get_final_output)


    def get_final_output(self):
        self.input_path_txt = self.inputText.text()
        self.output_path_txt = self.outputText.text()
        self.df_loaded = pd.read_csv(self.input_path_txt, delimiter="\n", header=None)
        self.df_loaded = list(self.df_loaded[0])
        self.function_list = []
        self.perc_list = []
        self.final_df = pd.DataFrame(columns=self.columns)

        if self.ForceYes.isChecked():
            if self.NumberOfCasesText.text() != "":
                self.number_test_cases = int(self.NumberOfCasesText.text())


                if self.Initials.isChecked():
                    self.function_list.append(self.Initials.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.InitialsPerc.currentText())

                if self.DoubleCharacters.isChecked():
                    self.function_list.append(self.DoubleCharacters.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.DoubleCharPerc.currentText())

                if self.CharacterExtension.isChecked():
                    self.function_list.append(self.CharacterExtension.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.CharExtPerc.currentText())

                if self.Spaces.isChecked():
                    self.function_list.append(self.Spaces.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.SpacesPerc.currentText())

                if self.CharacterReplacement.isChecked():
                    self.function_list.append(self.CharacterReplacement.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.CharRepPerc.currentText())

                if self.NameOrder.isChecked():
                    self.function_list.append(self.NameOrder.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.NameOrderPerc.currentText())

                if self.CharacterReduction.isChecked():
                    self.function_list.append(self.CharacterReduction.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.CharRedPerc.currentText())

                if self.Titles.isChecked():
                    self.function_list.append(self.Titles.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.TitlesPerc.currentText())

                if self.Transposition.isChecked():
                    self.function_list.append(self.Transposition.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.TranspositionPerc.currentText())

                if self.MissingNameComp.isChecked():
                    self.function_list.append(self.MissingNameComp.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.MissNameCompPerc.currentText())

                if self.AlsoKnownAs.isChecked():
                    self.function_list.append(self.AlsoKnownAs.text())
                    if self.ForceYes.isChecked():
                        self.perc_list.append(self.AlsoKnownAsPerc.currentText())

                if self.ForceYes.isChecked():
                    for i, j in enumerate(self.perc_list):
                        self.perc_list[i] = int(j.replace("%", ""))
                        if self.perc_list[i] == 0:
                            pass
                        else:
                            self.perc_list[i] = self.perc_list[i]/100

                    if sum(self.perc_list) != 1:
                        msg = QMessageBox()
                        msg.setWindowTitle("Warning")
                        msg.setText("The percentages chosen do not add up to 100%.\n Current percentage: {}%".
                                    format(round(sum(self.perc_list)*100)))
                        msg.setIcon(QMessageBox.Information)
                        msg.setStandardButtons(QMessageBox.Ok)
                        y = msg.exec_()

                    else:
                        self.number_test_cases_lst = [self.number_test_cases]*len(self.perc_list)
                        self.final_perc = []
                        for num1, num2 in zip(self.perc_list, self.number_test_cases_lst):
                            self.final_perc.append(round(num1 * num2))
                        self.perc_dict = dict(zip(self.function_list, self.final_perc))
                        for name in self.df_loaded:
                            self.final_df = self.final_df.append(get_name_var(name, self.function_list), ignore_index=True)

                        self.final_df.to_csv(self.output_path_txt)
                        self.final_df_len = "The file saved has {} records.".format(len(self.final_df))
                        msg = QMessageBox()
                        msg.setWindowTitle("Output Successfully saved")
                        msg.setText("The file generated was saved at: " + self.output_path_txt)
                        msg.setIcon(QMessageBox.Information)
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.setInformativeText(self.final_df_len)
                        # msg.setDetailedText("Details:\n"
                        #                     "Initials:\n"
                        #                     "Character Extension:\n"
                        #                     "Character Replacement:\n"
                        #                     "Character Reduction:\n"
                        #                     "Transposition:\n"
                        #                     "Double Characters:\n"
                        #                     "Spaces:\n"
                        #                     "Name Order:\n"
                        #                     "Titles:\n"
                        #                     "Missing Name Component:\n"
                        #                     "Also Known As:\n")
                        x = msg.exec_()
                else:
                    for name in self.df_loaded:
                        self.final_df = self.final_df.append(get_name_var(name, self.function_list), ignore_index=True)

                    self.final_df.to_csv(self.output_path_txt)
                    self.final_df_len = "The file saved has {} records.".format(len(self.final_df))
                    msg = QMessageBox()
                    msg.setWindowTitle("Output successfully saved")
                    msg.setText("The file generated was saved at: " + self.output_path_txt)
                    msg.setIcon(QMessageBox.Information)
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setInformativeText(self.final_df_len)
                    # msg.setDetailedText("Details:\n"
                    #                     "Initials:\n"
                    #                     "Character Extension:\n"
                    #                     "Character Replacement:\n"
                    #                     "Character Reduction:\n"
                    #                     "Transposition:\n"
                    #                     "Double Characters:\n"
                    #                     "Spaces:\n"
                    #                     "Name Order:\n"
                    #                     "Titles:\n"
                    #                     "Missing Name Component:\n"
                    #                     "Also Known As:\n")
                    x = msg.exec_()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText('"Number of test cases to be generated" is empty.')
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                y = msg.exec_()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()