import PyQt5
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication
import sys
import test2
from source.namevariationfunctions import *


class MainWindow(QMainWindow, test2.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.input_path_txt = None
        self.output_path_txt = None
        self.output_name = None
        self.number_test_cases = None
        self.number_test_cases_lst = None
        self.function_list = None
        self.buttonReply = None
        self.perc_list = None
        self.final_perc = None
        self.perc_dict = None
        self.df_loaded = None
        self.final_df = None
        self.final_df_force = None
        self.columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name",
                        "Resulting Name", "Success"]

        self.NumberOfCasesText.editingFinished.connect(self.warn_cases)
        self.outputFileNameText.editingFinished.connect(self.warn_output_format)

        self.inputButton.clicked.connect(self.get_input_file)
        self.outputButton.clicked.connect(self.get_output_file)
        self.estimateButton.clicked.connect(self.get_estimate)
        self.submitButton.clicked.connect(self.get_final_output)

        self.InitialsPerc.editingFinished.connect(self.ip_spin_changed)
        self.CharExtPerc.editingFinished.connect(self.cep_spin_changed)
        self.CharRedPerc.editingFinished.connect(self.credp_spin_changed)
        self.CharRepPerc.editingFinished.connect(self.crepp_spin_changed)
        self.TranspositionPerc.editingFinished.connect(self.transp_spin_changed)
        self.DoubleCharPerc.editingFinished.connect(self.dcp_spin_changed)
        self.SpacesPerc.editingFinished.connect(self.sp_spin_changed)
        self.NameOrderPerc.editingFinished.connect(self.nop_spin_changed)
        self.TitlesPerc.editingFinished.connect(self.titlesp_spin_changed)
        self.MissNameCompPerc.editingFinished.connect(self.mncp_spin_changed)
        self.AlsoKnownAsPerc.editingFinished.connect(self.akap_spin_changed)

    def get_input_file(self):
        self.popup('Information', 'The format of the input file must be a csv and it should contain all the names in a'
                                  ' single column.')
        fname = QFileDialog.getOpenFileName(self, 'Open file', filter='csv(*.csv)')
        self.input_path_txt = fname[0]
        self.inputText.setText(self.input_path_txt)
        try:
            self.df_loaded = pd.read_csv(self.input_path_txt, delimiter=";", header=None, encoding='latin1')
        except pd.errors.EmptyDataError:
            self.popup('Warning', 'The file loaded is empty. Please choose another file.')
        else:
            if self.df_loaded.shape[1] != 1:
                self.popup("Warning", "The input file has {} columns instead of one. Please choose a file that contains"
                                      " all the names in a single column.".format(self.df_loaded.shape[1]))
                self.df_loaded = None
            else:
                self.df_loaded = list(self.df_loaded[0])

    def get_output_file(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.output_path_txt = file
        self.outputText.setText(self.output_path_txt)

    def get_estimate(self):
        if self.inputText.text().startswith('C:/'):
            if not self.inputText.text().endswith(".csv"):
                return self.popup("Warning", "The input path does not contain a csv file.")

        if not self.inputText.text().startswith('C:/'):
            self.df_loaded = self.convert(self.inputText.text().replace(", ", ","))

        if self.inputText.text() == "":
            return self.popup("Warning", "No input file was selected.")
        else:
            self.function_list = []
            self.perc_list = []
            self.final_df = pd.DataFrame(columns=self.columns)
            self.function_list = ["Initials", "Character Extension", "Character Reduction", "Character Replacement",
                                  "Transposition", "Double Characters", "Spaces", "Name Order", "Titles",
                                  "Missing Name Component", "Also Known As"]
            for name in self.df_loaded:
                self.final_df = self.final_df.append(get_name_var(name, self.function_list), ignore_index=True)

            self.TotalEstimate.display(len(self.final_df))
            self.initialsEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Initials']))
            self.charextEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Character Extension']))
            self.charredEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Character Reduction']))
            self.charrepEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Character Replacement']))
            self.transEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Transposition']))
            self.doublecharEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Double Characters']))
            self.spacesEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Spaces']))
            self.nameorderEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Name Order']))
            self.titlesEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Titles']))
            self.missnamecompEstimate.display(
                len(self.final_df[self.final_df['Variation Category'] == 'Missing Name Component']))
            self.akaEstimate.display(len(self.final_df[self.final_df['Variation Category'] == 'Alias']))

            self.popup("Estimates Calculated", "The estimates shown represent the maximum number of test cases that can be "
                                               "generated from each variation category.")

    def convert(self, name):
        list_of_names = list(name.split(","))
        return list_of_names

    def get_final_output(self):
        self.function_list = []
        self.perc_list = []
        self.final_df = pd.DataFrame(columns=self.columns)

        if self.inputText.text().startswith('C:/'):
            if not self.inputText.text().endswith(".csv"):
                return self.popup("Warning", "The input path does not contain a csv file.")

        if not self.inputText.text().startswith('C:/'):
            self.df_loaded = self.convert(self.inputText.text().replace(", ", ","))

        if self.inputText.text() == "":
            self.popup("Warning", "No input file was selected.")
        elif self.outputText.text() == "":
            self.popup("Warning", "No output path was selected.")
        elif self.outputFileNameText.text() == "":
            self.popup("Warning", "No output file name was specified.")
        elif self.ForceYes.isChecked():
            if self.NumberOfCasesText.text() != "":
                self.number_test_cases = int(self.NumberOfCasesText.text())

                self.final_df_force = pd.DataFrame(columns=self.columns)

                if self.Initials.isChecked():
                    self.function_list.append(self.Initials.text())
                    self.perc_list.append(self.InitialsPerc.value())

                if self.DoubleCharacters.isChecked():
                    self.function_list.append(self.DoubleCharacters.text())
                    self.perc_list.append(self.DoubleCharPerc.value())

                if self.CharacterExtension.isChecked():
                    self.function_list.append(self.CharacterExtension.text())
                    self.perc_list.append(self.CharExtPerc.value())

                if self.Spaces.isChecked():
                    self.function_list.append(self.Spaces.text())
                    self.perc_list.append(self.SpacesPerc.value())

                if self.CharacterReplacement.isChecked():
                    self.function_list.append(self.CharacterReplacement.text())
                    self.perc_list.append(self.CharRepPerc.value())

                if self.NameOrder.isChecked():
                    self.function_list.append(self.NameOrder.text())
                    self.perc_list.append(self.NameOrderPerc.value())

                if self.CharacterReduction.isChecked():
                    self.function_list.append(self.CharacterReduction.text())
                    self.perc_list.append(self.CharRedPerc.value())

                if self.Titles.isChecked():
                    self.function_list.append(self.Titles.text())
                    self.perc_list.append(self.TitlesPerc.value())

                if self.Transposition.isChecked():
                    self.function_list.append(self.Transposition.text())
                    self.perc_list.append(self.TranspositionPerc.value())

                if self.MissingNameComp.isChecked():
                    self.function_list.append(self.MissingNameComp.text())
                    self.perc_list.append(self.MissNameCompPerc.value())

                if self.AlsoKnownAs.isChecked():
                    self.function_list.append(self.AlsoKnownAs.text())
                    self.perc_list.append(self.AlsoKnownAsPerc.value())

                if sum(self.perc_list) == 0:
                    return self.popup("Error", "No percentages were selected.")
                elif sum(self.perc_list) < 100:
                    return self.popup("Error", "The percentages do not add up to 100%. The current sum of percentages"
                                               "is {}".format(sum(self.perc_list)))

                for i, j in enumerate(self.perc_list):
                    if self.perc_list[i] == 0:
                        pass
                    else:
                        self.perc_list[i] = self.perc_list[i] / 100

                self.number_test_cases_lst = [self.number_test_cases] * len(self.perc_list)
                self.final_perc = []
                for num1, num2 in zip(self.perc_list, self.number_test_cases_lst):
                    self.final_perc.append(round(num1 * num2))
                self.perc_dict = dict(zip(self.function_list, self.final_perc))
                for name in self.df_loaded:
                    self.final_df = self.final_df.append(get_name_var(name, self.function_list), ignore_index=True)

                counter_of_exceeting_perc = 0
                for key, value in self.perc_dict.items():
                    temp = self.final_df[self.final_df["Variation Category"] == key]
                    if value <= len(temp):
                        self.final_df_force = self.final_df_force.append(temp.sample(n=value), ignore_index=True)
                    else:
                        self.final_df_force = self.final_df_force.append(temp, ignore_index=True)
                        counter_of_exceeting_perc += 1

                self.final_df = self.final_df_force
                if len(self.final_df) != self.number_test_cases:
                    self.popup("Warning", 'The percentage of {} category/ies is a greater number of name '
                                          'variations than the estimated maximum. As a result, the estimated '
                                          'maximum will be saved and the total number of test cases will be {} '
                                          'instead of {}.'.
                               format(counter_of_exceeting_perc, len(self.final_df), self.number_test_cases))

                self.popup("Output Successfully Generated", "Would you like to save the output?", save=True)

            else:
                self.popup("Warning", '"Number of test cases to be generated" is empty.')

        else:
            if self.Initials.isChecked():
                self.function_list.append(self.Initials.text())

            if self.DoubleCharacters.isChecked():
                self.function_list.append(self.DoubleCharacters.text())

            if self.CharacterExtension.isChecked():
                self.function_list.append(self.CharacterExtension.text())

            if self.Spaces.isChecked():
                self.function_list.append(self.Spaces.text())

            if self.CharacterReplacement.isChecked():
                self.function_list.append(self.CharacterReplacement.text())

            if self.NameOrder.isChecked():
                self.function_list.append(self.NameOrder.text())

            if self.CharacterReduction.isChecked():
                self.function_list.append(self.CharacterReduction.text())

            if self.Titles.isChecked():
                self.function_list.append(self.Titles.text())

            if self.Transposition.isChecked():
                self.function_list.append(self.Transposition.text())

            if self.MissingNameComp.isChecked():
                self.function_list.append(self.MissingNameComp.text())

            if self.AlsoKnownAs.isChecked():
                self.function_list.append(self.AlsoKnownAs.text())

            for name in self.df_loaded:
                self.final_df = self.final_df.append(get_name_var(name, self.function_list), ignore_index=True)

            self.popup("Output Successfully Generated", "Would you like to save the output?", save=True)

    def popup(self, title, message, save=False):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        if save:
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.popup_clicked)
        else:
            msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def popup_clicked(self, i):
        if i.text() == "Save":
            self.output_name = self.outputFileNameText.text()
            self.final_df.to_csv(self.output_path_txt + "/" + self.output_name + ".csv", index=False,
                                 encoding='utf-8-sig')

    def warn_cases(self):
        if self.TotalEstimate.value() != 0:
            if int(self.NumberOfCasesText.text()) > self.TotalEstimate.value():
                self.popup("Warning", "Number of test cases entered is larger than the estimated maximum. Please choose"
                                      " a smaller number.")

    def warn_output_format(self):
        if self.outputFileNameText.text().endswith(".csv"):
            self.popup("Waring", 'The output file name does not require a ".csv" at the end.')
            self.outputFileNameText.setText(self.outputFileNameText.text().replace(".csv", ""))

    def ip_spin_changed(self):
        self.InitialsPerc.setMaximum(self.InitialsPerc.value())

        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())

        max_value = 100 - self.spin_value_sum

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def cep_spin_changed(self):
        self.CharExtPerc.setMaximum(self.CharExtPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def credp_spin_changed(self):
        self.CharRedPerc.setMaximum(self.CharRedPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def crepp_spin_changed(self):
        self.CharRepPerc.setMaximum(self.CharRepPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def transp_spin_changed(self):
        self.TranspositionPerc.setMaximum(self.TranspositionPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def dcp_spin_changed(self):
        self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def sp_spin_changed(self):
        self.SpacesPerc.setMaximum(self.SpacesPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def nop_spin_changed(self):
        self.NameOrderPerc.setMaximum(self.NameOrderPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def titlesp_spin_changed(self):
        self.TitlesPerc.setMaximum(self.TitlesPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def mncp_spin_changed(self):
        self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)

        if self.AlsoKnownAsPerc.value() == 0:
            self.AlsoKnownAsPerc.setMaximum(max_value)
        else:
            self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value() + max_value)

    def akap_spin_changed(self):
        self.AlsoKnownAsPerc.setMaximum(self.AlsoKnownAsPerc.value())
        self.spin_value_sum = (self.InitialsPerc.value() + self.CharExtPerc.value() + self.CharRedPerc.value() +
                               self.CharRepPerc.value() + self.TranspositionPerc.value() + self.DoubleCharPerc.value() +
                               self.SpacesPerc.value() + self.NameOrderPerc.value() + self.TitlesPerc.value() +
                               self.MissNameCompPerc.value() + self.AlsoKnownAsPerc.value())
        max_value = 100 - self.spin_value_sum

        if self.InitialsPerc.value() == 0:
            self.InitialsPerc.setMaximum(max_value)
        else:
            self.InitialsPerc.setMaximum(self.InitialsPerc.value() + max_value)

        if self.CharRedPerc.value() == 0:
            self.CharRedPerc.setMaximum(max_value)
        else:
            self.CharRedPerc.setMaximum(self.CharRedPerc.value() + max_value)

        if self.CharRepPerc.value() == 0:
            self.CharRepPerc.setMaximum(max_value)
        else:
            self.CharRepPerc.setMaximum(self.CharRepPerc.value() + max_value)

        if self.TranspositionPerc.value() == 0:
            self.TranspositionPerc.setMaximum(max_value)
        else:
            self.TranspositionPerc.setMaximum(self.TranspositionPerc.value() + max_value)

        if self.DoubleCharPerc.value() == 0:
            self.DoubleCharPerc.setMaximum(max_value)
        else:
            self.DoubleCharPerc.setMaximum(self.DoubleCharPerc.value() + max_value)

        if self.SpacesPerc.value() == 0:
            self.SpacesPerc.setMaximum(max_value)
        else:
            self.SpacesPerc.setMaximum(self.SpacesPerc.value() + max_value)

        if self.NameOrderPerc.value() == 0:
            self.NameOrderPerc.setMaximum(max_value)
        else:
            self.NameOrderPerc.setMaximum(self.NameOrderPerc.value() + max_value)

        if self.TitlesPerc.value() == 0:
            self.TitlesPerc.setMaximum(max_value)
        else:
            self.TitlesPerc.setMaximum(self.TitlesPerc.value() + max_value)

        if self.MissNameCompPerc.value() == 0:
            self.MissNameCompPerc.setMaximum(max_value)
        else:
            self.MissNameCompPerc.setMaximum(self.MissNameCompPerc.value() + max_value)

        if self.CharExtPerc.value() == 0:
            self.CharExtPerc.setMaximum(max_value)
        else:
            self.CharExtPerc.setMaximum(self.CharExtPerc.value() + max_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
