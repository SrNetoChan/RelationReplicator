# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RelationReplicator
                                 A QGIS plugin
 Plugin to replicate child non spatial features in a 1:n relation with a spatial parent table
                             -------------------
        begin                : 2014-06-23
        copyright            : (C) 2014 by Alexandre Neto / Cascais Ambiente
        email                : senhor.neto@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load RelationReplicator class from file RelationReplicator.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .relation_replicator import RelationReplicator
    return RelationReplicator(iface)
