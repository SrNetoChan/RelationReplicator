# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'relation_replicator_dialog_base.ui'
#
# Created: Wed Jun 25 10:50:42 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_RelationReplicatorDialogBase(object):
    def setupUi(self, RelationReplicatorDialogBase):
        RelationReplicatorDialogBase.setObjectName(_fromUtf8("RelationReplicatorDialogBase"))
        RelationReplicatorDialogBase.resize(400, 120)
        self.button_box = QtGui.QDialogButtonBox(RelationReplicatorDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 80, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.relations_combobox = QtGui.QComboBox(RelationReplicatorDialogBase)
        self.relations_combobox.setGeometry(QtCore.QRect(60, 20, 271, 22))
        self.relations_combobox.setObjectName(_fromUtf8("relations_combobox"))

        self.retranslateUi(RelationReplicatorDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), RelationReplicatorDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), RelationReplicatorDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(RelationReplicatorDialogBase)

    def retranslateUi(self, RelationReplicatorDialogBase):
        RelationReplicatorDialogBase.setWindowTitle(_translate("RelationReplicatorDialogBase", "Relation Replicator", None))

