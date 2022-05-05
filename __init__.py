# -*- coding: utf-8 -*-

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load NGQRosreestrTools class from file NGQRosreestrTools

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .qgis_easy_query import QGISEasyQuery
    return QGISEasyQuery(iface)
