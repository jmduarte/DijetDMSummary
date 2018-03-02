import os
import sys
sys.path.append("./python/")
from gq_summary_plot import GQSummaryPlot, seaborn_colors
from dijet_data import DijetData

# Set all the plot styling here
style = {
	"default":{
		"line_color":1,
		"line_width":2,
		"line_style":1,
		"marker_style":20,
		"marker_size":0,
		"marker_color":1,
		"fill_style":0,
		"fill_color":0,
	}, "EXO16046_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 3),		
	}, "EXO16056_narrow_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 2),		
	}, "EXO16056_wide_obs":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 3),		
	}, "EXO16057_SR1_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR2_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO17001_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 2),		
	}, "CDF_Run1":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 5),		
		"line_style":8,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 5),		
	}, "CDF_Run2":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 3),		
		"line_style":6,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 3),
	}, "UA2":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 0),		
		"line_style":4,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 0),
	}, "EXO14005_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 1),
		"line_style":1, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 1),
	}, "ATLAS_8TeV":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 4),
		"line_style":3, 
		"fill_color":seaborn_colors.get_root_color("Greens_d", 4),
	}, "ATLAS_EXOT1701_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 4),
		"line_style":3, 
		"fill_color":seaborn_colors.get_root_color("Reds_d", 4),
	}
}

legend_entries = {
	"EXO16046_obs":"CMS Dijet #chi, 13 TeV",
	"EXO16056_narrow_obs":"CMS Narrow Dijet, 13 TeV",
	"EXO16056_wide_obs":"CMS Wide Dijet, 13 TeV",
	"EXO16057_SR1_obs":"CMS Dijet w/b Tag, 8 TeV",
	"EXO16057_SR2_obs":False, # Only need one of SR1/SR2 for the legend
	"EXO17001_obs":"CMS Boosted Dijet, 13 TeV",
	"CDF_Run1":"CDF Run1",
	"CDF_Run2":"CDF Run2",
	"UA2":"UA2",
	"EXO14005_obs":"CMS Dijet, 8 TeV",
	"ATLAS_8TeV":"ATLAS Dijet, 8 TeV",
	"ATLAS_EXOT1701_obs":"ATLAS Boosted Dijet, 13 TeV"
}

# Maximum Gamma/M values
max_gom = {
	"EXO16056_narrow_obs":0.12,
	"EXO16056_wide_obs":0.3,
	"EXO16057_SR1_obs":0.12,
	"EXO16057_SR2_obs":0.12,
	"EXO17001_obs":0.12,
	"EXO14005_obs":0.12,
	"CDF_Run1":0.12,
	"CDF_Run2":0.12,
	"UA2":0.12,
	"ATLAS_8TeV":0.12,
	"ATLAS_EXOT1701_obs":0.12,
}

# Maximum gq values 
max_gq = {
	"EXO16046_obs":1.45,
}

if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser(description='Make g_q summary plot')
	parser.add_argument('--analyses', type=str, default="\
EXO17001_obs,EXO16057_SR1_obs,EXO16046_obs,\
EXO14005_obs,EXO16056_narrow_obs,EXO16056_wide_obs,\
ATLAS_EXOT1701_obs,ATLAS_8TeV,UA2,\
CDF_Run1,CDF_Run2,EXO16057_SR2_obs", help="Analyses to plot (CADI lines, comma-separated)") 
	parser.add_argument('--logx', action='store_true', help='Log x')
	parser.add_argument('--logy', action='store_true', help='Log y')
	parser.add_argument('--goms', type=str, default="0.1,0.3", help='List of Gamma/M values to draw')
	parser.add_argument('--gom_fills', action='store_true', help='Draw fills for exclusions with Gamma/M or gq upper bound')	
	cms_label_group = parser.add_mutually_exclusive_group(required=False)
	cms_label_group.add_argument('--cms', action='store_true', help="Draw CMS label")
	cms_label_group.add_argument('--cms_text', type=str, help="Draw CMS label with extra text")
	args = parser.parse_args()

	gq_plot = GQSummaryPlot("gq_all")

	# If args.goms_fills is specified, don't draw the "line_width=402" style fill
	if args.gom_fills:
		for style_name in style:
			style[style_name]["line_width"] = 2

	# Load data
	analysis_data = {}
	analyses = args.analyses.split(",")
	for analysis in analyses:
		analysis_data[analysis] = DijetData(analysis)
		if args.gom_fills and analysis in max_gom:
			this_max_gom = max_gom[analysis]
		else:
			this_max_gom = False
		if args.gom_fills and analysis in max_gq:
			this_max_gq = max_gq[analysis]
		else:
			this_max_gq = False		
		analysis_data[analysis].load_data("data/{}.dat".format(analysis))
		gq_plot.add_data(analysis_data[analysis], analysis, legend_entries[analysis], max_gom=this_max_gom, max_gq=this_max_gq)

	# Style the plot
	gq_plot.set_style(style)
	gq_plot.set_width_curves([float(x) for x in args.goms.split(",")])
	if args.cms:
		cms_label_option = ""
	elif args.cms_text:
		cms_label_option = args.cms_text
	else:
		cms_label_option = False
	gq_plot.draw(
		logx=args.logx, 
		logy=args.logy, 
		draw_cms=cms_label_option,
		x_title="M_{Z'} [GeV]",
		y_title="g'_{q}",
		x_range=[40.,7000.],
		y_range=[0.01, 2.],
		canvas_dim=[1800, 1200],
		legend_coords=[0.24, 0.15, 0.94, 0.4],
		legend_text_size=0.0245,
		legend_ncolumns=3,
		draw_Z_constraint=True,
		gom_x=60.,
		model_label={"x":2100., "y":0.06, "text":"Z'#rightarrowq#bar{q}"},
		gom_fills=args.gom_fills
		)
	gq_plot.save("plots")


