import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as Navi
from matplotlib.figure import Figure






def open_csv(name, argument = None, ):
    df = pd.read_csv(name, encoding='utf-8').fillna(0)
    column_names = df.columns.values.tolist()
    if argument == "columns":
        return column_names
    else:
        return df
    


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5,dpi = 120):
        fig = Figure(figsize = (width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(fig)
        fig.tight_layout()
        

# GUI
class graph_from_csv(QMainWindow):
    def __init__(self):
        super(graph_from_csv, self).__init__()
        uic.loadUi("graph_csv_gui.ui", self)
        self.show()
        
        self.canvas = MatplotlibCanvas(self)
        self.verticalLayout1.addWidget(self.canvas)
        
        
        self.toolbar = Navi(self.canvas, self.centralwidget) ### check centralwidget
        self.horizontalLayout_1.addWidget(self.toolbar)
        self.canvas.hide()
        self.df = []
        self.label = self.findChild(QLabel, 'ColumnNames')
        self.FileButton.clicked.connect(self.getFile)
        self.PlotButton.clicked.connect(self.graph)
        
        
    def update(self, value):
        print()
        
    # plotting graph        
    def graph(self):
        X_column = str(self.comboBox_1.currentText())
        Y_column = str(self.comboBox_2.currentText())
        # self.scene = QtWidgets.QGraphicsScene()
        # self.view = QtWidgets.QGraphicsView(self.scene)  
        self.canvas.axes.cla()
        #toolbat 

        # self.proxy_widget = self.scene.addWidget(self.canvas)
        self.df = open_csv(self.filename)
        ax = self.canvas.axes
        ax.set_position([0.15, 0.15, 0.8, 0.8])
        
        ax.plot(self.df[X_column], self.df[Y_column])
        legend = ax.legend()
        legend.set_draggable(True)
        ax.set_xlabel(X_column)
        ax.set_ylabel(Y_column)
        ax.set_title(f'{Y_column} dependance on {X_column}')
        self.canvas.draw()
        self.canvas.show()
    
    #inputs data to the database; shows the BMI value
    def getFile(self):
        self.filename = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
        self.list_of_columns = open_csv(self.filename, "columns")
        self.comboBox_1.currentIndexChanged['QString'].connect(self.update)
        self.comboBox_2.currentIndexChanged['QString'].connect(self.update)
        self.comboBox_1.addItems(self.list_of_columns)
        self.comboBox_2.addItems(self.list_of_columns)


def main():
    app = QtWidgets.QApplication([])
    window = graph_from_csv()
    window.show()
    app.exec_()

    
if __name__ == "__main__":
    main()
    