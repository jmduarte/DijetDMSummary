import os
import sys
sys.path.append("./python/")
from gq_summary_plot import GQSummaryPlot, seaborn_colors
from dijet_data import DijetData

# Set all the plot styling here
style = {
	"default":{
		"line_color":1,
		"line_width":402,
		"line_style":1,
		"marker_style":20,
		"marker_size":0,
		"marker_color":1,
		"fill_style":3004,
		"fill_color":0,
	}, "EXO16046_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 2),		
	}, "EXO16046_exp":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 5),		
	}, "EXO16056_narrow_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 2),		
	}, "EXO16056_narrow_exp":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 5),		
	}, "EXO16056_wide_obs":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 2),		
	}, "EXO16056_wide_exp":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 5),		
	}, "EXO16057_SR1_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR1_exp":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 5),		
	}, "EXO16057_SR2_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR2_exp":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 5),		
	}, "EXO17001_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 2),		
	}, "EXO17001_exp":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 5),		
	}, "EXO14005_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 1),
		"line_style":1, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 1),
	}, "EXO14005_exp":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 4),
		"line_style":2, 
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 4),
	}
}

legend_entries = {
	"EXO16046_obs":"#splitline{Dijet #chi (EXO-16-046)}{35.9 fb^{-1}, 13 TeV}",
	"EXO16046_exp":False,
	"EXO16056_narrow_obs":"#splitline{Narrow Dijet (EXO-16-056)}{35.9 fb^{-1}, 13 TeV}",
	"EXO16056_narrow_exp":False,
	"EXO16056_wide_obs":"#splitline{Wide Dijet (EXO-16-056)}{35.9 fb^{-1}, 13 TeV}",
	"EXO16056_wide_exp":False,
	"EXO16057_SR1_obs":"#splitline{Dijet w/b Tag (EXO-16-057)}{19.7 fb^{-1}, 8 TeV}",
	"EXO16057_SR1_exp":False,
	"EXO16057_SR2_obs":False, # Only need one of SR1/SR2 for the legend
	"EXO16057_SR2_exp":False,
	"EXO17001_obs":"#splitline{Boosted Dijet (EXO-17-001)}{35.9 fb^{-1}, 13 TeV}",
	"EXO17001_exp":False,
	"EXO14005_obs":"#splitline{Dijet (EXO-14-005)}{19.7 fb^{-1}, 8 TeV}",
	"EXO14005_exp":False
}

# graph = TGraph to be styled
# name = CADI line etc



if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser(description='Make g_q summary plot')
	parser.add_argument('--analyses', type=str, default="\
EXO17001_obs,EXO17001_exp,\
EXO16057_SR1_obs,EXO16057_SR1_exp,\
EXO16057_SR2_obs,EXO16057_SR2_exp,\
EXO14005_obs,\
EXO16056_narrow_obs,EXO16056_narrow_exp,\
EXO16056_wide_obs,EXO16056_wide_exp,\
EXO16046_obs,EXO16046_exp", help="Analyses to plot (CADI lines, comma-separated)") 
	parser.add_argument('--logx', action='store_true', help='Log x')
	parser.add_argument('--logy', action='store_true', help='Log y')
	parser.add_argument('--goms', type=str, default="0.1,0.3", help='List of Gamma/M values to draw')
	cms_label_group = parser.add_mutually_exclusive_group(required=False)
	cms_label_group.add_argument('--cms', action='store_true', help="Draw CMS label")
	cms_label_group.add_argument('--cms_text', type=str, help="Draw CMS label with extra text")
	args = parser.parse_args()

	gq_plot = GQSummaryPlot("gq_cms")

	# Load data
	analysis_data = {}
	analyses = args.analyses.split(",")
	for analysis in analyses:
		analysis_data[analysis] = DijetData(analysis)
		analysis_data[analysis].load_data("data/{}.dat".format(analysis))
		gq_plot.add_data(analysis_data[analysis], analysis, legend_entries[analysis])

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
		canvas_dim=[1800, 1200],
		legend_coords=[0.12, 0.24, 0.42, 0.92],
		legend_text_size=0.028,
		legend_obsexp=True,
		vector_label={"x":1500., "y":1.2, "text":"Z'#rightarrowq#bar{q}"}
		)
	gq_plot.save("plots")


