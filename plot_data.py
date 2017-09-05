import pyart
import matplotlib.pyplot as plt
def plot_data(infilename, outpng, maxrange,rdr,year,month,day,hms):
  plt.close("all")
  radar = pyart.io.read_nexrad_archive(infilename)
  display = pyart.graph.RadarDisplay(radar)
  fig = plt.figure(figsize=(10, 10))
  title="Radar: "+rdr+" Year: "+year+" Month:"+month+" Day:"+day+" Time:"+hms+"UTC"
  fig.suptitle(title, fontsize=14, fontweight='bold')
  ax = fig.add_subplot(221)
  display.plot('velocity', 1, ax=ax, title='Doppler Velocity',
             colorbar_label='',
             axislabels=('', 'North South distance from radar (km)'))
  display.set_limits((-maxrange, maxrange), (-maxrange, maxrange), ax=ax)
  ax = fig.add_subplot(222)
  display.plot('reflectivity', 0, ax=ax,
             title='Reflectivity lowest', colorbar_label='',
             axislabels=('', ''))
  display.set_limits((-maxrange, maxrange), (-maxrange, maxrange), ax=ax)

  ax = fig.add_subplot(223)
  display.plot('reflectivity', 1, ax=ax,
             title='Reflectivity second', colorbar_label='')
  display.set_limits((-maxrange, maxrange), (-maxrange, maxrange), ax=ax)

  ax = fig.add_subplot(224)
  display.plot('cross_correlation_ratio', 0, ax=ax,
             title='Correlation Coefficient', colorbar_label='',
             axislabels=('East West distance from radar (km)', ''))
  display.set_limits((-maxrange, maxrange), (-maxrange, maxrange), ax=ax)
  plt.savefig(outpng)
  plt.close(fig)
  del fig
  del ax
  del display
  return outpng
  #plt.show()
