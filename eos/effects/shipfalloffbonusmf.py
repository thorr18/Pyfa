# shipFalloffBonusMF
#
# Used by:
# Ship: Chremoas
# Ship: Dramiel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
