from RgbStripManager import RgbStripManager

mgr = RgbStripManager()

if (!mgr.try_get_default_sequence()):
	return

mgr.run()