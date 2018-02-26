Usage: 
```
python make_plot_all.py --logx --cms_text Preliminary --goms 0.1,0.3,0.5,1.0 --logy
python make_plot_cms.py --logx --cms_text Preliminary --goms 0.1,0.3,0.5
```

More details:
- Data is stored in DijetData objects. These load the g_q vs. m_{Z'} files in data/[CADI]_[obs/exp].dat. 
	- The data can also be saved as sigma_{95} vs. m_{Z'}, where sigma_{95}=excluded cross section times branching ratio to qq. This is converted to g_q using the reference cross sections in data/reference/*dat according to g_q = g_q0 * sqrt(xs / xs0). This behavior is controlled by the header row, e.g. in data/EXO16057_SR1_obs.dat, # m_med xs8. The number is sqrt(s). 
- Plots are created by the class GQSummaryPlot. 
- The executables are make_plot_*.py. These contain all the plot styling options, which are passed as function arguments to GQSummaryPlot::add_data() and GQSummaryPlot::draw(). 

Command line arguments:

`--analyses`: Analyses to plot, corresponding to filenames in data/*.dat. The order of analyses corresponds to the legend order (remembe that TLegends with multiple columns fill in entries from left to right, then top to bottom).

`--logx`

`--logy`

`--goms`: Gamma/M values to draw as dashed lines.

`--gom_fills`: Draw filled areas corresponding to excluded range, including the range of validity due to Gamma/M getting too large.

`--cms`: Draw CMS label.

`--cms_text [extra text]`: Draw CMS label with extra text, e.g. CMS Preliminary
