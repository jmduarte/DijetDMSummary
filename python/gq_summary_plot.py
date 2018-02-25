import os
import sys
import math
import ROOT
from ROOT import TCanvas, TLegend, TGraph, TF1, TLatex, TH1D, TColor
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

from dijet_data import DijetData
from zprime_equations import *
from cms_label import CMSLabel

from seaborn_colors import SeabornColors
seaborn_colors = SeabornColors()
seaborn_colors.load_palette("Blues_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Reds_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Oranges_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Greens_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Purples_d", palette_dir="./python/seaborn_palettes")


class GQSummaryPlot:
	def __init__(self, name):
		self._name = name
		self._analyses = []
		self._dijet_data = {}
		self._legend_entries = {}
		self._graphs = {}
		self._GoMs = []
		self._vtype = "vector"
		self._style = {"default":{
			"line_color":1,
			"line_width":402,
			"line_style":1,
			"marker_style":20,
			"marker_size":0,
			"marker_color":1,
			"fill_style":3004,
			"fill_color":0,
			}
		}


	# style = dict of <analysis name>:{"line_color":1, "marker_style":20, etc}
	# See the default option in __init__ for the full list of options
	def set_style(self, style):
		self._style.update(style)

	def set_vtype(self, vtype):
		vtype = vtype.lower()
		if not vtype in ["vector", "axial"]:
			raise ValueError("[set_vtype] Argument vtype must be 'vector' or 'axial'")
		self._vtype = vtype

	def add_data(self, dijet_data, name, legend):
		self._analyses.append(name)
		self._dijet_data[name] = dijet_data
		self._legend_entries[name] = legend
		self._graphs[name] = dijet_data.get_graph()

	def set_width_curves(self, GoMs):
		self._GoMs = GoMs

	def style_graph(self, graph, name):
		if not name in self._style:
			print "[style_graph] ERROR : Analysis {} is not present in the style dict. Please add.".format(name)
			sys.exit(1)
		if "line_color" in self._style[name]:
			graph.SetLineColor(self._style[name]["line_color"])
		else:
			graph.SetLineColor(self._style["default"]["line_color"])
		if "line_style" in self._style[name]:
			graph.SetLineStyle(self._style[name]["line_style"])
		else:
			graph.SetLineStyle(self._style["default"]["line_style"])
		if "line_width" in self._style[name]:
			graph.SetLineWidth(self._style[name]["line_width"])
		else:
			graph.SetLineWidth(self._style["default"]["line_width"])
		if "marker_color" in self._style[name]:
			graph.SetMarkerColor(self._style[name]["marker_color"])
		else:
			graph.SetMarkerColor(self._style["default"]["marker_color"])
		if "marker_style" in self._style[name]:
			graph.SetMarkerStyle(self._style[name]["marker_style"])
		else:
			graph.SetMarkerStyle(self._style["default"]["marker_style"])
		if "marker_size" in self._style[name]:
			graph.SetMarkerSize(self._style[name]["marker_size"])
		else:
			graph.SetMarkerSize(self._style["default"]["marker_size"])
		if "fill_style" in self._style[name]:
			graph.SetFillStyle(self._style[name]["fill_style"])
		else:
			graph.SetFillStyle(self._style["default"]["fill_style"])
		if "fill_color" in self._style[name]:
			graph.SetFillColor(self._style[name]["fill_color"])
		else:
			graph.SetFillColor(self._style["default"]["fill_color"])

	# Create a polygon TGraph corresponding to the excluded range including an upper limit from Gamma/M
	def create_limit_gom_fill(self, limit_graph, gom):
		tf_gom = TF1("tmp_tf1_gq_{}".format(GoM), lambda x, this_gom=GoM: gom_to_gq(this_gom, x[0], self._vtype), 0.1, 10000., 0) # 

		# Calculate new graph that stays at or below the gom curve
		new_limit_points = {}
		limit_x = limit_graph.GetX()
		limit_y = limit_graph.GetY()
		for i in xrange(limit_graph.GetN() - 1):
			x1 = limit_x[i]
			x2 = limit_x[i+1]
			y1 = limit_y[i]
			y2 = limit_y[i+1]
			gom1 = tf_gom.Eval(x1)
			gom2 = tf_gom.Eval(x2)
			if (y1 < gom1 and y2 > gom2) or (y1 > gom1 and y2 < gom2):
				# Calculate intersection of interpolation with GOM using bisection
				xlow  = x1
				xhigh = x2
				ylow  = y1
				yhigh  = y2
				gomlow = tf_gom.Eval(xlow)
				gomhigh = tf_gom.Eval(xhigh)
				for j in xrange(20):
					xmid = (xlow + xhigh) / 2.
					ymid = (ylow + yhigh) / 2.
					gommid = tf_gom.Eval(xmid)
					if (ylow < gomlow and ymid < gommid) or (ylow > gomlow and ymid > gommid):
						xlow = xmid
						ylow = ymid
						gomlow = gommid
					elif (yhigh < gomhigh and ymid < gommid) or (yhigh > gomhigh and yhigh > gomhigh):
						xhigh = xmid
						yhigh = ymid
						gomhigh = gommid
				int_x = (xhigh + xlow) / 2.
				int_y = (yhigh + ylow) / 2.
			new_limit_points[int_x] = int_y

		# Move any old points above the GOM to the GOM
		for i in xrange(limit_graph.GetN()):
			if limit_y[i] > tf_gom.Eval(limit_x[i]):
				new_limit_points[limit_x[i]] = tf_gom.Eval(limit_x[i])
			else:
				new_limit_points[limit_x[i]] = limit_y[i]

		# New graph: limit points
		new_graph = TGraph(len(new_limit_points) + 10000)
		for i, x in enumerate(new_limit_points.keys().sorted()):
			new_graph.SetPoint(i, x, new_limit_points[x])

		# New graph: upper boundary corresponding to GOM
		xmin = min(new_limit_points.keys())
		xmax = max(new_limit_points.keys())
		for i in xrange(10001):
			this_x = xmax + (xmin - xmax) * i / 10000.
			new_graph.SetPoint(len(new_limit_points) + i, this_x, tf_gom.Eval(this_x))
		return new_graph

	def draw(self, 
		logx=False, 
		logy=False, 
		x_title="M_{Med} [GeV]", 
		y_title="g'_{q}", 
		x_range=[40., 7000.],
		y_range=[0, 1.45],
		canvas_dim=[1800, 1200],
		legend_coords=[0.12, 0.28, 0.42, 0.9],
		draw_cms=None,
		legend_text_size=0.028,
		legend_ncolumns=None,
		legend_obsexp=False,
		draw_Z_constraint=False,
		gom_x=None,
		vector_label=False):
		canvas_name = "c_{}_{}_{}".format(self._name, ("logx" if logx else "linearx"), ("logy" if logy else "lineary"))
		self._canvas = TCanvas(canvas_name, canvas_name, canvas_dim[0], canvas_dim[1])
		ROOT.gStyle.SetPadTickX(1)
		ROOT.gStyle.SetPadTickY(1)
		self._canvas.SetLeftMargin(0.09)
		self._canvas.SetBottomMargin(0.12)
		self._canvas.SetTopMargin(0.075)
		self._canvas.SetRightMargin(0.035)

		if logx:
			self._canvas.SetLogx()
		if logy:
			self._canvas.SetLogy()
		self._canvas.SetTicks(1, 1)
		self._canvas.cd()
		self._legend = TLegend(legend_coords[0], legend_coords[1], legend_coords[2], legend_coords[3])
		self._legend.SetFillStyle(0)
		self._legend.SetBorderSize(0)
		self._legend.SetTextSize(legend_text_size)
		if legend_ncolumns:
			self._legend.SetNColumns(legend_ncolumns)
		
		# Legend headers and obs/exp lines
		self._legend.SetHeader("95% CL exclusions")
		if legend_obsexp:
			self._g_obs_dummy = TGraph(10)
			self._g_obs_dummy.SetLineStyle(1)
			self._g_obs_dummy.SetLineColor(1)
			self._g_obs_dummy.SetLineWidth(402)
			self._g_obs_dummy.SetMarkerStyle(20)
			self._g_obs_dummy.SetMarkerSize(0)
			self._g_obs_dummy.SetFillStyle(3004)
			self._g_obs_dummy.SetFillColor(1)
			self._legend.AddEntry(self._g_obs_dummy, "Observed", "lf")
			self._g_exp_dummy = TGraph(10)
			self._g_exp_dummy.SetLineStyle(2)
			self._g_exp_dummy.SetLineColor(1)
			self._g_exp_dummy.SetLineWidth(402)
			self._g_exp_dummy.SetMarkerStyle(20)
			self._g_exp_dummy.SetMarkerSize(0)
			self._legend.AddEntry(self._g_exp_dummy, "Expected", "l")

		self._frame = TH1D("frame", "frame", 100, x_range[0], x_range[1])
		self._frame.SetDirectory(0)
		self._frame.GetYaxis().SetRangeUser(y_range[0], y_range[1])
		self._frame.GetXaxis().SetTitle(x_title)
		self._frame.GetYaxis().SetTitle(y_title)
		self._frame.Draw("axis")
		if logx:
			self._frame.GetXaxis().SetMoreLogLabels()
			self._frame.GetXaxis().SetNdivisions(10)
			self._frame.GetXaxis().SetNoExponent(True)
		self._frame.GetXaxis().SetTitleOffset(1.)
		self._frame.GetXaxis().SetTitleSize(0.05)
		self._frame.GetXaxis().SetLabelSize(0.04)
		self._frame.GetYaxis().SetTitleOffset(0.8)
		self._frame.GetYaxis().SetTitleSize(0.05)
		self._frame.GetYaxis().SetLabelSize(0.04)
		#if logy:
		#	self._frame.GetYaxis().SetMoreLogLabels()

		for analysis_name in self._analyses:
			self.style_graph(self._graphs[analysis_name], analysis_name)
			self._graphs[analysis_name].Draw("lp")
			if self._legend_entries[analysis_name] != False:
				self._legend.AddEntry(self._graphs[analysis_name], self._legend_entries[analysis_name], "l")

		if draw_Z_constraint:
			self._tf_Z_constraint = TF1("Z_constraint", gq_Z_constraint, x_range[0], x_range[1], 0)
			self._tf_Z_constraint.SetNpx(1000)
			self._tf_Z_constraint.SetLineColor(15)
			ROOT.gStyle.SetLineStyleString(9, "40 20");
			self._tf_Z_constraint.SetLineStyle(9)
			self._tf_Z_constraint.SetLineWidth(2)
			self._tf_Z_constraint.Draw("same")
			self._legend.AddEntry(self._tf_Z_constraint, "Z width", "l")

		# Lines at fixed Gamma / M
		self._GoM_tf1s = {}
		self._GoM_labels = {}
		for i, GoM in enumerate(self._GoMs):
			self._GoM_tf1s[GoM] = TF1("tf1_gq_{}".format(GoM), lambda x, this_gom=GoM: gom_to_gq(this_gom, x[0], self._vtype), x_range[0], x_range[1], 0) # 
			self._GoM_tf1s[GoM].SetLineColor(ROOT.kGray+1)
			self._GoM_tf1s[GoM].SetLineStyle(ROOT.kDashed)
			self._GoM_tf1s[GoM].SetLineWidth(1)
			self._GoM_tf1s[GoM].Draw("same")

			# TLatex for Gamma / M
			if gom_x:
				label_x = gom_x
			else: 
				if logx:
					label_xfrac = 0.05
				else:
					label_xfrac = 0.864
				label_x = (x_range[1] - x_range[0]) * label_xfrac + x_range[0]
			if logy:
				label_y = self._GoM_tf1s[GoM].Eval(label_x) * 0.8
				gom_text = "#Gamma/M_{{Med}} = {}%".format(int(GoM * 100))
			else:
				# label_y = self._GoM_tf1s[GoM].Eval(label_x) - 0.085 # For labels under the line
				label_y = self._GoM_tf1s[GoM].Eval(label_x) + 0.085 # For labels over the line
				gom_text = "#frac{{#Gamma}}{{M_{{Med}}}} = {}%".format(int(GoM * 100))
			self._GoM_labels[GoM] = TLatex(label_x, label_y, gom_text)
			if logy:
				self._GoM_labels[GoM].SetTextSize(0.028)
			else:
				self._GoM_labels[GoM].SetTextSize(0.033)
			self._GoM_labels[GoM].SetTextColor(ROOT.kGray+1)
			self._GoM_labels[GoM].Draw("same")

		# Vector label
		if vector_label:
			self._vector_label = TLatex(vector_label["x"], vector_label["y"], vector_label["text"])
			self._vector_label.SetTextSize(0.04)
			self._vector_label.SetTextColor(1)
			self._vector_label.Draw("same")

		# Legend last, to be on top of lines
		self._legend.Draw()

		if draw_cms:
			CMSLabel(self._canvas, extra_text=draw_cms, halign="left", valign="top", in_frame=False)

	def save(self, folder, exts=["pdf"]):
		for ext in exts:
			self._canvas.SaveAs("{}/{}.{}".format(folder, self._canvas.GetName(), ext))

