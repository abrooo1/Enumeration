def classFactory(iface):
    from .main_plugin import ETH_preEA_Tool
    return ETH_preEA_Tool(iface)