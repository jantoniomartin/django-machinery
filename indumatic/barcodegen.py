## code taken from https://code.djangoproject.com/wiki/Barcodes

from reportlab.lib.units import mm, inch
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart

class BarcodeDrawing(Drawing):
    def __init__(self, text_value, *args, **kw):
        barcode = createBarcodeDrawing('Code128', value=text_value, barWidth=0.02*inch, barHeight=1*inch, humanReadable=True, fontSize=24)
        Drawing.__init__(self,barcode.width,barcode.height,*args,**kw)       
        self.add(barcode, name='barcode')

if __name__=='__main__':
    #use the standard 'save' method to save barcode.gif, barcode.pdf etc
    #for quick feedback while working.
    BarcodeDrawing("HELLO WORLD").save(formats=['png',],outDir='.',fnRoot='barcode')
