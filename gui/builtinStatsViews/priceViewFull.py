#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
from gui.statsView import StatsView
from gui import builtinStatsViews
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
import service
import locale

class PriceViewFull(StatsView):
    name = "priceViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedShip = 0
        self._cachedFittings = 0
        self._cachedTotal = 0

    def getHeaderText(self, fit):
        return "Price"

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel
        self.headerPanel = headerPanel

        headerContentSizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer = headerPanel.GetSizer()
        hsizer.Add(headerContentSizer, 0, 0, 0)
        self.labelEMStatus = wx.StaticText(headerPanel, wx.ID_ANY, "")
        headerContentSizer.Add(self.labelEMStatus)
        headerPanel.GetParent().AddToggleItem(self.labelEMStatus)

        gridPrice = wx.GridSizer(1, 3, 0, 0)
        contentSizer.Add(gridPrice, 0, wx.EXPAND | wx.ALL, 0)
        for type in ("ship", "fittings", "total"):
            image = "%sPrice_big" % type if type != "ship" else "ship_big"
            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box, 0, wx.ALIGN_TOP)

            box.Add(BitmapLoader.getStaticBitmap(image, contentPanel, "gui"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00 ISK")
            setattr(self, "labelPrice%s" % type.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        if fit is not None:
            self.fit = fit
            # Compose a list of all the data we need & request it
            typeIDs = []
            typeIDs.append(fit.ship.item.ID)

            for mod in fit.modules:
                if not mod.isEmpty:
                    typeIDs.append(mod.itemID)

            for drone in fit.drones:
                for _ in xrange(drone.amount):
                    typeIDs.append(drone.itemID)
            for cargo in fit.cargo:
                for _ in xrange(cargo.amount):
                    typeIDs.append(cargo.itemID)

            sMkt = service.Market.getInstance()
            sMkt.getPrices(typeIDs, self.processPrices)
            self.labelEMStatus.SetLabel("Updating prices...")
        else:
            self.labelEMStatus.SetLabel("")
            self.labelPriceShip.SetLabel("0.0 ISK")
            self.labelPriceFittings.SetLabel("0.0 ISK")
            self.labelPriceTotal.SetLabel("0.0 ISK")
            self._cachedFittings = self._cachedShip = self._cachedTotal = 0
            self.panel.Layout()

    def processPrices(self, prices):
        shipPrice = prices[0].price
        modPrice = sum(map(lambda p: p.price or 0, prices[1:]))

        self.labelEMStatus.SetLabel("")

        if self._cachedShip != shipPrice:
            self.labelPriceShip.SetLabel("%s ISK" % formatAmount(shipPrice, 3, 3, 9, currency=True))
            self.labelPriceShip.SetToolTip(wx.ToolTip(locale.format('%.2f', shipPrice, 1)))
            self._cachedShip = shipPrice
        if self._cachedFittings != modPrice:
            self.labelPriceFittings.SetLabel("%s ISK" % formatAmount(modPrice, 3, 3, 9, currency=True))
            self.labelPriceFittings.SetToolTip(wx.ToolTip(locale.format('%.2f', modPrice, 1)))
            self._cachedFittings = modPrice
        if self._cachedTotal != (shipPrice+modPrice):
            self.labelPriceTotal.SetLabel("%s ISK" % formatAmount(shipPrice + modPrice, 3, 3, 9, currency=True))
            self.labelPriceTotal.SetToolTip(wx.ToolTip(locale.format('%.2f', (shipPrice + modPrice), 1)))
            self._cachedTotal = shipPrice + modPrice
        self.panel.Layout()

PriceViewFull.register()
