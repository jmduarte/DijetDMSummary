import os
import sys
import math
import ROOT
from ROOT import TFile, TGraph

# Take xs*BR limits and convert into xs limits
quark_masses = {
	"u":2.3e-3,
	"d":4.8e-3,
	"c":1.275,
	"s":0.095,
	"t":173.210,
	"b":4.180
}
def ZpBranchingRatio(m_med, selected_decays=["b"], zp_type="vector"):
	total_width = 0.
	selected_width = 0.
	for quark in ["u", "d", "s", "c", "b", "t"]:
		z = (quark_masses[quark] / m_med)**2
		if z > 0.25:
			continue
		if zp_type == "vector":
			this_width = (1 - 4*z)**0.5 * (1 + 2*z)
		elif zp_type == "avector":
			this_width = (1 - 4*z)**1.5
		else:
			print "[ZpBranchingRatio] ERROR : zp_type must be vector or avector"
			sys.exit(1)
		total_width += this_width
		if quark in selected_decays:
			selected_width += this_width
	return selected_width / total_width

for sr in ["SR1", "SR2"]:
	for what in ["obs", "exp"]:
		if sr == "SR1":
			f = TFile("limits_trigbbl_CSVTM_ZPrime_dijet4.root", "READ")
		else:
			f = TFile("limits_trigbbh_CSVTM_ZPrime_dijet4.root", "READ")
		if what == "obs":
			g = f.Get("graph_obs")
		else:
			g = f.Get("graph_exp")
		txt = open("../EXO16057_{}_{}.dat".format(sr, what), 'w')
		txt.write("# m_med xs8\n")
		for i in xrange(g.GetN()):
			mZp = g.GetX()[i]
			xsBRbb = g.GetY()[i]
			xs = xsBRbb / ZpBranchingRatio(mZp)
			txt.write("{} {}\n".format(mZp, xs))
		txt.close()
