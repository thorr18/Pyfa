# shipRemoteSensorDampenerCapNeedGF
#
# Used by:
# Ship: Keres
# Ship: Maulus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
