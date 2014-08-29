# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RelationReplicator
                                 A QGIS plugin
 Plugin to replicate child non spatial features in a 1:n relation with a
 spatial parent table
                              -------------------
        begin                : 2014-06-23
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Alexandre Neto / Cascais Ambiente
        email                : senhor.neto@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from relation_replicator_dialog import RelationReplicatorDialog
import os.path

class RelationReplicator:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RelationReplicator_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = RelationReplicatorDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Relation Replicator')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'RelationReplicator')
        self.toolbar.setObjectName(u'RelationReplicator')

        #self.valid_relations = []

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RelationReplicator', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/RelationReplicator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Replicate child features in relation'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Relation Replicator'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        self.mc = self.iface.mapCanvas()
        self.project = QgsProject.instance()
        self.rel_manager = self.project.relationManager()
        self.relations = self.rel_manager.relations()
        self.layer = self.mc.currentLayer()

        #Clear relations
        self.valid_relations = {}

        # Get all valid relations for the current layer
        self.get_valid_relations()

        #populate dialog combobox
        self.dlg.relations_combobox.clear()
        self.dlg.relations_combobox.addItems(list(self.valid_relations))

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            rel_name = self.dlg.relations_combobox.currentText()
            relation = self.valid_relations[rel_name]
            child_layer = relation.referencingLayer()
            parent_layer = self.layer

            # get referenced and referencing field
            rel_fields = relation.fieldPairs()
            for key in relation.fieldPairs():
                ref_ed_field = rel_fields[key]
                ref_ing_field = key

            # create an empty temporary feature that will be replicated
            temp_feature = QgsFeature()
            attributes = []

            # Get layer default values from provider
            # (this avoids problems with unique keys)
            provider = child_layer.dataProvider()

            for j in child_layer.pendingAllAttributesList():
                if provider.defaultValue(j):
                    attributes.append(provider.defaultValue(j))
                else:
                    attributes.append('34') #none

            temp_feature.setAttributes(attributes)

            # open feature form and waits for edits
            if self.iface.openFeatureForm(child_layer, temp_feature):

                # start edit command to allow undo\redo
                # TODO get layer name to put in Edit command
                child_layer.beginEditCommand("Add new rows in ...")

                new_attributes = temp_feature.attributes()
                print new_attributes

                # replicate child Layer's new record for each
                # of the selected features in the parent layer
                selected_ref_ed_keys = [feature.attribute(ref_ed_field) for feature in parent_layer.selectedFeatures()]

                for ref_key in selected_ref_ed_keys:
                    new_attributes[1] = ref_key
                    temp_feature.setAttributes(new_attributes)
                    new_feature = QgsFeature(temp_feature)
                    child_layer.addFeature(new_feature)

                child_layer.endEditCommand()
            else:
                pass
                # print "Cancelled"
                # child_layer.destroyEditCommand()

    def get_valid_relations(self):
        # purpose: get current layer relations
        layer = self.mc.currentLayer()
        relations = self.relations
        for rel_id in relations:
            relation = relations[rel_id]
            rel_ref_ed = relation.referencedLayer()
            if layer == rel_ref_ed:
                rel_name = relation.name()
                self.valid_relations[unicode(rel_name)] = relation
        return